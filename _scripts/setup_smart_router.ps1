# ============================================================
# setup_smart_router.ps1 -- Setup PuluSmartFlow on Windows
# Configures profile for both PS5.1 and PS7 (OneDrive & Local)
# ============================================================

$scriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { (Get-Location).Path }
$smartflow = Join-Path $scriptDir "pulu_smartflow.ps1"

$profileSnippet = @"

# === SMART AI ROUTER (PuluSmartFlow) ===
if (Test-Path '$smartflow') { . '$smartflow' }
elseif (Test-Path "`$env:USERPROFILE\Desktop\Pulu-workspace\_scripts\pulu_smartflow.ps1") { . "`$env:USERPROFILE\Desktop\Pulu-workspace\_scripts\pulu_smartflow.ps1" }
elseif (Test-Path "`$env:USERPROFILE\pulucowork\_scripts\pulu_smartflow.ps1") { . "`$env:USERPROFILE\pulucowork\_scripts\pulu_smartflow.ps1" }
# ============================================
"@

$targetProfiles = @(
    "$env:USERPROFILE\OneDrive\Documents\PowerShell\Microsoft.PowerShell_profile.ps1",
    "$env:USERPROFILE\OneDrive\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1",
    "$env:USERPROFILE\Documents\PowerShell\Microsoft.PowerShell_profile.ps1",
    "$env:USERPROFILE\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1"
)

foreach ($p in $targetProfiles) {
    $parentDir = Split-Path $p
    if (-not (Test-Path $parentDir)) {
        [System.IO.Directory]::CreateDirectory($parentDir) | Out-Null
    }

    if (-not (Test-Path $p)) {
        [System.IO.File]::WriteAllText($p, $profileSnippet)
        Write-Host "[OK] Created profile: $p" -ForegroundColor Green
    } else {
        $hasSmartFlow = Select-String -Path $p -Pattern "pulu_smartflow" -Quiet
        if (-not $hasSmartFlow) {
            Add-Content -Path $p -Value $profileSnippet
            Write-Host "[OK] Updated profile: $p" -ForegroundColor Green
        } else {
            Write-Host "[OK] Profile already configured: $p" -ForegroundColor Cyan
        }
    }
}

Write-Host "`nSetup completed! Run `. `$PROFILE` or open a new terminal." -ForegroundColor Green
