@echo off
echo Starting PMS Intelligence Hub - Client Dashboard...
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\streamlit.exe" (
    echo Virtual environment not found. Please run ultimate_setup.bat first.
    pause
    exit /b 1
)

echo Starting dashboard at http://localhost:8501
echo Press Ctrl+C to stop the dashboard
echo.

venv\Scripts\streamlit.exe run src\dashboard\main_dashboard.py --server.port 8501

pause

