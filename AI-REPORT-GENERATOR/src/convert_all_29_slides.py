#!/usr/bin/env python3
"""
Convert All 29 Slides Script — Content-Adaptive Executive Report Engine.
Parses '[2026] DM NW _ Meeting (3).pptx', intelligently analyzes content,
adds executive comments, key takeaways, and flexible layout per slide.
"""

import sys
import os
import json
import re
import importlib.util
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Dynamic imports
def import_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

parser_module = import_from_path("parse_pptx", os.path.join(PROJECT_ROOT, "TOOLS", "pptx-parser", "parse_pptx.py"))
parse_pptx_deck = parser_module.parse_pptx_deck

render_module = import_from_path("render_html", os.path.join(PROJECT_ROOT, "TOOLS", "renderer", "render_html.py"))
render_slide_to_html = render_module.render_slide_to_html

exporter_module = import_from_path("export_pptx", os.path.join(PROJECT_ROOT, "TOOLS", "pptx-exporter", "export_pptx.py"))
export_slide_json_to_pptx = exporter_module.export_slide_json_to_pptx

from src.schemas import (
    SlideJSONPayload, SlideDesignItem, HeroKPI, SlideCard, ExtractedTable
)


# Specific Executive Insights Generator per slide topic
EXECUTIVE_COMMENTS_MAP = {
    22: "Góc nhìn quản trị: Tỷ lệ no-show 32.2% không xuất phát từ thái độ tài xế mà do rào cản UX khi quên ấn Check-in (25.6% đơn hoàn thành trong ca nhưng không ghi nhận). Cần ưu tiên nâng cấp tính năng Auto Check-in trên App Driver.",
    23: "Góc nhìn vận hành: Ca sáng 08:00–12:00 đạt hiệu suất cao nhất (6.25 đơn/ca, gấp 2.8 lần ca tối). Đề xuất cắt giảm quota ca tối 18:00–20:00 (chỉ 2.26 đơn/ca) để tập trung nguồn lực thưởng cho khung giờ sáng.",
    24: "Góc nhìn Retention: 55.8% tài xế dừng lại sau ca đầu tiên. Cần xây dựng ngay điểm chạm Onboarding & hướng dẫn chạy Hub cho tài xế mới để giảm tỷ lệ rời bỏ và duy trì đà tăng trưởng quy mô x3.5 lần.",
    25: "Góc nhìn chuyển đổi EV: Nhu cầu tài xế quan tâm đến phương tiện điện tăng mạnh tại TP.HCM đối với các gói mượn Dat Bike & thuê Aizen. Cần sớm hoàn thiện hệ sinh thái trạm sạc & đối tác để bứt phá.",
    26: "Góc nhìn tuân thủ SLA: SGN duy trì GDR xuất sắc (96.61%), trong khi HAN CTR (72.72%) còn khoảng cách xa so với Target 130%. Cần tăng tần suất push notification & SMS nhắc nhở mở dịch vụ tại Hà Nội.",
    27: "Góc nhìn truyền thông: Đạt chỉ tiêu tuyển dụng Core cho Fuji & Ajinomoto, nhưng Core BigC Long Biên chưa đạt kỳ vọng. Cần mở rộng danh sách push noti trước ngày 20/8.",
    28: "Góc nhìn đối tác & Event: Chuỗi minigame pre-event 11 tuổi đang đúng tiến độ. Cần đẩy nhanh tiến độ đàm phán deal bảo hiểm tài xế & truyền thông gói thuê xe AIZEN trước 21/8.",
    29: "Góc nhìn VOC & Sự cố: Sự cố ngày 14/8 tự động bật dịch vụ 2H-4H gây bức xúc truyền thông trên nhóm Zalo/FB. Cần thắt chặt quy định testing release và nâng cao chất lượng CSKH hỗ trợ tài xế."
}


def convert_entire_deck_to_glassmorphism(pptx_path: str, output_dir: str):
    print("================================================================")
    print("🚀 AI REPORT GENERATOR — ADAPTIVE 29-SLIDE EXECUTIVE REPORT PIPELINE")
    print(f"   Source PPTX: {pptx_path}")
    print("================================================================")

    # 1. Ingest all slides
    ingested_data = parse_pptx_deck(pptx_path, slide_range="all")
    slides_list = ingested_data.get("slides", [])
    total_slides = len(slides_list)
    print(f"\n[Phase 1 — Ingest] Successfully ingested all {total_slides} slides.")

    slides_design_items = []

    for s in slides_list:
        slide_num = s.get("slide_number", 1)
        raw_title = s.get("raw_title", f"Slide {slide_num}")
        paragraphs = s.get("paragraphs", [])
        tables = s.get("tables", [])
        metrics = s.get("key_metrics_extracted", [])

        # Build Takeaway Header
        header_text = raw_title
        body_paragraphs = []
        for idx, p in enumerate(paragraphs):
            p_clean = p.strip()
            if not p_clean:
                continue
            if idx == 0 and len(p_clean) < 130 and ("Ahamove" not in p_clean and "Confidential" not in p_clean):
                header_text = p_clean
            elif "Ahamove" not in p_clean and "Confidential" not in p_clean:
                body_paragraphs.append(p_clean)

        # FLEXIBLE ADAPTATION: Only include Hero KPIs if real metrics exist!
        hero_kpis = []
        if len(metrics) > 0 and slide_num not in [27, 28, 29]:
            for m in metrics[:4]:
                val = m.get("value", "")
                ctx = m.get("context", "Metric")
                label = ctx.split(":")[0][:25] if ":" in ctx else "Metric"
                status = "positive" if "+" in val or "9" in val else ("negative" if "-" in val else "neutral")
                hero_kpis.append(HeroKPI(label=label, value=val, badge_status=status))

        # Build Content Cards from body paragraphs
        cards = []
        highlights = [p for p in body_paragraphs if "HIGHLIGHT" in p.upper() or "ĐÃ" in p.upper() or "TỐT" in p.upper()]
        lowlights = [p for p in body_paragraphs if "LOWLIGHT" in p.upper() or "CHƯA" in p.upper() or "CHẬM" in p.upper() or "BỨC XÚC" in p.upper()]
        normal_bullets = [p for p in body_paragraphs if p not in highlights and p not in lowlights]

        if highlights or lowlights:
            if highlights:
                cards.append(SlideCard(
                    card_id=f"s{slide_num}_h",
                    icon_badge="🏆",
                    title="Highlights & Thành Quả Đạt Được",
                    bullets=highlights
                ))
            if lowlights:
                cards.append(SlideCard(
                    card_id=f"s{slide_num}_l",
                    icon_badge="🔴",
                    title="Lowlights & Thách Thức Cần Tháo Gỡ",
                    bullets=lowlights
                ))
            if normal_bullets:
                cards.append(SlideCard(
                    card_id=f"s{slide_num}_n",
                    icon_badge="💡",
                    title="Chi Tiết Diễn Giải & Chi Tiết Hoạt Động",
                    bullets=normal_bullets
                ))
        elif body_paragraphs:
            half = max(1, len(body_paragraphs) // 2)
            cards.append(SlideCard(
                card_id=f"s{slide_num}_c1",
                icon_badge="💡",
                title="Tóm Tắt Diễn Giải Nội Dung",
                bullets=body_paragraphs[:half]
            ))
            if body_paragraphs[half:]:
                cards.append(SlideCard(
                    card_id=f"s{slide_num}_c2",
                    icon_badge="⚡",
                    title="Phân Tích Bổ Sung & Kế Hoạch",
                    bullets=body_paragraphs[half:]
                ))
        else:
            cards.append(SlideCard(
                card_id=f"s{slide_num}_c1",
                icon_badge="📊",
                title="Chi Tiết Bảng Biểu & Chỉ Số Vận Hành",
                bullets=["Slide tập trung trình bày bảng số liệu chi tiết bên dưới."]
            ))

        # Build Data Table if present
        data_table = None
        if tables and len(tables) > 0:
            tbl = tables[0]
            if tbl.get("headers") and tbl.get("rows"):
                data_table = ExtractedTable(
                    headers=tbl["headers"],
                    rows=tbl["rows"]
                )

        # Get Executive Comment if available
        exec_comment = EXECUTIVE_COMMENTS_MAP.get(
            slide_num,
            f"Góc nhìn quản trị Slide {slide_num}: Cần theo dõi sát sao chỉ số SLA và tiến độ thực thi của các PIC phụ trách để đảm bảo mục tiêu AOP."
        )

        slide_item = SlideDesignItem(
            slide_id=slide_num,
            layout_template="kpi-dashboard" if hero_kpis else "executive-summary",
            takeaway_header=header_text,
            hero_kpis=hero_kpis,
            cards=cards,
            data_table=data_table,
            executive_comment=exec_comment,
            source_slides=[slide_num]
        )
        slides_design_items.append(slide_item)

    # 2. Construct Full 29-Slide Payload
    full_payload = SlideJSONPayload(
        deck_title="Ahamove DM NW Meeting — Full 29-Slide Executive Report",
        style_theme="dark-glassmorphism",
        slides=slides_design_items
    )

    os.makedirs(output_dir, exist_ok=True)
    slide_json_path = os.path.join(output_dir, "full_29_slides_payload.json")
    with open(slide_json_path, 'w', encoding='utf-8') as f:
        json.dump(full_payload.model_dump(), f, indent=2, ensure_ascii=False)
    print(f"\n[Phase 2-6 — Design] Full 29-Slide JSON compiled: {slide_json_path}")

    # 3. Render Dark Glassmorphism 29-Slide Deck
    print("\n[Phase 7 — Render] Rendering Full 29-Slide Dark Glassmorphism HTML...")
    dark_style_path = os.path.join(PROJECT_ROOT, "STYLES", "dark-glassmorphism.json")
    dark_tpl_path = os.path.join(PROJECT_ROOT, "TEMPLATES", "dark-glassmorphism", "template.html")
    output_dark_html = os.path.join(output_dir, "full_29_slides_dark.html")
    render_slide_to_html(slide_json_path, output_dark_html, dark_style_path, dark_tpl_path)
    print(f"✔ Full 29-Slide Dark Glassmorphism HTML: {output_dark_html}")

    # 4. Render Light Glassmorphism 29-Slide Deck
    print("\n[Phase 7 — Render] Rendering Full 29-Slide Light Glassmorphism HTML...")
    light_style_path = os.path.join(PROJECT_ROOT, "STYLES", "light-glassmorphism.json")
    light_tpl_path = os.path.join(PROJECT_ROOT, "TEMPLATES", "light-glassmorphism", "template.html")
    output_light_html = os.path.join(output_dir, "full_29_slides_light.html")
    render_slide_to_html(slide_json_path, output_light_html, light_style_path, light_tpl_path)
    print(f"✔ Full 29-Slide Light Glassmorphism HTML: {output_light_html}")

    # 5. Export Full 29-Slide Native PPTX
    print("\n[Phase 10 — Export] Exporting Full 29-Slide Native Editable PPTX...")
    output_pptx_file = os.path.join(output_dir, "full_29_slides_editable.pptx")
    export_slide_json_to_pptx(slide_json_path, output_pptx_file)
    print(f"✔ Full 29-Slide Native Editable PPTX: {output_pptx_file}")

    print("\n================================================================")
    print("🎉 ADAPTIVE 29-SLIDE EXECUTIVE REPORT PIPELINE COMPLETE!")
    print(f"   1. Dark Glassmorphism 29-Slide HTML:  file://{output_dark_html}")
    print(f"   2. Light Glassmorphism 29-Slide HTML: file://{output_light_html}")
    print(f"   3. Native Editable 29-Slide PPTX:     {output_pptx_file}")
    print("================================================================")


if __name__ == "__main__":
    pptx_path = "/Users/ts-1148/Desktop/Pulu-workspace-v2/AI-REPORT-GENERATOR/OUTPUT/Ahamove_DM_Monthly_Report/[2026] DM NW _ Meeting (3).pptx"
    output_dir = os.path.join(PROJECT_ROOT, "OUTPUT", "Ahamove_DM_Full_29Slides")
    convert_entire_deck_to_glassmorphism(pptx_path, output_dir)
