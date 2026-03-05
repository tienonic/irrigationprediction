import streamlit as st
import ee
import folium
import geemap.core as geemap
from streamlit_folium import st_folium

st.set_page_config(page_title="Irrigation Tracker", layout="wide")
st.title("Irrigation Expansion Tracker")

# Initialize Earth Engine
@st.cache_resource
def init_ee():
    try:
        ee.Initialize(project="irrigationselectionworldwide")
    except Exception:
        ee.Authenticate()
        ee.Initialize(project="irrigationselectionworldwide")

init_ee()

# Sidebar controls
st.sidebar.header("Settings")

regions = {
    "India-Pakistan (Indus/Ganges)": [68, 20, 90, 35],
    "East Africa (Kenya/Tanzania)": [33, -8, 42, 5],
    "Central Asia (Uzbekistan/Kazakhstan)": [56, 37, 72, 46],
    "Nile Delta (Egypt)": [29, 29, 33, 32],
    "California Central Valley": [-122, 34, -118, 40],
    "Custom": None,
}

region_name = st.sidebar.selectbox("Region", list(regions.keys()))

if region_name == "Custom":
    col1, col2 = st.sidebar.columns(2)
    lon_min = col1.number_input("West", value=68.0)
    lat_min = col2.number_input("South", value=20.0)
    lon_max = col1.number_input("East", value=90.0)
    lat_max = col2.number_input("North", value=35.0)
    bbox = [lon_min, lat_min, lon_max, lat_max]
else:
    bbox = regions[region_name]

year = st.sidebar.slider("Year", 2017, 2025, 2024)

wet_months = st.sidebar.slider("Wet season months", 1, 12, (7, 9))
dry_months = st.sidebar.slider("Dry season months", 1, 12, (12, 2))

ndvi_threshold = st.sidebar.slider("Dry NDVI threshold (irrigated if above)", 0.0, 0.6, 0.25, 0.05)
contrast_threshold = st.sidebar.slider("Max wet-dry contrast (irrigated if below)", 0.0, 0.6, 0.3, 0.05)

cloud_pct = st.sidebar.slider("Max cloud cover %", 5, 50, 20)


@st.cache_data(ttl=3600)
def compute_irrigation(bbox, year, wet_months, dry_months, ndvi_thresh, contrast_thresh, cloud_pct):
    region = ee.Geometry.Rectangle(bbox)

    # Handle month ranges that wrap around year boundary (e.g., Dec-Feb)
    dry_start, dry_end = dry_months
    wet_start, wet_end = wet_months

    s2 = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterBounds(region)
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", cloud_pct))
    )

    # Wet season composite
    if wet_start <= wet_end:
        wet_col = s2.filter(ee.Filter.calendarRange(year, year, "year")).filter(
            ee.Filter.calendarRange(wet_start, wet_end, "month")
        )
    else:
        wet_col = s2.filter(
            ee.Filter.Or(
                ee.Filter.And(
                    ee.Filter.calendarRange(year, year, "year"),
                    ee.Filter.calendarRange(wet_start, 12, "month"),
                ),
                ee.Filter.And(
                    ee.Filter.calendarRange(year + 1, year + 1, "year"),
                    ee.Filter.calendarRange(1, wet_end, "month"),
                ),
            )
        )

    # Dry season composite
    if dry_start <= dry_end:
        dry_col = s2.filter(ee.Filter.calendarRange(year, year, "year")).filter(
            ee.Filter.calendarRange(dry_start, dry_end, "month")
        )
    else:
        dry_col = s2.filter(
            ee.Filter.Or(
                ee.Filter.And(
                    ee.Filter.calendarRange(year, year, "year"),
                    ee.Filter.calendarRange(dry_start, 12, "month"),
                ),
                ee.Filter.And(
                    ee.Filter.calendarRange(year + 1, year + 1, "year"),
                    ee.Filter.calendarRange(1, dry_end, "month"),
                ),
            )
        )

    ndvi_wet = wet_col.median().normalizedDifference(["B8", "B4"]).rename("NDVI_wet")
    ndvi_dry = dry_col.median().normalizedDifference(["B8", "B4"]).rename("NDVI_dry")

    contrast = ndvi_wet.subtract(ndvi_dry).rename("contrast")
    irrigation_proxy = ndvi_dry.gt(ndvi_thresh).And(contrast.lt(contrast_thresh))

    return region, ndvi_wet, ndvi_dry, contrast, irrigation_proxy


# Compute
with st.spinner("Computing NDVI composites via Google Earth Engine..."):
    region, ndvi_wet, ndvi_dry, contrast, irrigation = compute_irrigation(
        tuple(bbox), year, wet_months, dry_months, ndvi_threshold, contrast_threshold, cloud_pct
    )

# Map
st.subheader(f"Irrigation Proxy — {region_name} ({year})")

layer_choice = st.radio(
    "Layer", ["Irrigation Proxy", "Dry Season NDVI", "Wet Season NDVI", "Wet-Dry Contrast"],
    horizontal=True,
)

center_lat = (bbox[1] + bbox[3]) / 2
center_lon = (bbox[0] + bbox[2]) / 2
m = folium.Map(location=[center_lat, center_lon], zoom_start=6)

ndvi_vis = {"min": 0, "max": 0.8, "palette": ["white", "darkgreen"]}
contrast_vis = {"min": -0.2, "max": 0.6, "palette": ["brown", "white", "blue"]}
irrigation_vis = {"min": 0, "max": 1, "palette": ["white", "#2196F3"]}

layers = {
    "Dry Season NDVI": (ndvi_dry, ndvi_vis),
    "Wet Season NDVI": (ndvi_wet, ndvi_vis),
    "Wet-Dry Contrast": (contrast, contrast_vis),
    "Irrigation Proxy": (irrigation, irrigation_vis),
}

for name, (image, vis) in layers.items():
    tile_url = image.getMapId(vis)["tile_fetcher"].url_format
    folium.TileLayer(
        tiles=tile_url,
        attr="Google Earth Engine",
        name=name,
        overlay=True,
        show=(layer_choice == name),
    ).add_to(m)

folium.LayerControl().add_to(m)
st_folium(m, height=600, use_container_width=True)

# Info panel
with st.expander("How it works"):
    st.markdown("""
**Temporal NDVI contrast method:**

1. Compute median NDVI for wet season and dry season from Sentinel-2
2. Irrigated land = dry-season NDVI above threshold AND low wet-dry contrast
   - Irrigated fields stay green year-round (pumped water)
   - Rainfed fields go brown in dry season (high contrast)
3. Adjust thresholds in the sidebar to tune sensitivity

**Caveats:**
- Evergreen forests also have low contrast — mask with land cover data for production use
- Threshold-based, not ML — a trained model would be more accurate
- Cloud cover in wet season can cause artifacts
""")
