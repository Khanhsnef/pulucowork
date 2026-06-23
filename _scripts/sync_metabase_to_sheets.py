import requests
import json
import os
from datetime import datetime, timedelta

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "metabase_sync_config.json")
API_URL = "https://ws.ahamove.com/ops/trigger/export_to_gs"

def trigger_export(config):
    card_id = config.get("card_id")
    spreadsheet_url = config.get("spreadsheet_url")
    email = config.get("email")
    days_back = config.get("days_back", 63)
    source = config.get("source", "metabase")
    description = config.get("description", f"Card {card_id}")
    
    # Đọc filter từ config (nếu có), nếu không dùng mặc định
    filter_payload = config.get("filter", {})
    if not filter_payload:
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        filter_payload = {
            "start_date": start_date,
            "end_date": end_date
        }
    else:
        # Chuyển đổi các biến động như {today}, {today-63} thành ngày thực tế
        for key, value in filter_payload.items():
            if isinstance(value, str):
                if value == "{today}":
                    filter_payload[key] = datetime.now().strftime("%Y-%m-%d")
                elif value.startswith("{today-") and value.endswith("}"):
                    try:
                        days = int(value.replace("{today-", "").replace("}", ""))
                        filter_payload[key] = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
                    except ValueError:
                        pass
    
    payload = {
        "email": email,
        "card_id": card_id,
        "source": source,
        "filter": filter_payload,
        "spreadsheet_url": spreadsheet_url
    }
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    # Ép kiểu JSON string giống y hệt chuỗi thô (Raw) của Make.com
    raw_payload = json.dumps(payload, separators=(',', ':'))
    
    print(f"\n⏳ Đang trigger: [{description}] (Card: {card_id})")
    print("--- PAYLOAD PYTHON ĐANG GỬI ---")
    print(raw_payload)
    print("-------------------------------")
    
    try:
        response = requests.post(API_URL, headers=headers, data=raw_payload, timeout=30)
        if response.status_code in (200, 201, 202, 204):
            print(f"✅ THÀNH CÔNG: Lệnh xuất dữ liệu đã gửi cho Card {card_id}")
            print(f"Chi tiết phản hồi: {response.text}")
        else:
            print(f"❌ THẤT BẠI: Lỗi {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ LỖI KẾT NỐI: {str(e)}")

def main():
    if not os.path.exists(CONFIG_FILE):
        print(f"Không tìm thấy file cấu hình tại: {CONFIG_FILE}")
        return
        
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        try:
            configs = json.load(f)
        except json.JSONDecodeError:
            print("❌ LỖI: Định dạng file metabase_sync_config.json không hợp lệ. Vui lòng kiểm tra lại cú pháp JSON.")
            return
            
    print(f"🚀 Bắt đầu quá trình đồng bộ Metabase -> Google Sheets ({len(configs)} quy trình)")
    for config in configs:
        trigger_export(config)
    print("\n🎉 HOÀN TẤT QUÁ TRÌNH ĐỒNG BỘ!")

if __name__ == "__main__":
    main()
