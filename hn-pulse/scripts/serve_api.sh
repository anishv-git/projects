#!/usr/bin/env bash
set -euo pipefail
exec uvicorn hn_pulse.api:app --host 0.0.0.0 --port 8000 --reload
