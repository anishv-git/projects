from __future__ import annotations
from pathlib import Path
import os

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"
DB_PATH = DATA_DIR / "hn.duckdb"

HN_API_BASE = "https://hacker-news.firebaseio.com/v0"
USER_AGENT = "hn-pulse/0.1 (+https://github.com/)"

# Ensure directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)

# Env flags
REQUEST_TIMEOUT_S = float(os.getenv("REQUEST_TIMEOUT_S", "15"))
MAX_TOP_STORIES = int(os.getenv("MAX_TOP_STORIES", "250"))
