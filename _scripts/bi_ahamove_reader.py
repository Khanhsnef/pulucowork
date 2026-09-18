#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
BI AHAMOVE DATA EXTRACTOR & READER TOOL (bi.ahamove.com / Metabase)
===============================================================================
Công cụ chuyên dụng để tự động truy vấn, đọc và trích xuất dữ liệu từ Metabase
(bi.ahamove.com) phục vụ Phân tích Chiến lược Vận hành và AI Operations.

Hỗ trợ 3 Phương thức Trích xuất chính:
-------------------------------------------------------------------------------
1. Direct Metabase API (Trực tiếp qua REST API):
   - Đọc Card (Saved Question) theo Card ID + Tham số filter.
   - Thực thi câu lệnh SQL Native trực tiếp lên Database.
   - Tải về dạng Pandas DataFrame, JSON, hoặc CSV.

2. Ahamove Ops Webhook Trigger (Tích hợp Hệ thống Nội bộ):
   - Gọi API https://ws.ahamove.com/ops/trigger/export_to_gs để đẩy dữ liệu ra Google Sheets.
   - Tự động chuyển đổi link Google Sheet thành stream CSV và đọc thành DataFrame.

3. Public Card / Dashboard Embed Reader:
   - Trích xuất dữ liệu từ các Card được chia sẻ Public (Public UUID).

Tác giả: Enterprise Strategic AI Decision Architect
===============================================================================
"""

import os
import sys
import json
import time
import argparse
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union
import requests
import pandas as pd

# Thiết lập Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("BIAhamoveReader")


def parse_metabase_url(url: str) -> Dict[str, Any]:
    """
    Phân tích URL Metabase dạng:
    https://bi.ahamove.com/question/82572-dm-bi-n-ng-ranking...?city_id=SGN&DQS_T1=80&...
    Trả về dict: {"card_id": 82572, "filter": {"city_id": "SGN", "DQS_T1": "80", ...}}
    """
    from urllib.parse import urlparse, parse_qs
    import re
    
    parsed = urlparse(url)
    path_parts = [p for p in parsed.path.split('/') if p]
    
    card_id = None
    # Tìm segment chứa card ID (ví dụ: '82572-dm-bi-n-ng-ranking' hoặc '82572')
    for part in path_parts:
        match = re.match(r"^(\d+)", part)
        if match:
            card_id = int(match.group(1))
            break
            
    if not card_id:
        raise ValueError(f"Không thể trích xuất Card ID từ URL Metabase: {url}")
        
    query_params = parse_qs(parsed.query)
    # Trích xuất các filter params (lấy giá trị đơn thay vì list)
    filters = {k: v[0] if isinstance(v, list) and len(v) > 0 else v for k, v in query_params.items()}
    
    return {
        "card_id": card_id,
        "filter": filters,
        "raw_url": url
    }


def load_dotenv_file(env_path: Optional[str] = None):
    """
    Tự động nạp các biến từ file .env vào os.environ
    """
    if not env_path:
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        env_path = os.path.join(root_dir, ".env")
        
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if key and not os.environ.get(key):
                        os.environ[key] = val

# Gọi tự động khi nạp module
load_dotenv_file()


def auto_extract_chrome_metabase_session() -> Optional[str]:
    """
    Tự động bóc tách Cookie metabase.SESSION từ Google Chrome bằng browser_cookie3
    """
    try:
        import browser_cookie3
        cj = browser_cookie3.chrome(domain_name='bi.ahamove.com')
        for cookie in cj:
            if cookie.name == 'metabase.SESSION' and cookie.value:
                logger.info("🎉 Tự động bóc tách thành công Metabase Session Token từ Google Chrome!")
                return cookie.value
    except Exception as e:
        logger.debug(f"Không thể trích xuất Chrome cookie tự động: {e}")
    return None


class MetabaseClient:
    """
    Client tương tác trực tiếp với Metabase REST API (bi.ahamove.com)
    """

    def __init__(self, base_url: str = "https://bi.ahamove.com", session_id: Optional[str] = None):
        load_dotenv_file()
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })
        
        # 1. Thử nạp toàn bộ Chrome CookieJar để đi qua OAuth2 Proxy
        try:
            import browser_cookie3
            cj = browser_cookie3.chrome(domain_name='bi.ahamove.com')
            self.session.cookies.update(cj)
            logger.info("🔑 Đã tự động nạp CookieJar từ Google Chrome vào Session!")
            
            # Tự động lấy metabase.SESSION cookie từ CookieJar nếu có
            chrome_session = self.session.cookies.get("metabase.SESSION")
            if chrome_session:
                self.session_id = chrome_session
                logger.info(f"🎉 Tự động trích xuất Session Token thành công từ Chrome Cookies: {chrome_session[:8]}...")
        except Exception as e:
            logger.debug(f"Không thể nạp Chrome CookieJar: {e}")

        # 2. Nếu có Session ID riêng trong .env (ghi đè)
        env_session = session_id or os.environ.get("METABASE_SESSION")
        if env_session:
            self.session_id = env_session

        if self.session_id:
            self.session.headers["X-Metabase-Session"] = self.session_id

    def login(self, username: Optional[str] = None, password: Optional[str] = None) -> bool:
        """
        Đăng nhập vào Metabase để lấy X-Metabase-Session token
        """
        username = username or os.environ.get("METABASE_USERNAME")
        password = password or os.environ.get("METABASE_PASSWORD")

        if not username or not password:
            logger.error("❌ Cần cung cấp username và password (hoặc set METABASE_USERNAME, METABASE_PASSWORD trong .env)")
            return False

        login_url = f"{self.base_url}/api/session"
        payload = {"username": username, "password": password}

        try:
            res = self.session.post(login_url, json=payload, timeout=15)
            if res.status_code == 200:
                self.session_id = res.json().get("id")
                self.session.headers["X-Metabase-Session"] = self.session_id
                logger.info("✅ Đăng nhập Metabase thành công! Session ID đã được cập nhật.")
                return True
            else:
                logger.error(f"❌ Đăng nhập thất bại ({res.status_code}): {res.text}")
                return False
        except Exception as e:
            logger.error(f"❌ Lỗi kết nối khi đăng nhập Metabase: {e}")
            return False

    def check_session(self) -> bool:
        """
        Kiểm tra xem session token hiện tại còn hiệu lực hay không
        """
        if not self.session_id:
            return False
        try:
            res = self.session.get(f"{self.base_url}/api/user/current", timeout=10)
            return res.status_code == 200
        except Exception:
            return False

    def get_card_data(
        self,
        card_id: int,
        parameters: Optional[List[Dict[str, Any]]] = None,
        export_format: str = "json"
    ) -> Union[pd.DataFrame, List[Dict[str, Any]], bytes]:
        """
        Truy vấn dữ liệu từ một Card (Saved Question) trên Metabase.
        
        :param card_id: ID của Card trên Metabase (ví dụ: 74433)
        :param parameters: Danh sách filter parameters (nếu có)
        :param export_format: 'json', 'csv', 'xlsx' hoặc 'dataframe'
        :return: Pandas DataFrame, List of Dicts hoặc Raw Bytes (xlsx/csv)
        """
        if not self.session_id:
            logger.warning("⚠️ Chưa có Session ID. Đang thử tự động đăng nhập...")
            if not self.login():
                raise PermissionError("Không thể xác thực với Metabase bi.ahamove.com")

        # Endpoint truy vấn card
        url = f"{self.base_url}/api/card/{card_id}/query/{'json' if export_format in ('json', 'dataframe') else export_format}"
        
        payload = {}
        if parameters:
            payload["parameters"] = parameters

        logger.info(f"⏳ Đang tải dữ liệu từ Card ID {card_id} trên {self.base_url}...")
        res = self.session.post(url, json=payload, timeout=60)

        if res.status_code != 200:
            logger.error(f"❌ Lỗi khi tải Card {card_id} ({res.status_code}): {res.text[:300]}")
            res.raise_for_status()

        if export_format == "dataframe":
            data = res.json()
            df = pd.DataFrame(data)
            logger.info(f"✅ Tải dữ liệu thành công! Kích thước: {df.shape[0]} hàng, {df.shape[1]} cột.")
            return df
        elif export_format == "json":
            return res.json()
        else:
            return res.content

    def execute_sql(
        self,
        database_id: int,
        query: str,
        parameters: Optional[List[Dict[str, Any]]] = None
    ) -> pd.DataFrame:
        """
        Thực thi câu lệnh SQL Native trực tiếp trên Database thông qua Metabase API.
        
        :param database_id: ID của Database trong Metabase (ví dụ: 2, 3...)
        :param query: Câu lệnh SQL
        :return: Pandas DataFrame chứa kết quả
        """
        if not self.session_id:
            if not self.login():
                raise PermissionError("Không thể xác thực với Metabase")

        url = f"{self.base_url}/api/dataset"
        payload = {
            "database": database_id,
            "type": "native",
            "native": {
                "query": query,
                "template-tags": {}
            },
            "parameters": parameters or []
        }

        logger.info(f"⚡ Đang thực thi câu lệnh SQL Native trên DB #{database_id}...")
        res = self.session.post(url, json=payload, timeout=120)

        if res.status_code != 200:
            logger.error(f"❌ Lỗi thực thi SQL ({res.status_code}): {res.text[:300]}")
            res.raise_for_status()

        result_data = res.json()
        data = result_data.get("data", {})
        cols = [c["name"] for c in data.get("cols", [])]
        rows = data.get("rows", [])

        df = pd.DataFrame(rows, columns=cols)
        logger.info(f"✅ Thực thi SQL thành công! Thu được {df.shape[0]} hàng, {df.shape[1]} cột.")
        return df

    def get_public_card_data(self, public_uuid: str) -> pd.DataFrame:
        """
        Đọc dữ liệu từ Public Card qua UUID không cần đăng nhập.
        """
        url = f"{self.base_url}/public/question/{public_uuid}.json"
        logger.info(f"🌐 Đang đọc Public Card UUID: {public_uuid}...")
        res = requests.get(url, timeout=30)
        res.raise_for_status()
        df = pd.DataFrame(res.json())
        logger.info(f"✅ Đọc Public Card thành công! {df.shape[0]} hàng, {df.shape[1]} cột.")
        return df


class AhamoveOpsTrigger:
    """
    Client sử dụng Webhook Trigger Nội bộ Ahamove (ws.ahamove.com) để xuất dữ liệu ra Google Sheets & tải về.
    """

    TRIGGER_URL = "https://ws.ahamove.com/ops/trigger/export_to_gs"

    @classmethod
    def trigger_export(
        cls,
        card_id: int,
        spreadsheet_url: str,
        email: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        filter_dict: Optional[Dict[str, Any]] = None,
        days_back: int = 63,
        source: str = "metabase"
    ) -> bool:
        """
        Gửi request trigger xuất dữ liệu Metabase Card ra Google Sheets
        """
        if filter_dict:
            filter_payload = filter_dict
        else:
            if not start_date or not end_date:
                end_dt = datetime.now()
                start_dt = end_dt - timedelta(days=days_back)
                end_date = end_dt.strftime("%Y-%m-%d")
                start_date = start_dt.strftime("%Y-%m-%d")
            filter_payload = {
                "start_date": start_date,
                "end_date": end_date
            }

        payload = {
            "email": email,
            "card_id": card_id,
            "source": source,
            "filter": filter_payload,
            "spreadsheet_url": spreadsheet_url
        }

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        raw_payload = json.dumps(payload, separators=(',', ':'))
        logger.info(f"🚀 Triggering export cho Card ID {card_id} -> Google Sheet với Filter: {filter_payload}...")

        try:
            res = requests.post(cls.TRIGGER_URL, headers=headers, data=raw_payload, timeout=30)
            if res.status_code in (200, 201, 202, 204):
                logger.info("✅ THÀNH CÔNG: Lệnh xuất dữ liệu đã được gửi đến Ahamove Webhook Worker.")
                return True
            else:
                logger.error(f"❌ LỖI ({res.status_code}): {res.text}")
                return False
        except Exception as e:
            logger.error(f"❌ Lỗi kết nối Trigger Webhook: {e}")
            return False

    @staticmethod
    def read_google_sheet_csv(spreadsheet_url: str, gid: Union[str, int] = "0") -> pd.DataFrame:
        """
        Chuyển đổi URL Google Sheet thành link xuất CSV và đọc trực tiếp vào Pandas DataFrame.
        
        :param spreadsheet_url: URL dạng https://docs.google.com/spreadsheets/d/ID/edit#gid=GID
        :param gid: ID sheet tab (nếu URL chứa #gid=... sẽ tự trích xuất)
        """
        import io
        
        # Trích xuất Sheet ID
        sheet_id = None
        if "/d/" in spreadsheet_url:
            sheet_id = spreadsheet_url.split("/d/")[1].split("/")[0]
        
        # Trích xuất gid nếu có trong URL
        if "#gid=" in spreadsheet_url:
            gid = spreadsheet_url.split("#gid=")[1].split("&")[0]
        elif "gid=" in spreadsheet_url:
            gid = spreadsheet_url.split("gid=")[1].split("&")[0]

        if not sheet_id:
            raise ValueError(f"Không thể định dạng Google Sheet ID từ URL: {spreadsheet_url}")

        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
        logger.info(f"📥 Đang tải dữ liệu CSV trực tiếp từ Google Sheet (ID: {sheet_id}, GID: {gid})...")
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        res = requests.get(csv_url, headers=headers, allow_redirects=True, timeout=30)
        
        if res.status_code != 200:
            logger.error(f"❌ Lỗi khi tải Google Sheet CSV ({res.status_code}): {res.text[:200]}")
            res.raise_for_status()

        df = pd.read_csv(io.StringIO(res.text))
        logger.info(f"✅ Đọc Google Sheet thành công! Kích thước: {df.shape[0]} hàng, {df.shape[1]} cột.")
        return df


def generate_executive_summary(df: pd.DataFrame, title: str = "Tóm Tắt Dữ Liệu Metabase") -> str:
    """
    Tạo báo cáo tóm tắt executive summary cho DataFrame theo chuẩn Enterprise Strategic Architect
    """
    summary = []
    summary.append(f"📊 **{title}**")
    summary.append(f"- **Tổng số bản ghi (Rows):** `{len(df):,}`")
    summary.append(f"- **Số cột dữ liệu (Cols):** `{len(df.columns)}` ({', '.join(df.columns[:8])}{'...' if len(df.columns) > 8 else ''})")
    
    # Kiểm tra các cột số để thống kê
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    if numeric_cols:
        summary.append("\n📈 **Chỉ Số Tổng Quan (Numeric Metrics):**")
        for col in numeric_cols[:5]:
            total = df[col].sum()
            avg = df[col].mean()
            summary.append(f"  - **`{col}`**: Total = `{total:,.2f}` | Avg = `{avg:,.2f}`")
            
    return "\n".join(summary)


# ===============================================================================
# CLI COMMAND LINE INTERFACE
# ===============================================================================
def main():
    parser = argparse.ArgumentParser(description="Tool đọc và trích xuất dữ liệu từ bi.ahamove.com (Metabase)")
    
    subparsers = parser.add_subparsers(dest="command", help="Chức năng hoạt động")

    # Command 1: Card Direct API
    card_parser = subparsers.add_parser("card", help="Truy vấn dữ liệu Card ID từ Metabase API")
    card_parser.add_argument("--id", type=int, help="Metabase Card ID")
    card_parser.add_argument("--url", type=str, help="Full Metabase Question URL kèm tham số filter")
    card_parser.add_argument("--output", type=str, help="Đường dẫn file đầu ra (.csv hoặc .json)")
    card_parser.add_argument("--session", type=str, help="Metabase Session Token (hoặc set METABASE_SESSION)")
    card_parser.add_argument("--username", type=str, help="Metabase Username")
    card_parser.add_argument("--password", type=str, help="Metabase Password")

    # Command 2: Trigger Webhook Export
    trigger_parser = subparsers.add_parser("trigger", help="Kích hoạt trigger xuất Metabase Card -> Google Sheet")
    trigger_parser.add_argument("--id", type=int, help="Metabase Card ID")
    trigger_parser.add_argument("--url", type=str, help="Full Metabase Question URL chứa Card ID và filter params")
    trigger_parser.add_argument("--sheet", type=str, required=True, help="Google Sheet URL")
    trigger_parser.add_argument("--email", type=str, default="khanhlp@ahamove.com", help="Email đăng ký nhận thông báo")
    trigger_parser.add_argument("--days-back", type=int, default=63, help="Số ngày lùi về quá khứ")
    trigger_parser.add_argument("--download", action="store_true", help="Tự động đọc Google Sheet sau khi trigger")
    trigger_parser.add_argument("--output", type=str, help="Lưu dữ liệu tải về thành file CSV local")

    # Command 3: Read Google Sheet directly
    sheet_parser = subparsers.add_parser("sheet", help="Đọc dữ liệu trực tiếp từ Google Sheet CSV URL")
    sheet_parser.add_argument("--url", type=str, required=True, help="Google Sheet URL")
    sheet_parser.add_argument("--output", type=str, help="Đường dẫn lưu file CSV")

    # Command 4: Batch Sync Config File
    batch_parser = subparsers.add_parser("batch", help="Chạy hàng loạt từ file cấu hình metabase_sync_config.json")
    batch_parser.add_argument("--config", type=str, default="_scripts/metabase_sync_config.json", help="Đường dẫn file JSON config")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "card":
        card_id = args.id
        filter_dict = None
        if args.url:
            parsed_meta = parse_metabase_url(args.url)
            card_id = parsed_meta["card_id"]
            filter_dict = parsed_meta["filter"]
            logger.info(f"🔗 Đã phân tích URL -> Card ID: {card_id}, Filters: {filter_dict}")
            
        if not card_id:
            logger.error("❌ Cần cung cấp ít nhất --id hoặc --url")
            sys.exit(1)

        client = MetabaseClient(session_id=args.session)
        if not client.session_id and args.username and args.password:
            client.login(args.username, args.password)
            
        try:
            df = client.get_card_data(card_id, export_format="dataframe")
            print("\n" + generate_executive_summary(df, f"Kết quả Card #{card_id}"))
            
            if args.output:
                if args.output.endswith(".json"):
                    df.to_json(args.output, orient="records", force_ascii=False, indent=2)
                else:
                    df.to_csv(args.output, index=False, encoding="utf-8-sig")
                logger.info(f"💾 Đã lưu kết quả thành công vào: {args.output}")
        except Exception as e:
            logger.error(f"❌ Không thể đọc dữ liệu Card: {e}")

    elif args.command == "trigger":
        card_id = args.id
        filter_dict = None
        if args.url:
            parsed_meta = parse_metabase_url(args.url)
            card_id = parsed_meta["card_id"]
            filter_dict = parsed_meta["filter"]
            logger.info(f"🔗 Đã phân tích URL -> Card ID: {card_id}, Filters: {filter_dict}")

        if not card_id:
            logger.error("❌ Cần cung cấp ít nhất --id hoặc --url")
            sys.exit(1)

        success = AhamoveOpsTrigger.trigger_export(
            card_id=card_id,
            spreadsheet_url=args.sheet,
            email=args.email,
            filter_dict=filter_dict,
            days_back=args.days_back
        )
        if success and args.download:
            logger.info("⏳ Chờ 3 giây để Google Sheet cập nhật dữ liệu...")
            time.sleep(3)
            df = AhamoveOpsTrigger.read_google_sheet_csv(args.sheet)
            print("\n" + generate_executive_summary(df, f"Dữ Liệu Sheet cho Card #{args.id}"))
            if args.output:
                df.to_csv(args.output, index=False, encoding="utf-8-sig")
                logger.info(f"💾 Đã lưu file: {args.output}")

    elif args.command == "sheet":
        df = AhamoveOpsTrigger.read_google_sheet_csv(args.url)
        print("\n" + generate_executive_summary(df, "Dữ Liệu từ Google Sheet"))
        if args.output:
            df.to_csv(args.output, index=False, encoding="utf-8-sig")
            logger.info(f"💾 Đã lưu file: {args.output}")

    elif args.command == "batch":
        config_file = args.config
        if not os.path.exists(config_file):
            logger.error(f"❌ Không tìm thấy file config: {config_file}")
            sys.exit(1)
        with open(config_file, "r", encoding="utf-8") as f:
            configs = json.load(f)
        logger.info(f"🚀 Bắt đầu thực hiện Batch Sync cho {len(configs)} quy trình...")
        for item in configs:
            AhamoveOpsTrigger.trigger_export(
                card_id=item["card_id"],
                spreadsheet_url=item["spreadsheet_url"],
                email=item.get("email", "khanhlp@ahamove.com"),
                days_back=item.get("days_back", 63)
            )


if __name__ == "__main__":
    main()
