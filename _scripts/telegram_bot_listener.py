import os
import sys
import time
import urllib.request
import urllib.parse
import json
import glob
import datetime
import re

# ── LOAD ENV CONFIG ──────────────────────────────────────────────────────────
TOKEN = None
CHAT_ID = None
GEMINI_API_KEY = None
OPENAI_API_KEY = None
ANTHROPIC_API_KEY = None

# Try loading from environment or .env file
env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
if os.path.exists(env_file):
    with open(env_file, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith("#") and "=" in line:
                key, val = line.strip().split("=", 1)
                k = key.strip()
                v = val.strip().strip('"').strip("'")
                if k == "TELEGRAM_BOT_TOKEN":
                    TOKEN = v
                elif k == "TELEGRAM_CHAT_ID":
                    CHAT_ID = v
                elif k == "GEMINI_API_KEY":
                    GEMINI_API_KEY = v
                elif k == "OPENAI_API_KEY":
                    OPENAI_API_KEY = v
                elif k == "ANTHROPIC_API_KEY":
                    ANTHROPIC_API_KEY = v

# Override with environment variables if present
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", TOKEN)
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", CHAT_ID)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", GEMINI_API_KEY)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", OPENAI_API_KEY)
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", ANTHROPIC_API_KEY)

if not TOKEN:
    print("❌ Error: TELEGRAM_BOT_TOKEN is not set.")
    sys.exit(1)

MONITOR_DIR = "Output/Ahamove/06. COMPETITIVE_INTEL/monitoring"

# ── HELPER FUNCTIONS ──────────────────────────────────────────────────────────
def send_telegram_msg(chat_id, text, reply_to_message_id=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    if reply_to_message_id:
        payload["reply_to_message_id"] = reply_to_message_id

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"⚠️ Error sending message with Markdown: {e}. Retrying as plain text...")
        if "parse_mode" in payload:
            del payload["parse_mode"]
        req_fallback = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        try:
            with urllib.request.urlopen(req_fallback, timeout=10) as response:
                return json.loads(response.read().decode())
        except Exception as fallback_err:
            print(f"⚠️ Fallback sending failed: {fallback_err}")
            return None

def send_telegram_doc(chat_id, doc_path, reply_to_message_id=None):
    if not os.path.exists(doc_path):
        return None
    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    boundary = "Boundary-TelegramSendDocument"
    file_name = os.path.basename(doc_path)
    with open(doc_path, 'rb') as f:
        file_content = f.read()

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="chat_id"\r\n\r\n'
        f'{chat_id}\r\n'
    ).encode('utf-8')
    
    if reply_to_message_id:
        body += (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="reply_to_message_id"\r\n\r\n'
            f'{reply_to_message_id}\r\n'
        ).encode('utf-8')

    body += (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="document"; filename="{file_name}"\r\n'
        f'Content-Type: text/html\r\n\r\n'
    ).encode('utf-8') + file_content + f"\r\n--{boundary}--\r\n".encode('utf-8')

    req = urllib.request.Request(
        url,
        data=body,
        headers={
            'Content-Type': f'multipart/form-data; boundary={boundary}',
            'Content-Length': len(body)
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"⚠️ Error sending document: {e}")
        return None

def get_latest_report(pattern):
    files = glob.glob(os.path.join(MONITOR_DIR, pattern))
    if not files:
        return None, None
    latest_md = max(files, key=os.path.getmtime)
    latest_html = latest_md.replace(".md", ".html")
    if not os.path.exists(latest_html):
        latest_html = None
    return latest_md, latest_html

def parse_summary(md_path):
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return "Không thể đọc nội dung báo cáo.", "Báo cáo"

    title = "Báo cáo giám sát cạnh tranh"
    exec_summary = ""
    lines = content.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("# ") and not any(c in line for c in ["━", "=", "-"]):
            title = line.replace("# ", "").strip()
        if "Executive Summary" in line or "Tóm Tắt Thực Thi" in line or "📊 Executive Summary" in line:
            summary_lines = []
            for j in range(i + 1, len(lines)):
                next_line = lines[j].strip()
                if next_line.startswith("#") or next_line == "---":
                    break
                if next_line:
                    summary_lines.append(lines[j])
            exec_summary = "\n".join(summary_lines)
            
    return exec_summary, title

# ── AI API CALLERS ────────────────────────────────────────────────────────────
def call_gemini_api(user_message, system_context, api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{
            "parts": [{"text": f"System Context:\n{system_context}\n\nUser Question:\n{user_message}"}]
        }],
        "tools": [{
            "googleSearch": {}
        }],
        "generationConfig": {
            "maxOutputTokens": 512,
            "temperature": 0.5
        }
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            res = json.loads(response.read().decode())
            candidates = res.get("candidates", [])
            if candidates and candidates[0].get("content", {}).get("parts"):
                return candidates[0]["content"]["parts"][0]["text"]
            return "Tôi chưa xử lý được câu hỏi này."
    except Exception as e:
        print(f"⚠️ Gemini API Error: {e}")
        return None

def call_openai_api(user_message, system_context, api_key):
    url = "https://api.openai.com/v1/chat/completions"
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_context},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 512,
        "temperature": 0.5
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            res = json.loads(response.read().decode())
            choices = res.get("choices", [])
            if choices and choices[0].get("message", {}).get("content"):
                return choices[0]["message"]["content"]
            return "Tôi chưa xử lý được câu hỏi này."
    except Exception as e:
        print(f"⚠️ OpenAI API Error: {e}")
        return None

def call_anthropic_api(user_message, system_context, api_key):
    url = "https://api.anthropic.com/v1/messages"
    payload = {
        "model": "claude-3-5-haiku-20241022",
        "max_tokens": 512,
        "system": system_context,
        "messages": [
            {"role": "user", "content": user_message}
        ]
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            res = json.loads(response.read().decode())
            content = res.get("content", [])
            if content and content[0].get("type") == "text":
                return content[0]["text"]
            return "Tôi chưa xử lý được câu hỏi này."
    except Exception as e:
        print(f"⚠️ Anthropic API Error: {e}")
        return None

def get_system_context(user_message=""):
    md_file_daily, _ = get_latest_report("*-report.md")
    md_file_weekly, _ = get_latest_report("*-weekly-market-brief.md")
    
    context = (
        "Bạn là trợ lý AI chuyên nghiệp, nhiệt tình và thực tế của đội ngũ Driver Management Ahamove.\n"
        "Nhiệm vụ của bạn là giải đáp các câu hỏi của các thành viên trong nhóm về thị trường, đối thủ (Grab, Be, XanhSM, SPX, ShopeeFood), "
        "thông tin vận hành, quy trình chiến lược, OKRs và hệ thống phân hạng tài xế dựa trên tài liệu nội bộ được cung cấp.\n\n"
        "Hãy phản hồi ngắn gọn (dưới 4 câu), tự nhiên và thực tế như một đồng nghiệp hoặc trợ lý đang chat trực tiếp (tránh văn phong robot, chào hỏi dài dòng).\n"
        "Ưu tiên sử dụng tài liệu nội bộ được cung cấp để trả lời các câu hỏi chuyên môn. Đối với các câu hỏi ngoài lề (đời sống, thời tiết, tin tức mới...) hoặc khi tài liệu không có thông tin, bạn hãy sử dụng kết quả tìm kiếm từ công cụ Google Search được tích hợp để trả lời một cách chính xác nhất, tuyệt đối tránh việc từ chối trả lời do thiếu tài liệu.\n\n"
    )
    
    loaded_files = []
    
    if md_file_daily:
        try:
            with open(md_file_daily, 'r', encoding='utf-8') as f:
                context += f"### BÁO CÁO NGÀY MỚI NHẤT ({os.path.basename(md_file_daily)}):\n" + f.read() + "\n\n"
                loaded_files.append(os.path.basename(md_file_daily))
        except Exception:
            pass
            
    if md_file_weekly:
        try:
            with open(md_file_weekly, 'r', encoding='utf-8') as f:
                context += f"### BẢN TIN TUẦN MỚI NHẤT ({os.path.basename(md_file_weekly)}):\n" + f.read() + "\n\n"
                loaded_files.append(os.path.basename(md_file_weekly))
        except Exception:
            pass

    # 2. Dynamic RAG based on keyword matching
    # Map keywords to relative paths of documents from Output/Ahamove/
    rag_map = {
        ("okr", "kr", "mục tiêu", "target"): [
            "Output/Ahamove/01. STRATEGY & PLANNING/okr/2026-q2-dm-team-okr.md",
            "Output/Ahamove/01. STRATEGY & PLANNING/okr/2026-q2-okr-dm-internal.md"
        ],
        ("journey", "lifecycle", "vòng đời", "trải nghiệm", "hành trình"): [
            "Output/Ahamove/01. STRATEGY & PLANNING/driver-journey/2026-05-driver-journey-summary.md",
            "Output/Ahamove/01. STRATEGY & PLANNING/driver-journey/2026-06-driver-journey-milestones.md",
            "Output/Ahamove/01. STRATEGY & PLANNING/driver-journey/2026-06-driver-journey-proposal.md",
            "Output/Ahamove/06. COMPETITIVE_INTEL/2026-06-global-driver-lifecycle-benchmark.md"
        ],
        ("benchmark", "toàn cầu", "thế giới", "nước ngoài", "uber", "meituan", "doordash", "swiggy", "gojek", "deliveroo", "rappi", "ifood"): [
            "Output/Ahamove/06. COMPETITIVE_INTEL/2026-06-global-driver-lifecycle-benchmark.md"
        ],
        ("ranking", "phân hạng", "params", "level", "benefits", "ahabenefits", "quyền lợi", "thưởng điểm"): [
            "Output/Ahamove/01. STRATEGY & PLANNING/ahabenefits/2026-05-ahabenefits-points-flow.md",
            "Output/Ahamove/01. STRATEGY & PLANNING/driver-ranking/2026-05-driver-ranking-params.md",
            "Output/Ahamove/01. STRATEGY & PLANNING/driver-ranking/2026-05-driver-ranking-priority-registration.md"
        ],
        ("restructure", "tái cơ cấu", "cơ cấu", "org", "raci"): [
            "Output/Ahamove/01. STRATEGY & PLANNING/team-restructure/2026-06-driver-restructure-kickoff.md"
        ],
        ("open-source", "mã nguồn mở", "github", "git"): [
            "Output/Ahamove/01. STRATEGY & PLANNING/2026-06-open-source-repos-application.md"
        ],
        ("áo khỉ", "monkey", "campaign", "chiến dịch"): [
            "Output/Ahamove/02. CAMPAIGNS_PROJECTS/2026-05-ao-khi-campaign-plan.md",
            "Output/Ahamove/02. CAMPAIGNS_PROJECTS/2026-05-ao-khi-comms-drafts.md"
        ],
        ("pulu", "smartflow", "risk", "bảo mật", "hiệu năng"): [
            "Output/Ahamove/05. ANALYSIS & REPORTS/2026-06-pulu-smartflow-risk-assessment.md"
        ],
        ("dashboard", "sop", "duckdb", "streamlit"): [
            "Output/Ahamove/07. TEAM_MANAGEMENT/2026-06-new-dashboard-sop.md"
        ],
        ("claude", "ai", "training", "đào tạo"): [
            "Output/Ahamove/07. TEAM_MANAGEMENT/2026-05-claude-guide-for-team.md"
        ]
    }

    user_msg_lower = user_message.lower()
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    for keys, paths in rag_map.items():
        if any(k in user_msg_lower for k in keys):
            for rel_path in paths:
                full_path = os.path.join(root_dir, rel_path)
                filename = os.path.basename(rel_path)
                if filename not in loaded_files and os.path.exists(full_path):
                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            context += f"### TÀI LIỆU LIÊN QUAN: {filename} ({rel_path})\n" + f.read() + "\n\n"
                            loaded_files.append(filename)
                    except Exception:
                        pass
                        
    if loaded_files:
        print(f"📚 Loaded dynamic context files for query '{user_message}': {loaded_files}")
        
    return context

# ── COMMAND & MESSAGE HANDLERS ────────────────────────────────────────────────
def handle_command(chat_id, text, msg_id):
    cmd = text.split()[0].lower().replace("@", "")
    if "@" in cmd:
        cmd = cmd.split("@")[0]

    if cmd in ["/start", "/help"]:
        help_text = (
            "🤖 *Ahamove SmartOps Assistant*\n"
            "Tôi là trợ lý giám sát thị trường và đối thủ trực thuộc Driver Management Team.\n\n"
            "*Các lệnh khả dụng:*\n"
            "👉 /latest : Xem báo cáo giám sát đối thủ mới nhất trong ngày.\n"
            "👉 /weekly : Xem bản tin thị trường & đối thủ đầu tuần gần nhất.\n"
            "👉 /status : Kiểm tra trạng thái kết nối hệ thống SmartOps.\n"
            "👉 /help   : Hiển thị hướng dẫn này."
        )
        send_telegram_msg(chat_id, help_text, reply_to_message_id=msg_id)

    elif cmd == "/latest":
        md_file, html_file = get_latest_report("*-report.md")
        if not md_file:
            send_telegram_msg(chat_id, "⚠️ Hiện chưa có báo cáo giám sát ngày nào trong hệ thống.", reply_to_message_id=msg_id)
            return

        summary, title = parse_summary(md_file)
        message = f"🔔 *BÁO CÁO MỚI NHẤT: {title}*\n\n"
        if summary:
            message += f"📊 *Tóm tắt thực thi:*\n{summary}\n\n"
        message += "📎 _Báo cáo chi tiết dạng HTML được đính kèm bên dưới._"
        
        send_telegram_msg(chat_id, message, reply_to_message_id=msg_id)
        if html_file:
            send_telegram_doc(chat_id, html_file, reply_to_message_id=msg_id)

    elif cmd == "/weekly":
        md_file, html_file = get_latest_report("*-weekly-market-brief.md")
        if not md_file:
            send_telegram_msg(chat_id, "⚠️ Hiện chưa có bản tin đầu tuần nào trong hệ thống.", reply_to_message_id=msg_id)
            return

        summary, title = parse_summary(md_file)
        message = f"📰 *BẢN TIN ĐẦU TUẦN: {title}*\n\n"
        if summary:
            message += f"📊 *Tóm tắt thực thi:*\n{summary}\n\n"
        message += "📎 _Bản tin chi tiết dạng HTML được đính kèm bên dưới._"
        
        send_telegram_msg(chat_id, message, reply_to_message_id=msg_id)
        if html_file:
            send_telegram_doc(chat_id, html_file, reply_to_message_id=msg_id)

    elif cmd == "/status":
        streamlit_status = "⚠️ Ngoại tuyến (Offline)"
        try:
            with urllib.request.urlopen("http://localhost:8501", timeout=2) as response:
                if response.status == 200:
                    streamlit_status = "✅ Trực tuyến (http://localhost:8501)"
        except Exception:
            pass

        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status_text = (
            "💻 *Trạng thái Hệ thống Ahamove SmartOps:*\n\n"
            f"- *Daily Crawler & Monitor:* ✅ Sẵn sàng (chạy lúc 9:00 AM)\n"
            f"- *Weekly Brief Scheduler:* ✅ Sẵn sàng (chạy lúc 8:30 AM thứ Hai)\n"
            f"- *Simulator Dashboard (Streamlit):* {streamlit_status}\n"
            f"- *Thời gian hệ thống:* `{now_str}`"
        )
        send_telegram_msg(chat_id, status_text, reply_to_message_id=msg_id)

def handle_natural_message(chat_id, text, msg_id, message):
    is_private = int(chat_id) > 0
    
    # Check if bot is mentioned or replied to
    is_reply_to_bot = False
    reply_to = message.get("reply_to_message")
    if reply_to:
        reply_from = reply_to.get("from", {})
        # Ensure it is replying to our specific bot username
        if reply_from.get("is_bot") and reply_from.get("username") == "DMAIChat_Bot":
            is_reply_to_bot = True
            
    # Match only explicit username handle or the exact phrase "bot ơi" / "bot oi" with word boundaries
    text_lower = text.lower()
    mentioned = False
    if "@dmaichat_bot" in text_lower:
        mentioned = True
    elif re.search(r'\bbot\s+ơi\b', text_lower) or re.search(r'\bbot\s+oi\b', text_lower):
        mentioned = True
    
    # Only respond in group if it's a private chat, a direct reply, or explicitly mentioned
    if not is_private and not is_reply_to_bot and not mentioned:
        return
        
    print(f"💬 Handling natural message: '{text}' in Chat ID: {chat_id}")
    
    # Send typing action
    try:
        url_action = f"https://api.telegram.org/bot{TOKEN}/sendChatAction"
        payload = {"chat_id": chat_id, "action": "typing"}
        req_action = urllib.request.Request(
            url_action,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        urllib.request.urlopen(req_action, timeout=3)
    except Exception:
        pass
        
    context = get_system_context(text)
    
    # Try calling configured API Keys in sequence
    reply_text = None
    
    # Let's try Gemini first (recommended)
    if GEMINI_API_KEY and not reply_text:
        reply_text = call_gemini_api(text, context, GEMINI_API_KEY)
        
    # Then try OpenAI
    if OPENAI_API_KEY and not reply_text:
        reply_text = call_openai_api(text, context, OPENAI_API_KEY)
        
    # Finally try Anthropic (making sure key starts with sk-ant)
    if ANTHROPIC_API_KEY and not reply_text:
        if ANTHROPIC_API_KEY.startswith("sk-ant"):
            reply_text = call_anthropic_api(text, context, ANTHROPIC_API_KEY)
        else:
            # Stale or misconfigured key in env
            print("⚠️ System ANTHROPIC_API_KEY does not start with 'sk-ant'. Skipping.")
            
    if not reply_text:
        reply_text = (
            "⚠️ *Trợ lý AI chưa được cấu hình khóa kết nối.*\n\n"
            "Vui lòng điền một trong các API Key sau vào file `.env` của bạn để bắt đầu trò chuyện:\n"
            "- `GEMINI_API_KEY`=\"key_của_bạn\" (khuyên dùng)\n"
            "- `OPENAI_API_KEY`=\"key_của_bạn\"\n"
            "- `ANTHROPIC_API_KEY`=\"key_của_bạn\""
        )
        
    send_telegram_msg(chat_id, reply_text, reply_to_message_id=msg_id)

# ── MAIN LOOP (POLLING) ───────────────────────────────────────────────────────
def main():
    print("🤖 Starting Ahamove SmartOps Telegram Bot Listener (AI-enabled Polling)...")
    offset = None
    
    # Send online status message
    if CHAT_ID:
        send_telegram_msg(CHAT_ID, "🤖 *Ahamove SmartOps Bot (AI-enabled)* đã trực tuyến và sẵn sàng hỗ trợ bạn!")
        
    while True:
        try:
            url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
            params = {"timeout": 20}
            if offset:
                params["offset"] = offset
            
            data = urllib.parse.urlencode(params).encode('utf-8')
            req = urllib.request.Request(url, data=data)
            
            with urllib.request.urlopen(req, timeout=25) as response:
                res = json.loads(response.read().decode())
                
                if res.get("ok") and res.get("result"):
                    for update in res["result"]:
                        offset = update["update_id"] + 1
                        
                        message = update.get("message")
                        if not message:
                            continue
                            
                        chat = message.get("chat")
                        text = message.get("text")
                        msg_id = message.get("message_id")
                        
                        if chat and text:
                            chat_id = chat["id"]
                            if text.startswith("/"):
                                print(f"📩 Received command: '{text}' from Chat ID: {chat_id}")
                                handle_command(chat_id, text, msg_id)
                            else:
                                handle_natural_message(chat_id, text, msg_id, message)
                            
        except KeyboardInterrupt:
            print("\n🤖 Bot listener stopped by user.")
            break
        except Exception as e:
            print(f"⚠️ Connection error or API limit: {e}")
            time.sleep(5)
            
        time.sleep(1)

if __name__ == "__main__":
    main()
