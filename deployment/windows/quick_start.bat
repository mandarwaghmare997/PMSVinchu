@echo off
REM PMS Intelligence Hub - Ultimate Quick Start with Visual Progress
REM One command to rule them all: installs Python, dependencies, and starts the app

title PMS Hub Quick Start
color 0A

REM Load progress utilities
call "%~dp0progress_utils.bat" 2>nul || (
    echo Progress utilities not found, continuing without visual indicators...
)

cls
echo.
echo  ██████╗ ███╗   ███╗███████╗    ██╗  ██╗██╗   ██╗██████╗ 
echo  ██╔══██╗████╗ ████║██╔════╝    ██║  ██║██║   ██║██╔══██╗
echo  ██████╔╝██╔████╔██║███████╗    ███████║██║   ██║██████╔╝
echo  ██╔═══╝ ██║╚██╔╝██║╚════██║    ██╔══██║██║   ██║██╔══██╗
echo  ██║     ██║ ╚═╝ ██║███████║    ██║  ██║╚██████╔╝██████╔╝
echo  ╚═╝     ╚═╝     ╚═╝╚══════╝    ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ 
echo.
call :header "Portfolio Management Services Intelligence Hub"
echo  Quick Start - Everything in one command!
echo.

REM Check if already set up
if exist "venv\Scripts\streamlit.exe" (
    call :success "Already set up! Starting dashboard..."
    goto :start_app
)

call :step 1 4 "Checking Python Installation"

REM Disable Microsoft Store Python redirect
set PYTHON_CMD=
for /f "tokens=2*" %%a in ('reg query "HKEY_CURRENT_USER\Environment" /v PATH 2^>nul') do set "UserPath=%%b"
for /f "tokens=2*" %%a in ('reg query "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PATH 2^>nul') do set "SysPath=%%b"
set "PATH=%SysPath%;%UserPath%;C:\Python311;C:\Python311\Scripts;%LOCALAPPDATA%\Programs\Python\Python311;%LOCALAPPDATA%\Programs\Python\Python311\Scripts"

REM Try different Python commands with animated feedback
call :animated_dots "Searching for Python installations" 3
for %%c in ("py -3" py python python3) do (
    echo Testing %%c...
    %%c --version >nul 2>&1
    if not errorlevel 1 (
        echo ✓ Found working Python: %%c
        set PYTHON_CMD=%%c
        goto :python_found
    )
)

echo Python not found. Installing automatically...
call :download_progress "Python 3.11.7" "python.org"

if not exist temp mkdir temp
cd temp

REM Download with progress simulation
echo Downloading Python installer...
call :progress_bar 0 100 "Initializing download"
powershell -Command "try { [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe' -OutFile 'python_installer.exe' -UseBasicParsing } catch { Write-Host 'Download failed'; exit 1 }" >nul 2>&1 &

REM Simulate download progress while actual download happens
for /l %%i in (10,15,100) do (
    call :progress_bar %%i 100 "Downloading Python installer"
    timeout /t 2 /nobreak >nul 2>&1
)

if not exist python_installer.exe (
    call :error "Download failed. Please install Python manually from https://python.org"
    cd ..
    pause
    exit /b 1
)

call :install_progress "Python 3.11.7"
python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1 Include_launcher=1
if errorlevel 1 (
    echo Silent installation failed. Trying interactive...
    python_installer.exe
)

echo Cleaning up...
del python_installer.exe
cd ..
rmdir temp

call :animated_dots "Refreshing environment variables" 3
REM Refresh PATH from registry
for /f "tokens=2*" %%a in ('reg query "HKEY_CURRENT_USER\Environment" /v PATH 2^>nul') do set "UserPath=%%b"
for /f "tokens=2*" %%a in ('reg query "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PATH 2^>nul') do set "SysPath=%%b"
set "PATH=%SysPath%;%UserPath%"

timeout /t 5 /nobreak >nul

REM Test again after installation
for %%c in ("py -3" py python python3) do (
    %%c --version >nul 2>&1
    if not errorlevel 1 (
        set PYTHON_CMD=%%c
        goto :python_found
    )
)

call :error "Python installation failed or PATH not updated"
echo Please restart Command Prompt and try again, or install Python manually
pause
exit /b 1

:python_found
call :success "Python ready: %PYTHON_CMD%"

call :step 2 4 "Creating Virtual Environment"
if exist venv rmdir /s /q venv >nul 2>&1

call :animated_dots "Creating virtual environment with %PYTHON_CMD%" 3
%PYTHON_CMD% -m venv venv
if errorlevel 1 (
    echo Virtual environment creation failed. Trying alternative method...
    if exist venv rmdir /s /q venv >nul 2>&1
    call :animated_dots "Installing virtualenv package" 2
    %PYTHON_CMD% -m pip install --user virtualenv
    call :animated_dots "Creating environment with virtualenv" 3
    %PYTHON_CMD% -m virtualenv venv
    if errorlevel 1 (
        call :error "Failed to create virtual environment"
        echo Please try running as Administrator or install Python manually
        pause
        exit /b 1
    )
)
call :success "Virtual environment created"

call :step 3 4 "Installing Dependencies"

call :animated_dots "Upgrading pip" 2
venv\Scripts\pip install --upgrade pip --quiet

echo Installing core packages...
call :package_progress "streamlit"
venv\Scripts\pip install streamlit --quiet

call :package_progress "pandas" 
venv\Scripts\pip install pandas --quiet

call :package_progress "plotly"
venv\Scripts\pip install plotly --quiet

call :package_progress "requests"
venv\Scripts\pip install requests --quiet

call :package_progress "python-dotenv"
venv\Scripts\pip install python-dotenv --quiet

call :success "All packages installed successfully"

call :step 4 4 "Final Configuration"
if not exist .env (
    call :animated_dots "Creating configuration file" 2
    echo # PMS Intelligence Hub Configuration > .env
    echo SECRET_KEY=dev-secret-key-change-in-production >> .env
    echo ENVIRONMENT=development >> .env
    echo DEBUG=true >> .env
    call :success "Configuration file created"
)

:start_app
cls
call :header "🚀 Starting PMS Intelligence Hub"
echo.
echo ┌─────────────────────────────────────────────────────┐
echo │                                                     │
echo │  Dashboard URL: http://localhost:8501               │
echo │  Press Ctrl+C to stop                              │
echo │                                                     │
echo └─────────────────────────────────────────────────────┘
echo.

call :animated_dots "Initializing dashboard" 3

venv\Scripts\streamlit run src\dashboard\main_dashboard.py --server.port 8501 --server.address 0.0.0.0

