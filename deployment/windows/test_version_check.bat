@echo off
REM Test script to verify Python version checking logic
REM This script tests the version checking with various Python versions

echo Testing Python version checking logic...
echo.

REM Test function for version checking
:test_version
set TEST_VERSION=%1
echo Testing version: %TEST_VERSION%

REM Extract major and minor version numbers
for /f "tokens=1,2 delims=." %%a in ("%TEST_VERSION%") do (
    set MAJOR=%%a
    set MINOR=%%b
)

REM Remove any non-numeric characters from minor version
for /f "tokens=1 delims= " %%a in ("%MINOR%") do set MINOR=%%a

REM Check if major version is 3 and minor version is 8 or higher
if "%MAJOR%"=="3" (
    if %MINOR% geq 8 (
        echo   ✓ PASS - Version %TEST_VERSION% is supported
    ) else (
        echo   ✗ FAIL - Version %TEST_VERSION% is too old (need 3.8+)
    )
) else (
    echo   ✗ FAIL - Version %TEST_VERSION% is not Python 3.x
)
echo.
goto :eof

REM Test various Python versions
echo Testing various Python versions:
echo ================================

call :test_version "3.7.9"
call :test_version "3.8.0"
call :test_version "3.8.10"
call :test_version "3.9.0"
call :test_version "3.9.18"
call :test_version "3.10.0"
call :test_version "3.10.12"
call :test_version "3.11.0"
call :test_version "3.11.7"
call :test_version "3.12.0"
call :test_version "3.12.1"
call :test_version "3.13.0"
call :test_version "3.13.1"
call :test_version "3.14.0"
call :test_version "3.15.0"
call :test_version "2.7.18"
call :test_version "4.0.0"

echo Testing completed.
echo.
echo Expected results:
echo - Python 3.7.x and below: FAIL
echo - Python 3.8.x and above: PASS
echo - Python 2.x: FAIL
echo - Python 4.x: FAIL (for now)
echo.

REM Test with actual Python installation
echo Testing with your actual Python installation:
echo ============================================
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
) else (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set ACTUAL_VERSION=%%i
    echo Your Python version: %ACTUAL_VERSION%
    call :test_version "%ACTUAL_VERSION%"
)

pause

