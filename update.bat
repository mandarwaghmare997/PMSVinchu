@echo off
echo ========================================
echo PMS Intelligence Hub - Smart Update
echo ========================================
echo.

:: Check if git is available
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed or not in PATH
    echo Please install Git first: https://git-scm.com/download/win
    pause
    exit /b 1
)

:: Check if we're in a git repository
if not exist ".git" (
    echo ERROR: Not in a Git repository
    echo Please run this script from the PMSVinchu directory
    pause
    exit /b 1
)

echo [1/6] Backing up current configuration...
if exist ".env" copy ".env" ".env.backup" >nul 2>&1
if exist "pms_client_data.db" copy "pms_client_data.db" "pms_client_data.db.backup" >nul 2>&1

echo [2/6] Fetching latest changes from GitHub...
git fetch origin

echo [3/6] Checking for updates...
for /f %%i in ('git rev-list HEAD...origin/master --count') do set COMMITS_BEHIND=%%i

if "%COMMITS_BEHIND%"=="0" (
    echo ✅ Already up to date! No changes to pull.
    echo.
    goto :check_dependencies
)

echo Found %COMMITS_BEHIND% new commits. Updating...

echo [4/6] Stashing local changes (if any)...
git stash push -m "Auto-stash before update %date% %time%"

echo [5/6] Pulling latest changes...
git pull origin master

if errorlevel 1 (
    echo ERROR: Failed to pull changes
    echo Restoring stashed changes...
    git stash pop
    pause
    exit /b 1
)

echo [6/6] Restoring stashed changes...
git stash pop >nul 2>&1

:check_dependencies
echo.
echo ========================================
echo Checking Dependencies...
echo ========================================

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: Python not found. Please install Python 3.11+
) else (
    echo ✅ Python found
)

:: Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

:: Activate virtual environment and install/update dependencies
echo Updating Python dependencies...
call venv\Scripts\activate.bat
pip install --upgrade pip >nul 2>&1
pip install -r requirements-core.txt >nul 2>&1

echo.
echo ========================================
echo Restoring Data...
echo ========================================

:: Restore backed up files
if exist ".env.backup" (
    echo Restoring environment configuration...
    copy ".env.backup" ".env" >nul 2>&1
    del ".env.backup" >nul 2>&1
)

if exist "pms_client_data.db.backup" (
    echo Restoring database...
    copy "pms_client_data.db.backup" "pms_client_data.db" >nul 2>&1
    del "pms_client_data.db.backup" >nul 2>&1
)

echo.
echo ========================================
echo ✅ UPDATE COMPLETED SUCCESSFULLY!
echo ========================================
echo.
echo Your PMS Intelligence Hub has been updated with the latest features.
echo Your data and configuration have been preserved.
echo.
echo To start the dashboard:
echo   1. Run: deployment\windows\ultimate_setup.bat
echo   2. Or use: deployment\windows\simple_run.bat
echo.
echo Changes in this update:
git log --oneline -5 HEAD
echo.
pause

