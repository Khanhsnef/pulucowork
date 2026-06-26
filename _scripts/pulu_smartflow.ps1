# ============================================================
# PULU POWERSHELL PROFILE — PuluSmartFlow v1.0 (Windows)
# Port từ Mac .zshrc smart_claude → PowerShell
# ============================================================

# ── 9router — AI Proxy Router (localhost:20128) ──────────────
function Start-9router { & "$env:APPDATA\npm\9router.cmd" @args }
Set-Alias -Name 9router -Value Start-9router

# ── Biến môi trường 9router ──────────────────────────────────
# API key KHÔNG được hardcode ở đây — load từ file bảo mật
$_envFile = "$env:USERPROFILE\.config\pulu\env.ps1"
if (Test-Path $_envFile) {
    . $_envFile
} else {
    # Tạo file env nếu chưa có (chạy lần đầu)
    $null = New-Item -Path (Split-Path $_envFile) -ItemType Directory -Force
    @'
# Pulu Secure Environment — ĐỪNG commit file này lên Git!
# $env:ANTHROPIC_BASE_URL = "http://localhost:20128/api/v1"
# $env:ANTHROPIC_API_KEY  = "your-9router-key-here"
'@ | Set-Content $_envFile
}

# ── SMART AI ROUTER (Keyword-based, Regex-first) ─────────────
# Ported từ smart_claude() trong ~/.zshrc Mac
# Logic: Regex route trước (<1ms), KHÔNG gọi HTTP AI classifier
# → Giải quyết latency bug gốc (1.5s-3s/lần gõ)
function SmartClaude {
    param([Parameter(ValueFromRemainingArguments)][string[]]$Words)
    $prompt = $Words -join " "

    if (-not $prompt) {
        Write-Host "⚠️  Vui lòng nhập nội dung. Ví dụ: ai phân tích hệ thống..." -ForegroundColor Yellow
        return
    }

    $lower = $prompt.ToLower()
    $model = "cc/claude-sonnet-4-6"  # Mặc định

    # ── Tier 1: OPUS — Tư duy sâu, chiến lược, phân tích phức tạp ──
    if ($lower -match "phân tích|chiến lược|kế hoạch|logic|kiến trúc|hệ thống|quy hoạch|tư duy|chiều sâu|đánh đổi|trade.off|p&l|sla|nguyên nhân|root cause|insight|quyết định|decision|rủi ro|fraud|cung cầu|supply|demand|tâm lý|hành vi") {
        $model = "cc/claude-opus-4-8"
        Write-Host "`n🧠 [Smart Router] Task Tư Duy Sâu → OPUS (Max Logic)" -ForegroundColor Magenta

    # ── Tier 2: GEMINI PRO — Ngôn ngữ, context lớn, viết lách ──────
    } elseif ($lower -match "dịch thuật|dịch |thông báo|tài xế|zalo|email|chính tả|ngữ pháp|viết lại|caption|kịch bản|nội dung|tóm tắt|đọc file|\.log") {
        $model = "gc/gemini-3-pro-preview"
        Write-Host "`n⚡ [Smart Router] Task Ngôn Ngữ / Context → GEMINI PRO" -ForegroundColor Cyan

    # ── Tier 3: DEEPSEEK FLASH — Hỏi đáp nhanh, tính toán nhẹ ─────
    } elseif ($lower -match "hỏi nhanh|giải thích|tính toán|định nghĩa|là gì|như thế nào|thế nào|regex") {
        $model = "oc/deepseek-v4-flash-free"
        Write-Host "`n💨 [Smart Router] Task Nhanh → DEEPSEEK FLASH (Siêu Tốc)" -ForegroundColor Yellow

    # ── Tier 4: SONNET — Code, format, báo cáo, UI ──────────────────
    } elseif ($lower -match "trình bày|code|lập trình|html|css|giao diện|ui|ux|lark|docs|báo cáo|định dạng|table|bảng|markdown|website|landing page|sql") {
        $model = "cc/claude-sonnet-4-6"
        Write-Host "`n💻 [Smart Router] Task Code/Format → SONNET (Max Coding)" -ForegroundColor Green

    # ── Default ──────────────────────────────────────────────────────
    } else {
        Write-Host "`n🤖 [Smart Router] Task chung → SONNET (Mặc định)" -ForegroundColor Blue
    }

    # Gọi claude — KHÔNG dùng --dangerously-skip-permissions (security fix)
    claude --model $model -p $prompt
}
Set-Alias -Name ai -Value SmartClaude

# ── SMART CHAT — Interactive mode (giống smart_chat Mac) ──────
# Khác với `ai`: không dùng -p flag → Claude chạy interactive TTY
# Hiển thị permission prompt (y/N) thay vì auto-skip
function SmartChat {
    param([Parameter(ValueFromRemainingArguments)][string[]]$Words)
    $prompt = $Words -join " "

    $lower = $prompt.ToLower()
    $model = "cc/claude-sonnet-4-6"  # Mặc định

    if ($lower -match "phân tích|chiến lược|kế hoạch|logic|kiến trúc|hệ thống|quy hoạch|tư duy|chiều sâu|đánh đổi|trade.off|p&l|sla|nguyên nhân|root cause|insight|quyết định|decision|rủi ro|fraud|cung cầu|supply|demand|tâm lý|hành vi") {
        $model = "cc/claude-opus-4-8"
        Write-Host "`n🧠 [Smart Router] Task Tư Duy Sâu → OPUS" -ForegroundColor Magenta
    } elseif ($lower -match "dịch thuật|dịch |thông báo|tài xế|zalo|email|chính tả|ngữ pháp|viết lại|caption|kịch bản|nội dung|tóm tắt|đọc file|\.log") {
        $model = "gc/gemini-3-pro-preview"
        Write-Host "`n⚡ [Smart Router] Task Ngôn Ngữ / Context → GEMINI PRO" -ForegroundColor Cyan
    } elseif ($lower -match "hỏi nhanh|giải thích|tính toán|định nghĩa|là gì|như thế nào|thế nào|regex") {
        $model = "oc/deepseek-v4-flash-free"
        Write-Host "`n💨 [Smart Router] Task Nhanh → DEEPSEEK FLASH" -ForegroundColor Yellow
    } elseif ($lower -match "trình bày|code|lập trình|html|css|giao diện|ui|ux|lark|docs|báo cáo|định dạng|table|bảng|markdown|website|landing page|sql") {
        $model = "cc/claude-sonnet-4-6"
        Write-Host "`n💻 [Smart Router] Task Code/Format → SONNET" -ForegroundColor Green
    } else {
        Write-Host "`n🤖 [Smart Router] Task chung → SONNET (Mặc định)" -ForegroundColor Blue
    }

    # Interactive mode — KHÔNG có -p flag → hiển thị permission prompt
    if ($prompt) {
        claude --model $model --continue -p $prompt
    } else {
        claude --model $model
    }
}
Set-Alias -Name chat -Value SmartChat

# ── Claude Aliases nhanh ─────────────────────────────────────
function CThink { claude --model "cc/claude-opus-4-8"         @args }
function CCode  { claude --model "cc/claude-sonnet-4-6"       @args }
function CFast  { claude --model "oc/deepseek-v4-flash-free"  @args }

Set-Alias -Name c-think -Value CThink
Set-Alias -Name c-code  -Value CCode
Set-Alias -Name c-fast  -Value CFast

# ── Kích hoạt 9router endpoint cho Claude ───────────────────
# Chạy lệnh này trước khi dùng `claude` hoặc `ai`
function Use9router {
    $env:ANTHROPIC_BASE_URL = "http://localhost:20128/api/v1"
    Write-Host "✅ Claude đã trỏ về 9router (localhost:20128)" -ForegroundColor Green
}
Set-Alias -Name use-9router -Value Use9router

Write-Host "🚀 PuluSmartFlow loaded | Aliases: chat, ai, c-think, c-code, c-fast, 9router, use-9router" -ForegroundColor DarkGray
