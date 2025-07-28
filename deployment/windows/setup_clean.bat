@echo off
REM PMS Intelligence Hub - Streamlined Windows Setup
REM One-command setup with automatic Python installation and dependency management

setlocal enabledelayedexpansion
title PMS Intelligence Hub Setup

echo.
echo ==========================================
echo  PMS Intelligence Hub - Quick Setup
echo ==========================================
echo.

REM Function to find working Python command
call :find_python
if errorlevel 1 (
    echo No Python found. Installing Python automatically...
    call :install_python
    if errorlevel 1 exit /b 1
    call :find_python
    if errorlevel 1 (
        echo ERROR: Python installation failed
        pause
        exit /b 1
    )
)

echo ✓ Using Python: %PYTHON_CMD%
echo ✓ Version: %PYTHON_VERSION%
echo.

REM Setup virtual environment
call :setup_venv
if errorlevel 1 exit /b 1

REM Install dependencies
call :install_deps
if errorlevel 1 exit /b 1

REM Create basic config
call :create_config

echo.
echo ==========================================
echo  Setup Complete!
echo ==========================================
echo.
echo Starting PMS Intelligence Hub...
echo Dashboard will open at: http://localhost:8501
echo Press Ctrl+C to stop
echo.
pause

REM Start application
venv\Scripts\streamlit.exe run src\dashboard\main_dashboard.py --server.port 8501
goto :eof

REM ==========================================
REM Functions
REM ==========================================

:find_python
set PYTHON_CMD=
set PYTHON_VERSION=

for %%c in (python py "py -3" python3) do (
    %%c --version >nul 2>&1
    if not errorlevel 1 (
        for /f "tokens=2" %%v in ('%%c --version 2^>^&1') do (
            set PYTHON_VERSION=%%v
            set PYTHON_CMD=%%c
            goto :check_version
        )
    )
)
exit /b 1

:check_version
REM Extract version numbers
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set MAJOR=%%a
    set MINOR=%%b
)
if %MAJOR%==3 if %MINOR% geq 8 exit /b 0
echo ERROR: Python 3.8+ required, found %PYTHON_VERSION%
exit /b 1

:install_python
echo.
echo Downloading and installing Python 3.11...
if not exist temp mkdir temp
cd temp

REM Download Python installer
set INSTALLER=python-3.11.7-amd64.exe
set URL=https://www.python.org/ftp/python/3.11.7/%INSTALLER%

echo Downloading Python installer...
powershell -Command "Invoke-WebRequest -Uri '%URL%' -OutFile '%INSTALLER%'" >nul 2>&1
if errorlevel 1 (
    echo Download failed. Please install Python manually from https://python.org
    cd ..
    exit /b 1
)

echo Installing Python (this may take a few minutes)...
%INSTALLER% /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1
if errorlevel 1 (
    echo Installation failed. Running interactive installer...
    %INSTALLER%
)

cd ..
rmdir /s /q temp 2>nul
echo ✓ Python installation completed
timeout /t 3 >nul
exit /b 0

:setup_venv
echo Setting up virtual environment...
if exist venv rmdir /s /q venv
%PYTHON_CMD% -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    exit /b 1
)
echo ✓ Virtual environment created
exit /b 0

:install_deps
echo Installing dependencies...
venv\Scripts\python.exe -m pip install --upgrade pip --quiet

REM Try minimal requirements first
if exist requirements-minimal.txt (
    echo Installing minimal requirements...
    venv\Scripts\pip.exe install -r requirements-minimal.txt --quiet
    if not errorlevel 1 (
        echo ✓ Minimal dependencies installed
        exit /b 0
    )
)

REM Fallback to full requirements with error handling
echo Installing full requirements...
venv\Scripts\pip.exe install -r requirements.txt --quiet
if errorlevel 1 (
    echo Some packages failed. Installing core packages individually...
    for %%p in (streamlit pandas plotly requests python-dotenv) do (
        echo Installing %%p...
        venv\Scripts\pip.exe install %%p --quiet
    )
)
echo ✓ Dependencies installed
exit /b 0

:create_config
if not exist .env (
    echo Creating basic configuration...
    echo # PMS Intelligence Hub Configuration > .env
    echo SECRET_KEY=dev-secret-key-change-in-production >> .env
    echo ENVIRONMENT=development >> .env
    echo DEBUG=true >> .env
    echo ✓ Configuration created
)
exit /b 0

