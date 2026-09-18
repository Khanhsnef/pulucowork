#!/usr/bin/env python3
"""
run.py — AI Report Slide Generator
Usage:
  python run.py                          # interactive mode
  python run.py --input deck.pptx        # PPTX file
  python run.py --input "https://docs.google.com/..." --slides 1-15
  python run.py assemble                 # chỉ chạy assemble (sau khi có ảnh từ ChatGPT)
"""
import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))
from reader import read_pptx, read_google_slides, save_raw
from analyzer import analyze_slides, save_analysis
from prompts import export_image_prompts, wait_for_images
from assembler import assemble_html, assemble_pptx


def main():
    parser = argparse.ArgumentParser(description="AI Report Slide Generator")
    parser.add_argument("command", nargs="?", default="full",
                        choices=["full", "assemble"],
                        help="full = full pipeline | assemble = chỉ ghép (khi đã có ảnh)")
    parser.add_argument("--input", "-i", help="PPTX file path hoặc Google Slides URL")
    parser.add_argument("--slides", "-s", default="all",
                        help="Slide range: '1-15', '3-10', 'all'")
    parser.add_argument("--type", "-t", default="Management Report",
                        help="Report type: 'Weekly Report', 'Business Review', etc.")
    parser.add_argument("--compression", "-c", default="Medium",
                        choices=["Light", "Medium", "Aggressive"])
    parser.add_argument("--style", default="Modern Corporate",
                        choices=["Corporate", "Executive", "Modern Corporate",
                                 "Data-driven", "Minimal", "Premium"])
    parser.add_argument("--lang", default="auto",
                        help="Output language: auto, Vietnamese, English, Bilingual")
    parser.add_argument("--no-wait", action="store_true",
                        help="Không chờ ảnh ChatGPT, tạo placeholder ngay")
    args = parser.parse_args()

    # ─── Determine output directory ───────────────────────────────────────────
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(__file__).parent / "output" / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)
    images_dir = output_dir / "images"
    images_dir.mkdir(exist_ok=True)

    analysis_file = output_dir / "analysis.json"

    # ─── ASSEMBLE ONLY mode ───────────────────────────────────────────────────
    if args.command == "assemble":
        # Tìm analysis.json mới nhất
        analysis_file = _find_latest_analysis()
        if not analysis_file:
            print("Lỗi: Không tìm thấy analysis.json. Hãy chạy full pipeline trước.")
            sys.exit(1)

        with open(analysis_file, encoding="utf-8") as f:
            analysis = json.load(f)
        images_dir = analysis_file.parent / "images"
        _assemble(analysis, str(images_dir), analysis_file.parent, timestamp)
        return

    # ─── FULL PIPELINE ────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("  AI REPORT SLIDE GENERATOR")
    print("=" * 60)

    # 1. Get input
    input_source = args.input
    if not input_source:
        print("\nPaste Google Slides URL hoặc nhập đường dẫn PPTX file:")
        input_source = input("> ").strip()

    slide_range = args.slides
    if slide_range == "all" and not args.input:
        print(f"\nSlide range (ví dụ: 1-20, 3-10, all) [default: all]:")
        r = input("> ").strip()
        if r:
            slide_range = r

    # 2. Read
    print(f"\n[1/5] Đọc slides ({slide_range})...")
    slides = _read(input_source, slide_range)
    save_raw(slides, str(output_dir / "raw_slides.json"))
    print(f"      → Đọc được {len(slides)} slides")

    # 3. Analyze
    print(f"\n[2/5] Phân tích nội dung với Claude AI...")
    analysis = analyze_slides(
        slides,
        report_type=args.type,
        compression=args.compression,
        language=args.lang,
        style=args.style,
    )
    save_analysis(analysis, str(analysis_file))

    total_out = len(analysis.get("output_slides", []))
    print(f"      → {len(slides)} slides → {total_out} output slides")

    # 4. Image prompts
    print(f"\n[3/5] Xuất image prompts cho ChatGPT...")
    needed = export_image_prompts(analysis, str(images_dir))

    if needed and not args.no_wait:
        wait_for_images(needed, timeout_seconds=1800)  # 30 phút timeout
    elif needed and args.no_wait:
        from prompts import _create_placeholders
        _create_placeholders(needed)

    # 5. Assemble
    print(f"\n[4/5] Tạo HTML slides + PPTX...")
    _assemble(analysis, str(images_dir), output_dir, timestamp)

    # 6. Summary
    print(f"\n[5/5] Quality check + Summary")
    _print_summary(analysis, output_dir)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _read(source: str, slide_range: str) -> list[dict]:
    if source.startswith("http"):
        return read_google_slides(source, slide_range)
    else:
        if not Path(source).exists():
            print(f"Lỗi: File không tồn tại: {source}")
            sys.exit(1)
        return read_pptx(source, slide_range)


def _assemble(analysis: dict, images_dir: str, output_dir: Path, timestamp: str):
    html_path = output_dir / f"report_{timestamp}.html"
    pptx_path = output_dir / f"report_{timestamp}.pptx"

    # Detect branding từ analysis nếu có
    brand = analysis.get("brand")

    assemble_html(analysis, images_dir, str(html_path), brand)
    assemble_pptx(analysis, images_dir, str(pptx_path), brand)

    print(f"\n{'='*60}")
    print(f"  ✓ DONE")
    print(f"{'='*60}")
    print(f"  HTML:  {html_path}")
    print(f"  PPTX:  {pptx_path}")
    print(f"{'='*60}\n")

    # Auto-open HTML
    import subprocess
    try:
        subprocess.run(["open", str(html_path)], check=False)
    except Exception:
        pass


def _find_latest_analysis() -> Path | None:
    output_base = Path(__file__).parent / "output"
    analyses = sorted(output_base.glob("*/analysis.json"), key=lambda p: p.stat().st_mtime)
    return analyses[-1] if analyses else None


def _print_summary(analysis: dict, output_dir: Path):
    summary = analysis.get("analysis_summary", [])
    if not summary:
        return

    print("\n  Analysis Summary:")
    print(f"  {'Input Slides':<15} {'Topic':<25} {'Key Insight':<35} {'Output'}")
    print(f"  {'-'*15} {'-'*25} {'-'*35} {'-'*8}")
    for row in summary:
        print(f"  {str(row.get('input_slides','')):<15} "
              f"{str(row.get('topic',''))[:24]:<25} "
              f"{str(row.get('key_insight',''))[:34]:<35} "
              f"Slide {row.get('output_slide','?')}")

    out_slides = analysis.get("output_slides", [])
    print(f"\n  Total: {analysis.get('total_input_slides','?')} input → "
          f"{len(out_slides)} output slides")
    print(f"  Output: {output_dir}")


if __name__ == "__main__":
    main()
