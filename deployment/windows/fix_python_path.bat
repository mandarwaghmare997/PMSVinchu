@echo off
REM Fix Python PATH issues on Windows with Visual Progress
REM This script helps resolve common Python installation and PATH problems

title Fix Python PATH Issues
color 0E

REM Load progress utilities
call "%~dp0progress_utils.bat" 2>nul || (
    echo Progress utilities not found, continuing without visual indicators...
)

cls
call :header "Python PATH Fix Utility"
echo  Diagnosing and fixing Python installation issues
echo.

call :step 1 4 "System Diagnosis"

call :animated_dots "Analyzing current PATH configuration" 2
echo Current PATH contains:
echo %PATH% | findstr /i python >nul && echo ✓ Python paths found in PATH || echo ❌ No Python paths in PATH
echo.

call :step 2 4 "Python Installation Search"

call :animated_dots "Searching for Python installations" 3
set FOUND_PYTHON=0

echo Checking common installation locations...
if exist "C:\Python311\python.exe" (
    echo ✓ Found Python at C:\Python311\python.exe
    set FOUND_PYTHON=1
    set PYTHON_PATH=C:\Python311
)

if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    echo ✓ Found Python at %LOCALAPPDATA%\Programs\Python\Python311\python.exe
    set FOUND_PYTHON=1
    set PYTHON_PATH=%LOCALAPPDATA%\Programs\Python\Python311
)

if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe" (
    echo ✓ Found Python at C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe
    set FOUND_PYTHON=1
    set PYTHON_PATH=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311
)

if %FOUND_PYTHON%==0 (
    call :error "No Python installation found in common locations"
    echo.
    echo Please install Python from https://python.org with these options:
    echo - Check "Add Python to PATH"
    echo - Install for all users
    echo.
    pause
    exit /b 1
)

call :success "Found Python installation at: %PYTHON_PATH%"

call :step 3 4 "Python Command Testing"

call :animated_dots "Testing Python commands" 2

"%PYTHON_PATH%\python.exe" --version >nul 2>&1
if not errorlevel 1 (
    echo ✓ python.exe works
    set WORKING_PYTHON="%PYTHON_PATH%\python.exe"
) else (
    echo ❌ python.exe not working
)

py --version >nul 2>&1
if not errorlevel 1 (
    echo ✓ py launcher works
    set WORKING_PYTHON=py
) else (
    echo ❌ py launcher not working
)

call :step 4 4 "System Configuration Fix"

call :animated_dots "Disabling Microsoft Store Python redirect" 2
reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\App Paths\python.exe" /ve /d "%PYTHON_PATH%\python.exe" /f >nul 2>&1
reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\App Paths\python3.exe" /ve /d "%PYTHON_PATH%\python.exe" /f >nul 2>&1

call :success "Microsoft Store redirect disabled"

call :animated_dots "Checking PATH configuration" 2
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not in PATH. Adding to user PATH...
    
    call :progress_bar 25 100 "Reading current PATH"
    for /f "tokens=2*" %%a in ('reg query "HKEY_CURRENT_USER\Environment" /v PATH 2^>nul') do set "CurrentPath=%%b"
    
    call :progress_bar 50 100 "Preparing new PATH"
    set "NewPath=%CurrentPath%;%PYTHON_PATH%;%PYTHON_PATH%\Scripts"
    
    call :progress_bar 75 100 "Updating registry"
    reg add "HKEY_CURRENT_USER\Environment" /v PATH /d "%NewPath%" /f >nul
    
    call :progress_bar 100 100 "PATH update complete"
    call :success "Added Python to user PATH"
    echo.
    echo ⚠️  IMPORTANT: You need to restart Command Prompt for PATH changes to take effect
) else (
    call :success "Python is already in PATH"
)

echo.
call :header "🎉 Fix Summary"

if defined WORKING_PYTHON (
    call :success "Python is working correctly!"
    echo.
    echo ┌─────────────────────────────────────────────────────┐
    echo │                                                     │
    echo │  ✅ Working Python command: %WORKING_PYTHON%        │
    echo │  📁 Installation path: %PYTHON_PATH%               │
    echo │                                                     │
    echo │  You can now run:                                  │
    echo │    deployment\windows\quick_start.bat              │
    echo │                                                     │
    echo └─────────────────────────────────────────────────────┘
    echo.
) else (
    call :error "Python still not working properly"
    echo.
    echo Troubleshooting steps:
    echo 1. Restart Command Prompt
    echo 2. Try running: py --version
    echo 3. Reinstall Python from https://python.org
    echo 4. Make sure to check "Add Python to PATH" during installation
    echo.
)

echo Press any key to continue...
pause >nul

