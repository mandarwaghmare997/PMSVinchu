@echo off
REM PMS Intelligence Hub - Windows Service Installation Script
REM This script installs the PMS Hub as a Windows service

setlocal enabledelayedexpansion

echo.
echo ==========================================
echo  PMS Intelligence Hub Service Installer
echo ==========================================
echo.

REM Check for administrator privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Administrator privileges required!
    echo.
    echo Please run this script as Administrator:
    echo 1. Right-click on Command Prompt
    echo 2. Select "Run as administrator"
    echo 3. Navigate to this directory and run the script again
    echo.
    pause
    exit /b 1
)

echo Running with administrator privileges ✓
echo.

REM Check if Python virtual environment exists
if not exist "venv\Scripts\python.exe" (
    echo ERROR: Python virtual environment not found!
    echo.
    echo Please run the setup first:
    echo   deployment\windows\setup.bat
    echo.
    pause
    exit /b 1
)

echo Python virtual environment found ✓

REM Check if pywin32 is installed
echo Checking pywin32 installation...
venv\Scripts\python.exe -c "import win32serviceutil" >nul 2>&1
if errorlevel 1 (
    echo Installing pywin32...
    venv\Scripts\pip.exe install pywin32
    if errorlevel 1 (
        echo ERROR: Failed to install pywin32
        pause
        exit /b 1
    )
    
    REM Run post-install script for pywin32
    echo Running pywin32 post-install...
    venv\Scripts\python.exe venv\Scripts\pywin32_postinstall.py -install
)

echo pywin32 is available ✓
echo.

REM Install the service
echo Installing PMS Intelligence Hub Windows Service...
venv\Scripts\python.exe deployment\windows\service\pms_hub_service.py install

if errorlevel 1 (
    echo.
    echo ERROR: Service installation failed!
    echo.
    echo Common issues:
    echo - Make sure you're running as Administrator
    echo - Check that no antivirus is blocking the installation
    echo - Ensure Windows Service Control Manager is running
    echo.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo  Service Installation Completed!
echo ==========================================
echo.
echo Service Details:
echo   Name: PMSIntelligenceHub
echo   Display Name: PMS Intelligence Hub Dashboard
echo   Description: Portfolio Management Services Intelligence Dashboard
echo.
echo Service Management Commands:
echo   Start:   net start PMSIntelligenceHub
echo   Stop:    net stop PMSIntelligenceHub
echo   Remove:  deployment\windows\service\remove_service.bat
echo.

set /p START_SERVICE="Do you want to start the service now? (y/n): "
if /i "%START_SERVICE%"=="y" (
    echo.
    echo Starting service...
    net start PMSIntelligenceHub
    
    if errorlevel 1 (
        echo.
        echo Service start failed. Check the logs for details:
        echo   logs\pms_service.log
        echo.
    ) else (
        echo.
        echo ==========================================
        echo  Service Started Successfully!
        echo ==========================================
        echo.
        echo The PMS Intelligence Hub is now running as a Windows service.
        echo.
        echo Access the dashboard at: http://localhost:8501
        echo.
        echo The service will automatically start when Windows boots.
        echo.
    )
)

echo.
echo Installation script completed.
pause

