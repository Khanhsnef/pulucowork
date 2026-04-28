#!/bin/bash
# sync-pull.sh — Chạy trên máy Ở NHÀ
# Kéo Claude Code config từ Google Drive về máy

# Tự động tìm đường dẫn Google Drive (dùng account nào cũng được)
DRIVE_BASE="$HOME/Library/CloudStorage"
DRIVE=$(find "$DRIVE_BASE" -maxdepth 1 -name "GoogleDrive-*" | head -1)

if [ -z "$DRIVE" ]; then
  echo "❌ Không tìm thấy Google Drive. Hãy cài Google Drive for Desktop trước."
  exit 1
fi

SOURCE="$DRIVE/My Drive/Cowork/.claude-config"
DEST="$HOME/.claude"

if [ ! -d "$SOURCE" ]; then
  echo "❌ Chưa có config trên Drive. Hãy chạy sync-push.sh ở văn phòng trước."
  exit 1
fi

echo "📥 Đang kéo Claude config từ Drive về máy..."
echo "   Nguồn : $SOURCE"
echo "   Đích  : $DEST"
echo ""

# Backup config hiện tại (nếu có)
if [ -d "$DEST" ]; then
  BACKUP="$HOME/.claude-backup-$(date +%Y%m%d-%H%M)"
  echo "💾 Backup config cũ vào $BACKUP"
  cp -r "$DEST" "$BACKUP"
fi

mkdir -p "$DEST"

rsync -av --delete \
  --exclude='cache/' \
  --exclude='sessions/' \
  --exclude='downloads/' \
  --exclude='backups/' \
  --exclude='telemetry/' \
  --exclude='shell-snapshots/' \
  --exclude='session-env/' \
  --exclude='ide/' \
  "$SOURCE/" "$DEST/"

echo ""
echo "✅ Xong! Claude Code trên máy này đã có đầy đủ:"
echo "   - Memory & context từ văn phòng"
echo "   - Settings, skills, plans"
echo ""
echo "👉 Mở Claude Code và trỏ vào folder:"
echo "   $DRIVE/My Drive/Cowork"
