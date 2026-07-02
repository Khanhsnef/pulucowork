# setup-9router.ps1
# Script tự động cấu hình và cài đặt 9router trên Windows

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

# 1. Kiểm tra Node.js và Git
Write-Host "[*] Đang kiểm tra môi trường..." -ForegroundColor Yellow
try {
    $nodeVersion = node -v
    Write-Host "[OK] Node.js đã được cài đặt: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Node.js chưa được cài đặt trên máy Windows của bạn." -ForegroundColor Red
    Write-Host "Vui lòng cài đặt Node.js LTS tại: https://nodejs.org/" -ForegroundColor Yellow
    Exit
}

try {
    $gitVersion = git --version
    Write-Host "[OK] Git đã được cài đặt: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Git chưa được cài đặt trên máy Windows." -ForegroundColor Red
    Write-Host "Vui lòng cài đặt Git tại: https://git-scm.com/" -ForegroundColor Yellow
    Exit
}

# 2. Khởi tạo thư mục dữ liệu và giải mã cấu hình
Write-Host "`n[*] Đang giải mã và cấu hình thư mục dữ liệu tại AppData..." -ForegroundColor Yellow
if (-not (Test-Path $TargetDataDir)) {
    New-Item -ItemType Directory -Path $TargetDataDir -Force | Out-Null
    Write-Host "[OK] Đã tạo thư mục dữ liệu AppData: $TargetDataDir" -ForegroundColor Green
}

$DecryptScript = Join-Path $WorkspaceDir "9router-backup\decrypt.js"
if (Test-Path $DecryptScript) {
    node $DecryptScript $TargetDataDir
    Write-Host "[OK] Khôi phục dữ liệu cấu hình thành công!" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Không tìm thấy tệp tin giải mã: $DecryptScript" -ForegroundColor Red
    Exit
}

# 3. Clone repository 9router
Write-Host "`n[*] Đang kiểm tra mã nguồn 9router..." -ForegroundColor Yellow
if (-not (Test-Path $RepoDir)) {
    Write-Host "[*] Đang clone mã nguồn 9router từ GitHub..." -ForegroundColor Yellow
    git clone https://github.com/decolua/9router.git $RepoDir
    if (-not (Test-Path $RepoDir)) {
        Write-Host "[ERROR] Không thể clone repository 9router." -ForegroundColor Red
        Exit
    }
    Write-Host "[OK] Đã clone thành công 9router về: $RepoDir" -ForegroundColor Green
} else {
    Write-Host "[OK] Mã nguồn 9router đã tồn tại tại: $RepoDir" -ForegroundColor Green
}

# 4. Ghi đè các file tùy chỉnh (Patches)
if (Test-Path $BackupPatchDir) {
    Write-Host "`n[*] Đang áp dụng các file tùy chỉnh (Model registry, esbuild patches)..." -ForegroundColor Yellow
    Copy-Item -Path "$BackupPatchDir\*" -Destination $RepoDir -Recurse -Force
    Write-Host "[OK] Đã áp dụng toàn bộ các bản vá thành công." -ForegroundColor Green
}

# 5. Khởi tạo file cấu hình môi trường .env.local
Write-Host "`n[*] Đang tạo file cấu hình .env.local cho Windows..." -ForegroundColor Yellow
$EnvPath = Join-Path $RepoDir ".env.local"
$EnvContent = @"
JWT_SECRET=8a781e77bc4f6023737d95798ee2ba9ed8a220c5e89b49ab525e3044b3205e2c
INITIAL_PASSWORD=Khanh.le@123
PORT=20128
NODE_ENV=production
"@
[System.IO.File]::WriteAllText($EnvPath, $EnvContent)
Write-Host "[OK] Đã lưu file .env.local tại: $EnvPath" -ForegroundColor Green

# 6. Cài đặt thư viện và build dự án
Write-Host "`n[*] Đang cài đặt thư viện và build 9router (quá trình này mất khoảng 1-2 phút)..." -ForegroundColor Yellow
Set-Location $RepoDir
npm install --no-audit
npm run build

# 7. Tạo file batch khởi động nhanh start-9router.bat
Write-Host "`n[*] Đang tạo shortcut khởi chạy nhanh..." -ForegroundColor Yellow
$StartBatPath = Join-Path $RepoDir "start-9router.bat"
$StartBatContent = @"
@echo off
title 9Router Server
cd /d "%~dp0"
node .next/standalone/server.js
pause
"@
[System.IO.File]::WriteAllText($StartBatPath, $StartBatContent)
Write-Host "[OK] Đã tạo file khởi chạy nhanh: $StartBatPath" -ForegroundColor Green

# 8. Giải mã và khôi phục bộ nhớ Agent (Brain/Conversations)
Write-Host "`n[*] Đang khôi phục bộ nhớ và lịch sử của Agent (Brain/Conversations)..." -ForegroundColor Yellow
$RestoreScript = Join-Path $WorkspaceDir "9router-backup\unpack-memory.js"
if (Test-Path $RestoreScript) {
    node $RestoreScript
} else {
    Write-Host "[WARNING] Không tìm thấy file khôi phục bộ nhớ: $RestoreScript" -ForegroundColor Yellow
}

Write-Host "`n==============================================" -ForegroundColor Green
Write-Host "[THÀNH CÔNG] Đồng bộ và cài đặt hoàn tất!" -ForegroundColor Green
Write-Host "Bây giờ bạn chỉ cần đúp chuột vào file sau để chạy 9router:" -ForegroundColor Green
Write-Host "  $StartBatPath" -ForegroundColor Yellow
Write-Host "Truy cập ứng dụng tại: http://localhost:20128" -ForegroundColor Green
Write-Host "==============================================" -ForegroundColor Green
