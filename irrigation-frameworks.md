# Irrigation Expansion Tracking — Framework Options

## The Core Insight

Irrigated fields stay green in dry season; rainfed fields don't. A temporal NDVI contrast (wet minus dry season) is a strong irrigation proxy. All frameworks below exploit this signal.

---

## 1. GEE + geemap + Streamlit (Recommended First)

**What:** Google Earth Engine does all satellite processing in Google's cloud (free). geemap gives a Pythonic interface. Streamlit wraps it into a web dashboard you access from Windows.

**Why it fits:**
- Mac mini does almost nothing — GEE processes petabytes of imagery server-side
- Streamlit serves on `localhost:8501`, accessible from Windows via Tailscale (`http://100.104.51.108:8501`)
- geemap has built-in split-panel maps, time sliders, and layer controls
- Largest community, most tutorials, most examples for exactly this kind of work

**Stack:**
```
conda create -n irrigation python=3.11
conda activate irrigation
conda install -c conda-forge geopandas rasterio
pip install earthengine-api geemap streamlit streamlit-folium scikit-learn spyndex
```

**What you build:** A Streamlit app with:
- Region selector (dropdown or map click)
- Date range picker for wet/dry seasons
- Live NDVI contrast map rendered from GEE
- Irrigation classification overlay (threshold or ML-based)
- Time series chart showing expansion year over year

**Cost:** Free (GEE is free for research/non-commercial use)

**Docs:**
- geemap: https://geemap.org (excellent — 300+ examples)
- Streamlit: https://docs.streamlit.io
- GEE Python: https://developers.google.com/earth-engine/guides/python_install

**Limitations:** GEE requires Google account + signup (usually approved within a day). Compute quotas exist but are generous. You're locked into Google's ecosystem for processing.

---

## 2. JupyterLab + geemap + ipyleaflet (Best for Exploration)

**What:** Same GEE backend, but the interface is a Jupyter notebook with inline interactive maps. You iterate cell-by-cell, see maps immediately, and build up analysis interactively.

**Why it fits:**
- JupyterLab runs on Mac mini, access from Windows browser via `http://100.104.51.108:8888`
- geemap renders full interactive maps inside notebook cells (zoom, pan, layers, inspector)
- Perfect for prototyping — test different thresholds, seasons, regions interactively
- Easy to mix code, maps, charts, and narrative in one document
- Can export notebooks as reports

**Stack:**
```
conda create -n irrigation python=3.11
conda activate irrigation
conda install -c conda-forge jupyterlab geopandas rasterio xarray rioxarray
pip install earthengine-api geemap spyndex rasterstats
```

**What you build:** A series of notebooks:
1. `01_explore_ndvi.ipynb` — visualize wet/dry NDVI for sample regions
2. `02_irrigation_proxy.ipynb` — threshold-based classification, compare to FAO ground truth
3. `03_temporal_expansion.ipynb` — year-over-year change detection, 2016-2025
4. `04_validation.ipynb` — cross-validate against IWMI/India census data

**Cost:** Free

**Docs:**
- JupyterLab: https://jupyterlab.readthedocs.io
- geemap in Jupyter: https://geemap.org/notebooks/

**Limitations:** Notebooks are great for exploration but bad for sharing a polished tool with others. You'll eventually want to graduate to a Streamlit app (Framework 1).

---

## 3. Planetary Computer + STAC + xarray + hvPlot (GEE Alternative)

**What:** Microsoft's Planetary Computer provides free access to the same satellite data (Sentinel-2, Landsat, MODIS) via STAC API, without needing a Google account. Process locally with xarray, visualize with hvPlot/Panel.

**Why it fits:**
- No GEE signup needed — data is accessed via open STAC protocol
- xarray handles time-series rasters natively (e.g., monthly NDVI composites as a 3D array)
- hvPlot generates interactive Bokeh maps from xarray objects in one line
- Panel (same ecosystem) can turn any hvPlot into a deployable dashboard
- More portable — not locked to any cloud provider

**Stack:**
```
conda create -n irrigation python=3.11
conda activate irrigation
conda install -c conda-forge geopandas rasterio xarray rioxarray dask
pip install pystac-client odc-stac planetary-computer hvplot panel holoviews
```

**What you build:**
```python
import pystac_client, planetary_computer, odc.stac, hvplot.xarray

catalog = pystac_client.Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=planetary_computer.sign_inplace,
)
items = catalog.search(
    collections=["sentinel-2-l2a"],
    bbox=[68, 20, 90, 35],
    datetime="2024-01/2024-03",
    query={"eo:cloud_cover": {"lt": 20}},
).item_collection()

ds = odc.stac.load(items, bands=["B08", "B04"], resolution=100)
ndvi = (ds.B08 - ds.B04) / (ds.B08 + ds.B04)
ndvi.mean("time").hvplot.image(geo=True, cmap="YlGn", tiles="OSM")
```

**Cost:** Free (Planetary Computer is free, data download is free). Local compute costs depend on region size — for a country, ~2-4 GB RAM. For global, you'd need to tile.

**Docs:**
- Planetary Computer: https://planetarycomputer.microsoft.com/docs/overview/about
- pystac-client: https://pystac-client.readthedocs.io
- odc-stac: https://odc-stac.readthedocs.io
- hvPlot: https://hvplot.holoviz.org

**Limitations:** Processing happens on your Mac mini, not in the cloud. For large regions (continental+), you'll need Dask for chunked processing. Slower than GEE for global-scale work. But for country/state-level analysis, it's perfectly fine.

---

## 4. Leafmap + Solara (Lightweight, Flexible, Any Data Source)

**What:** Leafmap is a general-purpose geospatial mapping library that works with GEE, local files, COGs (Cloud-Optimized GeoTIFFs), and any XYZ tile service. Solara turns it into a reactive web app without needing Streamlit.

**Why it fits:**
- Works with or without GEE — can use downloaded GeoTIFFs, STAC, WMS, etc.
- Solara is lighter than Streamlit and designed for Jupyter widget-based apps
- Can display split maps (before/after), time sliders, drawing tools
- Good for building a tool that works fully offline after initial data download
- leafmap has built-in tools for downloading GEE/STAC data to local GeoTIFF

**Stack:**
```
conda create -n irrigation python=3.11
conda activate irrigation
pip install leafmap solara localtileserver geopandas rasterio
pip install earthengine-api  # optional, if using GEE as a data source
```

**What you build:** A Solara web app where you:
- Load pre-computed irrigation classification GeoTIFFs
- Side-by-side compare years (2018 vs 2024)
- Draw polygons to compute area statistics
- Toggle layers (NDVI, irrigation class, ground truth)
- Works fully offline once data is downloaded

**Cost:** Free. If using local data, zero ongoing cloud dependency.

**Docs:**
- Leafmap: https://leafmap.org (by Qiusheng Wu, same author as geemap)
- Solara: https://solara.dev/docs
- localtileserver: https://localtileserver.banesullivan.com

**Limitations:** Less polished than Streamlit for complex dashboards. Solara is newer and has a smaller community. But for map-centric apps, it's excellent.

---

## 5. QGIS + Temporal Controller + GEE Plugin (Desktop GIS)

**What:** QGIS is the open-source desktop GIS. It has a built-in Temporal Controller for animating time-series data, a GEE plugin for direct satellite access, and a full Python console for scripting.

**Why it fits:**
- Most powerful visualization for geospatial data — full cartographic control
- Temporal Controller can animate irrigation expansion year by year
- GEE plugin (by Gennadii Donchyts) lets you load GEE layers directly into QGIS
- Python console lets you script everything (PyQGIS)
- Can produce publication-quality maps

**Setup on Mac mini:**
```bash
brew install --cask qgis
# For remote access from Windows:
brew install --cask vnc-server  # or use macOS built-in Screen Sharing
```

Access from Windows via VNC/Screen Sharing through Tailscale: `vnc://100.104.51.108`

Install GEE plugin: QGIS > Plugins > Manage and Install Plugins > search "Google Earth Engine"

**What you build:**
- Load FAO irrigation map as base layer
- Add GEE NDVI layers for wet/dry season
- Use Temporal Controller to animate 2015-2025
- Style with graduated colors showing irrigation probability
- Export frames as GIF or video

**Cost:** Free

**Docs:**
- QGIS: https://docs.qgis.org/3.34/en/docs/
- Temporal Controller: https://docs.qgis.org/3.34/en/docs/user_manual/map_views/map_view.html#temporal-control
- GEE QGIS plugin: https://gee-community.github.io/qgis-earthengine-plugin/

**Limitations:** Requires a display — you'd need VNC or macOS Screen Sharing from Windows, which adds latency. Not great for a headless workflow. But for cartographic quality and temporal animation, nothing else comes close.

---

## Comparison Matrix

| Criteria               | 1. GEE+Streamlit | 2. Jupyter+geemap | 3. Planetary Computer | 4. Leafmap+Solara | 5. QGIS       |
|------------------------|-------------------|--------------------|----------------------|-------------------|----------------|
| Setup difficulty       | Low               | Low                | Medium               | Low               | Medium (VNC)   |
| Local compute needed   | Minimal           | Minimal            | Moderate             | Low-Moderate      | Moderate       |
| Interactive maps       | Yes (web)         | Yes (notebook)     | Yes (Bokeh)          | Yes (web)         | Yes (desktop)  |
| Works headless         | Yes               | Yes                | Yes                  | Yes               | No (needs VNC) |
| Temporal animation     | Custom            | Custom             | Built-in (hvPlot)    | Custom            | Built-in       |
| Offline capable        | No (needs GEE)    | No (needs GEE)     | Yes (after download) | Yes               | Yes            |
| Community/docs         | Excellent         | Excellent          | Good                 | Good              | Excellent      |
| Best for               | Polished tool     | Prototyping        | GEE-free workflow    | Flexible/offline  | Cartography    |

## Recommended Path

**Start with Framework 2** (Jupyter + geemap) to explore the data and validate the irrigation signal. Once you have a working methodology, **graduate to Framework 1** (Streamlit) for a polished interactive tool. Use **Framework 3** if you want to avoid GEE dependency, or **Framework 5** for publication-quality maps.

The temporal approach (dry-season NDVI > threshold + low wet-dry contrast = irrigated) should work well with any of these. The GEE JavaScript snippet you already have translates almost 1:1 to Python via geemap.
