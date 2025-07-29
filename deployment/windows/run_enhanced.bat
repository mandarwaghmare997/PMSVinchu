@echo off
REM PMS Intelligence Hub - Enhanced Dashboard Launcher
REM Run the enhanced dashboard with all new features

title PMS Hub Enhanced Dashboard

echo.
echo ================================================
echo  PMS Intelligence Hub - Enhanced Dashboard
echo  Loading advanced features...
echo ================================================
echo.

REM Check if virtual environment exists
if exist venv\Scripts\streamlit.exe (
    echo Starting enhanced dashboard...
    echo.
    echo Dashboard Features:
    echo ✅ Data Upload (Excel/CSV)
    echo ✅ 100+ Sample Records
    echo ✅ Advanced Financial Metrics
    echo ✅ Professional UI/UX
    echo ✅ SQLite Data Persistence
    echo ✅ Export Capabilities
    echo.
    echo Dashboard URL: http://localhost:8501
    echo Press Ctrl+C to stop
    echo.
    
    venv\Scripts\streamlit.exe run src\dashboard\enhanced_dashboard.py --server.port 8501 --server.address 0.0.0.0
) else (
    echo Virtual environment not found. Please run setup first:
    echo deployment\windows\ultimate_setup.bat
    pause
)

pause

