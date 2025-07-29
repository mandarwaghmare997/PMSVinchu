@echo off
REM PMS Intelligence Hub - Interactive Setup with Visual Progress
REM Clean, efficient setup with detailed progress indicators

setlocal enabledelayedexpansion
title PMS Intelligence Hub Setup

REM Load progress utilities
call "%~dp0progress_utils.bat" 2>nul || (
    echo Progress utilities not found, continuing without visual indicators...
)

cls
call :header "PMS Intelligence Hub - Interactive Setup"
echo ==========================================
echo  Portfolio Management Services Dashboard
echo  Interactive Setup with Progress Tracking
echo ==========================================
echo.

call :step 1 5 "Python Environment Check"

REM Function to find working Python command
call :find_python
if errorlevel 1 (
    call :error "No Python found. Installing Python automatically..."
    call :install_python
    if errorlevel 1 exit /b 1
    call :find_python
    if errorlevel 1 (
        call :error "Python installation failed"
        pause
        exit /b 1
    )
)

call :success "Using Python: %PYTHON_CMD% - Version: %PYTHON_VERSION%"

call :step 2 5 "Virtual Environment Setup"
call :setup_venv
if errorlevel 1 exit /b 1

call :step 3 5 "Dependency Installation"
call :install_deps
if errorlevel 1 exit /b 1

call :step 4 5 "Configuration Setup"
call :create_config

call :step 5 5 "Starting Application"
call :header "🎉 Setup Complete!"
echo.
echo ┌─────────────────────────────────────────────────────┐
echo │                                                     │
echo │  ✅ PMS Intelligence Hub is ready!                  │
echo │                                                     │
echo │  Dashboard will open at: http://localhost:8501     │
echo │  Press Ctrl+C to stop the application              │
echo │                                                     │
echo └─────────────────────────────────────────────────────┘
echo.

call :animated_dots "Starting dashboard" 3
pause

REM Start application
venv\Scripts\streamlit.exe run src\dashboard\main_dashboard.py --server.port 8501
goto :eof

REM ==========================================
REM Functions with Visual Progress
REM ==========================================

:find_python
set PYTHON_CMD=
set PYTHON_VERSION=

REM Refresh PATH from registry first
call :animated_dots "Refreshing system PATH" 2
for /f "tokens=2*" %%a in ('reg query "HKEY_CURRENT_USER\Environment" /v PATH 2^>nul') do set "UserPath=%%b"
for /f "tokens=2*" %%a in ('reg query "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PATH 2^>nul') do set "SysPath=%%b"
set "PATH=%SysPath%;%UserPath%;C:\Python311;C:\Python311\Scripts;%LOCALAPPDATA%\Programs\Python\Python311;%LOCALAPPDATA%\Programs\Python\Python311\Scripts"

call :animated_dots "Testing Python installations" 3
for %%c in ("py -3" py python python3) do (
    echo   Trying %%c...
    %%c --version >nul 2>&1
    if not errorlevel 1 (
        for /f "tokens=2" %%v in ('%%c --version 2^>^&1') do (
            set PYTHON_VERSION=%%v
            set PYTHON_CMD=%%c
            echo   ✓ Found working Python: %%c (%%v)
            goto :check_version
        )
    )
)

echo No working Python found. Please run:
echo   deployment\windows\fix_python_path.bat
echo.
echo Or install Python manually from https://python.org
exit /b 1

:check_version
REM Extract version numbers
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set MAJOR=%%a
    set MINOR=%%b
)
if "%MAJOR%"=="3" if %MINOR% geq 8 exit /b 0
call :error "Python 3.8+ required, found %PYTHON_VERSION%"
exit /b 1

:install_python
call :header "Automatic Python Installation"
call :animated_dots "Preparing Python installation" 2

if not exist temp mkdir temp
cd temp

call :download_progress "Python 3.11.7" "python.org"

REM Download Python installer
set INSTALLER=python-3.11.7-amd64.exe
set URL=https://www.python.org/ftp/python/3.11.7/%INSTALLER%

powershell -Command "Invoke-WebRequest -Uri '%URL%' -OutFile '%INSTALLER%'" >nul 2>&1
if errorlevel 1 (
    call :error "Download failed. Please install Python manually from https://python.org"
    cd ..
    exit /b 1
)

call :install_progress "Python 3.11.7"
%INSTALLER% /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1
if errorlevel 1 (
    echo Installation failed. Running interactive installer...
    %INSTALLER%
)

cd ..
rmdir /s /q temp 2>nul
call :success "Python installation completed"
call :animated_dots "Waiting for PATH update" 3
exit /b 0

:setup_venv
call :animated_dots "Setting up virtual environment" 2
if exist venv rmdir /s /q venv
%PYTHON_CMD% -m venv venv
if errorlevel 1 (
    call :error "Failed to create virtual environment"
    exit /b 1
)
call :success "Virtual environment created"
exit /b 0

:install_deps
call :animated_dots "Upgrading pip" 2
venv\Scripts\python.exe -m pip install --upgrade pip --quiet

echo Installing dependencies with progress tracking...

REM Try minimal requirements first
if exist requirements-core.txt (
    echo Installing core requirements...
    call :package_progress "Core Dependencies"
    venv\Scripts\pip.exe install -r requirements-core.txt --quiet
    if not errorlevel 1 (
        call :success "Core dependencies installed"
        exit /b 0
    )
)

REM Fallback to individual packages
echo Installing packages individually...
for %%p in (streamlit pandas plotly requests python-dotenv) do (
    call :package_progress "%%p"
    venv\Scripts\pip.exe install %%p --quiet
)
call :success "Dependencies installed"
exit /b 0

:create_config
if not exist .env (
    call :animated_dots "Creating configuration file" 2
    echo # PMS Intelligence Hub Configuration > .env
    echo SECRET_KEY=dev-secret-key-change-in-production >> .env
    echo ENVIRONMENT=development >> .env
    echo DEBUG=true >> .env
    call :success "Configuration created"
)
exit /b 0

