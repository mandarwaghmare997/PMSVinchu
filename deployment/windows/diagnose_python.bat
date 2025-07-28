@echo off
REM Python Installation Diagnostic Script
REM This script helps identify Python installation issues on Windows

setlocal enabledelayedexpansion

echo.
echo ==========================================
echo  Python Installation Diagnostic Tool
echo ==========================================
echo.
echo This tool will help identify why Python is not being detected.
echo.

echo Step 1: Testing different Python commands...
echo ============================================

REM Test python command
echo Testing 'python' command:
python --version >nul 2>&1
if errorlevel 1 (
    echo   ❌ 'python' command not found
    set PYTHON_CMD=
) else (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo   ✅ 'python' found: Python !PYTHON_VERSION!
    set PYTHON_CMD=python
)

REM Test py command
echo Testing 'py' command:
py --version >nul 2>&1
if errorlevel 1 (
    echo   ❌ 'py' command not found
) else (
    for /f "tokens=2" %%i in ('py --version 2^>^&1') do set PY_VERSION=%%i
    echo   ✅ 'py' found: Python !PY_VERSION!
    if "!PYTHON_CMD!"=="" set PYTHON_CMD=py
)

REM Test py -3 command
echo Testing 'py -3' command:
py -3 --version >nul 2>&1
if errorlevel 1 (
    echo   ❌ 'py -3' command not found
) else (
    for /f "tokens=2" %%i in ('py -3 --version 2^>^&1') do set PY3_VERSION=%%i
    echo   ✅ 'py -3' found: Python !PY3_VERSION!
    if "!PYTHON_CMD!"=="" set PYTHON_CMD=py -3
)

REM Test python3 command
echo Testing 'python3' command:
python3 --version >nul 2>&1
if errorlevel 1 (
    echo   ❌ 'python3' command not found
) else (
    for /f "tokens=2" %%i in ('python3 --version 2^>^&1') do set PYTHON3_VERSION=%%i
    echo   ✅ 'python3' found: Python !PYTHON3_VERSION!
    if "!PYTHON_CMD!"=="" set PYTHON_CMD=python3
)

echo.
echo Step 2: Checking PATH environment variable...
echo =============================================
echo Current PATH contains:
echo %PATH% | findstr /i python >nul
if errorlevel 1 (
    echo   ❌ No Python directories found in PATH
) else (
    echo   ✅ Python directories found in PATH:
    for %%i in ("%PATH:;=" "%") do (
        echo %%i | findstr /i python >nul
        if not errorlevel 1 echo     %%~i
    )
)

echo.
echo Step 3: Searching for Python installations...
echo =============================================

REM Check common Python installation locations
set FOUND_INSTALLATIONS=0

REM Check Program Files
if exist "C:\Program Files\Python*" (
    echo   ✅ Found Python in Program Files:
    for /d %%i in ("C:\Program Files\Python*") do (
        echo     %%i
        set /a FOUND_INSTALLATIONS+=1
    )
)

REM Check Program Files (x86)
if exist "C:\Program Files (x86)\Python*" (
    echo   ✅ Found Python in Program Files (x86):
    for /d %%i in ("C:\Program Files (x86)\Python*") do (
        echo     %%i
        set /a FOUND_INSTALLATIONS+=1
    )
)

REM Check AppData Local
if exist "%LOCALAPPDATA%\Programs\Python\Python*" (
    echo   ✅ Found Python in AppData Local:
    for /d %%i in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
        echo     %%i
        set /a FOUND_INSTALLATIONS+=1
    )
)

REM Check Microsoft Store Python
if exist "%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe" (
    echo   ✅ Found Microsoft Store Python:
    echo     %LOCALAPPDATA%\Microsoft\WindowsApps\python.exe
    set /a FOUND_INSTALLATIONS+=1
)

if %FOUND_INSTALLATIONS%==0 (
    echo   ❌ No Python installations found in common locations
)

echo.
echo Step 4: Testing pip availability...
echo ===================================

if not "!PYTHON_CMD!"=="" (
    echo Testing pip with !PYTHON_CMD!:
    !PYTHON_CMD! -m pip --version >nul 2>&1
    if errorlevel 1 (
        echo   ❌ pip not available with !PYTHON_CMD!
    ) else (
        for /f "tokens=*" %%i in ('!PYTHON_CMD! -m pip --version 2^>^&1') do echo   ✅ %%i
    )
) else (
    echo   ❌ No working Python command found to test pip
)

echo.
echo Step 5: Registry check for Python installations...
echo =================================================

REM Check registry for Python installations
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Python" >nul 2>&1
if errorlevel 1 (
    echo   ❌ No Python found in HKEY_LOCAL_MACHINE\SOFTWARE\Python
) else (
    echo   ✅ Python entries found in registry:
    for /f "tokens=*" %%i in ('reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Python" 2^>nul') do (
        echo %%i | findstr "Python" >nul
        if not errorlevel 1 echo     %%i
    )
)

echo.
echo ==========================================
echo  Diagnostic Summary
echo ==========================================

if not "!PYTHON_CMD!"=="" (
    echo ✅ SOLUTION FOUND: Use '!PYTHON_CMD!' instead of 'python'
    echo.
    echo Recommended fix:
    echo 1. The deployment scripts should be updated to try multiple Python commands
    echo 2. Or add Python to your PATH environment variable
    echo.
    echo Quick test with your working Python command:
    echo   !PYTHON_CMD! --version
    echo   !PYTHON_CMD! -m pip --version
) else (
    echo ❌ PROBLEM: No working Python command found
    echo.
    echo Possible solutions:
    echo 1. Reinstall Python from https://python.org
    echo    - Make sure to check "Add Python to PATH" during installation
    echo 2. Add existing Python installation to PATH manually
    echo 3. Use the Python Launcher (py command) if available
)

echo.
echo Additional Information:
echo - Total Python installations found: %FOUND_INSTALLATIONS%
echo - Working Python command: !PYTHON_CMD!
echo.

if not "!PYTHON_CMD!"=="" (
    echo Creating temporary fix script...
    echo @echo off > temp_python_fix.bat
    echo REM Temporary fix - use this Python command >> temp_python_fix.bat
    echo set PYTHON_CMD=!PYTHON_CMD! >> temp_python_fix.bat
    echo echo Using Python command: !PYTHON_CMD! >> temp_python_fix.bat
    echo !PYTHON_CMD! %%* >> temp_python_fix.bat
    echo.
    echo ✅ Created temp_python_fix.bat - you can use this as a workaround
)

echo.
echo Press any key to continue...
pause >nul

