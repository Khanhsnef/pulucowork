#!/bin/bash
# sync-push.sh — Chạy trên máy VĂN PHÒNG
# Đẩy Claude Code config lên Google Drive để dùng ở nhà

DRIVE="$HOME/Library/CloudStorage/GoogleDrive-lephuongkhanh1995@gmail.com/My Drive/Cowork"
DEST="$DRIVE/.claude-config"
SOURCE="$HOME/.claude"

echo "📦 Đang backup Claude config lên Drive..."

mkdir -p "$DEST"

# Sync các folder quan trọng (bỏ qua cache, sessions, telemetry)
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
echo "✅ Xong! Config đã được đẩy lên Drive tại:"
echo "   $DEST"
echo ""
echo "⏳ Chờ Google Drive sync xong (~30 giây) rồi mới chạy sync-pull.sh ở nhà."
