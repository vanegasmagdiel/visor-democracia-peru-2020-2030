Set-Location $PSScriptRoot
if (-not (Test-Path .venv)) { py -3 -m venv .venv }
& .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m shiny run --launch-browser app.py
