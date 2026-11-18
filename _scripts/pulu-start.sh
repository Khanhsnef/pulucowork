#!/usr/bin/env zsh
# pulu-start.sh — Khởi động hệ thống Pulu Gateway Stack (9Router :20128 Local-Only)

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║       🚀 PULU GATEWAY STACK — KHỞI ĐỘNG HỆ THỐNG      ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

check_port() {
    lsof -i ":$1" -sTCP:LISTEN &>/dev/null
}

# ─── 9Router (:20128 — Bind 127.0.0.1 chống lộ cổng ra mạng LAN) ─────
if check_port 20128; then
    echo "  🟢  9Router     :20128   [ĐANG CHẠY — bỏ qua]"
else
    echo "  🔵  9Router     :20128   [Đang khởi động chế độ Local-Only...]"
    nohup 9router -H 127.0.0.1 -p 20128 -n -t &>/dev/null &
    sleep 2
    if check_port 20128; then
        echo "  ✅  9Router     :20128   [ONLINE — Bound 127.0.0.1]"
    else
        echo "  ❌  9Router     :20128   [THẤT BẠI — kiểm tra log ~/.9router/daemon.log]"
    fi
fi

echo ""
echo "────────────────────────────────────────────────────────"
echo "  9Router Dashboard →  http://127.0.0.1:20128"
echo "  Claude Base URL   →  http://127.0.0.1:20128/v1"
echo "────────────────────────────────────────────────────────"
echo ""
