@echo off
REM PMS Intelligence Hub - Windows Deployment Script
REM Supports local development and Docker deployment on Windows

setlocal enabledelayedexpansion

echo.
echo ========================================
echo  PMS Intelligence Hub - Windows Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

REM Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found Python %PYTHON_VERSION%

REM Check Python version (check for 3.8+)
REM Extract major and minor version numbers
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set MAJOR=%%a
    set MINOR=%%b
)

REM Remove any non-numeric characters from minor version
for /f "tokens=1 delims= " %%a in ("%MINOR%") do set MINOR=%%a

REM Check if major version is 3 and minor version is 8 or higher
if "%MAJOR%"=="3" (
    if %MINOR% geq 8 (
        echo ✓ Python version check passed
    ) else (
        echo ERROR: Python 3.8+ is required. Found: %PYTHON_VERSION%
        echo Please install Python 3.8 or higher from https://python.org
        pause
        exit /b 1
    )
) else (
    echo ERROR: Python 3.8+ is required. Found: %PYTHON_VERSION%
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

REM Parse command line arguments
set ENVIRONMENT=%1
if "%ENVIRONMENT%"=="" set ENVIRONMENT=local

echo Deployment environment: %ENVIRONMENT%
echo.

REM Validate environment
if "%ENVIRONMENT%"=="local" goto :deploy_local
if "%ENVIRONMENT%"=="docker" goto :deploy_docker
if "%ENVIRONMENT%"=="help" goto :show_help

echo ERROR: Invalid environment '%ENVIRONMENT%'
echo Valid options: local, docker, help
pause
exit /b 1

:show_help
echo Usage: deploy.bat [environment]
echo.
echo Environments:
echo   local   - Local development setup (default)
echo   docker  - Docker containerized deployment
echo   help    - Show this help message
echo.
echo Examples:
echo   deploy.bat local
echo   deploy.bat docker
echo.
pause
exit /b 0

:deploy_local
echo ========================================
echo  Local Development Deployment
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env file with your configuration
    echo Press any key to open .env file in notepad...
    pause >nul
    notepad .env
)

REM Create necessary directories
echo Creating application directories...
if not exist "cache" mkdir cache
if not exist "logs" mkdir logs
if not exist "exports" mkdir exports
if not exist "uploads" mkdir uploads

REM Start the application
echo.
echo ========================================
echo  Starting PMS Intelligence Hub
echo ========================================
echo.
echo Dashboard will be available at: http://localhost:8501
echo Press Ctrl+C to stop the application
echo.

REM Start Streamlit dashboard
streamlit run src\dashboard\main_dashboard.py --server.port 8501 --server.address 0.0.0.0
goto :end

:deploy_docker
echo ========================================
echo  Docker Deployment
echo ========================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed or not running
    echo Please install Docker Desktop from https://docker.com
    pause
    exit /b 1
)

REM Check if Docker Compose is available
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker Compose is not available
    echo Please ensure Docker Desktop is properly installed
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env file with your configuration
    echo Press any key to open .env file in notepad...
    pause >nul
    notepad .env
)

REM Stop any existing containers
echo Stopping existing containers...
docker-compose down

REM Build and start containers
echo Building and starting Docker containers...
docker-compose up --build -d
if errorlevel 1 (
    echo ERROR: Failed to start Docker containers
    echo Check Docker Desktop is running and try again
    pause
    exit /b 1
)

REM Wait for services to start
echo Waiting for services to start...
timeout /t 10 /nobreak >nul

REM Check container status
echo.
echo Container Status:
docker-compose ps

echo.
echo ========================================
echo  Docker Deployment Complete!
echo ========================================
echo.
echo Services are now available at:
echo   Dashboard:  http://localhost:8501
echo   API:        http://localhost:8000
echo   API Docs:   http://localhost:8000/docs
echo   Grafana:    http://localhost:3000 (admin/admin123)
echo.
echo To view logs: docker-compose logs -f
echo To stop:      docker-compose down
echo.
goto :end

:end
echo.
echo Deployment script completed.
pause

