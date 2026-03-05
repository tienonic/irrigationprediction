#!/bin/bash
source /opt/homebrew/Caskroom/miniforge/base/etc/profile.d/conda.sh
conda activate irrigation
cd "$(dirname "$0")"
streamlit run app.py --server.address 0.0.0.0
