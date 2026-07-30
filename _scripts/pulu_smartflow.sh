# ============================================================
# PULU BASH/ZSH PROFILE — PuluSmartFlow v2.0 (macOS/Linux)
# Logic: Regex route trước (<1ms), KHÔNG gọi HTTP AI classifier
# ============================================================

# === Start local 9router AI Proxy ===
alias 9router="9router"

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

# === Claude Aliases for 9Router ===
alias c-think="claude --model cc/claude-opus-4-8"
alias c-code="claude --model cc/claude-sonnet-4-6"
alias c-fast="claude --model oc/deepseek-v4-flash"
# ============================================

# === SMART AI ROUTER (Keyword-based v2) ===
smart_claude() {
    local prompt="$*"
    if [[ -z "$prompt" ]]; then
        echo "⚠️ Vui lòng nhập nội dung. Ví dụ: ai phân tích hệ thống..."
        return 1
    fi
    
    # Chuyển về chữ thường để kiểm tra từ khóa
    local lower_prompt=$(echo "$prompt" | awk '{print tolower($0)}')
    local model="cc/claude-sonnet-4-6" # Mặc định là Sonnet

    # 1. Phân nhóm Opus (The Brain - Tư duy sâu, chiến lược, phân tích phức tạp)
    if [[ "$lower_prompt" =~ (phân tích|chiến lược|kế hoạch|logic|kiến trúc|hệ thống|quy hoạch|tư duy|chiều sâu|đánh đổi|trade-off|p\&l|sla|nguyên nhân gốc rễ|root cause|insight|quyết định|decision|rủi ro|fraud|cung cầu|supply|demand|tâm lý|hành vi) ]]; then
        model="cc/claude-opus-4-8"
        echo -e "\n🧠 [Smart Router] Nhận diện Task Tư Duy Sâu -> 🚀 Đang bật OPUS 4.8 (Max Logic)..."
        
    # 2. Phân nhóm Gemini Pro (The Communicator / Context - Giao tiếp, đọc/xử lý văn bản lớn, thông báo Zalo, dịch thuật)
    elif [[ "$lower_prompt" =~ (dịch thuật|dịch|thông báo|tài xế|zalo|email|chính tả|ngữ pháp|viết lại|caption|kịch bản|nội dung|tóm tắt|đọc file|log) ]]; then
        model="gc/gemini-3.1-pro-preview"
        echo -e "\n⚡ [Smart Router] Nhận diện Task Ngôn Ngữ / Data -> 🚀 Đang bật GEMINI 3.1 PRO (Max Context)..."
        
    # 3. Phân nhóm DeepSeek Flash (The Sprinter - Việc vặt, hỏi đáp siêu nhanh, tính toán nhẹ)
    elif [[ "$lower_prompt" =~ (hỏi nhanh|giải thích|tính toán|định nghĩa|là gì|như thế nào|thế nào|regex) ]]; then
        model="oc/deepseek-v4-flash"
        echo -e "\n💨 [Smart Router] Nhận diện Task Nhanh -> 🚀 Đang bật DEEPSEEK V4 FLASH (Siêu Tốc)..."

    # 4. Phân nhóm Sonnet (The Coder / Formatter - Trình bày, Code, Giao diện)
    elif [[ "$lower_prompt" =~ (trình bày|code|lập trình|html|css|giao diện|ui|ux|lark|docs|báo cáo|định dạng|table|bảng|markdown|website|landing page|sql|git|docker|k8s) ]]; then
        model="cc/claude-sonnet-4-6"
        echo -e "\n💻 [Smart Router] Nhận diện Task Code/Format -> 🚀 Đang bật SONNET 4.6 (Max Coding)..."
        
    # 5. Mặc định
    else
        echo -e "\n🤖 [Smart Router] Task chung chung -> 🚀 Kích hoạt SONNET 4.6 (Mặc định)..."
    fi

    # Gọi Claude Code
    claude --model "$model" -p "$prompt"
}
alias ai="smart_claude"

# === SMART CHAT (TTY Interactive Mode) ===
smart_chat() {
    local prompt="$*"
    local lower_prompt=$(echo "$prompt" | awk '{print tolower($0)}')
    local model="cc/claude-sonnet-4-6" # Mặc định

    if [[ "$lower_prompt" =~ (phân tích|chiến lược|kế hoạch|logic|kiến trúc|hệ thống|quy hoạch|tư duy|chiều sâu|đánh đổi|trade-off|p\&l|sla|nguyên nhân gốc rễ|root cause|insight|quyết định|decision|rủi ro|fraud|cung cầu|supply|demand|tâm lý|hành vi) ]]; then
        model="cc/claude-opus-4-8"
        echo -e "\n🧠 [Smart Router] Task Tư Duy Sâu -> 🚀 Đang bật OPUS 4.8 (Max Logic)..."
    elif [[ "$lower_prompt" =~ (dịch thuật|dịch|thông báo|tài xế|zalo|email|chính tả|ngữ pháp|viết lại|caption|kịch bản|nội dung|tóm tắt|đọc file|log) ]]; then
        model="gc/gemini-3.1-pro-preview"
        echo -e "\n⚡ [Smart Router] Task Ngôn Ngữ / Data -> 🚀 Đang bật GEMINI 3.1 PRO (Max Context)..."
    elif [[ "$lower_prompt" =~ (hỏi nhanh|giải thích|tính toán|định nghĩa|là gì|như thế nào|thế nào|regex) ]]; then
        model="oc/deepseek-v4-flash"
        echo -e "\n💨 [Smart Router] Nhận diện Task Nhanh -> 🚀 Đang bật DEEPSEEK V4 FLASH (Siêu Tốc)..."
    elif [[ "$lower_prompt" =~ (trình bày|code|lập trình|html|css|giao diện|ui|ux|lark|docs|báo cáo|định dạng|table|bảng|markdown|website|landing page|sql|git|docker|k8s) ]]; then
        model="cc/claude-sonnet-4-6"
        echo -e "\n💻 [Smart Router] Nhận diện Task Code/Format -> 🚀 Đang bật SONNET 4.6 (Max Coding)..."
    else
        echo -e "\n🤖 [Smart Router] Task chung chung -> 🚀 Kích hoạt SONNET 4.6 (Mặc định)..."
    fi

    # Tương tác đầy đủ (TTY) - KHÔNG có -p flag trừ khi được chuyển tiếp bằng cờ --continue
    if [[ -n "$prompt" ]]; then
        claude --model "$model" --continue -p "$prompt"
    else
        claude --model "$model"
    fi
}
alias chat="smart_chat"

# === Use 9Router Endpoint wrapper ===
use_9router() {
    export ANTHROPIC_BASE_URL="http://localhost:20128/api/v1"
    echo -e "✅ Claude đã trỏ về 9router (localhost:20128)"
}
alias use-9router="use_9router"

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
echo "🚀 PuluSmartFlow loaded | Aliases: chat, ai, c-think, c-code, c-fast, use-9router, 9router"
