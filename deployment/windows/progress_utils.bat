@echo off
REM Progress Bar and Loader Utilities for Windows Batch Scripts
REM Functions to create visual progress indicators

REM ==========================================
REM Progress Bar Function
REM Usage: call :progress_bar <current> <total> <description>
REM ==========================================
:progress_bar
setlocal enabledelayedexpansion
set /a current=%1
set /a total=%2
set description=%3

REM Calculate percentage
set /a percent=(%current% * 100) / %total%
set /a filled=(%current% * 50) / %total%
set /a empty=50 - %filled%

REM Build progress bar
set bar=
for /l %%i in (1,1,%filled%) do set bar=!bar!█
for /l %%i in (1,1,%empty%) do set bar=!bar!░

REM Display progress bar
echo [!bar!] %percent%%% - %description%
endlocal
goto :eof

REM ==========================================
REM Spinner Animation Function
REM Usage: call :spinner <message> <duration_seconds>
REM ==========================================
:spinner
setlocal enabledelayedexpansion
set message=%1
set /a duration=%2
set /a iterations=%duration% * 4

set chars=^|/-\
for /l %%i in (1,1,%iterations%) do (
    set /a index=%%i %% 4
    for %%j in (!index!) do (
        set char=!chars:~%%j,1!
        <nul set /p "=!char! %message%"
        timeout /t 1 /nobreak >nul 2>&1
        for /l %%k in (1,1,50) do <nul set /p "= "
        <nul set /p "="
    )
)
echo.
endlocal
goto :eof

REM ==========================================
REM Animated Dots Function
REM Usage: call :animated_dots <message> <duration_seconds>
REM ==========================================
:animated_dots
setlocal enabledelayedexpansion
set message=%1
set /a duration=%2
set /a iterations=%duration% * 2

for /l %%i in (1,1,%iterations%) do (
    set /a dots=%%i %% 4
    set dotstr=
    for /l %%j in (1,1,!dots!) do set dotstr=!dotstr!.
    
    <nul set /p "=%message%!dotstr!   "
    timeout /t 1 /nobreak >nul 2>&1
    for /l %%k in (1,1,50) do <nul set /p "= "
    <nul set /p "="
)
echo.
endlocal
goto :eof

REM ==========================================
REM Download Progress Function
REM Usage: call :download_progress <filename> <url>
REM ==========================================
:download_progress
setlocal enabledelayedexpansion
set filename=%1
set url=%2

echo.
echo ┌─────────────────────────────────────────────────────┐
echo │                 Downloading %filename%                 │
echo └─────────────────────────────────────────────────────┘
echo.

REM Simulate download progress (since we can't get real progress from PowerShell easily)
for /l %%i in (0,5,100) do (
    call :progress_bar %%i 100 "Downloading %filename%"
    timeout /t 1 /nobreak >nul 2>&1
)

echo ✓ Download completed!
echo.
endlocal
goto :eof

REM ==========================================
REM Installation Progress Function
REM Usage: call :install_progress <software_name>
REM ==========================================
:install_progress
setlocal enabledelayedexpansion
set software=%1

echo.
echo ┌─────────────────────────────────────────────────────┐
echo │              Installing %software%                     │
echo └─────────────────────────────────────────────────────┘
echo.

REM Installation phases
call :progress_bar 10 100 "Preparing installation"
timeout /t 2 /nobreak >nul 2>&1

call :progress_bar 25 100 "Extracting files"
timeout /t 3 /nobreak >nul 2>&1

call :progress_bar 50 100 "Installing components"
timeout /t 5 /nobreak >nul 2>&1

call :progress_bar 75 100 "Configuring settings"
timeout /t 2 /nobreak >nul 2>&1

call :progress_bar 90 100 "Updating PATH"
timeout /t 2 /nobreak >nul 2>&1

call :progress_bar 100 100 "Installation complete"
echo.
echo ✓ %software% installed successfully!
echo.
endlocal
goto :eof

REM ==========================================
REM Package Installation Progress
REM Usage: call :package_progress <package_name>
REM ==========================================
:package_progress
setlocal enabledelayedexpansion
set package=%1

echo Installing %package%...
for /l %%i in (0,10,100) do (
    set /a filled=%%i / 2
    set /a empty=50 - !filled!
    
    set bar=
    for /l %%j in (1,1,!filled!) do set bar=!bar!▓
    for /l %%j in (1,1,!empty!) do set bar=!bar!░
    
    <nul set /p "=  [!bar!] %%i%% %package%"
    timeout /t 1 /nobreak >nul 2>&1
    echo.
)
echo ✓ %package% installed
echo.
endlocal
goto :eof

REM ==========================================
REM Colorful Header Function
REM Usage: call :header <title>
REM ==========================================
:header
setlocal
set title=%1

echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║                                                      ║
echo ║                    %title%                    ║
echo ║                                                      ║
echo ╚══════════════════════════════════════════════════════╝
echo.
endlocal
goto :eof

REM ==========================================
REM Success Message Function
REM Usage: call :success <message>
REM ==========================================
:success
setlocal
set message=%1

echo.
echo ┌─────────────────────────────────────────────────────┐
echo │  ✅ SUCCESS: %message%                              │
echo └─────────────────────────────────────────────────────┘
echo.
endlocal
goto :eof

REM ==========================================
REM Error Message Function
REM Usage: call :error <message>
REM ==========================================
:error
setlocal
set message=%1

echo.
echo ┌─────────────────────────────────────────────────────┐
echo │  ❌ ERROR: %message%                                │
echo └─────────────────────────────────────────────────────┘
echo.
endlocal
goto :eof

REM ==========================================
REM Step Counter Function
REM Usage: call :step <current> <total> <description>
REM ==========================================
:step
setlocal
set /a current=%1
set /a total=%2
set description=%3

echo.
echo ┌─ Step %current%/%total% ─────────────────────────────────────────┐
echo │  %description%
echo └──────────────────────────────────────────────────────┘
echo.
endlocal
goto :eof

