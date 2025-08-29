@echo off
setlocal enabledelayedexpansion

echo ========================================
echo PMS Intelligence Hub - Smart Update v2.0
echo ========================================
echo.

:: Store original directory
set "ORIGINAL_DIR=%CD%"

:: Find PMSVinchu directory
if exist "PMSVinchu" (
    cd PMSVinchu
) else if exist "..\PMSVinchu" (
    cd ..\PMSVinchu
) else if exist "..\..\PMSVinchu" (
    cd ..\..\PMSVinchu
) else (
    echo Searching for PMSVinchu directory...
    for /d %%i in (C:\Users\%USERNAME%\*PMSVinchu*) do (
        if exist "%%i\.git" (
            cd /d "%%i"
            goto :found_repo
        )
    )
    echo ERROR: PMSVinchu directory not found
    echo Please run this script from the PMSVinchu directory or its parent
    pause
    exit /b 1
)

:found_repo
echo Found repository at: %CD%
echo.

:: Kill any running processes
echo [0/8] Stopping running services...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im streamlit.exe >nul 2>&1
timeout /t 2 >nul

:: Check git status
echo [1/8] Checking repository status...
git status --porcelain > temp_status.txt
set /p GIT_STATUS=<temp_status.txt
del temp_status.txt

if not "!GIT_STATUS!"=="" (
    echo WARNING: You have uncommitted changes
    echo These will be safely stashed during update
    echo.
)

:: Backup critical files
echo [2/8] Creating backup of important files...
if not exist "backup" mkdir backup
if exist ".env" copy ".env" "backup\.env_%date:~-4,4%%date:~-10,2%%date:~-7,2%" >nul 2>&1
if exist "pms_client_data.db" copy "pms_client_data.db" "backup\pms_client_data.db_%date:~-4,4%%date:~-10,2%%date:~-7,2%" >nul 2>&1
if exist "src\dashboard\pms_client_data.db" copy "src\dashboard\pms_client_data.db" "backup\dashboard_db_%date:~-4,4%%date:~-10,2%%date:~-7,2%" >nul 2>&1

:: Fetch and check for updates
echo [3/8] Checking for updates...
git fetch origin master
for /f %%i in ('git rev-list HEAD...origin/master --count') do set COMMITS_BEHIND=%%i

if "!COMMITS_BEHIND!"=="0" (
    echo ✅ Repository is up to date!
    goto :update_dependencies
)

echo Found !COMMITS_BEHIND! new updates. Downloading...

:: Stash changes and pull
echo [4/8] Stashing local changes...
git add . >nul 2>&1
git stash push -m "Auto-backup before update %date% %time%" >nul 2>&1

echo [5/8] Downloading latest version...
git pull origin master
if errorlevel 1 (
    echo ERROR: Failed to download updates
    echo Restoring your changes...
    git stash pop >nul 2>&1
    pause
    exit /b 1
)

echo [6/8] Restoring your local changes...
git stash pop >nul 2>&1

:update_dependencies
echo [7/8] Updating dependencies...

:: Check and setup Python environment
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        echo Make sure Python 3.11+ is installed
        pause
        exit /b 1
    )
)

:: Activate and update dependencies
call venv\Scripts\activate.bat
echo Updating Python packages...
python -m pip install --upgrade pip >nul 2>&1

:: Install based on available requirements file
if exist "requirements-core.txt" (
    pip install -r requirements-core.txt >nul 2>&1
) else if exist "requirements.txt" (
    pip install -r requirements.txt >nul 2>&1
) else (
    echo Installing essential packages...
    pip install streamlit pandas numpy plotly openpyxl >nul 2>&1
)

:: Restore important files
echo [8/8] Finalizing setup...
if exist "backup\.env*" (
    for %%f in (backup\.env*) do (
        copy "%%f" ".env" >nul 2>&1
        break
    )
)

if exist "backup\pms_client_data.db*" (
    for %%f in (backup\pms_client_data.db*) do (
        copy "%%f" "pms_client_data.db" >nul 2>&1
        copy "%%f" "src\dashboard\pms_client_data.db" >nul 2>&1
        break
    )
)

echo.
echo ========================================
echo ✅ UPDATE COMPLETED SUCCESSFULLY!
echo ========================================
echo.
echo 🎉 Your PMS Intelligence Hub is now updated!
echo 📊 All your data has been preserved
echo 🔧 Dependencies are up to date
echo.

if not "!COMMITS_BEHIND!"=="0" (
    echo 📋 Recent changes:
    git log --oneline -3 HEAD
    echo.
)

echo 🚀 Ready to launch:
echo   • Quick Start: deployment\windows\simple_run.bat
echo   • Full Setup:  deployment\windows\ultimate_setup.bat
echo.
echo 💡 Tip: Your database and settings are automatically backed up in the 'backup' folder
echo.
pause

