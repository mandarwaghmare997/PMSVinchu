@echo off
REM PMS Intelligence Hub - Simple Windows 10 Deployment
REM Single script to install and run everything

title PMS Hub Setup
echo.
echo PMS Intelligence Hub - Simple Setup
echo ===================================
echo.

REM Check if already set up
if exist "venv\Scripts\streamlit.exe" (
    echo Setup already complete. Starting dashboard...
    goto :start_app
)

echo Step 1: Finding Python...

REM Try different Python commands
set PYTHON_CMD=
py --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=py
    echo Found Python: py
    goto :python_ok
)

python --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python
    echo Found Python: python
    goto :python_ok
)

python3 --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python3
    echo Found Python: python3
    goto :python_ok
)

echo Python not found. Please install Python from https://python.org
echo Make sure to check "Add Python to PATH" during installation
pause
exit /b 1

:python_ok
echo Step 2: Creating virtual environment...
if exist venv rmdir /s /q venv
%PYTHON_CMD% -m venv venv
if errorlevel 1 (
    echo Failed to create virtual environment
    echo Trying alternative method...
    %PYTHON_CMD% -m pip install virtualenv --user
    %PYTHON_CMD% -m virtualenv venv
    if errorlevel 1 (
        echo ERROR: Cannot create virtual environment
        echo Please run as Administrator or check Python installation
        pause
        exit /b 1
    )
)
echo Virtual environment created

echo Step 3: Installing packages...
venv\Scripts\python.exe -m pip install --upgrade pip
if errorlevel 1 (
    echo Warning: pip upgrade failed, continuing...
)

echo Installing streamlit...
venv\Scripts\pip.exe install streamlit
if errorlevel 1 (
    echo Failed to install streamlit
    pause
    exit /b 1
)

echo Installing pandas...
venv\Scripts\pip.exe install pandas
if errorlevel 1 (
    echo Warning: pandas installation failed, continuing...
)

echo Installing plotly...
venv\Scripts\pip.exe install plotly
if errorlevel 1 (
    echo Warning: plotly installation failed, continuing...
)

echo Installing requests...
venv\Scripts\pip.exe install requests
if errorlevel 1 (
    echo Warning: requests installation failed, continuing...
)

echo Installing python-dotenv...
venv\Scripts\pip.exe install python-dotenv
if errorlevel 1 (
    echo Warning: python-dotenv installation failed, continuing...
)

echo Step 4: Creating config...
if not exist .env (
    echo SECRET_KEY=dev-key > .env
    echo ENVIRONMENT=development >> .env
)

:start_app
echo.
echo Starting PMS Intelligence Hub...
echo Dashboard URL: http://localhost:8501
echo Press Ctrl+C to stop
echo.

REM Check if streamlit exists
if not exist "venv\Scripts\streamlit.exe" (
    echo ERROR: Streamlit not installed properly
    echo Please check the installation errors above
    pause
    exit /b 1
)

REM Start the application
venv\Scripts\streamlit.exe run src\dashboard\main_dashboard.py --server.port 8501 --server.address 0.0.0.0
if errorlevel 1 (
    echo.
    echo ERROR: Failed to start dashboard
    echo Possible issues:
    echo 1. Missing src\dashboard\main_dashboard.py file
    echo 2. Python package conflicts
    echo 3. Port 8501 already in use
    echo.
    echo Trying alternative startup...
    venv\Scripts\python.exe -m streamlit run src\dashboard\main_dashboard.py --server.port 8501
)

pause

