#!/usr/bin/env bash
set -euo pipefail
exec streamlit run hn_pulse/dashboard.py --server.port 8501 --server.address 0.0.0.0
