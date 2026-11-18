#!/bin/bash
# Cài đặt Smart Claude Router (macOS/Linux)
# Tự động dò đường dẫn thực tế của workspace

echo "📦 Đang cài đặt Smart AI Router vào ~/.zshrc..."

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SMART_FLOW_SCRIPT="$SCRIPT_DIR/pulu_smartflow.sh"

if grep -q "pulu_smartflow.sh" ~/.zshrc 2>/dev/null; then
    echo "✅ Cấu hình Smart Router đã tồn tại trong ~/.zshrc. Bỏ qua."
else
    cat >> ~/.zshrc << EOF

# === SMART AI ROUTER (PuluSmartFlow) ===
if [ -f "$SMART_FLOW_SCRIPT" ]; then
    source "$SMART_FLOW_SCRIPT"
elif [ -f "\$HOME/Desktop/Pulu-workspace/_scripts/pulu_smartflow.sh" ]; then
    source "\$HOME/Desktop/Pulu-workspace/_scripts/pulu_smartflow.sh"
elif [ -f "\$HOME/pulucowork/_scripts/pulu_smartflow.sh" ]; then
    source "\$HOME/pulucowork/_scripts/pulu_smartflow.sh"
fi
# ============================================
EOF
    echo "✅ Đã thêm Smart Router vào ~/.zshrc ($SMART_FLOW_SCRIPT)"
fi

echo "🎉 Hãy chạy 'source ~/.zshrc' để cập nhật."
