@echo off
REM PMS Intelligence Hub - Ultimate Quick Start
REM One command to rule them all: installs Python, dependencies, and starts the app

title PMS Hub Quick Start
color 0A

echo.
echo  ██████╗ ███╗   ███╗███████╗    ██╗  ██╗██╗   ██╗██████╗ 
echo  ██╔══██╗████╗ ████║██╔════╝    ██║  ██║██║   ██║██╔══██╗
echo  ██████╔╝██╔████╔██║███████╗    ███████║██║   ██║██████╔╝
echo  ██╔═══╝ ██║╚██╔╝██║╚════██║    ██╔══██║██║   ██║██╔══██╗
echo  ██║     ██║ ╚═╝ ██║███████║    ██║  ██║╚██████╔╝██████╔╝
echo  ╚═╝     ╚═╝     ╚═╝╚══════╝    ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ 
echo.
echo  Portfolio Management Services Intelligence Hub
echo  Quick Start - Everything in one command!
echo.

REM Check if already set up
if exist "venv\Scripts\streamlit.exe" (
    echo ✓ Already set up! Starting dashboard...
    goto :start_app
)

echo [1/4] Checking Python...
for %%c in (python py "py -3") do (
    %%c --version >nul 2>&1 && (
        set PYTHON_CMD=%%c
        goto :python_ok
    )
)

echo Python not found. Installing automatically...
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe' -OutFile 'python_installer.exe'" && python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1 && del python_installer.exe && timeout /t 5 >nul
set PYTHON_CMD=python

:python_ok
echo ✓ Python ready

echo [2/4] Creating environment...
if exist venv rmdir /s /q venv >nul 2>&1
%PYTHON_CMD% -m venv venv || (echo ERROR: Virtual environment failed & pause & exit /b 1)
echo ✓ Environment created

echo [3/4] Installing packages...
venv\Scripts\pip install streamlit pandas plotly requests python-dotenv --quiet || (
    echo Trying alternative installation...
    venv\Scripts\pip install streamlit pandas plotly --quiet
)
echo ✓ Packages installed

echo [4/4] Creating config...
if not exist .env echo SECRET_KEY=dev-key > .env
echo ✓ Config ready

:start_app
echo.
echo ==========================================
echo  🚀 Starting PMS Intelligence Hub
echo ==========================================
echo.
echo Dashboard URL: http://localhost:8501
echo Press Ctrl+C to stop
echo.
timeout /t 3 >nul

venv\Scripts\streamlit run src\dashboard\main_dashboard.py --server.port 8501 --server.address 0.0.0.0

