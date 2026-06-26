#!/bin/bash
# Cài đặt Smart Claude Router (macOS/Linux)
# Source từ kho pulucowork để đồng bộ đa nền tảng

echo "📦 Đang cài đặt Smart AI Router vào ~/.zshrc..."

SMART_FLOW_SCRIPT="$HOME/pulucowork/_scripts/pulu_smartflow.sh"

if grep -q "pulu_smartflow.sh" ~/.zshrc; then
    echo "✅ Cấu hình Smart Router đã tồn tại trong ~/.zshrc. Bỏ qua."
else
    cat >> ~/.zshrc << EOF

# === SMART AI ROUTER (PuluSmartFlow) ===
if [ -f "$SMART_FLOW_SCRIPT" ]; then
    source "$SMART_FLOW_SCRIPT"
else
    echo "⚠️ PuluSmartFlow script not found at $SMART_FLOW_SCRIPT"
fi
# ============================================
EOF
    echo "✅ Đã thêm Smart Router vào ~/.zshrc"
fi

echo "🎉 Hãy chạy 'source ~/.zshrc' để cập nhật."
