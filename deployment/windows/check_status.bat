@echo off
echo ========================================
echo PMS Intelligence Hub - Status Check
echo ========================================
echo.

:: Check Git status
echo 📋 Repository Status:
echo -------------------
if exist ".git" (
    git status --short
    echo.
    echo Current branch: 
    git branch --show-current
    echo.
    echo Commits behind origin:
    for /f %%i in ('git rev-list HEAD...origin/master --count 2^>nul') do echo %%i commits
) else (
    echo ❌ Not a Git repository
)

echo.
echo 🐍 Python Environment:
echo --------------------
if exist "venv" (
    echo ✅ Virtual environment exists
    call venv\Scripts\activate.bat
    python --version
    echo.
    echo Installed packages:
    pip list --format=columns | findstr /i "streamlit pandas numpy plotly"
) else (
    echo ❌ Virtual environment not found
)

echo.
echo 📊 Database Status:
echo ----------------
if exist "pms_client_data.db" (
    echo ✅ Main database found
) else (
    echo ❌ Main database missing
)

if exist "src\dashboard\pms_client_data.db" (
    echo ✅ Dashboard database found
) else (
    echo ❌ Dashboard database missing
)

echo.
echo 🔧 Configuration:
echo ---------------
if exist ".env" (
    echo ✅ Environment file exists
) else (
    echo ⚠️  Environment file missing (optional)
)

echo.
echo 🚀 Quick Actions:
echo ---------------
echo 1. Update:           smart_update.bat
echo 2. Quick Update:     quick_update.bat  
echo 3. Reset Everything: reset_and_update.bat
echo 4. Start Dashboard:  simple_run.bat
echo.
pause

