#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
[ -d .venv ] || python3 -m venv .venv
source .venv/bin/activate
python -m pip install --disable-pip-version-check -r requirements-lock.txt
python -m shiny run --launch-browser app.py
