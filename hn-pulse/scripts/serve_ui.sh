#!/usr/bin/env bash
set -euo pipefail
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
export STREAMLIT_HEADLESS=true
exec streamlit run hn_pulse/dashboard.py --server.port 8501 --server.address 0.0.0.0 --server.headless true --browser.gatherUsageStats false
