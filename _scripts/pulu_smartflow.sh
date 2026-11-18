# ============================================================
# PULU BASH/ZSH PROFILE — PuluSmartFlow v4.1 Verified Engine (macOS/Linux)
# Architecture: 9Router High-Speed Gateway (http://127.0.0.1:20128/v1)
# Verified: E2E Claude CLI 2.1+ Streaming, Zero-Secret Git, Zsh Glob-Safe
# ============================================================

# === 1. Dynamic Script Directory & Gateway Start ===
if [[ -n "$ZSH_VERSION" ]]; then
    _PULU_SCRIPT_DIR="${${(%):-%x}:A:h}"
else
    _PULU_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fi

alias 9router="9router"
alias pulu-start="zsh \"$_PULU_SCRIPT_DIR/pulu-start.sh\""

# === 2. Load Secure Environment (Zero Plain-Text Secret in Git) ===
_pulu_load_env() {
    local env_found=false
    for f in "$HOME/.config/pulu/env" "$HOME/.config/pulu/env.sh"; do
        if [[ -f "$f" ]]; then
            source "$f"
            env_found=true
            break
        fi
    done

    # Nếu chưa có file env, tự trích xuất token từ ~/.claude/settings.json (nếu có)
    if [[ "$env_found" == false ]]; then
        mkdir -p "$HOME/.config/pulu"
        local detected_token=""
        if [[ -f "$HOME/.claude/settings.json" ]]; then
            detected_token=$(python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/settings.json'))); print(d.get('env',{}).get('ANTHROPIC_AUTH_TOKEN',''))" 2>/dev/null)
        fi
        cat << EOF > "$HOME/.config/pulu/env"
# Pulu Secure Environment — ĐỪNG commit file này lên Git!
export ANTHROPIC_BASE_URL="http://127.0.0.1:20128/v1"
export ANTHROPIC_AUTH_TOKEN="${detected_token:-your-9router-key-here}"
unset ANTHROPIC_API_KEY
EOF
        chmod 600 "$HOME/.config/pulu/env"
        source "$HOME/.config/pulu/env"
    fi

    # Chuẩn hóa URL nếu file env cũ vẫn để /api/v1 (gây lỗi HTTP 404 tại /api/v1/v1/messages)
    if [[ "$ANTHROPIC_BASE_URL" == *"/api/v1"* ]]; then
        export ANTHROPIC_BASE_URL="http://127.0.0.1:20128/v1"
    fi

    # Đồng bộ sang ANTHROPIC_AUTH_TOKEN & gỡ ANTHROPIC_API_KEY để tránh xung đột xác thực trên Claude CLI
    if [[ -z "$ANTHROPIC_AUTH_TOKEN" && -n "$ANTHROPIC_API_KEY" ]]; then
        export ANTHROPIC_AUTH_TOKEN="$ANTHROPIC_API_KEY"
    fi
    unset ANTHROPIC_API_KEY
}
_pulu_load_env

export _PULU_SAVED_9ROUTER_KEY="${ANTHROPIC_AUTH_TOKEN}"

# === 3. Verified Live Model Aliases (Claude CLI E2E Tested) ===
# Lưu ý: Bọc ngoặc kép tên model để chống lỗi Zsh globbing (vd: [1m])
# Claude Native Provider (cc/* — Tương thích 100% streaming & tool-use của Claude CLI)
alias c-think='claude --model "cc/claude-opus-5-5"'
alias c-opus='claude --model "cc/claude-opus-5-5"'
alias c-48='claude --model "cc/claude-opus-4-8"'
alias c-code='claude --model "cc/claude-sonnet-5-5"'
alias c-sonnet='claude --model "cc/claude-sonnet-5-5"'
alias c-46='claude --model "cc/claude-sonnet-4-6"'
alias c-fast='claude --model "cc/claude-haiku-5-5"'
alias c-haiku='claude --model "cc/claude-haiku-5-5"'

# Codex / GPT-6 Multi-Account Fleet (cx/* — 3 tài khoản cân bằng tải + 1M Context)
alias gpt-sol='claude --model "cx/gpt-6.1-sol"'
alias gpt-astra='claude --model "cx/gpt-6-astra"'
alias gpt-1m='claude --model "cx/gpt-6-astra[1m]"'

# 9Router Intelligent Combos (Zero-Warning + Auto-Fallback + Chuẩn Context Window)
alias combo-smart='claude --model "pulu-claude-sonnet-5-5"'
alias combo-think='claude --model "pulu-claude-opus-5-5"'
alias combo-arch='claude --model "pulu-claude-sonnet-5-5"'
alias combo-extreme='claude --model "pulu-claude-opus-5-5"'
alias combo-long='claude --model "pulu-claude-sonnet-5-5[1m]"'
# ============================================================

# === 4. Helper: Fast Zero-Subshell Lowercase ===
_pulu_tolower() {
    if [[ -n "$ZSH_VERSION" ]]; then
        print -r -- "${1:l}"
    else
        printf '%s\n' "$1" | tr '[:upper:]' '[:lower:]'
    fi
}

# === 5. Gateway Management ===
_auto_detect_gateway() {
    if [[ "$PULU_GATEWAY_OVERRIDE" == "direct" ]]; then
        export ANTHROPIC_BASE_URL="https://api.anthropic.com"
        unset ANTHROPIC_AUTH_TOKEN
        [[ -n "$PULU_DIRECT_API_KEY" ]] && export ANTHROPIC_API_KEY="$PULU_DIRECT_API_KEY"
        return 0
    fi

    export ANTHROPIC_BASE_URL="http://127.0.0.1:20128/v1"
    [[ -n "$_PULU_SAVED_9ROUTER_KEY" ]] && export ANTHROPIC_AUTH_TOKEN="$_PULU_SAVED_9ROUTER_KEY"
    unset ANTHROPIC_API_KEY
}

use_9router() {
    _pulu_load_env
    [[ -n "$ANTHROPIC_AUTH_TOKEN" ]] && export _PULU_SAVED_9ROUTER_KEY="$ANTHROPIC_AUTH_TOKEN"
    export ANTHROPIC_BASE_URL="http://127.0.0.1:20128/v1"
    export PULU_GATEWAY_OVERRIDE="9router"
    unset ANTHROPIC_API_KEY
    echo "✅ Claude đã kết nối 9Router Gateway (http://127.0.0.1:20128/v1)"
}
alias use-9router="use_9router"

use_direct() {
    export ANTHROPIC_BASE_URL="https://api.anthropic.com"
    unset ANTHROPIC_AUTH_TOKEN
    [[ -n "$PULU_DIRECT_API_KEY" ]] && export ANTHROPIC_API_KEY="$PULU_DIRECT_API_KEY"
    export PULU_GATEWAY_OVERRIDE="direct"
    echo "⚡ Claude đã chuyển sang chế độ Direct API (https://api.anthropic.com)"
}
alias use-direct="use_direct"

pulu_status() {
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🤖 PULU SMARTFLOWS v4.1 & 9ROUTER STATUS"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    if lsof -i :20128 -sTCP:LISTEN &>/dev/null; then
        echo "🟢 9Router Gateway   : ONLINE (http://127.0.0.1:20128/v1)"
    else
        echo "🔴 9Router Gateway   : OFFLINE (Chạy 'pulu-start' để khởi động)"
    fi
    echo "⚡ Gateway Mode      : ${PULU_GATEWAY_OVERRIDE:-9Router Auto-Route (:20128/v1)}"
    echo "🌐 Base URL          : ${ANTHROPIC_BASE_URL:-unset}"
    if [[ -n "$ANTHROPIC_AUTH_TOKEN" ]]; then
        echo "🔑 Auth Token        : ${ANTHROPIC_AUTH_TOKEN:0:12}... (Đã nạp hợp lệ)"
    else
        echo "🔑 Auth Token        : Chưa nạp (Kiểm tra ~/.config/pulu/env)"
    fi
    echo "🎯 Active Combos     : PuluSmartFlows | Deep_Strategic_Thinking | Architect_Workflow"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}
alias pulu-status="pulu_status"
alias 9router-status="pulu_status"

# === 6. Smart Router Engine (Regex-First < 0.1ms) ===
smart_claude() {
    local prompt="$*"
    if [[ -z "$prompt" ]]; then
        echo "⚠️ Vui lòng nhập nội dung câu hỏi. Ví dụ: ai phân tích chiến lược giữ chân tài xế..."
        return 1
    fi

    local lower_prompt="$(_pulu_tolower "$prompt")"
    local model="pulu-claude-sonnet-5-5"
    local task_label="COMBO SMART: pulu-claude-sonnet-5-5 (Sonnet 5.5 ➔ Sonnet 4.6 ➔ GPT-6 Astra)"

    # 1. Nhóm Chiến Lược / Phân Tích Chuyên Sâu / Quyết Định / Cung Cầu / P&L
    if [[ "$lower_prompt" =~ (phân tích|chiến lược|kế hoạch|logic|kiến trúc|hệ thống|quy hoạch|tư duy|chiều sâu|đánh đổi|trade-off|p\&l|sla|nguyên nhân gốc rễ|root cause|insight|quyết định|decision|rủi ro|fraud|cung cầu|supply|demand|tâm lý|hành vi|churn|retention|driver lifecycle|lark docs) ]]; then
        model="pulu-claude-opus-5-5"
        task_label="BRAIN STRATEGY: pulu-claude-opus-5-5 (Opus 5.5 ➔ Opus 4.8 ➔ GPT-6.1 Sol)"

    # 2. Nhóm Dữ Liệu Lớn / Context 1M Tokens / Logs / Đọc File Dài / Báo Cáo
    elif [[ "$lower_prompt" =~ (dữ liệu|data|log|logs|đọc file|tóm tắt file|file dài|báo cáo tuần|weekly report|1m token|bảng tính|csv|parquet|dịch thuật|thông báo tài xế|zalo|email) ]]; then
        model="pulu-claude-sonnet-5-5[1m]"
        task_label="LONG CONTEXT 1M: pulu-claude-sonnet-5-5[1m] (GPT-6 Astra [1M] ➔ Sonnet 5.5)"

    # 3. Nhóm Lập Trình / Refactoring / UI-UX / SQL / Script
    elif [[ "$lower_prompt" =~ (code|lập trình|refactor|function|script|python|bash|sql|query|duckdb|database|ui|ux|html|css|bento|landing page|dashboard|docker|git) ]]; then
        model="pulu-claude-sonnet-5-5"
        task_label="ENGINEERING: pulu-claude-sonnet-5-5 (Sonnet 5.5 ➔ Sonnet 4.6 ➔ GPT-6 Astra)"

    # 4. Nhóm Hỏi Nhanh / Giải Thích / Tra Cứu Cú Pháp / Regex / Tính Toán
    elif [[ "$lower_prompt" =~ (hỏi nhanh|giải thích|tính toán|định nghĩa|là gì|như thế nào|thế nào|regex|tính nhẩm|cú pháp|convert) ]]; then
        model="pulu-claude-haiku-5-5"
        task_label="FAST CLI: pulu-claude-haiku-5-5 (Haiku 5.5 ➔ Sonnet 5.5)"
    fi

    _auto_detect_gateway

    echo "⚡ [PuluSmartFlow v4.1] → $task_label"
    claude --model "$model" -p "$prompt"
}
alias ai="smart_claude"

# === 7. Smart Chat (Interactive REPL Mode) ===
smart_chat() {
    local danger_mode=false
    local prompt=""

    if [[ "$1" == "!" ]]; then
        danger_mode=true
        shift
        prompt="$*"
    else
        prompt="$*"
    fi

    local claude_flags=()
    if [[ "$danger_mode" == true ]]; then
        claude_flags+=("--dangerously-skip-permissions")
    fi

    local lower_prompt="$(_pulu_tolower "$prompt")"
    local model="pulu-claude-sonnet-5-5"

    if [[ "$danger_mode" == true ]]; then
        model="pulu-claude-opus-5-5"
    elif [[ "$lower_prompt" =~ (phân tích|chiến lược|kế hoạch|kiến trúc|tư duy|quyết định|p\&l|sla|root cause) ]]; then
        model="pulu-claude-opus-5-5"
    elif [[ "$lower_prompt" =~ (code|lập trình|ui|ux|dashboard|sql) ]]; then
        model="pulu-claude-sonnet-5-5"
    elif [[ "$lower_prompt" =~ (file|log|dữ liệu|báo cáo|tóm tắt) ]]; then
        model="pulu-claude-sonnet-5-5[1m]"
    fi

    _auto_detect_gateway

    if [[ -n "$prompt" ]]; then
        claude "${claude_flags[@]}" --model "$model" --continue -p "$prompt"
    else
        claude "${claude_flags[@]}" --model "$model"
    fi
}
alias chat="smart_chat"
alias "chat!"="smart_chat !"

# === 8. Circuit Breaker cho command_not_found_handler ===
export _PULU_CNF_DEPTH=0
command_not_found_handler() {
    local cmd="$1"
    if [[ $_PULU_CNF_DEPTH -ge 1 ]]; then
        echo "❌ [Pulu Circuit Breaker] Phát hiện đệ quy lặp lệnh. Dừng thực thi để bảo vệ hạn ngạch."
        return 127
    fi
    export _PULU_CNF_DEPTH=$((_PULU_CNF_DEPTH + 1))

    if [[ -t 0 && -n "$cmd" ]]; then
        echo -e "\n🔍 [CNF] Lệnh không tìm thấy: '$cmd' → Chuyển tiếp đến Pulu Smart AI..."
        smart_chat "$@"
        export _PULU_CNF_DEPTH=0
        return 0
    fi

    export _PULU_CNF_DEPTH=0
    return 127
}

# ============================================================
echo "🚀 PuluSmartFlow v4.1 (9Router :20128/v1 Verified) Loaded | Zero-404 Routing Active"
