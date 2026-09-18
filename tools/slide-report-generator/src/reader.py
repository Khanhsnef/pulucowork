"""
reader.py — Đọc PPTX hoặc Google Slides → trả về list slide data
"""
import os
import io
import json
import base64
import requests
from pathlib import Path
from pptx import Presentation
from pptx.util import Pt
from PIL import Image


def read_pptx(file_path: str, slide_range: str = "all") -> list[dict]:
    """Đọc file PPTX, trả về list slide data theo range."""
    prs = Presentation(file_path)
    total = len(prs.slides)
    indices = _parse_range(slide_range, total)

    slides = []
    for i in indices:
        slide = prs.slides[i]
        data = _extract_slide(slide, i + 1)
        slides.append(data)
        print(f"  [read] Slide {i+1}/{total}: {data['title'] or '(no title)'}")

    return slides


def read_google_slides(url: str, slide_range: str = "all") -> list[dict]:
    """
    Đọc Google Slides bằng cách export PDF từng slide rồi parse.
    Yêu cầu file public hoặc shared 'anyone with link can view'.
    """
    presentation_id = _extract_gslides_id(url)
    if not presentation_id:
        raise ValueError(f"Không thể extract Google Slides ID từ: {url}")

    print(f"  [read] Google Slides ID: {presentation_id}")
    print(f"  [read] Export từng slide dưới dạng PNG...")

    # Export mỗi slide thành PNG qua thumbnail API (không cần auth nếu public)
    slides_raw = _export_gslides_as_images(presentation_id, slide_range)
    return slides_raw


# ─── Internal helpers ────────────────────────────────────────────────────────

def _parse_range(slide_range: str, total: int) -> list[int]:
    """Parse '1-10', '3', 'all', '1-xx' → list index (0-based)."""
    s = slide_range.strip().lower()
    if s == "all":
        return list(range(total))
    if "-" in s:
        parts = s.split("-")
        start = int(parts[0]) - 1
        end = total - 1 if parts[1] in ("xx", "all", "") else int(parts[1]) - 1
        return list(range(max(0, start), min(total - 1, end) + 1))
    return [int(s) - 1]


def _extract_slide(slide, slide_num: int) -> dict:
    """Extract text, tables, notes từ một pptx slide."""
    title = ""
    texts = []
    tables = []
    bullet_points = []

    for shape in slide.shapes:
        if not shape.has_text_frame and not shape.has_table:
            continue

        # Title — dùng try/except vì placeholder_format raise ValueError nếu không phải placeholder
        try:
            ph = shape.placeholder_format
            if ph is not None and ph.idx == 0 and shape.has_text_frame:
                title = shape.text_frame.text.strip()
                continue
        except (ValueError, AttributeError):
            pass

        if shape.has_text_frame:
            frame_text = []
            for para in shape.text_frame.paragraphs:
                text = para.text.strip()
                if not text:
                    continue
                level = para.level
                if level > 0:
                    bullet_points.append({"level": level, "text": text})
                frame_text.append(text)
            if frame_text:
                texts.append("\n".join(frame_text))

        if shape.has_table:
            tbl = shape.table
            table_data = []
            for row in tbl.rows:
                table_data.append([cell.text.strip() for cell in row.cells])
            tables.append(table_data)

    # Notes
    notes_text = ""
    if slide.has_notes_slide:
        notes_frame = slide.notes_slide.notes_text_frame
        if notes_frame:
            notes_text = notes_frame.text.strip()

    from pptx.enum.shapes import MSO_SHAPE_TYPE
    return {
        "slide_num": slide_num,
        "title": title,
        "texts": texts,
        "bullet_points": bullet_points,
        "tables": tables,
        "notes": notes_text,
        "has_images": any(
            getattr(shape, "shape_type", None) == MSO_SHAPE_TYPE.PICTURE
            for shape in slide.shapes
        ),
    }


def _extract_gslides_id(url: str) -> str | None:
    """Extract presentation ID từ Google Slides URL."""
    import re
    patterns = [
        r"presentation/d/([a-zA-Z0-9_-]+)",
        r"presentation/([a-zA-Z0-9_-]+)/",
    ]
    for pat in patterns:
        m = re.search(pat, url)
        if m:
            return m.group(1)
    return None


def _export_gslides_as_images(presentation_id: str, slide_range: str) -> list[dict]:
    """
    Export Google Slides slides thành PNG images.
    Dùng thumbnail endpoint (public access).
    Trả về list dict giống format của _extract_slide nhưng có thêm 'image_base64'.
    """
    # Lấy tổng số slide qua oEmbed / thumbnail page
    # Nếu không có auth, chỉ get được thumbnails
    slides = []
    page = 1
    max_pages = 100  # safety limit

    while page <= max_pages:
        # Google Slides thumbnail URL pattern
        thumb_url = (
            f"https://docs.google.com/presentation/d/{presentation_id}"
            f"/export/png?id={presentation_id}&pageid=p{page}"
        )
        resp = requests.get(thumb_url, timeout=15)
        if resp.status_code != 200:
            break  # hết slide

        img_b64 = base64.b64encode(resp.content).decode()
        slides.append({
            "slide_num": page,
            "title": f"Slide {page}",
            "texts": [],
            "bullet_points": [],
            "tables": [],
            "notes": "",
            "has_images": True,
            "image_base64": img_b64,  # sẽ gửi lên Claude để đọc
        })
        print(f"  [read] Exported slide {page}")
        page += 1

    # Apply range filter
    total = len(slides)
    indices = _parse_range(slide_range, total)
    return [slides[i] for i in indices if i < total]


def save_raw(slides: list[dict], output_path: str):
    """Lưu raw slide data ra JSON để debug."""
    with open(output_path, "w", encoding="utf-8") as f:
        # Bỏ image_base64 cho dễ đọc
        clean = []
        for s in slides:
            c = {k: v for k, v in s.items() if k != "image_base64"}
            clean.append(c)
        json.dump(clean, f, ensure_ascii=False, indent=2)
    print(f"  [read] Raw data saved: {output_path}")
