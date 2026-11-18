#!/usr/bin/env python3
"""
HCM Live Traffic Cams Server
Khởi chạy web server nội bộ và tự động mở trình duyệt xem camera giao thông TP.HCM.
"""

import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 5055

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # In log ngắn gọn
        sys.stderr.write(f"[{self.log_date_time_string()}] {args[0]}\n")

def run():
    web_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(web_dir)
    
    # Cho phép tái sử dụng cổng
    socketserver.TCPServer.allow_reuse_address = True
    
    port = PORT
    while port < PORT + 20:
        try:
            with socketserver.TCPServer(("", port), QuietHandler) as httpd:
                url = f"http://localhost:{port}"
                print("\n" + "=" * 60)
                print("🚦 HỆ THỐNG CAMERA GIAO THÔNG TRỰC TUYẾN TP. HỒ CHÍ MINH")
                print("=" * 60)
                print(f"👉 Đang phục vụ tại: {url}")
                print(f"📁 Thư mục: {web_dir}")
                print("💡 Nhấn Ctrl + C để dừng máy chủ")
                print("=" * 60 + "\n")
                
                # Mở trình duyệt mặc định
                webbrowser.open(url)
                httpd.serve_forever()
                break
        except OSError:
            port += 1

if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\n🛑 Đã tắt máy chủ. Chúc bạn một ngày làm việc hiệu quả!")

