@echo off
echo ========================================
echo PMS Intelligence Hub - Reset & Update
echo ========================================
echo.
echo ⚠️  WARNING: This will reset your installation
echo     Your data will be backed up but settings may be lost
echo.
set /p CONFIRM="Type 'RESET' to continue: "
if not "%CONFIRM%"=="RESET" (
    echo Cancelled.
    pause
    exit /b 0
)

echo.
echo [1/6] Backing up your data...
if not exist "backup" mkdir backup
if exist "pms_client_data.db" copy "pms_client_data.db" "backup\pms_client_data.db_reset_%date:~-4,4%%date:~-10,2%%date:~-7,2%" >nul 2>&1
if exist "src\dashboard\pms_client_data.db" copy "src\dashboard\pms_client_data.db" "backup\dashboard_db_reset_%date:~-4,4%%date:~-10,2%%date:~-7,2%" >nul 2>&1
if exist ".env" copy ".env" "backup\.env_reset_%date:~-4,4%%date:~-10,2%%date:~-7,2%" >nul 2>&1

echo [2/6] Stopping all processes...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im streamlit.exe >nul 2>&1

echo [3/6] Cleaning up old installation...
if exist "venv" rmdir /s /q "venv"
if exist "__pycache__" rmdir /s /q "__pycache__"
if exist "src\dashboard\__pycache__" rmdir /s /q "src\dashboard\__pycache__"

echo [4/6] Resetting to latest version...
git reset --hard origin/master
git clean -fd

echo [5/6] Setting up fresh environment...
python -m venv venv
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
if exist "requirements-core.txt" (
    pip install -r requirements-core.txt
) else (
    pip install streamlit pandas numpy plotly openpyxl
)

echo [6/6] Restoring your data...
if exist "backup\pms_client_data.db_reset*" (
    for %%f in (backup\pms_client_data.db_reset*) do (
        copy "%%f" "pms_client_data.db" >nul 2>&1
        copy "%%f" "src\dashboard\pms_client_data.db" >nul 2>&1
        break
    )
)

echo.
echo ========================================
echo ✅ RESET COMPLETED SUCCESSFULLY!
echo ========================================
echo.
echo 🔄 Fresh installation ready
echo 📊 Your data has been restored
echo 🚀 Ready to launch: deployment\windows\simple_run.bat
echo.
pause

