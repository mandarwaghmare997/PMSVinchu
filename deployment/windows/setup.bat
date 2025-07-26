@echo off
REM PMS Intelligence Hub - Quick Windows Setup
REM This script provides a simple one-click setup for Windows users

setlocal enabledelayedexpansion

echo.
echo ==========================================
echo  PMS Intelligence Hub - Quick Setup
echo ==========================================
echo.
echo This script will:
echo  1. Check system requirements
echo  2. Set up Python virtual environment
echo  3. Install dependencies
echo  4. Configure the application
echo  5. Start the dashboard
echo.

REM Check for administrator privileges
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running with administrator privileges
) else (
    echo Note: Not running as administrator
    echo Some features may require elevated privileges
)

echo.
set /p CONTINUE="Do you want to continue? (y/n): "
if /i not "%CONTINUE%"=="y" (
    echo Setup cancelled.
    pause
    exit /b 0
)

echo.
echo ==========================================
echo  Step 1: Checking Requirements
echo ==========================================

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python is not installed!
    echo.
    echo Please install Python 3.8+ from: https://python.org
    echo Make sure to:
    echo  - Check "Add Python to PATH" during installation
    echo  - Install for all users (recommended)
    echo.
    echo After installing Python, run this script again.
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ Python %PYTHON_VERSION% found

REM Check pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: pip is not available!
    echo Please reinstall Python with pip included.
    pause
    exit /b 1
)
echo ✓ pip is available

REM Check Git (optional)
git --version >nul 2>&1
if errorlevel 1 (
    echo ! Git not found (optional for development)
) else (
    echo ✓ Git is available
)

echo.
echo ==========================================
echo  Step 2: Setting Up Environment
echo ==========================================

REM Create virtual environment
if exist "venv" (
    echo Virtual environment already exists
    set /p RECREATE="Do you want to recreate it? (y/n): "
    if /i "!RECREATE!"=="y" (
        echo Removing existing virtual environment...
        rmdir /s /q venv
    )
)

if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment activated

echo.
echo ==========================================
echo  Step 3: Installing Dependencies
echo ==========================================

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip --quiet

REM Install requirements
echo Installing application dependencies...
echo This may take a few minutes...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo.
    echo This might be due to:
    echo  - Network connectivity issues
    echo  - Missing system dependencies
    echo  - Incompatible Python version
    echo.
    echo Try running: pip install -r requirements.txt
    echo to see detailed error messages.
    pause
    exit /b 1
)
echo ✓ Dependencies installed successfully

echo.
echo ==========================================
echo  Step 4: Configuration Setup
echo ==========================================

REM Create directories
echo Creating application directories...
if not exist "cache" mkdir cache
if not exist "logs" mkdir logs
if not exist "exports" mkdir exports
if not exist "uploads" mkdir uploads
if not exist "backups" mkdir backups
echo ✓ Directories created

REM Setup configuration file
if not exist ".env" (
    if exist ".env.example" (
        echo Creating configuration file...
        copy .env.example .env >nul
        echo ✓ Configuration file created from template
        echo.
        echo IMPORTANT: You need to configure your API credentials
        echo The .env file contains settings for:
        echo  - Salesforce CRM integration
        echo  - Wealth Spectrum PMS integration
        echo  - Database configuration
        echo  - Security settings
        echo.
        set /p EDIT_CONFIG="Do you want to edit the configuration now? (y/n): "
        if /i "!EDIT_CONFIG!"=="y" (
            notepad .env
        )
    ) else (
        echo WARNING: .env.example file not found
        echo You may need to create a .env file manually
    )
) else (
    echo ✓ Configuration file already exists
)

echo.
echo ==========================================
echo  Step 5: Starting Application
echo ==========================================

echo.
echo Setup completed successfully!
echo.
echo The PMS Intelligence Hub dashboard will now start.
echo.
echo Access URLs:
echo  Dashboard: http://localhost:8501
echo  API Docs:  http://localhost:8000/docs (if API is running)
echo.
echo Press Ctrl+C to stop the application when you're done.
echo.
pause

REM Start the dashboard
echo Starting PMS Intelligence Hub...
streamlit run src\dashboard\main_dashboard.py --server.port 8501 --server.address 0.0.0.0

echo.
echo Application stopped.
echo.
echo To start again, run:
echo   venv\Scripts\activate.bat
echo   streamlit run src\dashboard\main_dashboard.py
echo.
echo Or use the deployment scripts:
echo   deployment\windows\deploy.bat local
echo   deployment\windows\deploy.ps1 -Environment local
echo.
pause

