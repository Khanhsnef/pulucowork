import os
import json
import datetime
import urllib.request
import urllib.parse
import sys

BASE_DIR = "/Users/ts-1148/Desktop/Pulu-workspace"
MONITOR_DIR = os.path.join(BASE_DIR, "Output/Ahamove/06. COMPETITIVE_INTEL", "monitoring")
SIGNAL_FILE = os.path.join(MONITOR_DIR, "raw-signals.json")
ENV_PATH = os.path.join(BASE_DIR, ".env")

def load_env():
    env = {}
    if os.path.exists(ENV_PATH):
        for line in open(ENV_PATH, encoding="utf-8"):
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            env[key.strip()] = val.strip().strip('"').strip("'")
    return env

def call_gemini(prompt, api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    headers = {
        "Content-Type": "application/json"
    }
    
    system_prompt = """Bạn là một Chuyên gia Tình báo Cạnh tranh (Competitive Intelligence Analyst) xuất sắc của Ahamove.
Nhiệm vụ: Đọc dữ liệu thô (raw signals) và viết báo cáo dưới định dạng Markdown chuẩn Lark Docs.
Cấu trúc bắt buộc:
1. Executive Summary
2. Competitor Move (Động thái đối thủ) - phân loại CONFIRMED / INFERRED / HYPOTHESIS.
3. Likely Impact on Ahamove (Tác động ngắn hạn & dài hạn)
4. Recommended Response (Khuyến nghị hành động)
5. FAROUT Score (Đánh giá độ tin cậy x/60)

Nguyên tắc:
- LUÔN ƯU TIÊN thông tin về mảng giao hàng (delivery) và xe 2 bánh (bikes) lên đầu. Xe 4 bánh hoặc taxi đẩy xuống dưới.
- BẮT BUỘC chèn URL nguồn vào từng sự kiện bằng cú pháp [Nguồn bài viết](link_url).
"""
    
    data = {
        "system_instruction": {
            "parts": [{"text": system_prompt}]
        },
        "contents": [
            {"parts": [{"text": prompt}]}
        ],
        "generationConfig": {
            "maxOutputTokens": 4000
        }
    }
    
    req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        sys.exit(1)

def main():
    report_type = sys.argv[1] if len(sys.argv) > 1 else "daily"
    env = load_env()
    api_key = env.get("GEMINI_API_KEY")
    if not api_key:
        print("Missing GEMINI_API_KEY in .env")
        sys.exit(1)
        
    if not os.path.exists(SIGNAL_FILE):
        print(f"Signal file not found: {SIGNAL_FILE}")
        sys.exit(1)
        
    with open(SIGNAL_FILE, "r", encoding="utf-8") as f:
        signals = json.load(f)
        
    # Lọc signals (Daily = 24h qua, Weekly = 7 ngày qua)
    now = datetime.datetime.now(datetime.timezone.utc)
    hours = 24 if report_type == "daily" else 24 * 7
    cutoff = now - datetime.timedelta(hours=hours)
    
    recent_signals = [s for s in signals if datetime.datetime.fromisoformat(s["published_at"]) >= cutoff]
    
    if not recent_signals:
        print("Không có tín hiệu mới nào trong khoảng thời gian này.")
        sys.exit(0)
        
    prompt = f"Đây là dữ liệu {report_type} report. Tổng cộng {len(recent_signals)} tín hiệu mới.\nDữ liệu: {json.dumps(recent_signals, ensure_ascii=False)}"
    print(f"Đang gọi AI xử lý {report_type} report với {len(recent_signals)} tín hiệu...")
    
    markdown_content = call_gemini(prompt, api_key)
    
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    if report_type == "weekly":
        filename = f"{date_str}-weekly-market-brief.md"
        html_filename = f"{date_str}-weekly-market-brief.html"
    else:
        filename = f"{date_str}-competitor-intel-report.md"
        html_filename = f"{date_str}-competitor-intel-report.html"
        
    out_path = os.path.join(MONITOR_DIR, filename)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
        
    # Output JSON for n8n to parse easily
    result = {
        "status": "success",
        "report_type": report_type,
        "md_path": out_path,
        "html_path": os.path.join(MONITOR_DIR, html_filename)
    }
    print(json.dumps(result))

if __name__ == "__main__":
    main()
