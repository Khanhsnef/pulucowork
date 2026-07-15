#!/usr/bin/env bash
# ── Trading Analysis System — macOS/Linux launcher ──
cd "$(dirname "$0")"

if [ ! -f ".venv/bin/python" ]; then
    echo "[Setup] Tạo virtual env + cài dependencies (chỉ lần đầu)..."
    python3 -m venv .venv
    .venv/bin/python -m pip install --upgrade pip -q
    .venv/bin/python -m pip install -r requirements.txt
fi

echo ""
echo "🌐 Trading Analysis System → http://127.0.0.1:8899"
echo "   Ctrl+C để tắt server."
echo ""
(sleep 1.5 && open "http://127.0.0.1:8899" 2>/dev/null) &
.venv/bin/python -m trading_system.server
