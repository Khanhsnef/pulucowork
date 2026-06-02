#!/bin/bash
# github-auto-sync.sh — Chạy ngầm để tự động push code lên Github

PROJECT_DIR="/Users/ts-1148/Desktop/Cowork"
cd "$PROJECT_DIR" || exit 1

echo "======================================"
echo "🔄 Bắt đầu kiểm tra Github Sync lúc $(date '+%Y-%m-%d %H:%M:%S')"

# Kiểm tra xem có thay đổi nào không
if [ -z "$(git status --porcelain)" ]; then
  echo "✅ Không có thay đổi nào mới. Bỏ qua."
else
  echo "📦 Phát hiện thay đổi. Đang commit và push..."
  
  # Add tất cả thay đổi
  git add .
  
  # Commit với timestamp
  git commit -m "chore(auto): auto-sync workspace lúc $(date '+%Y-%m-%d %H:%M:%S')"
  
  # Push lên remote
  if git push; then
    echo "✅ Push thành công!"
  else
    echo "❌ Lỗi khi push! Vui lòng kiểm tra lại kết nối mạng hoặc conflict."
  fi
fi

echo "======================================"
echo ""
