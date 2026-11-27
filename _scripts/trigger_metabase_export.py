import requests
from datetime import datetime, timedelta

def trigger_metabase_export(card_id: int, spreadsheet_url: str, email: str, days_back: int = 63):
    """
    Gọi API nội bộ của Ahamove để xuất dữ liệu từ Metabase ra Google Sheet.
    Tương đương với HTTP module trên Make.com.
    """
    url = "https://ws.ahamove.com/ops/trigger/export_to_gs"
    
    # Tính toán ngày động (Dynamic Dates) giống hệt hàm addDays(now; -63) trên Make
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    
    payload = {
        "email": email,
        "card_id": card_id,
        "source": "metabase",
        "filter": {
            "start_date": start_date,
            "end_date": end_date
        },
        "spreadsheet_url": spreadsheet_url
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print(f"🚀 Bắt đầu kích hoạt tiến trình xuất dữ liệu...")
    print(f"📊 Card ID: {card_id}")
    print(f"📅 Chu kỳ: {start_date} -> {end_date}")
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        # Check HTTP Status Code (2xx is success)
        if response.status_code in (200, 201, 202, 204):
            print("\n✅ THÀNH CÔNG! Lệnh xuất dữ liệu đã được gửi đi.")
            print(f"📎 File đích: {spreadsheet_url}")
            print(f"Chi tiết phản hồi: {response.text}")
        else:
            print(f"\n❌ LỖI ({response.status_code}): Không thể kích hoạt API.")
            print(f"Chi tiết: {response.text}")
            
    except Exception as e:
        print(f"\n❌ LỖI KẾT NỐI: {str(e)}")

if __name__ == "__main__":
    import sync_metabase_to_sheets
    sync_metabase_to_sheets.main()
