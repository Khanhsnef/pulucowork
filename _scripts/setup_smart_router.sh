#!/bin/bash
# Backup cấu hình 9Router và Smart Claude Router

echo "📦 Đang cài đặt Smart AI Router vào ~/.zshrc..."

# Kiểm tra xem cấu hình đã tồn tại chưa
if grep -q "SMART AI ROUTER" ~/.zshrc; then
    echo "✅ Cấu hình Smart Router đã tồn tại trong ~/.zshrc. Bỏ qua."
else
    cat >> ~/.zshrc << 'EOF'

# === Claude Aliases for 9Router ===
alias c-think="claude --model cc/claude-opus-4-7"
alias c-code="claude --model cc/claude-sonnet-4-6"
alias c-fast="claude --model oc/deepseek-v4-flash-free"
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
        model="cc/claude-opus-4-7"
        echo -e "\n🧠 [Smart Router] Nhận diện Task Tư Duy Sâu -> 🚀 Đang bật OPUS (Max Logic)..."
        
    # 2. Phân nhóm Gemini Pro (The Communicator / Context - Giao tiếp, đọc/xử lý văn bản lớn, thông báo Zalo, dịch thuật)
    elif [[ "$lower_prompt" =~ (dịch thuật|dịch|thông báo|tài xế|zalo|email|chính tả|ngữ pháp|viết lại|caption|kịch bản|nội dung|tóm tắt|đọc file|log) ]]; then
        model="gc/gemini-3-pro-preview"
        echo -e "\n⚡ [Smart Router] Nhận diện Task Ngôn Ngữ / Data -> 🚀 Đang bật GEMINI PRO (Max Context)..."
        
    # 3. Phân nhóm DeepSeek Flash (The Sprinter - Việc vặt, hỏi đáp siêu nhanh, tính toán nhẹ)
    elif [[ "$lower_prompt" =~ (hỏi nhanh|giải thích|tính toán|định nghĩa|là gì|như thế nào|thế nào|regex) ]]; then
        model="oc/deepseek-v4-flash-free"
        echo -e "\n💨 [Smart Router] Nhận diện Task Nhanh -> 🚀 Đang bật DEEPSEEK FLASH (Siêu Tốc)..."

    # 4. Phân nhóm Sonnet (The Coder / Formatter - Trình bày, Code, Giao diện)
    elif [[ "$lower_prompt" =~ (trình bày|code|lập trình|html|css|giao diện|ui|ux|lark|docs|báo cáo|định dạng|table|bảng|markdown|website|landing page) ]]; then
        model="cc/claude-sonnet-4-6"
        echo -e "\n💻 [Smart Router] Nhận diện Task Code/Format -> 🚀 Đang bật SONNET (Max Coding)..."
        
    # 5. Mặc định
    else
        echo -e "\n🤖 [Smart Router] Task chung chung -> 🚀 Kích hoạt SONNET (Mặc định)..."
    fi

    # Gọi Claude Code
    claude --model "$model" -p "$prompt"
}
alias ai="smart_claude"
# ============================================
EOF
    echo "✅ Đã thêm Smart Router vào ~/.zshrc"
fi

echo "🎉 Hãy chạy 'source ~/.zshrc' để cập nhật."
