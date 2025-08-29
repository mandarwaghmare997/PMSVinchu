@echo off
echo ========================================
echo PMS Intelligence Hub - Advanced Analytics
echo Windows Deployment Script
echo ========================================

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
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

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Install/upgrade requirements
echo Installing requirements...
pip install --upgrade pip
pip install streamlit pandas numpy plotly sqlite3 datetime

:: Check if database exists, if not create sample data
if not exist "src\dashboard\pms_client_data.db" (
    echo Creating sample database...
    cd src\dashboard
    python -c "from advanced_analytics_dashboard import AdvancedAnalyticsDashboard; dashboard = AdvancedAnalyticsDashboard(); data = dashboard.load_data(); print(f'Sample data created: {len(data)} records')"
    cd ..\..
)

:: Start the advanced analytics dashboard
echo ========================================
echo Starting PMS Intelligence Hub - Advanced Analytics
echo ========================================
echo.
echo Dashboard will be available at:
echo http://localhost:8504
echo.
echo Press Ctrl+C to stop the dashboard
echo ========================================

cd src\dashboard
streamlit run advanced_analytics_dashboard.py --server.port 8504

pause

