#!/bin/bash
# Script tự động chạy toàn bộ luồng Competitor Intel Report
# Dùng để tích hợp vào n8n qua 1 node Execute Command duy nhất.

REPORT_TYPE=$1
if [ -z "$REPORT_TYPE" ]; then
    REPORT_TYPE="daily"
fi

cd /Users/ts-1148/Desktop/Pulu-workspace

echo "🚀 [1/4] Chạy Crawler thu thập tin tức..."
python3 _scripts/crawl_competitor_intel.py

echo "🧠 [2/4] Gọi Claude AI để phân tích và viết báo cáo ($REPORT_TYPE)..."
# auto_generate_intel_report.py sẽ in ra dòng JSON ở cuối cùng
AI_OUTPUT=$(python3 _scripts/auto_generate_intel_report.py "$REPORT_TYPE")
echo "$AI_OUTPUT"

# Dùng awk để lấy dòng cuối cùng (là dòng JSON), sau đó dùng jq để bóc tách
LAST_LINE=$(echo "$AI_OUTPUT" | tail -n 1)

# Kiểm tra nếu LAST_LINE không phải là JSON hợp lệ (ví dụ: báo lỗi Missing API Key)
if ! echo "$LAST_LINE" | jq empty 2>/dev/null; then
    if [[ "$LAST_LINE" == *"Không có tín hiệu mới"* ]]; then
        echo "✅ $LAST_LINE"
        exit 0
    fi
    echo "❌ Lỗi từ AI Script: $LAST_LINE"
    exit 1
fi

MD_PATH=$(echo "$LAST_LINE" | jq -r '.md_path')
HTML_PATH=$(echo "$LAST_LINE" | jq -r '.html_path')

if [ -z "$MD_PATH" ] || [ "$MD_PATH" == "null" ]; then
    echo "❌ Lỗi: Không lấy được đường dẫn file MD từ AI Agent."
    exit 1
fi

echo "🎨 [3/4] Biên dịch Markdown sang giao diện HTML Ahamove..."
python3 _scripts/md_to_html.py "$MD_PATH"

echo "✈️ [4/4] Gửi báo cáo lên Telegram..."
python3 _scripts/send_telegram.py "$MD_PATH" "$HTML_PATH"

echo "✅ Hoàn tất toàn bộ quy trình!"
