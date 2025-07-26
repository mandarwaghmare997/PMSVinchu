@echo off
REM PMS Intelligence Hub - Windows Service Removal Script
REM This script removes the PMS Hub Windows service

setlocal enabledelayedexpansion

echo.
echo ==========================================
echo  PMS Intelligence Hub Service Removal
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

REM Check if service exists
sc query PMSIntelligenceHub >nul 2>&1
if errorlevel 1 (
    echo Service 'PMSIntelligenceHub' is not installed.
    echo Nothing to remove.
    pause
    exit /b 0
)

echo Service 'PMSIntelligenceHub' found.
echo.

REM Confirm removal
set /p CONFIRM="Are you sure you want to remove the PMS Intelligence Hub service? (y/n): "
if /i not "%CONFIRM%"=="y" (
    echo Service removal cancelled.
    pause
    exit /b 0
)

REM Stop the service if running
echo Checking service status...
sc query PMSIntelligenceHub | find "RUNNING" >nul
if not errorlevel 1 (
    echo Service is running. Stopping...
    net stop PMSIntelligenceHub
    
    REM Wait a moment for service to stop
    timeout /t 5 /nobreak >nul
)

REM Remove the service
echo Removing service...
venv\Scripts\python.exe deployment\windows\service\pms_hub_service.py remove

if errorlevel 1 (
    echo.
    echo ERROR: Service removal failed!
    echo.
    echo You can try manual removal:
    echo   sc delete PMSIntelligenceHub
    echo.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo  Service Removal Completed!
echo ==========================================
echo.
echo The PMS Intelligence Hub Windows service has been removed.
echo.
echo To reinstall the service, run:
echo   deployment\windows\service\install_service.bat
echo.
echo To run the application manually:
echo   deployment\windows\deploy.bat local
echo.
pause

