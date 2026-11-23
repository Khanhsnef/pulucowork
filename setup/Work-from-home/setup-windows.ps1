<#
.SYNOPSIS
    Cai dat va dong bo toan bo moi truong Pulu-workspace tren Windows
    de hoat dong giong may Mac cong ty.
#>

$ErrorActionPreference = "Continue"

$ScriptDir = $PSScriptRoot
if (-not $ScriptDir) { $ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path }
$WorkspaceDir = (Resolve-Path (Join-Path $ScriptDir "..\..")).Path

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "   PULU WORKSPACE - WINDOWS SETUP (2026)             " -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "Workspace: $WorkspaceDir`n" -ForegroundColor Gray

function Test-Cmd($Name) {
    return $null -ne (Get-Command $Name -ErrorAction SilentlyContinue)
}

# 1. Kiem tra cac cong cu nen tang
Write-Host "[1/7] Kiem tra cong cu he thong..." -ForegroundColor Yellow
$Missing = @()
if (Test-Cmd "git") { Write-Host "  [OK] $(git --version)" -ForegroundColor Green } else { $Missing += "Git.Git" }
if (Test-Cmd "node") { Write-Host "  [OK] Node $(node -v)" -ForegroundColor Green } else { $Missing += "OpenJS.NodeJS.LTS" }
if (Test-Cmd "python") { Write-Host "  [OK] $(python --version)" -ForegroundColor Green } else { $Missing += "Python.Python.3.14" }
if (Test-Cmd "uv") { Write-Host "  [OK] $(uv --version)" -ForegroundColor Green } else { Write-Host "  [WARN] Chua co 'uv' (can cho MCP fetch). Cai bang: winget install astral-sh.uv" -ForegroundColor DarkYellow }
if (Test-Cmd "gh") { Write-Host "  [OK] GitHub CLI san sang" -ForegroundColor Green } else { Write-Host "  [WARN] Chua co 'gh' (GitHub CLI). Cai bang: winget install GitHub.cli" -ForegroundColor DarkYellow }

if ($Missing.Count -gt 0) {
    Write-Host "`n[ERROR] Thieu cong cu bat buoc. Hay cai bang winget roi chay lai:" -ForegroundColor Red
    foreach ($pkg in $Missing) {
        Write-Host "  winget install -e --id $pkg" -ForegroundColor Yellow
    }
    exit 1
}

# 2. Cau hinh Git symlink & khoi tao submodules
Write-Host "`n[2/7] Cau hinh Git symlinks & submodules..." -ForegroundColor Yellow
Set-Location $WorkspaceDir
git config --global core.symlinks true
git config core.symlinks true
git submodule update --init --recursive

# Kiem tra .claude/skills/* neu bi checkout thanh file text thay vi symlink
$ClaudeSkillsDir = Join-Path $WorkspaceDir ".claude\skills"
if (Test-Path $ClaudeSkillsDir) {
    $Broken = 0
    Get-ChildItem $ClaudeSkillsDir | ForEach-Object {
        if (-not $_.Attributes.HasFlag([System.IO.FileAttributes]::ReparsePoint) -and -not $_.PSIsContainer) {
            $targetRel = (Get-Content $_.FullName -Raw).Trim()
            $targetAbs = Join-Path (Join-Path $WorkspaceDir ".claude\skills") $targetRel
            if (Test-Path $targetAbs) {
                Remove-Item $_.FullName -Force
                cmd /c mklink /J "`"$($_.FullName)`"" "`"$((Resolve-Path $targetAbs).Path)`"" | Out-Null
                $Broken++
            }
        }
    }
    if ($Broken -gt 0) {
        Write-Host "  [OK] Da chuyen $Broken skill links sang Windows Directory Junction." -ForegroundColor Green
    } else {
        Write-Host "  [OK] Toan bo .claude/skills hoat dong binh thuong." -ForegroundColor Green
    }
}

# 3. Tao Python .venv & cai requirements.txt
Write-Host "`n[3/7] Kiem tra Python .venv & thu vien..." -ForegroundColor Yellow
$VenvDir = Join-Path $WorkspaceDir ".venv"
$VenvPython = Join-Path $VenvDir "Scripts\python.exe"
if (-not (Test-Path $VenvPython)) {
    Write-Host "  [*] Dang tao .venv..." -ForegroundColor Cyan
    python -m venv $VenvDir
}
& $VenvPython -m pip install --upgrade pip --quiet
$ReqFile = Join-Path $WorkspaceDir "requirements.txt"
if (Test-Path $ReqFile) {
    Write-Host "  [*] Dang cai thu vien tu requirements.txt..." -ForegroundColor Cyan
    & $VenvPython -m pip install -r $ReqFile --quiet
    Write-Host "  [OK] Python .venv da san sang." -ForegroundColor Green
}

# 4. Kiem tra file .env
Write-Host "`n[4/7] Kiem tra file .env..." -ForegroundColor Yellow
$EnvFile = Join-Path $WorkspaceDir ".env"
$EnvExample = Join-Path $WorkspaceDir ".env.example"
if (-not (Test-Path $EnvFile)) {
    if (Test-Path $EnvExample) {
        Copy-Item $EnvExample $EnvFile
        Write-Host "  [WARN] Da tao .env tu .env.example. Hay chep 8 API keys tu may Mac vao file .env!" -ForegroundColor DarkYellow
    }
} else {
    Write-Host "  [OK] Da co file .env tai $EnvFile" -ForegroundColor Green
}

# 5. Cai dat 9Router (0.5.123) & Claude Code CLI
Write-Host "`n[5/7] Kiem tra 9Router & Claude Code CLI..." -ForegroundColor Yellow
if (-not (Test-Cmd "9router")) {
    Write-Host "  [*] Dang cai 9router@0.5.123..." -ForegroundColor Cyan
    npm install -g 9router@0.5.123 --no-audit
} else {
    Write-Host "  [OK] 9router da duoc cai: $(9router --version)" -ForegroundColor Green
}
if (-not (Test-Cmd "claude")) {
    Write-Host "  [*] Dang cai @anthropic-ai/claude-code..." -ForegroundColor Cyan
    npm install -g @anthropic-ai/claude-code --no-audit
} else {
    Write-Host "  [OK] Claude Code CLI da co." -ForegroundColor Green
}

# 6. Cau hinh bien moi truong User cho 9Router -> Claude CLI
Write-Host "`n[6/7] Thiet lap bien moi truong ANTHROPIC_BASE_URL..." -ForegroundColor Yellow
[Environment]::SetEnvironmentVariable("ANTHROPIC_BASE_URL", "http://127.0.0.1:20128/v1", "User")
[Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", $null, "User")
$ExistingToken = [Environment]::GetEnvironmentVariable("ANTHROPIC_AUTH_TOKEN", "User")
if (-not $ExistingToken) {
    Write-Host "  [WARN] Chua co ANTHROPIC_AUTH_TOKEN. Sau khi dang nhap 9Router tai http://localhost:20128, hay set:" -ForegroundColor DarkYellow
    Write-Host '         setx ANTHROPIC_AUTH_TOKEN "<token-tu-9router>"' -ForegroundColor Gray
} else {
    Write-Host "  [OK] Da co ANTHROPIC_BASE_URL va ANTHROPIC_AUTH_TOKEN." -ForegroundColor Green
}

# 7. Khoi tao %USERPROFILE%\.gemini\GEMINI.md (neu chua co)
Write-Host "`n[7/7] Kiem tra cau hinh Antigravity (%USERPROFILE%\.gemini)..." -ForegroundColor Yellow
$GeminiDir = Join-Path $env:USERPROFILE ".gemini"
if (-not (Test-Path $GeminiDir)) {
    New-Item -ItemType Directory -Path $GeminiDir -Force | Out-Null
}
$GeminiMd = Join-Path $GeminiDir "GEMINI.md"
if (-not (Test-Path $GeminiMd)) {
    $GeminiMdContent = @"
<!-- codebase-memory-mcp:start -->
# Codebase Knowledge Graph (codebase-memory-mcp)

This project uses codebase-memory-mcp to maintain a knowledge graph of the codebase.
ALWAYS prefer MCP graph tools over grep/glob/file-search for code discovery.
<!-- codebase-memory-mcp:end -->
"@
    [System.IO.File]::WriteAllText($GeminiMd, $GeminiMdContent)
    Write-Host "  [OK] Da tao $GeminiMd" -ForegroundColor Green
} else {
    Write-Host "  [OK] Da co $GeminiMd" -ForegroundColor Green
}

Write-Host "`n=====================================================" -ForegroundColor Green
Write-Host "   HOAN TAT CAI DAT WINDOWS!                         " -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Green
Write-Host "Cac buoc con lai (lam 1 lan):" -ForegroundColor White
Write-Host "  1. Chep .env va thu muc .9router tu may Mac (neu can giu nguyen login)." -ForegroundColor Gray
Write-Host "  2. Mo Antigravity, dang nhap Google Account & bat cac plugins." -ForegroundColor Gray
Write-Host "  3. Chay 'start-9router.bat' de bat 9Router tai http://localhost:20128" -ForegroundColor Gray
