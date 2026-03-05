#!/bin/bash
# Run this in tmux: tmux new -s irrigation
# Then: bash setup-remaining.sh
set -e

echo "=== Activating conda environment ==="
source /opt/homebrew/Caskroom/miniforge/base/etc/profile.d/conda.sh
conda activate irrigation

echo "=== Installing pip packages ==="
pip install earthengine-api geemap streamlit streamlit-folium scikit-learn spyndex folium lightgbm

echo "=== Verifying installation ==="
python -c "
import ee, geemap, streamlit, geopandas, rasterio, xarray, sklearn, folium
print('All imports successful!')
print(f'  geemap: {geemap.__version__}')
print(f'  streamlit: {streamlit.__version__}')
print(f'  geopandas: {geopandas.__version__}')
print(f'  scikit-learn: {sklearn.__version__}')
"

echo ""
echo "=== DONE ==="
echo "Next steps:"
echo "  1. Run: earthengine authenticate"
echo "     (This opens a browser URL — copy the URL, paste in browser, authorize, paste code back)"
echo "  2. Run: cd /Users/minimel/Documents/projects/agdev && streamlit run app.py"
echo "  3. Access from Windows: http://100.104.51.108:8501"
