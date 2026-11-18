# ============================================================
# PULU POWERSHELL PROFILE -- PuluSmartFlow v4.1 Verified Engine (Windows)
# Sync với pulu_smartflow.sh (macOS/Linux)
# Architecture: 9Router High-Speed Gateway (http://127.0.0.1:20128/v1)
# Security: Zero Plain-Text API Key in Git
# ============================================================

# --- 1. 9router Proxy CLI -----------------------------------
function Start-9router { & "$env:APPDATA\npm\9router.cmd" @args }
Set-Alias -Name 9router -Value Start-9router -ErrorAction SilentlyContinue

# --- 2. Load Secure Environment (Zero Plain-Text Secret in Git) ---
$_envFile = "$env:USERPROFILE\.config\pulu\env.ps1"
if (Test-Path $_envFile) {
    . $_envFile
} else {
    $null = New-Item -Path (Split-Path $_envFile) -ItemType Directory -Force
    $detectedToken = "your-9router-key-here"
    $claudeSettings = "$env:USERPROFILE\.claude\settings.json"
    if (Test-Path $claudeSettings) {
        try {
            $json = Get-Content $claudeSettings -Raw | ConvertFrom-Json
            if ($json.env.ANTHROPIC_AUTH_TOKEN) {
                $detectedToken = $json.env.ANTHROPIC_AUTH_TOKEN
            }
        } catch {}
    }
    @"
# Pulu Secure Environment - DO NOT COMMIT TO GIT
`$env:ANTHROPIC_BASE_URL   = "http://127.0.0.1:20128/v1"
`$env:ANTHROPIC_AUTH_TOKEN = "$detectedToken"
Remove-Item env:ANTHROPIC_API_KEY -ErrorAction SilentlyContinue
"@ | Set-Content $_envFile
    . $_envFile
}

# Fix legacy /api/v1 URL (which caused HTTP 404 at /api/v1/v1/messages)
if ($env:ANTHROPIC_BASE_URL -like "*/api/v1*") {
    $env:ANTHROPIC_BASE_URL = "http://127.0.0.1:20128/v1"
}
if (-not $env:ANTHROPIC_AUTH_TOKEN -and $env:ANTHROPIC_API_KEY) {
    $env:ANTHROPIC_AUTH_TOKEN = $env:ANTHROPIC_API_KEY
}
Remove-Item env:ANTHROPIC_API_KEY -ErrorAction SilentlyContinue
$global:PULU_SAVED_9ROUTER_KEY = $env:ANTHROPIC_AUTH_TOKEN

# --- 3. Verified Live Aliases (Claude CLI 2.1+ Compatible) ----
function CThink   { claude --model "cc/claude-opus-5-5"        @args }
function COpus48  { claude --model "cc/claude-opus-4-8"        @args }
function CCode    { claude --model "cc/claude-sonnet-5-5"      @args }
function CSonnet46{ claude --model "cc/claude-sonnet-4-6"      @args }
function CFast    { claude --model "cc/claude-haiku-5-5"       @args }
function GPTSol   { claude --model "cx/gpt-6.1-sol"            @args }
function GPTAstra { claude --model "cx/gpt-6-astra"            @args }
function GPT1M    { claude --model "cx/gpt-6-astra[1m]"        @args }
function CSmart   { claude --model "pulu-claude-sonnet-5-5"     @args }
function CDeep    { claude --model "pulu-claude-opus-5-5"       @args }
function CArch    { claude --model "pulu-claude-sonnet-5-5"     @args }
function CLong    { claude --model "pulu-claude-sonnet-5-5[1m]" @args }

Set-Alias -Name c-think      -Value CThink    -ErrorAction SilentlyContinue
Set-Alias -Name c-opus       -Value CThink    -ErrorAction SilentlyContinue
Set-Alias -Name c-48         -Value COpus48   -ErrorAction SilentlyContinue
Set-Alias -Name c-code       -Value CCode     -ErrorAction SilentlyContinue
Set-Alias -Name c-sonnet     -Value CCode     -ErrorAction SilentlyContinue
Set-Alias -Name c-46         -Value CSonnet46 -ErrorAction SilentlyContinue
Set-Alias -Name c-fast       -Value CFast     -ErrorAction SilentlyContinue
Set-Alias -Name c-haiku      -Value CFast     -ErrorAction SilentlyContinue
Set-Alias -Name gpt-sol      -Value GPTSol    -ErrorAction SilentlyContinue
Set-Alias -Name gpt-astra    -Value GPTAstra  -ErrorAction SilentlyContinue
Set-Alias -Name gpt-1m       -Value GPT1M     -ErrorAction SilentlyContinue
Set-Alias -Name combo-smart  -Value CSmart    -ErrorAction SilentlyContinue
Set-Alias -Name combo-think  -Value CDeep     -ErrorAction SilentlyContinue
Set-Alias -Name combo-arch   -Value CArch     -ErrorAction SilentlyContinue
Set-Alias -Name combo-long   -Value CLong     -ErrorAction SilentlyContinue

# --- 4. Gateway Switcher & Detection --------------------------
function Select-PuluGateway {
    if ($global:PULU_GATEWAY_OVERRIDE -eq "direct") {
        $env:ANTHROPIC_BASE_URL = "https://api.anthropic.com"
        Remove-Item env:ANTHROPIC_AUTH_TOKEN -ErrorAction SilentlyContinue
        if ($env:PULU_DIRECT_API_KEY) { $env:ANTHROPIC_API_KEY = $env:PULU_DIRECT_API_KEY }
        Write-Host "[Gateway] Direct Connection (https://api.anthropic.com)" -ForegroundColor Yellow
        return
    }

    $env:ANTHROPIC_BASE_URL = "http://127.0.0.1:20128/v1"
    if ($global:PULU_SAVED_9ROUTER_KEY) {
        $env:ANTHROPIC_AUTH_TOKEN = $global:PULU_SAVED_9ROUTER_KEY
    }
    Remove-Item env:ANTHROPIC_API_KEY -ErrorAction SilentlyContinue
    Write-Host "[Gateway] 9Router (:20128/v1 - Verified Speed Route)" -ForegroundColor Cyan
}

function Use9router {
    $global:PULU_GATEWAY_OVERRIDE = "9router"
    $env:ANTHROPIC_BASE_URL = "http://127.0.0.1:20128/v1"
    if ($global:PULU_SAVED_9ROUTER_KEY) { $env:ANTHROPIC_AUTH_TOKEN = $global:PULU_SAVED_9ROUTER_KEY }
    Remove-Item env:ANTHROPIC_API_KEY -ErrorAction SilentlyContinue
    Write-Host "[OK] Claude switched to 9Router (http://127.0.0.1:20128/v1)" -ForegroundColor Green
}
function UseDirect {
    $global:PULU_GATEWAY_OVERRIDE = "direct"
    $env:ANTHROPIC_BASE_URL = "https://api.anthropic.com"
    Remove-Item env:ANTHROPIC_AUTH_TOKEN -ErrorAction SilentlyContinue
    if ($env:PULU_DIRECT_API_KEY) { $env:ANTHROPIC_API_KEY = $env:PULU_DIRECT_API_KEY }
    Write-Host "[OK] Claude switched to DIRECT mode (https://api.anthropic.com)" -ForegroundColor Yellow
}
Set-Alias -Name use-9router -Value Use9router -ErrorAction SilentlyContinue
Set-Alias -Name use-direct  -Value UseDirect  -ErrorAction SilentlyContinue

# --- 5. SMART AI ROUTER (Keyword-based) -----------------------
function SmartClaude {
    param([Parameter(ValueFromRemainingArguments)][string[]]$Words)
    $prompt = $Words -join " "

    if (-not $prompt) {
        Write-Host "[Warning] Vui long nhap noi dung. Vi du: ai phan tich he thong..." -ForegroundColor Yellow
        return
    }

    $lower = $prompt.ToLower()
    $model = "pulu-claude-sonnet-5-5"
    $taskLabel = "COMBO SMART: pulu-claude-sonnet-5-5 (Sonnet 5.5 -> Sonnet 4.6 -> GPT-6 Astra)"

    if ($lower -match "phan tich|chien luoc|ke hoach|logic|kien truc|he thong|quy hoach|tu duy|chieu sau|danh doi|trade.off|p&l|sla|nguyen nhan|root cause|insight|quyet dinh|decision|rui ro|fraud|cung cau|supply|demand|tam ly|hanh vi|churn|retention") {
        $model = "pulu-claude-opus-5-5"
        $taskLabel = "BRAIN STRATEGY: pulu-claude-opus-5-5 (Opus 5.5 -> Opus 4.8 -> GPT-6.1 Sol)"
    } elseif ($lower -match "du lieu|data|log|logs|doc file|tom tat file|file dai|bao cao|csv|dich thuat|thong bao|tai xe|zalo|email") {
        $model = "pulu-claude-sonnet-5-5[1m]"
        $taskLabel = "LONG CONTEXT 1M: pulu-claude-sonnet-5-5[1m] (GPT-6 Astra [1M] -> Sonnet 5.5)"
    } elseif ($lower -match "code|lap trinh|refactor|function|script|python|bash|sql|query|database|ui|ux|html|css|landing page|dashboard|docker|git") {
        $model = "pulu-claude-sonnet-5-5"
        $taskLabel = "ENGINEERING: pulu-claude-sonnet-5-5 (Sonnet 5.5 -> Sonnet 4.6 -> GPT-6 Astra)"
    } elseif ($lower -match "hoi nhanh|giai thich|tinh toan|dinh nghia|la gi|nhu the nao|the nao|regex") {
        $model = "pulu-claude-haiku-5-5"
        $taskLabel = "FAST CLI: pulu-claude-haiku-5-5 (Haiku 5.5 -> Sonnet 5.5)"
    }

    Write-Host "`n[Auto-Detect v4.1] " -NoNewline
    Select-PuluGateway
    Write-Host "[Model] $taskLabel`n" -ForegroundColor DarkGray

    claude --model $model -p $prompt
}
Set-Alias -Name ai -Value SmartClaude -ErrorAction SilentlyContinue

# --- 6. SMART CHAT (Interactive Mode) -------------------------
function SmartChat {
    param(
        [switch]$Danger,
        [Parameter(ValueFromRemainingArguments)][string[]]$Words
    )
    $prompt = $Words -join " "
    $lower = $prompt.ToLower()
    $model = "pulu-claude-sonnet-5-5"

    if ($Danger) {
        $model = "pulu-claude-opus-5-5"
    } elseif ($lower -match "phan tich|chien luoc|ke hoach|logic|kien truc|quy hoach|tu duy|quyet dinh|p&l|sla") {
        $model = "pulu-claude-opus-5-5"
    } elseif ($lower -match "code|lap trinh|ui|ux|dashboard|sql") {
        $model = "pulu-claude-sonnet-5-5"
    } elseif ($lower -match "file|log|du lieu|bao cao|tom tat") {
        $model = "pulu-claude-sonnet-5-5[1m]"
    }

    Select-PuluGateway

    $claudeArgs = @()
    if ($Danger) {
        $claudeArgs += "--dangerously-skip-permissions"
    }

    if ($prompt) {
        claude @claudeArgs --model $model --continue -p $prompt
    } else {
        claude @claudeArgs --model $model
    }
}
Set-Alias -Name chat -Value SmartChat -ErrorAction SilentlyContinue

function chat! {
    param([Parameter(ValueFromRemainingArguments)][string[]]$Words)
    SmartChat -Danger @Words
}

Write-Host "PuluSmartFlow v4.1 (9Router :20128/v1 Verified) Loaded | Zero-404 Routing Active" -ForegroundColor DarkGray
