# ============================================================
# PULU BASH/ZSH PROFILE — PuluSmartFlow v3.0 Hybrid Engine (macOS/Linux)
# Architecture: Dual-Gateway Router (9router :20128 + OmniRoute :20130)
# Logic: Regex-first routing (<1ms), Token compression, Auto-fallback
# ============================================================

# === Start local AI Proxies ===
alias 9router="9router"
alias pulu-start="zsh /Users/ts-1148/Desktop/Pulu-workspace/_scripts/pulu-start.sh"

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

# === Default Environment Settings ===
# Không mặc định cưỡng chế PULU_DIRECT_MODE để Auto-Detect Gateway hoạt động mượt mà
unset PULU_DIRECT_MODE

# === Claude & Gemini Aliases for Dual-Gateway ===
alias c-think="claude --model cc/claude-opus-4-8"
alias c-code="claude --model cc/claude-sonnet-4-6"
alias c-fast="claude --model cc/claude-sonnet-4-6"
alias c-37="claude --model cc/claude-3-7-sonnet-20250219"
alias g-37="claude --model gc/gemini-3.7-pro"
alias g-fast="claude --model gc/gemini-3.7-flash"
# ============================================

# === SMART AI ROUTER (Gateway Management) ===
_auto_detect_gateway() {
    if [[ "$PULU_GATEWAY_OVERRIDE" == "direct" ]]; then
        unset ANTHROPIC_BASE_URL
        PULU_ACTIVE_GW_LABEL="Direct API"
        echo "⚡ Gateway: Direct Connection (Trực tiếp Anthropic API)"
        return 0
    fi

    export ANTHROPIC_BASE_URL="http://localhost:20128/api/v1"
    export ANTHROPIC_API_KEY="sk-9router"
    PULU_ACTIVE_GW_LABEL="9Router (:20128)"
    echo "⚡ Gateway: 9Router (:20128 - Terminal Siêu Tốc < 1ms)"
}

smart_claude() {
    local prompt="$*"
    if [[ -z "$prompt" ]]; then
        echo "⚠️ Vui lòng nhập nội dung. Ví dụ: ai phân tích hệ thống..."
        return 1
    fi
    
    local lower_prompt=$(echo "$prompt" | awk '{print tolower($0)}')
    local model="cc/claude-sonnet-4-6" # Mặc định là Sonnet
    local task_label="SONNET 4.6 (Max Coding)"

    # 1. Phân nhóm Opus / Brain Code Combo
    if [[ "$lower_prompt" =~ (phân tích|chiến lược|kế hoạch|logic|kiến trúc|hệ thống|quy hoạch|tư duy|chiều sâu|đánh đổi|trade-off|p\&l|sla|nguyên nhân gốc rễ|root cause|insight|quyết định|decision|rủi ro|fraud|cung cầu|supply|demand|tâm lý|hành vi) ]]; then
        model="cc/claude-opus-4-8"
        task_label="COMBO: PULU-BRAIN-CODE (Opus 4.8 + Sonnet 4.6 + DeepSeek)"
        
    # 2. Phân nhóm Data / Log / Context Combo
    elif [[ "$lower_prompt" =~ (dịch thuật|dịch|thông báo|tài xế|zalo|email|chính tả|ngữ pháp|viết lại|caption|kịch bản|nội dung|tóm tắt|đọc file|log) ]]; then
        model="gc/gemini-3.7-pro"
        task_label="COMBO: PULU-DATA-LOG (Gemini 3.7 Pro + Sonnet 4.6 + DeepSeek)"
        
    # 3. Phân nhóm Hỏi nhanh CLI Combo
    elif [[ "$lower_prompt" =~ (hỏi nhanh|giải thích|tính toán|định nghĩa|là gì|như thế nào|thế nào|regex) ]]; then
        model="cc/claude-sonnet-4-6"
        task_label="COMBO: PULU-FAST-CLI (DeepSeek V3/R1 + Sonnet 4.6)"

    # 4. Phân nhóm Sonnet Code
    elif [[ "$lower_prompt" =~ (trình bày|code|lập trình|html|css|giao diện|ui|ux|lark|docs|báo cáo|định dạng|table|bảng|markdown|website|landing page|sql|git|docker|k8s) ]]; then
        model="cc/claude-sonnet-4-6"
        task_label="SONNET 4.6 (Max Coding)"
    fi

    # Tự động chọn Gateway tối ưu
    _auto_detect_gateway "$prompt" "$lower_prompt" > /dev/null

    local start_ts=$(python3 -c "import time; print(time.time())")

    # Gọi Claude Code bằng UI gốc
    claude --model "$model" -p "$prompt"
}
alias ai="smart_claude"

# === SMART CHAT (TTY Interactive Mode & Auto-Detect Engine) ===
smart_chat() {
    local danger_mode=false
    local prompt=""

    if [[ "$1" == "!" ]]; then
        danger_mode=true
        shift
        prompt="$*"
    else
        prompt="$*"
    fi

    local claude_flags=()
    if [[ "$danger_mode" == true ]]; then
        claude_flags+=("--dangerously-skip-permissions")
    fi

    local lower_prompt=$(echo "$prompt" | awk '{print tolower($0)}')
    local model="cc/claude-sonnet-4-6" # Mặc định

    if [[ "$lower_prompt" =~ (phân tích|chiến lược|kế hoạch|logic|kiến trúc|hệ thống|quy hoạch|tư duy|chiều sâu|đánh đổi|trade-off|p\&l|sla|nguyên nhân gốc rễ|root cause|insight|quyết định|decision|rủi ro|fraud|cung cầu|supply|demand|tâm lý|hành vi) ]]; then
        model="cc/claude-opus-4-8"
    elif [[ "$lower_prompt" =~ (dịch thuật|dịch|thông báo|tài xế|zalo|email|chính tả|ngữ pháp|viết lại|caption|kịch bản|nội dung|tóm tắt|đọc file|log) ]]; then
        model="cc/claude-sonnet-4-6"
    elif [[ "$lower_prompt" =~ (hỏi nhanh|giải thích|tính toán|định nghĩa|là gì|như thế nào|thế nào|regex) ]]; then
        model="cc/claude-sonnet-4-6"
    elif [[ "$lower_prompt" =~ (trình bày|code|lập trình|html|css|giao diện|ui|ux|lark|docs|báo cáo|định dạng|table|bảng|markdown|website|landing page|sql|git|docker|k8s) ]]; then
        model="cc/claude-sonnet-4-6"
    fi

    _auto_detect_gateway "$prompt" "$lower_prompt" > /dev/null

    # Nếu có truyền câu hỏi trực tiếp:
    if [[ -n "$prompt" ]]; then
        claude "${claude_flags[@]}" --model "$model" --continue -p "$prompt"
    else
        # Mở trực tiếp Giao diện TTY gốc của Claude CLI (Chế độ tương tác REPL)
        claude "${claude_flags[@]}" --model "$model"
    fi
}
alias chat="smart_chat"
alias "chat!"="smart_chat !"

# === Gateway Switcher Wrappers (Thủ công hoặc Tự động) ===
use_9router() {
    export ANTHROPIC_BASE_URL="http://localhost:20128/api/v1"
    export ANTHROPIC_API_KEY="sk-9router"
    export PULU_GATEWAY_OVERRIDE="9router"
    echo -e "✅ Claude đã cố định trỏ về 9Router (localhost:20128)"
}
alias use-9router="use_9router"

use_direct() {
    unset ANTHROPIC_BASE_URL
    export PULU_GATEWAY_OVERRIDE="direct"
    echo -e "⚡ Claude đã chuyển sang chế độ TRỰC TIẾP (Bỏ qua 9Router Proxy)"
}
alias use-direct="use_direct"

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
echo "🚀 PuluSmartFlow v3.5 Auto-Detect Engine Loaded | Auto Model Enabled"
