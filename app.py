import streamlit as st
import ee
import folium
from streamlit_folium import st_folium
from regions import REGIONS
from events import EVENTS

st.set_page_config(page_title="Irrigation & Groundwater Monitor", layout="wide")

# Max region area in degrees² (~50,000 km² at mid-latitudes, roughly 220km x 220km)
MAX_AREA_DEG2 = 25.0


@st.cache_resource
def init_ee():
    try:
        ee.Initialize(project="irrigationselectionworldwide")
    except Exception:
        ee.Authenticate()
        ee.Initialize(project="irrigationselectionworldwide")

init_ee()

# --- Lookups ---
region_map = {r["name"]: r for r in REGIONS}
region_names = [r["name"] for r in REGIONS]

# --- Region search at the top ---
st.markdown(
    '<h1 style="margin-bottom:0">Irrigation & Groundwater Monitor</h1>',
    unsafe_allow_html=True,
)

search = st.text_input(
    "Search regions", placeholder="Type to filter (e.g. Egypt, Punjab, California...)",
    label_visibility="collapsed",
)

if search:
    matches = [r for r in REGIONS if search.lower() in r["name"].lower()]
    # Also search events
    event_matches = []
    for rname, evts in EVENTS.items():
        for evt in evts:
            if search.lower() in evt["title"].lower() or search.lower() in evt["summary"].lower():
                event_matches.append({**evt, "region": rname})

    if matches:
        st.caption(f"{len(matches)} region(s) found")
        for r in matches:
            st.markdown(f"**{r['name']}** — {r['why'][:120]}...")
    if event_matches:
        st.caption(f"{len(event_matches)} related story/stories")
        for evt in event_matches[:5]:
            st.markdown(f"- **{evt['year']}** {evt['region']}: [{evt['title']}]({evt['url']})")
    if not matches and not event_matches:
        st.caption("No results")

st.divider()

# --- Sidebar ---
st.sidebar.header("Navigation")
nav = st.sidebar.radio("View", ["Map Explorer", "Stories"])

if nav == "Stories":
    # --- Stories mode ---
    st.subheader("Groundwater Stories")

    all_events = []
    for rname, evts in EVENTS.items():
        for evt in evts:
            all_events.append({**evt, "region": rname})
    all_events.sort(key=lambda e: e["year"], reverse=True)

    filter_region = st.sidebar.selectbox(
        "Filter by region", ["All"] + list(EVENTS.keys())
    )
    if filter_region != "All":
        all_events = [e for e in all_events if e["region"] == filter_region]

    for i, evt in enumerate(all_events):
        with st.container():
            col_text, col_btn = st.columns([5, 1])
            with col_text:
                st.markdown(
                    f"**{evt['year']}** &mdash; {evt['region']}  \n"
                    f"**{evt['title']}**  \n"
                    f"{evt['summary']}  \n"
                    f"[Source]({evt['url']})",
                )
            with col_btn:
                if evt["region"] in region_map:
                    if st.button("View", key=f"evt_{i}"):
                        preset = region_map[evt["region"]]
                        bbox = preset["bbox"]
                        center_lat = (bbox[1] + bbox[3]) / 2
                        center_lon = (bbox[0] + bbox[2]) / 2
                        m = folium.Map(location=[center_lat, center_lon],
                                       zoom_start=preset["zoom"], tiles="CartoDB positron")
                        folium.Rectangle(
                            bounds=[[bbox[1], bbox[0]], [bbox[3], bbox[2]]],
                            color="#0868ac", weight=2, fill=True, fill_opacity=0.1,
                        ).add_to(m)
                        st_folium(m, height=350, use_container_width=True)
            st.divider()

else:
    # --- Map Explorer mode ---
    mode = st.sidebar.radio("Mode", ["Single Year", "Year-over-Year"])
    region_name = st.sidebar.selectbox("Region", region_names + ["Custom"])

    if region_name == "Custom":
        st.sidebar.caption("Enter a small area (max ~220km per side)")
        col1, col2 = st.sidebar.columns(2)
        lon_min = col1.number_input("West", value=29.5)
        lat_min = col2.number_input("South", value=30.0)
        lon_max = col1.number_input("East", value=32.0)
        lat_max = col2.number_input("North", value=31.7)
        bbox = [lon_min, lat_min, lon_max, lat_max]
        zoom = 8
        wet_default, dry_default = (7, 9), (12, 2)
        ndvi_default, contrast_default = 0.25, 0.30
    else:
        preset = region_map[region_name]
        bbox = preset["bbox"]
        zoom = preset["zoom"]
        wet_default = preset["wet"]
        dry_default = preset["dry"]
        ndvi_default = preset["ndvi"]
        contrast_default = preset["contrast"]

    # --- Area check ---
    area_deg2 = abs(bbox[2] - bbox[0]) * abs(bbox[3] - bbox[1])
    if area_deg2 > MAX_AREA_DEG2:
        st.error(
            f"Region too large ({area_deg2:.0f} deg\u00b2, max {MAX_AREA_DEG2:.0f}). "
            "Select a smaller area or use one of the preset regions. "
            "Large regions cause timeouts and blurry results."
        )
        st.stop()

    if mode == "Single Year":
        year = st.sidebar.slider("Year", 2017, 2025, 2024)
    else:
        year_a = st.sidebar.slider("Year A (earlier)", 2017, 2025, 2019)
        year_b = st.sidebar.slider("Year B (later)", 2017, 2025, 2024)

    with st.sidebar.expander("Advanced", expanded=False):
        wet_months = st.slider("Wet season months", 1, 12, wet_default)
        dry_months = st.slider("Dry season months", 1, 12, dry_default)
        ndvi_threshold = st.slider("Dry NDVI threshold", 0.0, 0.6, ndvi_default, 0.05)
        contrast_threshold = st.slider("Max wet-dry contrast", 0.0, 0.6, contrast_default, 0.05)
        cloud_pct = st.slider("Max cloud cover %", 5, 50, 20)

    # --- Region context ---
    if region_name != "Custom":
        preset = region_map[region_name]
        st.markdown(f"**{region_name}** — {preset['why']}")
        with st.expander("What to look for"):
            for item in preset["what_to_look_for"]:
                st.markdown(f"- {item}")
        if region_name in EVENTS and EVENTS[region_name]:
            with st.expander(f"Related stories ({len(EVENTS[region_name])})"):
                for evt in EVENTS[region_name]:
                    st.markdown(
                        f"**{evt['year']}** — [{evt['title']}]({evt['url']})  \n"
                        f"{evt['summary']}"
                    )

    # --- Computation ---
    def _build_irrigation(bbox, year, wet_months, dry_months, ndvi_thresh, contrast_thresh, cloud_pct):
        region = ee.Geometry.Rectangle(list(bbox))
        dry_start, dry_end = dry_months
        wet_start, wet_end = wet_months

        s2 = (
            ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
            .filterBounds(region)
            .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", cloud_pct))
        )

        def _filter_season(col, start, end, yr):
            if start <= end:
                return col.filter(ee.Filter.calendarRange(yr, yr, "year")).filter(
                    ee.Filter.calendarRange(start, end, "month")
                )
            return col.filter(
                ee.Filter.Or(
                    ee.Filter.And(
                        ee.Filter.calendarRange(yr, yr, "year"),
                        ee.Filter.calendarRange(start, 12, "month"),
                    ),
                    ee.Filter.And(
                        ee.Filter.calendarRange(yr + 1, yr + 1, "year"),
                        ee.Filter.calendarRange(1, end, "month"),
                    ),
                )
            )

        wet_col = _filter_season(s2, wet_start, wet_end, year)
        dry_col = _filter_season(s2, dry_start, dry_end, year)

        ndvi_wet = wet_col.median().normalizedDifference(["B8", "B4"]).rename("NDVI_wet")
        ndvi_dry = dry_col.median().normalizedDifference(["B8", "B4"]).rename("NDVI_dry")
        contrast = ndvi_wet.subtract(ndvi_dry).rename("contrast")
        irrigation = ndvi_dry.gt(ndvi_thresh).And(contrast.lt(contrast_thresh)).rename("irrigation")

        return region, ndvi_wet, ndvi_dry, contrast, irrigation

    @st.cache_data(ttl=3600)
    def get_irrigation(bbox, year, wet_months, dry_months, ndvi_thresh, contrast_thresh, cloud_pct):
        return _build_irrigation(bbox, year, wet_months, dry_months, ndvi_thresh, contrast_thresh, cloud_pct)

    @st.cache_data(ttl=3600)
    def get_area_km2(bbox, year, wet_months, dry_months, ndvi_thresh, contrast_thresh, cloud_pct):
        region, _, _, _, irrigation = _build_irrigation(
            bbox, year, wet_months, dry_months, ndvi_thresh, contrast_thresh, cloud_pct
        )
        stats = (
            irrigation.multiply(ee.Image.pixelArea())
            .reduceRegion(reducer=ee.Reducer.sum(), geometry=region, scale=500, maxPixels=1e9)
            .getInfo()
        )
        return stats.get("irrigation", 0) / 1e6

    def _add_ee_layer(m, image, vis, name, show):
        tile_url = image.getMapId(vis)["tile_fetcher"].url_format
        folium.TileLayer(
            tiles=tile_url, attr="Google Earth Engine", name=name, overlay=True, show=show,
        ).add_to(m)

    # --- Map ---
    center_lat = (bbox[1] + bbox[3]) / 2
    center_lon = (bbox[0] + bbox[2]) / 2

    ndvi_vis = {"min": 0, "max": 0.8, "palette": ["#f7f7f7", "#d9f0a3", "#78c679", "#005a32"]}
    contrast_vis = {"min": -0.2, "max": 0.6, "palette": ["#8c510a", "#f5f5f5", "#2166ac"]}
    irrigation_vis = {"min": 0, "max": 1, "palette": ["#f7f7f7", "#0868ac"]}

    if mode == "Single Year":
        with st.spinner("Analyzing satellite imagery..."):
            region, ndvi_wet, ndvi_dry, contrast, irrigation = get_irrigation(
                tuple(bbox), year, wet_months, dry_months, ndvi_threshold, contrast_threshold, cloud_pct
            )

        layer_choice = st.radio(
            "Layer", ["Irrigation Proxy", "Dry Season NDVI", "Wet Season NDVI", "Wet-Dry Contrast"],
            horizontal=True,
        )

        m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom, tiles="CartoDB positron")
        layers = {
            "Irrigation Proxy": (irrigation, irrigation_vis),
            "Dry Season NDVI": (ndvi_dry, ndvi_vis),
            "Wet Season NDVI": (ndvi_wet, ndvi_vis),
            "Wet-Dry Contrast": (contrast, contrast_vis),
        }
        for name, (img, vis) in layers.items():
            _add_ee_layer(m, img, vis, name, show=(name == layer_choice))
        folium.LayerControl().add_to(m)
        st_folium(m, height=550, use_container_width=True)

        with st.spinner("Computing area..."):
            area_km2 = get_area_km2(
                tuple(bbox), year, wet_months, dry_months, ndvi_threshold, contrast_threshold, cloud_pct
            )

        col1, col2, col3 = st.columns(3)
        col1.metric("Irrigated Area", f"{area_km2:,.0f} km\u00b2")
        col2.metric("Irrigated Area", f"{area_km2 * 100:,.0f} ha")
        col3.metric("Irrigated Area", f"{area_km2 * 247.105:,.0f} acres")

    else:
        with st.spinner(f"Comparing {year_a} vs {year_b}..."):
            _, _, _, _, irrig_a = get_irrigation(
                tuple(bbox), year_a, wet_months, dry_months, ndvi_threshold, contrast_threshold, cloud_pct
            )
            _, _, _, _, irrig_b = get_irrigation(
                tuple(bbox), year_b, wet_months, dry_months, ndvi_threshold, contrast_threshold, cloud_pct
            )

        change = irrig_a.multiply(2).add(irrig_b).rename("change")

        layer_choice = st.radio(
            "Layer", ["Change Map", f"{year_a} Irrigation", f"{year_b} Irrigation"],
            horizontal=True,
        )

        m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom, tiles="CartoDB positron")
        change_vis = {"min": 0, "max": 3, "palette": ["#f7f7f7", "#2ca02c", "#d62728", "#0868ac"]}
        layers = {
            "Change Map": (change, change_vis),
            f"{year_a} Irrigation": (irrig_a, irrigation_vis),
            f"{year_b} Irrigation": (irrig_b, irrigation_vis),
        }
        for name, (img, vis) in layers.items():
            _add_ee_layer(m, img, vis, name, show=(name == layer_choice))
        folium.LayerControl().add_to(m)
        st_folium(m, height=550, use_container_width=True)

        if layer_choice == "Change Map":
            st.markdown(
                '<span style="color:#0868ac;font-size:1.2em">&#9632;</span> Stable irrigated &emsp; '
                '<span style="color:#2ca02c;font-size:1.2em">&#9632;</span> New irrigation &emsp; '
                '<span style="color:#d62728;font-size:1.2em">&#9632;</span> Lost irrigation &emsp; '
                '<span style="color:#ccc;font-size:1.2em">&#9632;</span> Never irrigated',
                unsafe_allow_html=True,
            )

        with st.spinner("Computing area statistics..."):
            area_a = get_area_km2(
                tuple(bbox), year_a, wet_months, dry_months, ndvi_threshold, contrast_threshold, cloud_pct
            )
            area_b = get_area_km2(
                tuple(bbox), year_b, wet_months, dry_months, ndvi_threshold, contrast_threshold, cloud_pct
            )

        delta = area_b - area_a
        pct = (delta / area_a * 100) if area_a > 0 else 0

        col1, col2, col3 = st.columns(3)
        col1.metric(f"{year_a} Irrigated", f"{area_a:,.0f} km\u00b2")
        col2.metric(f"{year_b} Irrigated", f"{area_b:,.0f} km\u00b2")
        col3.metric("Change", f"{delta:+,.0f} km\u00b2", f"{pct:+.1f}%")

    with st.expander("About"):
        st.markdown("""
This tool detects irrigated land from satellite imagery to support water governance.
Fields green through the dry season are receiving pumped water — from wells or canals.

**Method:** Sentinel-2 NDVI composites at 10m resolution. Low seasonal contrast + high
dry greenness = irrigated. **Limitations:** Forests also show low contrast. Threshold-based.
""")
