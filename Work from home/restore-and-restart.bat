@echo off
title Restore DB + Restart 9Router
cd /d "%~dp0"

echo [1/3] Dang tat 9router...
for /f "tokens=1" %%i in ('wmic process where "CommandLine like '%%server.js%%' and name='node.exe'" get ProcessId ^| findstr /r "[0-9]"') do (
    taskkill /PID %%i /F >nul 2>&1
)
for /f "tokens=1" %%i in ('wmic process where "CommandLine like '%%9router%%cli.js%%'" get ProcessId ^| findstr /r "[0-9]"') do (
    taskkill /PID %%i /F >nul 2>&1
)
timeout /t 2 /nobreak >nul
echo [OK] Da tat 9router

echo [2/3] Dang giai ma database...
node 9router-backup\decrypt.js "%APPDATA%\9router"
if errorlevel 1 (
    echo [ERROR] Giai ma that bai!
    pause
    exit /b 1
)
echo [OK] Giai ma database thanh cong

echo [3/3] Dang khoi dong lai 9router...
start "" "9router\start-9router.bat"
echo [OK] 9router dang khoi dong tai http://localhost:20128

timeout /t 3 /nobreak >nul
