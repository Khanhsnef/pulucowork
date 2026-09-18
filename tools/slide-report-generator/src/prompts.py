"""
prompts.py — Xuất image prompts để user gen trên ChatGPT, rồi match ảnh vào slide
"""
import os
import json
import shutil
from pathlib import Path


def export_image_prompts(analysis: dict, output_dir: str) -> list[dict]:
    """
    Đọc analysis JSON, xuất danh sách image prompts.
    Trả về list các slide cần ảnh.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    needed = []

    for slide in analysis.get("output_slides", []):
        if slide.get("image_needed") and slide.get("image_prompt"):
            needed.append({
                "slide_num": slide["slide_num"],
                "slide_title": slide["slide_title"],
                "image_prompt": slide["image_prompt"],
                "filename": f"slide_{slide['slide_num']:02d}_image.png",
                "save_to": str(Path(output_dir) / f"slide_{slide['slide_num']:02d}_image.png"),
            })

    if not needed:
        print("[prompts] Không có slide nào cần image generation.")
        return []

    # In ra màn hình để user copy vào ChatGPT
    _print_prompts_for_chatgpt(needed, output_dir)
    return needed


def _print_prompts_for_chatgpt(needed: list[dict], output_dir: str):
    """In hướng dẫn rõ ràng cho user."""
    divider = "=" * 65

    print(f"\n{divider}")
    print("  IMAGE GENERATION — CHATGPT WEB")
    print(divider)
    print(f"\nCó {len(needed)} slide cần ảnh. Làm theo các bước:\n")
    print("1. Mở ChatGPT tại https://chatgpt.com")
    print("2. Với mỗi prompt bên dưới:")
    print("   a. Copy prompt → paste vào ChatGPT")
    print("   b. ChatGPT sẽ generate ảnh")
    print("   c. Download ảnh về")
    print(f"   d. Đặt tên file ĐÚNG như hướng dẫn → lưu vào:")
    print(f"      {output_dir}")
    print("\n3. Sau khi lưu đủ ảnh → chạy: python run.py assemble")
    print(f"\n{divider}\n")

    for item in needed:
        print(f"SLIDE {item['slide_num']:02d}: {item['slide_title']}")
        print(f"Save as: {item['filename']}")
        print(f"Prompt:\n{item['image_prompt']}")
        print()

    print(divider)

    # Lưu ra file để tham khảo lại
    prompts_file = Path(output_dir).parent / "image_prompts.txt"
    with open(prompts_file, "w", encoding="utf-8") as f:
        f.write(f"IMAGE PROMPTS — {len(needed)} slides\n")
        f.write(f"Save images to: {output_dir}\n\n")
        for item in needed:
            f.write(f"--- SLIDE {item['slide_num']:02d} ---\n")
            f.write(f"Filename: {item['filename']}\n")
            f.write(f"Title: {item['slide_title']}\n")
            f.write(f"Prompt:\n{item['image_prompt']}\n\n")

    print(f"[prompts] Prompts saved to: {prompts_file}")
    print(f"[prompts] Waiting for images in: {output_dir}\n")


def check_images_ready(needed: list[dict]) -> tuple[list[dict], list[dict]]:
    """Kiểm tra ảnh nào đã có, ảnh nào còn thiếu."""
    ready = []
    missing = []
    for item in needed:
        if Path(item["save_to"]).exists():
            ready.append(item)
        else:
            missing.append(item)
    return ready, missing


def wait_for_images(needed: list[dict], timeout_seconds: int = 600):
    """
    Block và chờ user lưu đủ ảnh.
    Mỗi 10 giây check lại.
    """
    import time

    if not needed:
        return

    print(f"\n[prompts] Đang chờ {len(needed)} ảnh từ ChatGPT...")
    elapsed = 0
    while elapsed < timeout_seconds:
        ready, missing = check_images_ready(needed)
        if not missing:
            print(f"[prompts] Đủ ảnh! ({len(ready)} ảnh)")
            return
        print(f"[prompts] {len(ready)}/{len(needed)} ảnh — còn thiếu: "
              + ", ".join(m["filename"] for m in missing))
        time.sleep(10)
        elapsed += 10

    # Sau timeout: tiếp tục với ảnh placeholder
    ready, missing = check_images_ready(needed)
    if missing:
        print(f"[prompts] Timeout. Tiếp tục với {len(missing)} placeholder.")
        _create_placeholders(missing)


def _create_placeholders(missing: list[dict]):
    """Tạo placeholder PNG cho ảnh chưa có."""
    from PIL import Image, ImageDraw

    for item in missing:
        img = Image.new("RGB", (800, 450), color=(15, 65, 116))
        draw = ImageDraw.Draw(img)
        draw.text((400, 200), f"Slide {item['slide_num']}\nImage Placeholder",
                  fill=(255, 255, 255), anchor="mm")
        img.save(item["save_to"])
        print(f"[prompts] Placeholder created: {item['filename']}")
