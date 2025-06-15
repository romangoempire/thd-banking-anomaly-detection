# THD Banking Anomaly Detection

## Requirements
1. [uv](https://github.com/astral-sh/uv)

## Installation

1. Download [Purchase Card Transaction Dataset](https://opendata.dc.gov/datasets/DCGIS::purchase-card-transactions/about)
```sh
source scripts/download_dataset.sh
```
2. Create clean and encoded dataset
```sh
uv run scripts/clean_dataset.py
```

3. Start Streamlit app
```sh
source .venv/bin/activate
streamlit run main.py
# open http://localhost:8501 in your browser
```

## Data

[Purchase Card Transaction Dataset](https://opendata.dc.gov/datasets/DCGIS::purchase-card-transactions/about)
