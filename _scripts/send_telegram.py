import sys
import os
import urllib.request
import urllib.parse
import json

def send_telegram_notification(token, chat_id, md_path, html_path):
    print(f"Reading markdown from: {md_path}")
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading report file: {e}")
        return False
        
    # Extract Title and Executive Summary
    title = "Báo cáo giám sát cạnh tranh"
    exec_summary = ""
    lines = content.splitlines()
    for i, line in enumerate(lines):
        # Clean title line
        if line.startswith("# ") and not any(c in line for c in ["━", "=", "-"]):
            title = line.replace("# ", "").strip()
        if "Executive Summary" in line or "Tóm Tắt Thực Thi" in line or "📊 Executive Summary" in line:
            # Get next non-empty lines until next header or horizontal rule
            summary_lines = []
            for j in range(i + 1, len(lines)):
                next_line = lines[j].strip()
                if next_line.startswith("#") or next_line == "---":
                    break
                if next_line:
                    summary_lines.append(lines[j])
            exec_summary = "\n".join(summary_lines)
            
    # Format message for Telegram (Markdown)
    message = f"🔔 *{title}*\n\n"
    if exec_summary:
        message += f"📊 *Tóm tắt thực thi:*\n{exec_summary}\n\n"
    message += "📎 _Chi tiết báo cáo được gửi kèm dưới dạng file HTML đính kèm bên dưới._"
    
    # Send message to Telegram
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            res = json.loads(response.read().decode())
            if not res.get("ok"):
                print(f"❌ Telegram API Error: {res}")
                return False
            print("✅ Telegram notification message sent successfully.")
    except Exception as e:
        print(f"❌ Error sending Telegram message: {e}")
        return False
        
    # Send HTML file as document
    if html_path and os.path.exists(html_path):
        print(f"Uploading HTML document: {html_path}")
        url_file = f"https://api.telegram.org/bot{token}/sendDocument"
        
        # Build multipart/form-data manually to avoid external dependencies like requests
        boundary = "Boundary-TelegramSendDocument"
        file_name = os.path.basename(html_path)
        with open(html_path, 'rb') as f:
            file_content = f.read()
            
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="chat_id"\r\n\r\n'
            f'{chat_id}\r\n'
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="document"; filename="{file_name}"\r\n'
            f'Content-Type: text/html\r\n\r\n'
        ).encode('utf-8') + file_content + f"\r\n--{boundary}--\r\n".encode('utf-8')
        
        req_file = urllib.request.Request(
            url_file,
            data=body,
            headers={
                'Content-Type': f'multipart/form-data; boundary={boundary}',
                'Content-Length': len(body)
            }
        )
        
        try:
            with urllib.request.urlopen(req_file, timeout=15) as response:
                res = json.loads(response.read().decode())
                if not res.get("ok"):
                    print(f"❌ Telegram Document API Error: {res}")
                    return False
                print("✅ Telegram HTML report document sent successfully.")
                return True
        except Exception as e:
            print(f"❌ Error sending Telegram document: {e}")
            return False
            
    return True

def main():
    if len(sys.argv) < 3:
        print("❌ Error: Missing markdown or HTML file argument.")
        print("Usage: python3 send_telegram.py <file.md> <file.html>")
        sys.exit(1)
        
    md_file = sys.argv[1]
    html_file = sys.argv[2]
    
    # Try loading from .env file in the workspace
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith("#") and "=" in line:
                    key, val = line.strip().split("=", 1)
                    if key.strip() == "TELEGRAM_BOT_TOKEN" and not token:
                        token = val.strip().strip('"').strip("'")
                    elif key.strip() == "TELEGRAM_CHAT_ID" and not chat_id:
                        chat_id = val.strip().strip('"').strip("'")

    if not token or not chat_id:
        print("❌ Error: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set in environment variables or .env file.")
        sys.exit(1)
        
    if not os.path.exists(md_file):
        print(f"❌ Error: Markdown file not found: {md_file}")
        sys.exit(1)
        
    send_telegram_notification(token, chat_id, md_file, html_file)

if __name__ == "__main__":
    main()
