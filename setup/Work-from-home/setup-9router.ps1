# setup-9router.ps1
# Script tu dong cau hinh va cai dat 9router tren Windows

$ErrorActionPreference = "Continue"

Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "   9ROUTER & AGENT MEMORY SETUP FOR WINDOWS   " -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan

$WorkspaceDir = $PSScriptRoot
if (-not $WorkspaceDir) { $WorkspaceDir = Get-Location }

$BackupDataDir = Join-Path $WorkspaceDir "9router-backup\data"
$BackupPatchDir = Join-Path $WorkspaceDir "9router-backup\patch"
$TargetDataDir = Join-Path $env:APPDATA "9router"
$RepoDir = Join-Path $WorkspaceDir "9router"

# 1. Kiem tra Node.js va Git
Write-Host "[*] Dang kiem tra moi truong..." -ForegroundColor Yellow
try {
    $nodeVersion = node -v
    Write-Host "[OK] Node.js da duoc cai dat: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Node.js chua duoc cai dat tren may Windows cua ban." -ForegroundColor Red
    Write-Host "Vui long cai dat Node.js LTS tai: https://nodejs.org/" -ForegroundColor Yellow
    Exit
}

try {
    $gitVersion = git --version
    Write-Host "[OK] Git da duoc cai dat: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Git chua duoc cai dat tren may Windows." -ForegroundColor Red
    Write-Host "Vui long cai dat Git tai: https://git-scm.com/" -ForegroundColor Yellow
    Exit
}

# 2. Khoi tao thu muc du lieu va giai ma cau hinh
Write-Host "`n[*] Dang giai ma va cau hinh thu muc du lieu tai AppData..." -ForegroundColor Yellow
if (-not (Test-Path $TargetDataDir)) {
    New-Item -ItemType Directory -Path $TargetDataDir -Force | Out-Null
    Write-Host "[OK] Da tao thu muc du lieu AppData: $TargetDataDir" -ForegroundColor Green
}

$DecryptScript = Join-Path $WorkspaceDir "9router-backup\decrypt.js"
if (Test-Path $DecryptScript) {
    node $DecryptScript $TargetDataDir
    Write-Host "[OK] Khoi phuc du lieu cau hinh thanh cong!" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Khong tim thay tep tin giai ma: $DecryptScript" -ForegroundColor Red
    Exit
}

# 3. Clone repository 9router
Write-Host "`n[*] Dang kiem tra ma nguon 9router..." -ForegroundColor Yellow
if (-not (Test-Path $RepoDir)) {
    Write-Host "[*] Dang clone ma nguon 9router tu GitHub..." -ForegroundColor Yellow
    git clone https://github.com/decolua/9router.git $RepoDir
    if (-not (Test-Path $RepoDir)) {
        Write-Host "[ERROR] Khong the clone repository 9router." -ForegroundColor Red
        Exit
    }
    Write-Host "[OK] Da clone thanh cong 9router ve: $RepoDir" -ForegroundColor Green
} else {
    Write-Host "[OK] Ma nguon 9router da ton tai tai: $RepoDir" -ForegroundColor Green
}

# 4. Ghi de cac file tuy chinh (Patches)
if (Test-Path $BackupPatchDir) {
    Write-Host "`n[*] Dang ap dung cac file tuy chinh (Model registry, esbuild patches)..." -ForegroundColor Yellow
    Copy-Item -Path "$BackupPatchDir\*" -Destination $RepoDir -Recurse -Force
    Write-Host "[OK] Da ap dung toan bo cac ban va thanh cong." -ForegroundColor Green
}

# 5. Khoi tao file cau hinh moi truong .env.local
Write-Host "`n[*] Dang tao file cau hinh .env.local cho Windows..." -ForegroundColor Yellow
$EnvPath = Join-Path $RepoDir ".env.local"
$EnvContent = @"
JWT_SECRET=8a781e77bc4f6023737d95798ee2ba9ed8a220c5e89b49ab525e3044b3205e2c
INITIAL_PASSWORD=Khanh.le@123
PORT=20128
NODE_ENV=production
"@
[System.IO.File]::WriteAllText($EnvPath, $EnvContent)
Write-Host "[OK] Da luu file .env.local tai: $EnvPath" -ForegroundColor Green

# 6. Cai dat thu vien va build du an
Write-Host "`n[*] Dang cai dat thu vien va build 9router (qua trinh nay mat khoang 1-2 phut)..." -ForegroundColor Yellow
Set-Location $RepoDir
npm install --no-audit
npm run build

# 7. Tao file batch khoi dong nhanh start-9router.bat
Write-Host "`n[*] Dang tao shortcut khoi chay nhanh..." -ForegroundColor Yellow
$StartBatPath = Join-Path $RepoDir "start-9router.bat"
$StartBatContent = @"
@echo off
title 9Router Server
cd /d "%~dp0"
node .next/standalone/server.js
pause
"@
[System.IO.File]::WriteAllText($StartBatPath, $StartBatContent)
Write-Host "[OK] Da tao file khoi chay nhanh: $StartBatPath" -ForegroundColor Green

# 8. Giai ma va khoi phuc bo nho Agent (Brain/Conversations)
Write-Host "`n[*] Dang khoi phuc bo nho va lich su cua Agent (Brain/Conversations)..." -ForegroundColor Yellow
$RestoreScript = Join-Path $WorkspaceDir "9router-backup\unpack-memory.js"
if (Test-Path $RestoreScript) {
    node $RestoreScript
} else {
    Write-Host "[WARNING] Khong tim thay file khoi phuc bo nho: $RestoreScript" -ForegroundColor Yellow
}

Write-Host "`n==============================================" -ForegroundColor Green
Write-Host "[THANH CONG] Dong bo va cai dat hoan tat!" -ForegroundColor Green
Write-Host "Bay gio ban chi can dup chuot vao file sau de chay 9router:" -ForegroundColor Green
Write-Host "  $StartBatPath" -ForegroundColor Yellow
Write-Host "Truy cap ung dung tai: http://localhost:20128" -ForegroundColor Green
Write-Host "==============================================" -ForegroundColor Green
