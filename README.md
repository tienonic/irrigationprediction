# Irrigation Expansion Tracker

A web dashboard for detecting and visualizing irrigated agricultural land worldwide using satellite imagery from Google Earth Engine.

## How It Works

The tool uses **temporal NDVI contrast** from Sentinel-2 satellite imagery to distinguish irrigated land from rainfed agriculture:

1. Computes median NDVI for wet and dry seasons separately
2. Irrigated fields maintain high NDVI in the dry season (sustained by pumped water)
3. Rainfed fields show low dry-season NDVI and high wet-dry contrast (they go brown)
4. A pixel is classified as irrigated when dry NDVI exceeds a threshold AND the wet-dry contrast is below a threshold

All satellite processing runs server-side on Google Earth Engine — no local data downloads required.

## Features

- **5 preset regions**: India-Pakistan, East Africa, Central Asia, Nile Delta, California Central Valley
- **Custom bounding box** support for any region worldwide
- **Adjustable parameters**: year (2017-2025), wet/dry season months, NDVI thresholds, cloud cover filter
- **4 map layers**: Irrigation proxy, dry-season NDVI, wet-season NDVI, wet-dry contrast
- **Interactive map** with layer toggling via Folium + Streamlit

## Prerequisites

- Python 3.11+
- [Miniforge](https://github.com/conda-forge/miniforge) (conda/mamba)
- A Google Earth Engine account with a registered GCP project
- `gcloud` CLI authenticated

## Installation

```bash
# Create and activate conda environment
conda create -n irrigation python=3.11 -y
conda activate irrigation

# Install C-library geospatial packages via conda
conda install -c conda-forge geopandas rasterio xarray rioxarray rasterstats cartopy -y

# Install Python packages via pip
pip install earthengine-api geemap streamlit streamlit-folium scikit-learn spyndex folium lightgbm
```

## Google Earth Engine Setup

You need a GCP project registered for Earth Engine. Replace `YOUR_PROJECT_ID` with your project ID.

```bash
# Authenticate (use --no-launch-browser for headless/remote machines)
gcloud auth application-default login --no-launch-browser

# Set the Earth Engine project
earthengine set_project YOUR_PROJECT_ID

# Set the quota project
gcloud auth application-default set-quota-project YOUR_PROJECT_ID

# Verify
python -c "import ee; ee.Initialize(project='YOUR_PROJECT_ID'); print('Connected')"
```

## Usage

```bash
conda activate irrigation
streamlit run app.py --server.address 0.0.0.0
```

Open `http://localhost:8501` in your browser (or the machine's IP if running remotely).

### Controls

| Parameter | Description | Default |
|---|---|---|
| Region | Preset region or custom bounding box | India-Pakistan |
| Year | Analysis year | 2024 |
| Wet season months | Month range for wet season composite | Jul-Sep |
| Dry season months | Month range for dry season composite | Dec-Feb |
| Dry NDVI threshold | Minimum dry-season NDVI to classify as irrigated | 0.25 |
| Max wet-dry contrast | Maximum NDVI contrast to classify as irrigated | 0.30 |
| Max cloud cover % | Filter out images with higher cloud percentage | 20% |

## Project Structure

```
agdev/
  app.py                    # Streamlit application
  README.md                 # This file
  requirements.txt          # Python (pip) dependencies
  environment.yml           # Full conda environment spec
  irrigation-frameworks.md  # Background research on detection methods
```

## Limitations

- **Evergreen forests** also show low seasonal contrast and may be misclassified as irrigated. Production use should incorporate a land cover mask (e.g., ESA WorldCover).
- **Threshold-based** classification — a trained ML model (Random Forest, LightGBM) on labeled data would be more accurate.
- **Cloud cover** in wet tropical regions can reduce composite quality and introduce artifacts.
- **Temporal resolution** depends on Sentinel-2 revisit frequency (5 days) and cloud filtering — sparse data in cloudy regions.

## Data Sources

- **Sentinel-2 SR Harmonized** (`COPERNICUS/S2_SR_HARMONIZED`) — 10m resolution surface reflectance imagery via Google Earth Engine

## License

MIT
