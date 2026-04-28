$ErrorActionPreference = "Stop"
$env:PATH += ";C:\Program Files\Git\cmd"

$workDir = "C:\Users\lephu\pulucowork"
$logFile = "$workDir\sync-github.log"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

Set-Location $workDir

try {
    $status = git status --porcelain
    if ($status) {
        git add -A
        git commit -m "auto-sync: $timestamp"
        git push origin main 2>&1
        Add-Content $logFile "[$timestamp] SUCCESS: pushed changes"
    } else {
        Add-Content $logFile "[$timestamp] SKIP: no changes"
    }
} catch {
    Add-Content $logFile "[$timestamp] ERROR: $_"
}
