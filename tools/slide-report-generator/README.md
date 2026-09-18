# AI Report Slide Generator

Tự động biến presentation thành executive report deck 16:9 chuyên nghiệp.

## Setup

```bash
cd tools/slide-report-generator
pip install -r requirements.txt

cp .env.example .env
# Điền ANTHROPIC_API_KEY vào .env
```

## Usage

### Interactive (đơn giản nhất)
```bash
python run.py
# → Nhập URL hoặc path PPTX
# → Nhập slide range (ví dụ: 1-20)
```

### Command line
```bash
# PPTX file
python run.py --input my_deck.pptx --slides 1-20 --type "Weekly Report"

# Google Slides (file phải public)
python run.py --input "https://docs.google.com/presentation/d/xxx" --slides 1-15

# Options
python run.py --input deck.pptx \
  --slides 1-25 \
  --type "Business Review" \
  --compression Aggressive \
  --style "Executive" \
  --lang Vietnamese
```

### Chỉ assemble (sau khi đã gen ảnh từ ChatGPT)
```bash
python run.py assemble
```

## Pipeline

```
Input (PPTX/GSlides)
  ↓
[reader.py]   Đọc tất cả slide content
  ↓
[analyzer.py] Claude AI analyze + compress + tạo storyline
  ↓
[prompts.py]  Xuất image prompts → User gen trên ChatGPT → Lưu ảnh vào output/images/
  ↓
[assembler.py] Ghép HTML + PPTX
  ↓
Output: report_YYYYMMDD.html + report_YYYYMMDD.pptx
```

## Image Generation Flow

1. Script in ra danh sách prompts
2. Mở ChatGPT web → paste từng prompt → gen ảnh
3. Download ảnh, đặt tên đúng (vd: `slide_03_image.png`)
4. Lưu vào `output/[timestamp]/images/`
5. Script tự detect và ghép vào slide

## Compression Levels

| Level | Behavior |
|---|---|
| Light | Giữ nhiều thông tin, merge duplicate |
| Medium | Ưu tiên insight, ~40% reduction |
| Aggressive | Key message + data + action only, ~60-70% reduction |

## Cấu trúc Output

```
output/
└── YYYYMMDD_HHMMSS/
    ├── raw_slides.json     # Data gốc từ input
    ├── analysis.json       # Storyline từ Claude
    ├── image_prompts.txt   # Prompts cho ChatGPT
    ├── images/             # Ảnh từ ChatGPT (user lưu vào đây)
    ├── report_*.html       # Preview + Export
    └── report_*.pptx       # Editable PPTX
```
