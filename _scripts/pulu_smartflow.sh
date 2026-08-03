# ============================================================
# PULU BASH/ZSH PROFILE — PuluSmartFlow v3.0 Hybrid Engine (macOS/Linux)
# Architecture: Dual-Gateway Router (9router :20128 + OmniRoute :20130)
# Logic: Regex-first routing (<1ms), Token compression, Auto-fallback
# ============================================================

# === Start local AI Proxies ===
alias 9router="9router"
alias omniroute="omniroute"

# === Load Secure Environment ===
_env_file="$HOME/.config/pulu/env.sh"
if [[ -f "$_env_file" ]]; then
    source "$_env_file"
else
    # Tạo file env nếu chưa có (chạy lần đầu)
    mkdir -p "$(dirname "$_env_file")"
    cat << 'EOF' > "$_env_file"
# Pulu Secure Environment — ĐỪNG commit file này lên Git!
# export ANTHROPIC_BASE_URL="http://localhost:20128/api/v1"
# export ANTHROPIC_API_KEY="your-9router-key-here"
EOF
    chmod 600 "$_env_file"
fi

# === Claude Aliases for Dual-Gateway ===
alias c-think="claude --model cc/claude-opus-4-8"
alias c-code="claude --model cc/claude-sonnet-4-6"
alias c-fast="claude --model oc/deepseek-v4-flash"
# ============================================

# === SMART AI ROUTER (v3.5 Auto-Detect Model & Gateway) ===
_auto_detect_gateway() {
    local prompt="$1"
    local lower_prompt="$2"
    local prompt_len=${#prompt}

    # Nếu prompt dài > 500 ký tự HOẶC chứa từ khóa xử lý log/data lớn -> Trỏ sang OmniRoute (:20130) để Nén Token & Fallback
    if [[ $prompt_len -gt 500 ]] || [[ "$lower_prompt" =~ (\.log|\.csv|\.json|\.pdf|tóm tắt file|đọc file|dữ liệu lớn|văn bản dài|báo cáo dài) ]]; then
        export ANTHROPIC_BASE_URL="http://localhost:20130/v1"
        echo "🛡️ Gateway: OmniRoute (:20130 - Nén Token & Dự Phòng Auto-Fallback)"
    else
        # Mặc định cho tác vụ ngắn & CLI -> Trỏ sang 9Router (:20128) để Đạt Tốc Độ Siêu Tốc < 1ms
        export ANTHROPIC_BASE_URL="http://localhost:20128/api/v1"
        echo "⚡ Gateway: 9Router (:20128 - Terminal Siêu Tốc < 1ms)"
    fi
}

smart_claude() {
    local prompt="$*"
    if [[ -z "$prompt" ]]; then
        echo "⚠️ Vui lòng nhập nội dung. Ví dụ: ai phân tích hệ thống..."
        return 1
    fi
    
    # Chuyển về chữ thường để kiểm tra từ khóa
    local lower_prompt=$(echo "$prompt" | awk '{print tolower($0)}')
    local model="cc/claude-sonnet-4-6" # Mặc định là Sonnet
    local task_label="SONNET 4.6 (Max Coding)"

    # 1. Phân nhóm Opus (The Brain - Tư duy sâu, chiến lược, phân tích phức tạp)
    if [[ "$lower_prompt" =~ (phân tích|chiến lược|kế hoạch|logic|kiến trúc|hệ thống|quy hoạch|tư duy|chiều sâu|đánh đổi|trade-off|p\&l|sla|nguyên nhân gốc rễ|root cause|insight|quyết định|decision|rủi ro|fraud|cung cầu|supply|demand|tâm lý|hành vi) ]]; then
        model="cc/claude-opus-4-8"
        task_label="OPUS 4.8 (Max Logic)"
        
    # 2. Phân nhóm Gemini Pro (The Communicator / Context - Giao tiếp, đọc/xử lý văn bản lớn, thông báo Zalo, dịch thuật)
    elif [[ "$lower_prompt" =~ (dịch thuật|dịch|thông báo|tài xế|zalo|email|chính tả|ngữ pháp|viết lại|caption|kịch bản|nội dung|tóm tắt|đọc file|log) ]]; then
        model="gc/gemini-3.1-pro-preview"
        task_label="GEMINI 3.1 PRO (Max Context)"
        
    # 3. Phân nhóm DeepSeek Flash (The Sprinter - Việc vặt, hỏi đáp siêu nhanh, tính toán nhẹ)
    elif [[ "$lower_prompt" =~ (hỏi nhanh|giải thích|tính toán|định nghĩa|là gì|như thế nào|thế nào|regex) ]]; then
        model="oc/deepseek-v4-flash"
        task_label="DEEPSEEK V4 FLASH (Siêu Tốc)"

    # 4. Phân nhóm Sonnet (The Coder / Formatter - Trình bày, Code, Giao diện)
    elif [[ "$lower_prompt" =~ (trình bày|code|lập trình|html|css|giao diện|ui|ux|lark|docs|báo cáo|định dạng|table|bảng|markdown|website|landing page|sql|git|docker|k8s) ]]; then
        model="cc/claude-sonnet-4-6"
        task_label="SONNET 4.6 (Max Coding)"
    fi

    # Tự động chọn Gateway tối ưu (9Router vs OmniRoute)
    echo -n "🔀 [Auto-Detect v3.5] "
    _auto_detect_gateway "$prompt" "$lower_prompt"
    echo -e "🧠 Model: $task_label\n"

    # Gọi Claude Code với /dev/null để tránh treo TTY stdin
    claude --model "$model" -p "$prompt" < /dev/null
}
alias ai="smart_claude"

# === SMART CHAT (TTY Interactive Mode) ===
smart_chat() {
    local prompt="$*"
    local lower_prompt=$(echo "$prompt" | awk '{print tolower($0)}')
    local model="cc/claude-sonnet-4-6" # Mặc định
    local task_label="SONNET 4.6 (Max Coding)"

    if [[ "$lower_prompt" =~ (phân tích|chiến lược|kế hoạch|logic|kiến trúc|hệ thống|quy hoạch|tư duy|chiều sâu|đánh đổi|trade-off|p\&l|sla|nguyên nhân gốc rễ|root cause|insight|quyết định|decision|rủi ro|fraud|cung cầu|supply|demand|tâm lý|hành vi) ]]; then
        model="cc/claude-opus-4-8"
        task_label="OPUS 4.8 (Max Logic)"
    elif [[ "$lower_prompt" =~ (dịch thuật|dịch|thông báo|tài xế|zalo|email|chính tả|ngữ pháp|viết lại|caption|kịch bản|nội dung|tóm tắt|đọc file|log) ]]; then
        model="gc/gemini-3.1-pro-preview"
        task_label="GEMINI 3.1 PRO (Max Context)"
    elif [[ "$lower_prompt" =~ (hỏi nhanh|giải thích|tính toán|định nghĩa|là gì|như thế nào|thế nào|regex) ]]; then
        model="oc/deepseek-v4-flash"
        task_label="DEEPSEEK V4 FLASH (Siêu Tốc)"
    elif [[ "$lower_prompt" =~ (trình bày|code|lập trình|html|css|giao diện|ui|ux|lark|docs|báo cáo|định dạng|table|bảng|markdown|website|landing page|sql|git|docker|k8s) ]]; then
        model="cc/claude-sonnet-4-6"
        task_label="SONNET 4.6 (Max Coding)"
    fi

    echo -n "🔀 [Auto-Detect v3.5] "
    _auto_detect_gateway "$prompt" "$lower_prompt"
    echo -e "🧠 Model: $task_label\n"

    # Tương tác đầy đủ (TTY) - KHÔNG có -p flag trừ khi được chuyển tiếp bằng cờ --continue
    if [[ -n "$prompt" ]]; then
        claude --model "$model" --continue -p "$prompt"
    else
        claude --model "$model"
    fi
}
alias chat="smart_chat"

# === Gateway Switcher Wrappers (Thủ công nếu muốn override) ===
use_9router() {
    export ANTHROPIC_BASE_URL="http://localhost:20128/api/v1"
    echo -e "✅ Claude đã cố định trỏ về 9Router (localhost:20128)"
}
alias use-9router="use_9router"

use_omni() {
    export ANTHROPIC_BASE_URL="http://localhost:20130/v1"
    echo -e "✅ Claude đã cố định trỏ về OmniRoute (localhost:20130)"
}
alias use-omni="use_omni"

# === Circuit Breaker cho command_not_found_handler ===
export _PULU_CNF_DEPTH=0
command_not_found_handler() {
    local cmd="$1"
    if [[ $_PULU_CNF_DEPTH -ge 1 ]]; then
        echo -e "❌ [Pulu Circuit Breaker] Phát hiện đệ quy lặp lệnh. Hủy thực thi để bảo vệ hệ thống."
        return 127
    fi
    export _PULU_CNF_DEPTH=$((_PULU_CNF_DEPTH + 1))
    
    # Chỉ hỏi Claude khi ở TTY tương tác và lệnh không rỗng
    if [[ -t 0 && -n "$cmd" ]]; then
        echo -e "\n🔍 [CNF] Lệnh không tìm thấy: '$cmd' -> Đang chuyển tiếp đến Claude..."
        smart_chat "$@"
        export _PULU_CNF_DEPTH=0
        return 0
    fi

    export _PULU_CNF_DEPTH=0
    return 127
}

# ============================================
echo "🚀 PuluSmartFlow v3.5 Auto-Detect Engine Loaded | Auto Model & Auto Gateway Enabled"
