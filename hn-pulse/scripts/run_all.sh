#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
cd "$ROOT_DIR"

# 1) Setup venv + deps if missing
if [ ! -x .venv/bin/python ]; then
  echo "[setup] Creating venv..."
  python3 -m venv .venv
fi
source .venv/bin/activate

if ! python -c 'import pkgutil,sys; sys.exit(0 if pkgutil.find_loader("fastapi") else 1)' >/dev/null 2>&1; then
  echo "[setup] Installing Python dependencies..."
  pip install -q --upgrade pip
  pip install -q -r requirements.txt
  pip install -q -e .
fi

# 2) Ingest + build + train (idempotent)
echo "[data] Ingesting top stories..."
python -m scripts.ingest || true

echo "[data] Building analytics..."
python -m scripts.build_analytics || true

echo "[ml] Training model..."
python -m scripts.train || true

# 3) Start API and UI
mkdir -p logs

if pgrep -fa "uvicorn hn_pulse.api:app" >/dev/null 2>&1; then
  echo "[api] Uvicorn already running"
else
  echo "[api] Starting FastAPI on :8000..."
  nohup uvicorn hn_pulse.api:app --host 0.0.0.0 --port 8000 --reload \
    > logs/api_8000.log 2>&1 & echo $! > logs/api_8000.pid
fi

if pgrep -fa "streamlit run hn_pulse/dashboard.py" >/dev/null 2>&1; then
  echo "[ui] Streamlit already running"
else
  echo "[ui] Starting Streamlit on :8501..."
  export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
  export STREAMLIT_HEADLESS=true
  nohup streamlit run hn_pulse/dashboard.py \
    --server.port 8501 --server.address 0.0.0.0 \
    --server.headless true --browser.gatherUsageStats false \
    > logs/ui_8501.log 2>&1 & echo $! > logs/ui_8501.pid
fi

# 4) Wait for ports
attempts=20
until curl -fsS http://localhost:8000/health >/dev/null 2>&1 || [ $attempts -le 0 ]; do sleep 0.5; attempts=$((attempts-1)); done
attempts=40
until curl -fsS http://localhost:8501 >/dev/null 2>&1 || [ $attempts -le 0 ]; do sleep 0.5; attempts=$((attempts-1)); done

API_LOCAL="http://localhost:8000/docs"
UI_LOCAL="http://localhost:8501"

# 5) Optional: start Cloudflare quick tunnels for public URLs
PUBLIC_API=""
PUBLIC_UI=""
if command -v cloudflared >/dev/null 2>&1 || [ -x ./cloudflared ]; then
  CF=cloudflared
  [ -x ./cloudflared ] && CF=./cloudflared
else
  echo "[tunnel] Downloading cloudflared..."
  curl -fsSL -o cloudflared https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 || true
  chmod +x cloudflared || true
  CF=./cloudflared
fi

if [ -x "$CF" ]; then
  echo "[tunnel] Starting public tunnels (best-effort)..."
  nohup "$CF" tunnel --url http://localhost:8000 --no-autoupdate > logs/cf_8000.log 2>&1 & echo $! > logs/cf_8000.pid || true
  nohup "$CF" tunnel --url http://localhost:8501 --no-autoupdate > logs/cf_8501.log 2>&1 & echo $! > logs/cf_8501.pid || true
  sleep 5
  PUBLIC_API=$(grep -m1 -Eo 'https://[^[:space:]]+trycloudflare.com' logs/cf_8000.log || true)
  PUBLIC_UI=$(grep -m1 -Eo 'https://[^[:space:]]+trycloudflare.com' logs/cf_8501.log || true)
fi

# 6) Print helpful output
echo
echo "✅ Ready!"
echo "- API (local):   $API_LOCAL"
[ -n "$PUBLIC_API" ] && echo "- API (public):  $PUBLIC_API"
echo "- UI  (local):   $UI_LOCAL"
[ -n "$PUBLIC_UI" ] && echo "- UI  (public):  $PUBLIC_UI"
echo