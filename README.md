# Irrigation signal mapper

This Streamlit application maps vegetation patterns that can be consistent with irrigation. It uses Sentinel-2 imagery through Google Earth Engine to compare wet- and dry-season vegetation indices.

The output is a screening signal. It does not identify wells, prove groundwater extraction, or establish whether water use is authorized. Confirm candidate areas with land-cover data, field records, permits, and local investigation.

## Method

The application uses temporal NDVI contrast:

1. Calculate median wet- and dry-season NDVI.
2. Identify pixels that remain green during the configured dry season.
3. Compare dry-season NDVI with the seasonal change.
4. Flag pixels that exceed the dry-season threshold and remain below the maximum wet-dry contrast.

Google Earth Engine performs the image processing. The local application renders controls, summary statistics, and map layers.

## Features

- **5 preset regions** with tuned defaults: Nile Delta, India-Pakistan, East Africa, Central Asia, California
- **Custom bounding box** for any region worldwide
- **Year-over-year comparison**: change detection map showing irrigation expansion, loss, and stable areas
- **Area statistics**: irrigated area in km², hectares, and acres: with delta and % change in comparison mode
- **Region-specific tips** explaining the water governance context for each area
- **Adjustable parameters**: season months, NDVI thresholds, cloud cover filter
- **Interactive map** with multiple layers via Folium + Streamlit

### Map layers

| Layer | What it shows | How to read it |
|---|---|---|
| Irrigation Proxy | Pixels classified as irrigated | Blue = irrigated, light = not |
| Dry Season NDVI | Vegetation greenness in dry months | Green patches in dry season = likely pumped water |
| Wet Season NDVI | Vegetation greenness in wet months | Baseline: everything is green |
| Wet-Dry Contrast | Seasonal NDVI difference | Brown = stable year-round (irrigated or forest), blue = seasonal (rainfed) |
| Change Map | Year-over-year irrigation change | Green = new, red = lost, blue = stable |

### Tips

- **Start with the Nile Delta**: it's small, loads fast, and the irrigation signal is very clear against the desert
- **Desert-edge fields** are the strongest signal for unauthorized wells: green patches in otherwise barren land
- **Lower the dry NDVI threshold** (e.g., 0.15) in arid regions where even irrigated land has modest greenness
- **Raise the max contrast** (e.g., 0.4) in tropical regions with seasonal irrigation variation
- **Adjust season months** to match local climate: defaults are tuned per region but may need refinement
- **Year-over-year**: compare 5+ year gaps for clearer expansion trends (e.g., 2018 vs 2024)
- **Forests** also stay green year-round: focus analysis on known agricultural zones

## Prerequisites

- Python 3.11+
- [Miniforge](https://github.com/conda-forge/miniforge) (conda/mamba)
- A Google Earth Engine account with a registered GCP project
- `gcloud` CLI authenticated

## Install

```bash
# Create and activate conda environment
conda create -n irrigation python=3.11 -y
conda activate irrigation

# Install C-library geospatial packages via conda
conda install -c conda-forge geopandas rasterio xarray rioxarray rasterstats cartopy -y

# Install Python packages via pip
pip install earthengine-api geemap streamlit streamlit-folium scikit-learn spyndex folium lightgbm
```

## Set up Google Earth Engine

You need a GCP project registered for Earth Engine. Replace `YOUR_PROJECT_ID` with your project ID.

```bash
gcloud auth application-default login --no-launch-browser
earthengine set_project YOUR_PROJECT_ID
gcloud auth application-default set-quota-project YOUR_PROJECT_ID

# Verify
python -c "import ee; ee.Initialize(project='YOUR_PROJECT_ID'); print('Connected')"
```

## Use the application

```bash
./dev.sh
# or manually:
conda activate irrigation
streamlit run app.py --server.address 0.0.0.0
```

Open `http://localhost:8501` in your browser.

### Controls

| Parameter | Description | Default |
|---|---|---|
| Mode | Single Year analysis or Year-over-Year comparison | Single Year |
| Region | Preset region or custom bounding box | Nile Delta |
| Year | Analysis year (or two years for comparison) | 2024 |
| Wet/Dry season months | Month ranges (auto-tuned per region) | Varies |
| Dry NDVI threshold | Minimum dry-season NDVI to classify as irrigated | 0.20-0.25 |
| Max wet-dry contrast | Maximum NDVI contrast to classify as irrigated | 0.25-0.30 |
| Max cloud cover % | Filter out cloudy satellite images | 20% |

## Limitations

- **Evergreen forests** show low seasonal contrast and may be misclassified as irrigated. A land cover mask (e.g., ESA WorldCover) would help in production use.
- **Threshold-based** classification: a trained ML model (Random Forest, LightGBM) on labeled data would be more accurate.
- **Cloud cover** in wet tropical regions can reduce composite quality and introduce artifacts.
- **Resolution** is limited to Sentinel-2's 10m pixels: individual wells are not visible, but their effect on fields is.

## Data sources

- **Sentinel-2 SR Harmonized** (`COPERNICUS/S2_SR_HARMONIZED`): 10m resolution surface reflectance imagery via Google Earth Engine

## License

MIT
