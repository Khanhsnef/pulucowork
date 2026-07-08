#!/usr/bin/env python3
import os
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime
import subprocess

def load_env(env_path):
    """Đọc tệp .env thủ công để tránh phụ thuộc thư viện python-dotenv"""
    if not os.path.exists(env_path):
        return {}
    env_vars = {}
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                env_vars[key] = val
    return env_vars

def call_dalle_api(api_key, model, prompt):
    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    body = {
        "model": model,
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024"
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode("utf-8"))

def main():
    # 1. Tải môi trường
    workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_vars = load_env(os.path.join(workspace_dir, ".env"))
    
    # Lấy API Key từ .env hoặc môi trường hệ thống
    api_key = env_vars.get("OPENAI_API_KEY") or os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        print("\n\033[91m[LỖI] Chưa cấu hình OPENAI_API_KEY!\033[0m")
        print("Vui lòng mở tệp `.env` ở thư mục gốc của workspace và điền khóa của bạn:")
        print("Ví dụ: \033[93mOPENAI_API_KEY=\"sk-proj-...\"\033[0m\n")
        sys.exit(1)

    # 2. Xử lý tham số prompt
    if len(sys.argv) < 2:
        print("\n\033[93m[HƯỚNG DẪN] Sử dụng lệnh như sau:\033[0m")
        print("python _scripts/generate_openai_image.py \"<prompt mô tả ảnh của bạn>\"")
        print("Ví dụ: python _scripts/generate_openai_image.py \"Một tài xế Ahamove công nghệ đội mũ cam đang cười\"\n")
        sys.exit(0)
        
    prompt = " ".join(sys.argv[1:])
    print(f"\n🚀 Đang gửi yêu cầu tạo ảnh tới DALL-E 3...")
    print(f"📝 Prompt: \033[96m{prompt}\033[0m")

    # 3. Thử gọi API với DALL-E 3 trước, nếu lỗi model thì tự động fallback sang DALL-E 2
    try:
        try:
            res_data = call_dalle_api(api_key, "dall-e-3", prompt)
            model_used = "dall-e-3"
        except urllib.error.HTTPError as e:
            # Kiểm tra xem có phải lỗi không tồn tại model dall-e-3 không
            is_model_missing = False
            try:
                err_res = json.loads(e.read().decode("utf-8"))
                error_msg = err_res['error']['message']
                if e.code == 400 and ("dall-e-3" in error_msg or "model_not_found" in error_msg):
                    is_model_missing = True
            except Exception:
                pass
            
            if is_model_missing:
                print("\n\033[93m[FALLBACK] Model DALL-E 3 không khả dụng trên tài khoản của bạn. Đang tự động chuyển sang DALL-E 2...\033[0m")
                res_data = call_dalle_api(api_key, "dall-e-2", prompt)
                model_used = "dall-e-2"
            else:
                # Nếu là lỗi khác (như hết tiền, sai key), ném lỗi tiếp
                raise e

        # 4. Tải ảnh về lưu trữ
        image_url = res_data["data"][0]["url"]
        revised_prompt = res_data["data"][0].get("revised_prompt", "")
        
        if revised_prompt:
            print(f"\n✨ Prompt đã được tối ưu hóa (Revised Prompt):\n\033[90m{revised_prompt}\033[0m")
        
        creative_dir = os.path.join(workspace_dir, "Output", "Creative")
        os.makedirs(creative_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        clean_prompt = "".join([c if c.isalnum() else "_" for c in prompt[:30].strip().lower()])
        filename = f"gen_{model_used}_{timestamp}_{clean_prompt}.png"
        filepath = os.path.join(creative_dir, filename)
        
        print(f"\n📥 Đang tải ảnh xuống ({model_used})...")
        urllib.request.urlretrieve(image_url, filepath)
        
        print(f"\n\033[92m[THÀNH CÔNG] Ảnh đã được lưu tại:\033[0m")
        print(f"👉 \033[4m{filepath}\033[0m")
        
        # 5. Mở ảnh tự động trên MacOS
        try:
            subprocess.run(["open", filepath])
            print("💻 Đang mở ảnh tự động...")
        except Exception:
            pass
            
    except urllib.error.HTTPError as e:
        print(f"\n\033[91m[LỖI API] OpenAI báo lỗi (Mã {e.code}):\033[0m")
        try:
            err_res = json.loads(e.read().decode("utf-8"))
            print(f"Chi tiết: {err_res['error']['message']}")
        except Exception:
            # Trường hợp e.read() đã được đọc ở trên, cố gắng hiển thị lỗi nguyên bản
            print(f"Lỗi kết nối API OpenAI. Vui lòng kiểm tra lại số dư tài khoản hoặc API Key.")
    except Exception as e:
        print(f"\n\033[91m[LỖI HỆ THỐNG] Không thể tải ảnh: {str(e)}\033[0m")

if __name__ == "__main__":
    main()
