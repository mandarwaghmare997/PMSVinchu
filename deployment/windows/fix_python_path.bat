@echo off
REM Python PATH Fix Script
REM This script helps add Python to the Windows PATH environment variable

setlocal enabledelayedexpansion

echo.
echo ==========================================
echo  Python PATH Fix Tool
echo ==========================================
echo.
echo This tool will help add Python to your PATH environment variable.
echo.

REM Check for administrator privileges
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running with administrator privileges ✓
    set IS_ADMIN=1
) else (
    echo Note: Not running as administrator
    echo Some operations may require elevated privileges
    set IS_ADMIN=0
)

echo.
echo Step 1: Searching for Python installations...
echo =============================================

set FOUND_PYTHONS=
set PYTHON_COUNT=0

REM Check common Python installation locations
echo Searching common installation directories...

REM Check Program Files
for /d %%i in ("C:\Program Files\Python*") do (
    if exist "%%i\python.exe" (
        echo   ✅ Found: %%i\python.exe
        set FOUND_PYTHONS=!FOUND_PYTHONS! "%%i"
        set /a PYTHON_COUNT+=1
    )
)

REM Check Program Files (x86)
for /d %%i in ("C:\Program Files (x86)\Python*") do (
    if exist "%%i\python.exe" (
        echo   ✅ Found: %%i\python.exe
        set FOUND_PYTHONS=!FOUND_PYTHONS! "%%i"
        set /a PYTHON_COUNT+=1
    )
)

REM Check AppData Local
for /d %%i in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
    if exist "%%i\python.exe" (
        echo   ✅ Found: %%i\python.exe
        set FOUND_PYTHONS=!FOUND_PYTHONS! "%%i"
        set /a PYTHON_COUNT+=1
    )
)

REM Check Microsoft Store Python
if exist "%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe" (
    echo   ✅ Found: %LOCALAPPDATA%\Microsoft\WindowsApps\python.exe
    echo   Note: This is Microsoft Store Python (may have limitations)
)

echo.
echo Found %PYTHON_COUNT% Python installation(s)

if %PYTHON_COUNT%==0 (
    echo.
    echo ❌ No Python installations found!
    echo.
    echo Please install Python from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo.
echo Step 2: Current PATH status...
echo ==============================

echo Checking current PATH for Python entries...
echo %PATH% | findstr /i python >nul
if errorlevel 1 (
    echo   ❌ No Python directories found in current PATH
) else (
    echo   ✅ Python directories already in PATH:
    for %%i in ("%PATH:;=" "%") do (
        echo %%i | findstr /i python >nul
        if not errorlevel 1 echo     %%~i
    )
)

echo.
echo Step 3: PATH modification options...
echo ====================================

if %PYTHON_COUNT%==1 (
    echo Only one Python installation found. Proceeding with automatic setup...
    for %%i in (%FOUND_PYTHONS%) do set SELECTED_PYTHON=%%~i
    goto :add_to_path
)

echo Multiple Python installations found. Please select one:
echo.

set COUNTER=1
for %%i in (%FOUND_PYTHONS%) do (
    echo   !COUNTER!. %%~i
    set PYTHON_!COUNTER!=%%~i
    set /a COUNTER+=1
)

echo.
set /p CHOICE="Enter your choice (1-%PYTHON_COUNT%): "

REM Validate choice
if "%CHOICE%"=="" goto :invalid_choice
if %CHOICE% lss 1 goto :invalid_choice
if %CHOICE% gtr %PYTHON_COUNT% goto :invalid_choice

REM Get selected Python
call set SELECTED_PYTHON=%%PYTHON_%CHOICE%%%
goto :add_to_path

:invalid_choice
echo Invalid choice. Please run the script again.
pause
exit /b 1

:add_to_path
echo.
echo Selected Python installation: %SELECTED_PYTHON%
echo.

REM Check if already in PATH
echo %PATH% | findstr /i "%SELECTED_PYTHON%" >nul
if not errorlevel 1 (
    echo ✅ This Python installation is already in PATH!
    echo.
    echo Testing Python access...
    "%SELECTED_PYTHON%\python.exe" --version
    if not errorlevel 1 (
        echo ✅ Python is working correctly!
    ) else (
        echo ❌ Python executable has issues
    )
    pause
    exit /b 0
)

echo Adding Python to PATH...
echo.
echo This will add the following directories to your PATH:
echo   1. %SELECTED_PYTHON%
echo   2. %SELECTED_PYTHON%\Scripts
echo.

set /p CONFIRM="Do you want to proceed? (y/n): "
if /i not "%CONFIRM%"=="y" (
    echo Operation cancelled.
    pause
    exit /b 0
)

REM Add to PATH
echo.
echo Adding to PATH...

REM Method 1: Try using setx (user PATH)
echo Attempting to add to user PATH...
setx PATH "%PATH%;%SELECTED_PYTHON%;%SELECTED_PYTHON%\Scripts" >nul 2>&1
if not errorlevel 1 (
    echo ✅ Successfully added to user PATH
    goto :path_added
)

REM Method 2: Registry modification (if admin)
if %IS_ADMIN%==1 (
    echo Attempting to add to system PATH...
    REM This would require more complex registry operations
    echo ⚠️  Manual PATH modification required
) else (
    echo ⚠️  Automatic PATH modification failed
)

echo.
echo Manual PATH modification instructions:
echo =====================================
echo.
echo 1. Press Win + X and select "System"
echo 2. Click "Advanced system settings"
echo 3. Click "Environment Variables"
echo 4. Under "User variables", select "Path" and click "Edit"
echo 5. Click "New" and add: %SELECTED_PYTHON%
echo 6. Click "New" and add: %SELECTED_PYTHON%\Scripts
echo 7. Click "OK" to save all changes
echo 8. Restart your command prompt
echo.

goto :end

:path_added
echo.
echo ==========================================
echo  PATH Update Complete!
echo ==========================================
echo.
echo Python has been added to your PATH.
echo.
echo IMPORTANT: You need to restart your command prompt
echo for the changes to take effect.
echo.
echo After restarting, test with:
echo   python --version
echo   pip --version
echo.

:end
echo Press any key to continue...
pause >nul

