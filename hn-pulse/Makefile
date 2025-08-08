.PHONY: setup ingest build train api ui test fmt

VENV?=.venv
PY?=$(VENV)/bin/python
PIP?=$(VENV)/bin/pip
UVICORN?=$(VENV)/bin/uvicorn
STREAMLIT?=$(VENV)/bin/streamlit
PYTEST?=$(VENV)/bin/pytest

setup:
	python3 -m venv $(VENV)
	. $(VENV)/bin/activate; $(PIP) install -r requirements.txt

ingest:
	$(PY) -m scripts.ingest

build:
	$(PY) -m scripts.build_analytics

train:
	$(PY) -m scripts.train

api:
	bash scripts/serve_api.sh

ui:
	bash scripts/serve_ui.sh

test:
	$(PYTEST) -q

fmt:
	$(PY) -m pip install ruff black
	ruff check --fix hn_pulse scripts tests
	black hn_pulse scripts tests
