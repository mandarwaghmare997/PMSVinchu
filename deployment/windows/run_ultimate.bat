@echo off
REM PMS Intelligence Hub - Ultimate Dashboard Launcher
REM Run the ultimate dashboard with all advanced features

title PMS Hub Ultimate Dashboard

echo.
echo ================================================
echo  PMS Intelligence Hub - Ultimate Dashboard
echo  Loading all advanced features...
echo ================================================
echo.

REM Check if virtual environment exists
if exist venv\Scripts\streamlit.exe (
    echo Starting ultimate dashboard...
    echo.
    echo Ultimate Features Available:
    echo ✅ Advanced Financial Metrics (Alpha, Beta, Sharpe, VaR)
    echo ✅ Professional UI/UX with Animations
    echo ✅ Data Upload with Intelligent Merging
    echo ✅ 150+ Sample Records with Realistic Data
    echo ✅ SQLite Data Persistence
    echo ✅ Advanced Charts and Visualizations
    echo ✅ Risk-Return Analysis
    echo ✅ Performance Attribution
    echo ✅ Export Capabilities (CSV, Excel, JSON)
    echo ✅ Real-time Filtering and Analytics
    echo.
    echo Dashboard URL: http://localhost:8501
    echo Press Ctrl+C to stop
    echo.
    
    venv\Scripts\streamlit.exe run src\dashboard\ultimate_dashboard.py --server.port 8501 --server.address 0.0.0.0
) else (
    echo Virtual environment not found. Please run setup first:
    echo deployment\windows\ultimate_setup.bat
    pause
)

pause

