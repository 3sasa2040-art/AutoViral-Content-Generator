@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  py -3 -m venv .venv || (echo Python 3 is vereist.&pause&exit /b 1)
  call .venv\Scripts\activate.bat
  python -m pip install --upgrade pip
  python -m pip install -r requirements.txt
  python -m playwright install chromium
) else call .venv\Scripts\activate.bat
python -m app.approval_gui
if errorlevel 1 pause
