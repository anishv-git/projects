# HN Pulse (Hacker News Pulse)

A fun, resume-ready data project that ingests Hacker News stories, builds a local analytics warehouse with DuckDB, trains a lightweight ML model to predict story popularity, and serves insights in a Streamlit dashboard and a FastAPI endpoint.

## Features
- Daily ingestion from Hacker News API (stories & top stories)
- Local analytics with DuckDB + SQL transforms
- Text features with TF-IDF
- ML model (Logistic Regression) predicting top-quartile score
- FastAPI service for predictions and aggregates
- Streamlit dashboard with trends, search and what-if predictions
- Makefile + CI, modular code, tests, and typed Python

## Stack
- Python 3.10+
- DuckDB
- Requests, Pandas
- scikit-learn, joblib
- FastAPI, Uvicorn
- Streamlit, Altair

## Quickstart
```bash
# 1) Setup
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2) Ingest latest data and build analytics tables
make ingest build

# 3) Train model
make train

# 4) Run API and UI (in two shells)
make api
make ui
```

## Repo layout
```
hn_pulse/
  __init__.py
  config.py
  io.py
  hn_client.py
  etl.py
  features.py
  model.py
  api.py
  dashboard.py
scripts/
  ingest.py
  build_analytics.py
  train.py
  serve_api.sh
  serve_ui.sh
models/
  (artifacts after training)
.data/
```


- End-to-end: data ingestion → warehouse → ML → API/UI
- Real, dynamic data and time-series trends
- Clear design choices, typed, tested, CI-ready
- Portable: all local with DuckDB

## Notes
- This is an educational project. Be mindful of API request limits.
