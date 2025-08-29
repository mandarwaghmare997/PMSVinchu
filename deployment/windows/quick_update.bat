@echo off
echo ========================================
echo PMS Intelligence Hub - Quick Update
echo ========================================
echo.

:: Quick git pull without full dependency check
echo [1/3] Fetching latest changes...
git fetch origin master

echo [2/3] Updating code...
git pull origin master

if errorlevel 1 (
    echo ERROR: Update failed
    echo Try running smart_update.bat for a full update
    pause
    exit /b 1
)

echo [3/3] Quick dependency check...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    pip install --upgrade --quiet streamlit pandas numpy plotly openpyxl
)

echo.
echo ✅ Quick update completed!
echo.
echo To start dashboard: deployment\windows\simple_run.bat
echo.
pause

