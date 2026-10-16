# ============================================================
# sync-github.ps1 - Sync GitHub Workspace on Windows Home Machine
# ============================================================

$ErrorActionPreference = "Stop"

function Write-Info ($msg) { Write-Host "[INFO] $msg" -ForegroundColor Cyan }
function Write-Success ($msg) { Write-Host "[SUCCESS] $msg" -ForegroundColor Green }
function Write-WarningMsg ($msg) { Write-Host "[WARNING] $msg" -ForegroundColor Yellow }
function Write-ErrorMsg ($msg) { Write-Host "[ERROR] $msg" -ForegroundColor Red }

# 1. Project Directory
$ProjectDir = "C:\Users\lephu\pulucowork"
if (-not (Test-Path $ProjectDir)) {
    Write-ErrorMsg "Project directory not found: $ProjectDir"
    exit 1
}

Set-Location $ProjectDir
Write-Info "Checking git status..."

# 2. Check Git Status
$gitStatus = git status --porcelain
$hasChanges = -not [string]::IsNullOrEmpty($gitStatus)
$stashed = $false

# 3. Stash if there are uncommitted changes
if ($hasChanges) {
    Write-WarningMsg "Detected uncommitted changes. Stashing..."
    git stash | Out-Null
    $stashed = $true
}

# 4. Pull updates from GitHub
Write-Info "Pulling latest changes (git pull --rebase origin main)..."
try {
    git fetch origin | Out-Null
    $pullResult = git pull --rebase origin main 2>&1
    Write-Output $pullResult
    Write-Success "Pull successful!"
} catch {
    Write-ErrorMsg "Failed to pull from GitHub: $_"
    if ($stashed) {
        Write-WarningMsg "Restoring stashed changes..."
        git stash pop | Out-Null
    }
    exit 1
}

# 5. Pop Stash if stashed
if ($stashed) {
    Write-Info "Restoring stashed changes (git stash pop)..."
    try {
        git stash pop | Out-Null
        Write-Success "Restored stashed changes successfully!"
    } catch {
        Write-WarningMsg "Conflict detected while applying stash. Please resolve conflicts manually."
    }
}

Write-Success "Sync completed at $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
