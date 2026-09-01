@echo off
setlocal
cd /d "%~dp0"
if not exist .venv (py -3.12 -m venv .venv)
call .venv\Scripts\activate.bat
python -m pip install --disable-pip-version-check -r requirements-lock.txt
python -m shiny run --launch-browser app.py
