# ============================================================
# PULU POWERSHELL PROFILE -- PuluSmartFlow v3.5 Hybrid Engine (Windows)
# Port tu Mac .zshrc / pulu_smartflow.sh -> PowerShell
# ============================================================

# --- 9router -- AI Proxy Router (localhost:20128) ------------
function Start-9router { & "$env:APPDATA\npm\9router.cmd" @args }
Set-Alias -Name 9router -Value Start-9router -ErrorAction SilentlyContinue

# --- Bien moi truong 9router ----------------------------------
$_envFile = "$env:USERPROFILE\.config\pulu\env.ps1"
if (Test-Path $_envFile) {
    . $_envFile
} else {
    $null = New-Item -Path (Split-Path $_envFile) -ItemType Directory -Force
    "# Pulu Secure Environment - DO NOT COMMIT" | Set-Content $_envFile
}

# --- AUTO-DETECT GATEWAY --------------------------------------
function Select-PuluGateway {
    param([string]$Prompt, [string]$LowerPrompt)

    if ($global:PULU_GATEWAY_OVERRIDE -eq "9router") {
        $env:ANTHROPIC_BASE_URL = "http://localhost:20128/api/v1"
        $env:ANTHROPIC_API_KEY  = "sk-9router"
        Write-Host "[Gateway] 9Router (:20128 - Terminal Route)" -ForegroundColor Cyan
        return
    } elseif ($global:PULU_GATEWAY_OVERRIDE -eq "direct") {
        Remove-Item env:ANTHROPIC_BASE_URL -ErrorAction SilentlyContinue
        Remove-Item env:ANTHROPIC_API_KEY -ErrorAction SilentlyContinue
        Write-Host "[Gateway] Direct Connection (Anthropic API)" -ForegroundColor Yellow
        return
    } elseif ($global:PULU_GATEWAY_OVERRIDE -eq "omni") {
        $env:ANTHROPIC_BASE_URL = "http://localhost:20130/v1"
        $env:ANTHROPIC_API_KEY  = "sk-omni"
        Write-Host "[Gateway] OmniRoute (:20130 - Multi-Provider Engine)" -ForegroundColor Green
        return
    }

    # Auto-Detect mode
    if ($Prompt.Length -gt 500 -or $LowerPrompt -match "\.log|\.csv|\.json|\.pdf|tom tat file|doc file|du lieu lon|van ban dai|bao cao dai") {
        $env:ANTHROPIC_BASE_URL = "http://localhost:20130/v1"
        $env:ANTHROPIC_API_KEY  = "sk-omni"
        Write-Host "[Gateway] OmniRoute (:20130 - Auto-Fallback Active)" -ForegroundColor Green
    } else {
        $env:ANTHROPIC_BASE_URL = "http://localhost:20128/api/v1"
        $env:ANTHROPIC_API_KEY  = "sk-9router"
        Write-Host "[Gateway] 9Router (:20128 - Speed Route)" -ForegroundColor Cyan
    }
}

# --- SMART AI ROUTER (Keyword-based) -------------------------
function SmartClaude {
    param([Parameter(ValueFromRemainingArguments)][string[]]$Words)
    $prompt = $Words -join " "

    if (-not $prompt) {
        Write-Host "[Warning] Vui long nhap noi dung. Vi du: ai phan tich he thong..." -ForegroundColor Yellow
        return
    }

    $lower = $prompt.ToLower()
    $model = "cc/claude-sonnet-4-6"
    $taskLabel = "SONNET 4.6 (Max Coding)"

    if ($lower -match "phan tich|chien luoc|ke hoach|logic|kien truc|he thong|quy hoach|tu duy|chieu sau|danh doi|trade.off|p&l|sla|nguyen nhan|root cause|insight|quyet dinh|decision|rui ro|fraud|cung cau|supply|demand|tam ly|hanh vi") {
        $model = "cc/claude-opus-4-8"
        $taskLabel = "COMBO: PULU-BRAIN-CODE (Opus 4.8 + Sonnet 4.6 + DeepSeek)"
    } elseif ($lower -match "dich thuat|dich |thong bao|tai xe|zalo|email|chinh ta|ngu phap|viet lai|caption|kich ban|noi dung|tom tat|doc file|\.log") {
        $model = "gc/gemini-3.1-pro-preview"
        $taskLabel = "COMBO: PULU-DATA-LOG (Gemini 3.1 Pro + Sonnet 4.6)"
    } elseif ($lower -match "hoi nhanh|giai thich|tinh toan|dinh nghia|la gi|nhu the nao|the nao|regex") {
        $model = "oc/deepseek-v4-flash"
        $taskLabel = "COMBO: PULU-FAST-CLI (DeepSeek V4 Flash)"
    } elseif ($lower -match "trinh bay|code|lap trinh|html|css|giao dien|ui|ux|lark|docs|bao cao|dinh dang|table|bang|markdown|website|landing page|sql|git|docker|k8s") {
        $model = "cc/claude-sonnet-4-6"
        $taskLabel = "SONNET 4.6 (Max Coding)"
    }

    Write-Host "`n[Auto-Detect v3.5] " -NoNewline
    Select-PuluGateway -Prompt $prompt -LowerPrompt $lower
    Write-Host "[Model] $taskLabel`n" -ForegroundColor DarkGray

    claude --model $model -p $prompt
}
Set-Alias -Name ai -Value SmartClaude -ErrorAction SilentlyContinue

# --- SMART CHAT -- Interactive mode ---------------------------
function SmartChat {
    param(
        [switch]$Danger,
        [Parameter(ValueFromRemainingArguments)][string[]]$Words
    )
    $prompt = $Words -join " "
    $lower = $prompt.ToLower()
    $model = "cc/claude-sonnet-4-6"
    $taskLabel = "SONNET 4.6 (Max Coding)"

    if ($lower -match "phan tich|chien luoc|ke hoach|logic|kien truc|he thong|quy hoach|tu duy|chieu sau|danh doi|trade.off|p&l|sla|nguyen nhan|root cause|insight|quyet dinh|decision|rui ro|fraud|cung cau|supply|demand|tam ly|hanh vi") {
        $model = "cc/claude-opus-4-8"
        $taskLabel = "COMBO: PULU-BRAIN-CODE (Opus 4.8 + Sonnet 4.6)"
    } elseif ($lower -match "dich thuat|dich |thong bao|tai xe|zalo|email|chinh ta|ngu phap|viet lai|caption|kich ban|noi dung|tom tat|doc file|\.log") {
        $model = "gc/gemini-3.1-pro-preview"
        $taskLabel = "COMBO: PULU-DATA-LOG (Gemini 3.1 Pro)"
    } elseif ($lower -match "hoi nhanh|giai thich|tinh toan|dinh nghia|la gi|nhu the nao|the nao|regex") {
        $model = "oc/deepseek-v4-flash"
        $taskLabel = "COMBO: PULU-FAST-CLI (DeepSeek V4 Flash)"
    } elseif ($lower -match "trinh bay|code|lap trinh|html|css|giao dien|ui|ux|lark|docs|bao cao|dinh dang|table|bang|markdown|website|landing page|sql|git|docker|k8s") {
        $model = "cc/claude-sonnet-4-6"
        $taskLabel = "SONNET 4.6 (Max Coding)"
    }

    Write-Host "`n[Auto-Detect v3.5] " -NoNewline
    Select-PuluGateway -Prompt $prompt -LowerPrompt $lower
    Write-Host "[Model] $taskLabel" -ForegroundColor DarkGray

    $claudeArgs = @()
    if ($Danger) {
        Write-Host "[CHAT!] Auto-Approve Permissions (--dangerously-skip-permissions)" -ForegroundColor Yellow
        $claudeArgs += "--dangerously-skip-permissions"
    } else {
        Write-Host "[CHAT] System Permission Verification Default" -ForegroundColor Green
    }

    if ($prompt) {
        claude @claudeArgs --model $model --continue -p $prompt
    } else {
        claude @claudeArgs --model $model
    }
}

Set-Alias -Name chat -Value SmartChat -ErrorAction SilentlyContinue

# Lenh `chat!` -- Che do tu dong cap quyen (Auto-approve permissions)
function chat! {
    param([Parameter(ValueFromRemainingArguments)][string[]]$Words)
    SmartChat -Danger @Words
}

# --- Claude Aliases nhanh -------------------------------------
function CThink { claude --model "cc/claude-opus-4-8"   @args }
function CCode  { claude --model "cc/claude-sonnet-4-6" @args }
function CFast  { claude --model "oc/deepseek-v4-flash" @args }

Set-Alias -Name c-think -Value CThink -ErrorAction SilentlyContinue
Set-Alias -Name c-code  -Value CCode  -ErrorAction SilentlyContinue
Set-Alias -Name c-fast  -Value CFast  -ErrorAction SilentlyContinue

# --- Gateway Switchers ----------------------------------------
function Use9router {
    $global:PULU_GATEWAY_OVERRIDE = "9router"
    $env:ANTHROPIC_BASE_URL = "http://localhost:20128/api/v1"
    $env:ANTHROPIC_API_KEY  = "sk-9router"
    Write-Host "[OK] Claude switched to 9Router (localhost:20128)" -ForegroundColor Green
}
function UseOmni {
    $global:PULU_GATEWAY_OVERRIDE = "omni"
    $env:ANTHROPIC_BASE_URL = "http://localhost:20130/v1"
    $env:ANTHROPIC_API_KEY  = "sk-omni"
    Write-Host "[OK] Claude switched to OmniRoute (localhost:20130)" -ForegroundColor Green
}
function UseDirect {
    $global:PULU_GATEWAY_OVERRIDE = "direct"
    Remove-Item env:ANTHROPIC_BASE_URL -ErrorAction SilentlyContinue
    Remove-Item env:ANTHROPIC_API_KEY -ErrorAction SilentlyContinue
    Write-Host "[OK] Claude switched to DIRECT mode" -ForegroundColor Yellow
}
function UseAuto {
    $global:PULU_GATEWAY_OVERRIDE = $null
    Write-Host "[OK] Activated AUTO-DETECT GATEWAY" -ForegroundColor Cyan
}

Set-Alias -Name use-9router -Value Use9router -ErrorAction SilentlyContinue
Set-Alias -Name use-omni    -Value UseOmni    -ErrorAction SilentlyContinue
Set-Alias -Name use-direct  -Value UseDirect  -ErrorAction SilentlyContinue
Set-Alias -Name use-auto    -Value UseAuto    -ErrorAction SilentlyContinue

Write-Host "PuluSmartFlow v3.5 Loaded | Aliases: chat, chat!, ai, c-think, c-code, c-fast, 9router, omniroute, use-9router, use-omni, use-direct, use-auto" -ForegroundColor DarkGray
