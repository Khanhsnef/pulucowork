@echo off
title 9Router Setup
cd /d "%~dp0"
echo Dang khoi chay setup 9router bang Quyen powershell bypass...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup-9router.ps1"
pause
