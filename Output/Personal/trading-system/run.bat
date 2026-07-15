@echo off
REM ── Trading Analysis System — Windows launcher ──
REM Lan dau: tu tao venv + cai dependencies. Cac lan sau: chay thang.
cd /d "%~dp0"
chcp 65001 >nul
set PYTHONIOENCODING=utf-8

if not exist ".venv\Scripts\python.exe" (
    echo [Setup] Tao virtual env va cai dependencies - chi lan dau, mat 2-3 phut...
    python -m venv .venv
    if errorlevel 1 (
        echo [LOI] Khong tim thay Python. Cai Python 3.10+ tu python.org, nho tick "Add to PATH".
        pause
        exit /b 1
    )
    ".venv\Scripts\python.exe" -m pip install --upgrade pip -q
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt
)

echo.
echo  Trading Analysis System - dang khoi dong...
echo  Mo trinh duyet: http://127.0.0.1:8899
echo  Dong cua so nay de tat server.
echo.
start "" http://127.0.0.1:8899
".venv\Scripts\python.exe" -m trading_system.server
pause
