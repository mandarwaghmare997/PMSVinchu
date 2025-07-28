@echo off
REM PMS Intelligence Hub - Clean Deployment Script
REM Usage: deploy_clean.bat [local|docker]

setlocal enabledelayedexpansion

set MODE=%1
if "%MODE%"=="" set MODE=local

echo.
echo ==========================================
echo  PMS Hub - %MODE% Deployment
echo ==========================================
echo.

if "%MODE%"=="docker" goto :docker_deploy

REM Local deployment
call :find_python
if errorlevel 1 (
    echo Python not found. Run setup_clean.bat first.
    pause
    exit /b 1
)

call :setup_local
goto :eof

:docker_deploy
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker not found. Please install Docker Desktop.
    pause
    exit /b 1
)

echo Starting Docker deployment...
docker-compose -f deployment\windows\docker-compose.windows.yml up -d
echo ✓ Docker services started
echo Dashboard: http://localhost:8501
goto :eof

:find_python
for %%c in (python py "py -3") do (
    %%c --version >nul 2>&1
    if not errorlevel 1 (
        set PYTHON_CMD=%%c
        exit /b 0
    )
)
exit /b 1

:setup_local
echo Setting up local environment...
if not exist venv %PYTHON_CMD% -m venv venv
venv\Scripts\pip.exe install -r requirements-minimal.txt --quiet
echo ✓ Environment ready
echo Starting dashboard...
venv\Scripts\streamlit.exe run src\dashboard\main_dashboard.py --server.port 8501
exit /b 0

