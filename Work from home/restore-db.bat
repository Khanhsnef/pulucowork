@echo off
title Restore 9Router Database
echo =============================================
echo  RESTORE DATABASE - Tat 9router truoc khi chay
echo =============================================
echo.
echo [!] Dam bao da TAT 9router (dong tray icon) truoc khi tiep tuc.
pause

cd /d "%~dp0"
node 9router-backup\decrypt.js "%APPDATA%\9router"
echo.
echo [OK] Khoi phuc database hoan tat!
echo Bay gio ban co the chay start-9router.bat
pause
