#!/bin/bash
# Mở Google Chrome với chế độ Remote Debugging trên macOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 > /dev/null 2>&1 &
echo "✅ Google Chrome đã được mở ở cổng debug 9222!"
echo "👉 Bạn hãy mở tab https://chatgpt.com và đăng nhập (nếu chưa đăng nhập)."
echo "👉 Sau đó chạy: python3 chatgpt_image_gen.py \"Nội dung ảnh muốn vẽ\""
