#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChatGPT Image Generator via Playwright & Chrome CDP (macOS Native Auto-Fix)
"""

import os
import sys
import time
import base64
import argparse
import asyncio
import subprocess
import urllib.request
from pathlib import Path
from playwright.async_api import async_playwright

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
DEBUG_PROFILE_DIR = os.path.join(WORKSPACE_DIR, ".chrome_debug_profile")
DEFAULT_OUTPUT_DIR = Path(WORKSPACE_DIR) / "generated_images"
CDP_PORT = 9222
CDP_URL = f"http://127.0.0.1:{CDP_PORT}"


def is_cdp_ready() -> bool:
    """Kiểm tra xem Chrome Debugging port 9222 đã sẵn sàng chưa."""
    try:
        req = urllib.request.Request(f"{CDP_URL}/json/version")
        with urllib.request.urlopen(req, timeout=1.2) as resp:
            return resp.status == 200
    except Exception:
        return False


def ensure_chrome_running():
    """Tự động mở Google Chrome độc lập trên macOS bằng LaunchServices."""
    if is_cdp_ready():
        print("✅ Đã phát hiện Chrome Debug đang chạy.")
        return True

    os.makedirs(DEBUG_PROFILE_DIR, exist_ok=True)
    print("🚀 Đang khởi động Google Chrome trên macOS (cổng debug 9222)...")

    cmd = [
        "open", "-na", "Google Chrome",
        "--args",
        f"--remote-debugging-port={CDP_PORT}",
        f"--user-data-dir={DEBUG_PROFILE_DIR}",
        "--no-first-run",
        "--no-default-browser-check",
        "https://chatgpt.com",
    ]

    try:
        subprocess.run(cmd, check=True)
    except Exception as e:
        print(f"⚠️ Không thể mở Chrome tự động qua lệnh open: {e}")

    # Chờ Chrome sẵn sàng
    for i in range(25):
        time.sleep(0.5)
        if is_cdp_ready():
            print("✅ Google Chrome đã sẵn sàng kết nối!")
            return True

    print("⏳ Đang tiếp tục thử kết nối...")
    return False


async def download_image_from_page(page, img_element, output_path: Path):
    """Trích xuất và lưu ảnh từ ChatGPT."""
    try:
        base64_data = await page.evaluate(
            """async (img) => {
                try {
                    const src = img.src;
                    if (!src) return null;
                    const response = await fetch(src);
                    const blob = await response.blob();
                    return new Promise((resolve, reject) => {
                        const reader = new FileReader();
                        reader.onloadend = () => resolve(reader.result.split(',')[1]);
                        reader.onerror = reject;
                        reader.readAsDataURL(blob);
                    });
                } catch (e) {
                    return null;
                }
            }""",
            img_element,
        )

        if base64_data:
            image_bytes = base64.b64decode(base64_data)
            output_path.write_bytes(image_bytes)
            return True
    except Exception as e:
        print(f"⚠️ Trích xuất base64 không thành công: {e}")

    try:
        src = await img_element.get_attribute("src")
        if src and src.startswith("http"):
            resp = await page.context.request.get(src)
            if resp.status == 200:
                output_path.write_bytes(await resp.body())
                return True
    except Exception as e:
        print(f"❌ Tải qua HTTP thất bại: {e}")

    return False


async def generate_image(prompt: str, output_path: str = None):
    DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if not output_path:
        timestamp = int(time.time())
        output_file = DEFAULT_OUTPUT_DIR / f"chatgpt_img_{timestamp}.png"
    else:
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

    print(f"\n=======================================================")
    print(f"🎨 BẮT ĐẦU TẠO ẢNH BẰNG CHATGPT")
    print(f"📝 Prompt: {prompt}")
    print(f"📁 Lưu tại: {output_file.resolve()}")
    print(f"=======================================================\n")

    ensure_chrome_running()

    async with async_playwright() as p:
        try:
            print(f"🔌 Đang kết nối tới Chrome...")
            browser = await p.chromium.connect_over_cdp(CDP_URL)
        except Exception as e:
            print(f"\n❌ CHƯA THỂ KẾT NỐI TỚI CHROME: {e}")
            print("👉 Vui lòng mở Chrome bằng lệnh: ./open_chrome.sh")
            print("👉 Sau đó chạy lại: python3 chatgpt_image_gen.py \"...\"")
            return None

        context = browser.contexts[0] if browser.contexts else await browser.new_context()

        # Tìm hoặc mở tab chatgpt.com
        page = None
        for pg in context.pages:
            if "chatgpt.com" in pg.url:
                page = pg
                break

        if not page:
            page = await context.new_page()
            print("🌐 Đang mở https://chatgpt.com...")
            await page.goto("https://chatgpt.com", wait_until="domcontentloaded")
        else:
            print("🌐 Đã kết nối vào tab ChatGPT đang mở.")
            await page.bring_to_front()

        # Kiểm tra trạng thái đăng nhập
        chat_box_selector = "#prompt-textarea, div[contenteditable='true'][id='prompt-textarea'], [contenteditable='true'], textarea[placeholder*='Message']"
        chat_box = page.locator(chat_box_selector).first

        try:
            await chat_box.wait_for(state="visible", timeout=8000)
            print("🔑 Đã nhận diện phiên đăng nhập ChatGPT!")
        except Exception:
            print("\n" + "!" * 60)
            print("⚠️ CHƯA ĐĂNG NHẬP CHATGPT:")
            print("👉 Vui lòng nhìn vào cửa sổ Chrome vừa mở và tiến hành ĐĂNG NHẬP.")
            print("👉 Phiên đăng nhập sẽ được tự động lưu vĩnh viễn.")
            print("⏳ Đang chờ đăng nhập (tối đa 120s)...")
            print("!" * 60 + "\n")
            try:
                await chat_box.wait_for(state="visible", timeout=120000)
                print("✅ Đăng nhập thành công!")
            except Exception:
                print("❌ Hết thời gian chờ đăng nhập.")
                return None

        await asyncio.sleep(1.5)

        # Đếm số ảnh hiện tại
        img_selector = "article img[alt*='Generated'], article img[src*='backend-api/files'], article img[src*='dalle'], article div[data-message-author-role='assistant'] img"
        initial_img_count = await page.locator(img_selector).count()

        # Nhập và gửi prompt
        formatted_prompt = f"Vẽ một bức ảnh chi tiết, chất lượng cao theo mô tả sau: {prompt}"
        print(f"💬 Đang nhập prompt vào ChatGPT...")

        await chat_box.click()
        await page.keyboard.press("Meta+A")
        await page.keyboard.press("Backspace")
        await chat_box.fill(formatted_prompt)
        await asyncio.sleep(1)

        send_btn = page.locator("button[data-testid='send-button'], button[aria-label='Send prompt']").first
        if await send_btn.is_visible():
            await send_btn.click()
        else:
            await page.keyboard.press("Enter")

        print("📨 Prompt đã được gửi! Đang đợi ChatGPT vẽ ảnh...")

        # Chờ DALL-E vẽ xong
        stop_btn = page.locator("button[data-testid='stop-button'], button[aria-label='Stop generating']").first
        try:
            await stop_btn.wait_for(state="visible", timeout=8000)
            print("⏳ DALL-E đang vẽ ảnh...")
            await stop_btn.wait_for(state="detached", timeout=120000)
            print("✨ ChatGPT đã vẽ xong!")
        except Exception:
            pass

        await asyncio.sleep(3)

        # Tìm ảnh được sinh ra
        img_locator = page.locator(img_selector)
        max_wait = 60
        start_time = time.time()
        target_img = None

        while time.time() - start_time < max_wait:
            current_count = await img_locator.count()
            if current_count > initial_img_count:
                target_img = img_locator.nth(current_count - 1)
                src = await target_img.get_attribute("src")
                if src:
                    break
            await asyncio.sleep(2)

        if not target_img:
            last_msg_imgs = page.locator("div[data-message-author-role='assistant']").last.locator("img")
            if await last_msg_imgs.count() > 0:
                target_img = last_msg_imgs.last

        if not target_img:
            print("❌ Không tìm thấy ảnh trong phản hồi.")
            return None

        # Tải ảnh
        print("📥 Đang tải ảnh về máy...")
        success = await download_image_from_page(page, target_img, output_file)

        if success and output_file.exists():
            print(f"\n🎉 HOÀN THÀNH TẠO ẢNH!")
            print(f"👉 File ảnh đã lưu tại: {output_file.resolve()}\n")
            return str(output_file.resolve())
        else:
            print("❌ Lưu file ảnh thất bại.")
            return None


def main():
    parser = argparse.ArgumentParser(description="Tự động tạo ảnh ChatGPT qua Chrome Session.")
    parser.add_argument("prompt", nargs="?", help="Mô tả bức ảnh bạn muốn vẽ")
    parser.add_argument("-o", "--output", help="Đường dẫn lưu file ảnh (tùy chọn)")

    args = parser.parse_args()

    prompt = args.prompt
    if not prompt:
        prompt = input("Nhập mô tả bức ảnh bạn muốn vẽ: ").strip()

    if not prompt:
        print("❌ Prompt không được để trống!")
        sys.exit(1)

    asyncio.run(generate_image(prompt, args.output))


if __name__ == "__main__":
    main()
