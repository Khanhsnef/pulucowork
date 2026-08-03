#!/usr/bin/env zsh
# pulu-start.sh — Khởi động toàn bộ Pulu Gateway Stack cùng lúc

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║       🚀 PULU GATEWAY STACK — KHỞI ĐỘNG HỆ THỐNG      ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Kiểm tra trạng thái trước khi khởi động
check_port() {
    lsof -i ":$1" -sTCP:LISTEN &>/dev/null
}

# ─── 9Router (:20128) ─────────────────────────────────────────
if check_port 20128; then
    echo "  🟢  9Router     :20128   [ĐANG CHẠY — bỏ qua]"
else
    echo "  🔵  9Router     :20128   [Đang khởi động...]"
    omniroute serve --port 20128 --daemon --no-open &>/dev/null
    sleep 1
    if check_port 20128; then
        echo "  ✅  9Router     :20128   [ONLINE]"
    else
        echo "  ❌  9Router     :20128   [THẤT BẠI — kiểm tra log]"
    fi
fi

# ─── OmniRoute (:20130) ───────────────────────────────────────
if check_port 20130; then
    echo "  🟢  OmniRoute   :20130   [ĐANG CHẠY — bỏ qua]"
else
    echo "  🔵  OmniRoute   :20130   [Đang khởi động...]"
    omniroute serve --port 20130 --daemon --no-open &>/dev/null
    sleep 1
    if check_port 20130; then
        echo "  ✅  OmniRoute   :20130   [ONLINE]"
    else
        echo "  ❌  OmniRoute   :20130   [THẤT BẠI — kiểm tra log]"
    fi
fi

echo ""
echo "────────────────────────────────────────────────────────"
echo "  9Router     →  http://localhost:20128"
echo "  OmniRoute   →  http://localhost:20130"
echo "────────────────────────────────────────────────────────"
echo ""
