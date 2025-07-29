@echo off
REM PMS Intelligence Hub - Ultimate Windows Setup
REM Single script that handles everything automatically

title PMS Hub Ultimate Setup

REM Check for admin privileges and elevate if needed
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting Administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

echo.
echo ================================================
echo  PMS Intelligence Hub - Ultimate Setup
echo  Running as Administrator
echo ================================================
echo.

REM Set working directory to script location
cd /d "%~dp0"
cd ..\..

echo Current directory: %CD%
echo.

echo [1/5] Checking Python installation...

REM Clear any existing Python variables
set PYTHON_CMD=
set PYTHON_FOUND=0

REM Add common Python paths to current session
set "PATH=%PATH%;C:\Python311;C:\Python311\Scripts;%LOCALAPPDATA%\Programs\Python\Python311;%LOCALAPPDATA%\Programs\Python\Python311\Scripts;C:\Program Files\Python311;C:\Program Files\Python311\Scripts"

REM Test Python commands without loops
echo Testing py command...
py --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=py
    set PYTHON_FOUND=1
    echo Found: py command works
    goto :python_ready
)

echo Testing python command...
python --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python
    set PYTHON_FOUND=1
    echo Found: python command works
    goto :python_ready
)

echo Testing python3 command...
python3 --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python3
    set PYTHON_FOUND=1
    echo Found: python3 command works
    goto :python_ready
)

REM If no Python found, install it
if %PYTHON_FOUND%==0 (
    echo No Python found. Installing Python 3.11.7...
    goto :install_python
)

:python_ready
echo Python command: %PYTHON_CMD%
%PYTHON_CMD% --version
echo.

echo [2/5] Setting up virtual environment...
if exist venv (
    echo Removing old virtual environment...
    rmdir /s /q venv
)

echo Creating new virtual environment...
%PYTHON_CMD% -m venv venv
if errorlevel 1 (
    echo Virtual environment creation failed. Installing venv module...
    %PYTHON_CMD% -m pip install virtualenv
    %PYTHON_CMD% -m virtualenv venv
    if errorlevel 1 (
        echo ERROR: Cannot create virtual environment
        echo This usually means Python is not properly installed
        goto :install_python
    )
)
echo Virtual environment created successfully
echo.

echo [3/5] Installing core packages...
echo Upgrading pip...
venv\Scripts\python.exe -m pip install --upgrade pip --quiet --no-warn-script-location

echo Installing streamlit...
venv\Scripts\python.exe -m pip install streamlit --quiet --no-warn-script-location
if errorlevel 1 (
    echo Streamlit installation failed, trying alternative...
    venv\Scripts\pip.exe install streamlit --no-deps --quiet
)

echo Installing pandas...
venv\Scripts\python.exe -m pip install pandas --quiet --no-warn-script-location

echo Installing plotly...
venv\Scripts\python.exe -m pip install plotly --quiet --no-warn-script-location

echo Installing openpyxl...
venv\Scripts\python.exe -m pip install openpyxl --quiet --no-warn-script-location

echo Installing numpy...
venv\Scripts\python.exe -m pip install numpy --quiet --no-warn-script-location

echo Core packages installed
echo.

echo [4/5] Creating configuration...
if not exist .env (
    echo Creating .env file...
    echo SECRET_KEY=dev-secret-key > .env
    echo ENVIRONMENT=development >> .env
    echo DEBUG=true >> .env
)
echo Configuration ready
echo.

echo [5/5] Starting application...
echo.
echo ================================================
echo  PMS Intelligence Hub is starting...
echo  
echo  Dashboard URL: http://localhost:8501
echo  Press Ctrl+C to stop the application
echo ================================================
echo.

REM Start the ultimate dashboard
if exist "src\dashboard\ultimate_dashboard.py" (
    echo Starting ultimate dashboard with all advanced features...
    echo.
    echo Ultimate Features Available:
    echo ✅ Advanced Financial Metrics (Alpha, Beta, Sharpe, VaR)
    echo ✅ Professional UI/UX with Animations  
    echo ✅ Data Upload with Intelligent Merging
    echo ✅ 150+ Sample Records with Realistic Data
    echo ✅ SQLite Data Persistence
    echo ✅ Advanced Charts and Visualizations
    echo ✅ Risk-Return Analysis
    echo ✅ Performance Attribution
    echo ✅ Export Capabilities (CSV, Excel, JSON)
    echo.
    venv\Scripts\streamlit.exe run src\dashboard\ultimate_dashboard.py --server.port 8501 --server.address 0.0.0.0
) else if exist "src\dashboard\enhanced_dashboard.py" (
    echo Starting enhanced dashboard...
    venv\Scripts\streamlit.exe run src\dashboard\enhanced_dashboard.py --server.port 8501 --server.address 0.0.0.0
) else if exist "src\dashboard\simple_dashboard.py" (
    echo Starting simplified dashboard...
    venv\Scripts\streamlit.exe run src\dashboard\simple_dashboard.py --server.port 8501 --server.address 0.0.0.0
) else if exist "src\dashboard\main_dashboard.py" (
    echo Starting main dashboard...
    venv\Scripts\streamlit.exe run src\dashboard\main_dashboard.py --server.port 8501 --server.address 0.0.0.0
) else (
    echo ERROR: Dashboard files not found
    echo Please ensure you are running this script from the PMSVinchu directory
    pause
    exit /b 1
)

goto :end

:install_python
echo.
echo ================================================
echo  Installing Python 3.11.7
echo ================================================
echo.

REM Create temp directory
if not exist temp mkdir temp
cd temp

echo Downloading Python installer...
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe' -OutFile 'python_installer.exe'}"

if not exist python_installer.exe (
    echo Download failed. Please check internet connection.
    echo You can manually download Python from: https://python.org
    pause
    exit /b 1
)

echo Installing Python (this will take a few minutes)...
python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1 Include_launcher=1 Include_test=0

echo Cleaning up...
del python_installer.exe
cd ..
rmdir temp

echo Python installation completed
echo Refreshing environment...

REM Refresh PATH
set "PATH=%PATH%;C:\Python311;C:\Python311\Scripts;%LOCALAPPDATA%\Programs\Python\Python311;%LOCALAPPDATA%\Programs\Python\Python311\Scripts"

REM Wait a moment for installation to complete
timeout /t 5 /nobreak >nul

REM Test Python again
py --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=py
    echo Python is now available: py
    goto :python_ready
)

python --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python
    echo Python is now available: python
    goto :python_ready
)

echo ERROR: Python installation failed or PATH not updated
echo Please restart your computer and try again
echo Or manually install Python from https://python.org
pause
exit /b 1

:end
echo.
echo Setup completed. Press any key to exit.
pause >nul

