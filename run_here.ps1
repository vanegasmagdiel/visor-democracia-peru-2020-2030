Set-Location $PSScriptRoot
if (-not (Test-Path .venv)) { py -3.12 -m venv .venv }
& .\.venv\Scripts\Activate.ps1
python -m pip install --disable-pip-version-check -r requirements-lock.txt
python -m shiny run --launch-browser app.py
