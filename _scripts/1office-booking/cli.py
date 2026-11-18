#!/usr/bin/env python3
"""
1Office CLI Tool for Antigravity Agent
Công cụ dòng lệnh hỗ trợ Antigravity IDE thực thi trực tiếp các tác vụ 1Office.
"""

import sys
import argparse
import json
import logging
from datetime import datetime, timedelta

from oneoffice_client import OneOfficeClient, ROOM_MAP, ROOM_NAME_MAP

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

DAY_MAP = {"monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6}

def get_next_weekday(day_name: str) -> str:
    target = DAY_MAP[day_name.lower()]
    today = datetime.now()
    days = (target - today.weekday()) % 7 or 7
    return (today + timedelta(days=days)).strftime("%d/%m/%Y")

def main():
    parser = argparse.ArgumentParser(description="1Office CLI Tool for Antigravity Agent")
    subparsers = parser.add_subparsers(dest="command", help="Danh sách lệnh khả dụng")

    # Command: status
    parser_status = subparsers.add_parser("status", help="Kiểm tra trạng thái kết nối & phiên làm việc 1Office")

    # Command: check-rooms
    parser_check = subparsers.add_parser("check-rooms", help="Kiểm tra phòng họp trống / lịch họp trong ngày")
    parser_check.add_argument("--date", type=str, default=datetime.now().strftime("%d/%m/%Y"), help="Ngày cần kiểm tra (DD/MM/YYYY)")

    # Command: book
    parser_book = subparsers.add_parser("book", help="Đặt phòng họp trên 1Office")
    parser_book.add_argument("--title", type=str, required=True, help="Tên cuộc họp")
    parser_book.add_argument("--room", type=str, required=True, help="Tên phòng họp (NANGA, DENALI...) hoặc ID")
    parser_book.add_argument("--date", type=str, required=True, help="Ngày họp (DD/MM/YYYY hoặc 'next-monday', 'next-friday')")
    parser_book.add_argument("--start", type=str, required=True, help="Giờ bắt đầu (HH:MM)")
    parser_book.add_argument("--end", type=str, required=True, help="Giờ kết thúc (HH:MM)")

    args = parser.parse_args()

    client = OneOfficeClient()

    if args.command == "status":
        res = client.check_session()
        print("\n=== 1OFFICE CONNECTION STATUS ===")
        print(f"Base URL: {client.base_url}")
        print(f"Session Valid: {'✅ HỢP LỆ' if res['valid'] else '❌ HẾT HẠN / LỖI'}")
        print(f"Chi tiết: {res['reason']}\n")
        sys.exit(0 if res["valid"] else 1)

    elif args.command == "check-rooms":
        print(f"\n=== TRẠNG THÁI PHÒNG HỌP NGÀY {args.date} ===")
        res = client.check_session()
        if not res["valid"]:
            print(f"❌ Không thể tra cứu: {res['reason']}")
            sys.exit(1)
        print("✅ Đã kết nối 1Office. Danh sách phòng họp khả dụng:")
        for name, room_id in ROOM_MAP.items():
            print(f" - Phòng {name} (ID: {room_id})")
        print("\n")

    elif args.command == "book":
        date_str = args.date
        if date_str.startswith("next-"):
            day_name = date_str.replace("next-", "")
            if day_name in DAY_MAP:
                date_str = get_next_weekday(day_name)

        print(f"\n=== THỰC THI ĐẶT PHÒNG HỌP ===")
        print(f"Tiêu đề: {args.title}")
        print(f"Phòng: {args.room}")
        print(f"Thời gian: {date_str} từ {args.start} tới {args.end}")
        
        result = client.book_room(
            title=args.title,
            room_name_or_id=args.room,
            date=date_str,
            time_start=args.start,
            time_end=args.end
        )

        if result["success"]:
            print("✅ ĐẶT PHÒNG HỌP THÀNH CÔNG!")
            sys.exit(0)
        else:
            print(f"❌ ĐẶT PHÒNG THẤT BẠI: {result.get('message', 'Unspecified error')}")
            sys.exit(1)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
