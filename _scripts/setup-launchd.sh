#!/bin/bash
# Quản lý toàn bộ launchd jobs cho Pulu-workspace (thay thế n8n)
# Usage:
#   ./setup-launchd.sh load     — load tất cả jobs
#   ./setup-launchd.sh unload   — unload tất cả jobs
#   ./setup-launchd.sh reload   — unload rồi load lại
#   ./setup-launchd.sh status   — kiểm tra trạng thái
#   ./setup-launchd.sh run <job> — chạy ngay 1 job (dry-run hoặc thật)

set -euo pipefail

AGENTS_DIR="$HOME/Library/LaunchAgents"

JOBS=(
    "com.pulu.sgn-daily-telegram-report"   # 7AM daily  — capture dashboard + gửi Telegram
    "com.pulu.competitor-intel"            # mỗi 6h     — crawl tin đối thủ
    "com.pulu.intel-report-daily"          # 8:05AM daily— tổng hợp intel report
    "com.pulu.intel-report-weekly"         # 8:05AM Mon  — weekly intel report
    "com.pulu.metabase-export"             # 6AM daily   — export Metabase trước khi chạy dashboard
    "com.pulu.github-auto-sync"            # mỗi 30ph    — auto git push
)

cmd="${1:-status}"

do_load() {
    local job="$1"
    local plist="$AGENTS_DIR/$job.plist"
    if [ ! -f "$plist" ]; then
        echo "  [SKIP]  $job — plist không tìm thấy"
        return
    fi
    if launchctl list | grep -q "$job"; then
        echo "  [OK]    $job — đã load sẵn"
    else
        launchctl load "$plist" && echo "  [LOAD]  $job" || echo "  [FAIL]  $job"
    fi
}

do_unload() {
    local job="$1"
    local plist="$AGENTS_DIR/$job.plist"
    if launchctl list | grep -q "$job"; then
        launchctl unload "$plist" && echo "  [UNLOAD] $job" || echo "  [FAIL]  $job"
    else
        echo "  [SKIP]  $job — chưa load"
    fi
}

do_status() {
    echo ""
    printf "  %-45s  %s\n" "Job" "PID / Status"
    printf "  %-45s  %s\n" "---" "------------"
    for job in "${JOBS[@]}"; do
        info=$(launchctl list | grep "$job" || true)
        if [ -n "$info" ]; then
            pid=$(echo "$info" | awk '{print $1}')
            last=$(echo "$info" | awk '{print $2}')
            status_str="running (pid $pid)"
            [ "$pid" = "-" ] && status_str="loaded, last exit=$last"
            printf "  %-45s  %s\n" "$job" "$status_str"
        else
            printf "  %-45s  %s\n" "$job" "NOT loaded"
        fi
    done
    echo ""
}

case "$cmd" in
    load)
        echo "Loading launchd jobs..."
        for job in "${JOBS[@]}"; do do_load "$job"; done
        echo "Done."
        ;;
    unload)
        echo "Unloading launchd jobs..."
        for job in "${JOBS[@]}"; do do_unload "$job"; done
        echo "Done."
        ;;
    reload)
        echo "Reloading launchd jobs..."
        for job in "${JOBS[@]}"; do do_unload "$job"; done
        for job in "${JOBS[@]}"; do do_load "$job"; done
        echo "Done."
        ;;
    status)
        do_status
        ;;
    run)
        job="${2:-}"
        if [ -z "$job" ]; then
            echo "Usage: $0 run <job-name>"
            echo "Jobs: sgn-daily  competitor-intel  intel-daily  intel-weekly  metabase-export"
            exit 1
        fi
        case "$job" in
            sgn-daily|sgn)
                echo "Running: sgn_daily_telegram_report.py --dry-run"
                python3 "$(dirname "$0")/sgn_daily_telegram_report.py" --dry-run
                ;;
            competitor-intel|intel)
                echo "Running: crawl_competitor_intel.py"
                python3 "$(dirname "$0")/crawl_competitor_intel.py"
                ;;
            intel-daily)
                echo "Running: run_intel_workflow.sh daily"
                bash "$(dirname "$0")/run_intel_workflow.sh" daily
                ;;
            intel-weekly)
                echo "Running: run_intel_workflow.sh weekly"
                bash "$(dirname "$0")/run_intel_workflow.sh" weekly
                ;;
            metabase-export|metabase)
                echo "Running: trigger_metabase_export.py"
                python3 "$(dirname "$0")/trigger_metabase_export.py"
                ;;
            *)
                echo "Unknown job: $job"
                exit 1
                ;;
        esac
        ;;
    *)
        echo "Usage: $0 {load|unload|reload|status|run <job>}"
        exit 1
        ;;
esac
