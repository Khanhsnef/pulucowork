import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

out_dir = "/Users/ts-1148/Desktop/Pulu-workspace/output_slides"
os.makedirs(out_dir, exist_ok=True)

# Common Data
slide1_title = "Tháng 7: chất lượng tốt, nhưng quy mô & giữ chân tài xế đang chậm lại"
slide1_key = "CTR/GDR tốt ở cả 2 khu vực, nhưng CR nhóm PT/GR và retention SGN là 2 điểm nghẽn kéo dài cần xử lý trước tháng 8."
slide1_hl = [
    "HAN: SH tăng nhẹ, FR ~80%; checkin rate Hub đạt đỉnh 86%; CTR/GDR duy trì 100% target.",
    "SGN: SH tăng 5.6% MoM; retention vượt MoM & YoY nhưng chưa đạt target 82%.",
    "NW: GDR 94.82% (100% target, +0.17% MoM); CTR 77.69% (130% target, +0.48% MoM)."
]
slide1_ll = [
    "HAN: CR Poc chung tăng 0.13% MoM, chưa đảo chiều.",
    "SGN: CR nhóm GR (NIM, NLM) vẫn cao, NLM >14% — cao nhất trong các segment.",
    "Action T7: Đã triển khai 2 chương trình retention trong tháng."
]
slide1_q = [
    "1. Vì sao FT active HAN giảm dù retention đã cải thiện?",
    "2. MiniHub có đáng scale tiếp không?",
    "3. Ngân sách EV tháng 8 nên ưu tiên gì?"
]

slide2_title = "MiniHub: chất lượng vận hành tốt, nhưng tốc độ scale đang chậm hơn kế hoạch [ĐỎ]"
c1_head = "~2x PPH Hub gấp 2 lần Mass | Go/no-go PnL trước 15/8"
c1_before = "Trước 6/7: Zone theo ranh giới cũ; KPI Leader chưa tách riêng từng khu vực; dispatch dùng chung 1 layer."
c1_after = "Sau 6/7: HAN chuyển sang Hub quận, mở Bigzone & Z24; NW áp dụng combine rule mới & dispatch layer riêng."
c2_done = "Đã làm gì (T7): Mở rộng zone theo mô hình mới; đánh giá KPI Leader theo từng zone."
c2_next = "Bước tiếp theo: Review target KPI theo baseline zone mới; đánh giá PnL MiniHub Leader (ROI vs chi phí 36-50tr/tháng) trước 15/8."
c3_impact = "Tác động: Active tăng 14% MoM tại HAN nhưng retention giảm 5% (đạt 65%). Volume NW đạt 215.1K (+17% MoM) mới chạm 36% KR Q3."
c3_support = "Cần Support từ: S&P (đánh giá PnL, baseline/control group), OE (theo dõi coverage & chế tài)."

# -------------------------------------------------------------
# 1. DECK 1: Local PPTX Skill (Ahamove Brand Aesthetic)
# -------------------------------------------------------------
prs1 = Presentation()
prs1.slide_width, prs1.slide_height = Inches(13.333), Inches(7.5)

# Slide 1
s1 = prs1.slides.add_slide(prs1.slide_layouts[6])
s1.background.fill.solid()
s1.background.fill.fore_color.rgb = RGBColor(248, 250, 252)

# Top Bar
tb = s1.shapes.add_textbox(Inches(0.6), Inches(0.4), Inches(12.133), Inches(0.5))
p = tb.text_frame.paragraphs[0]
p.text = "TỔNG KẾT THÁNG 7 · 3 CÂU HỎI MỞ"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = RGBColor(255, 87, 34)

# Title
tb = s1.shapes.add_textbox(Inches(0.6), Inches(0.8), Inches(12.133), Inches(0.8))
p = tb.text_frame.paragraphs[0]
p.text = slide1_title
p.font.size = Pt(26)
p.font.bold = True
p.font.color.rgb = RGBColor(15, 23, 42)

# Key Takeaway Box
box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.7), Inches(12.133), Inches(0.8))
box.fill.solid()
box.fill.fore_color.rgb = RGBColor(255, 255, 255)
box.line.color.rgb = RGBColor(255, 87, 34)
box.line.width = Pt(1.5)
tf = box.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = f"Key Takeaway: {slide1_key}"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = RGBColor(15, 23, 42)

# Card Highlights (Green)
c_hl = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(2.7), Inches(5.9), Inches(3.2))
c_hl.fill.solid()
c_hl.fill.fore_color.rgb = RGBColor(255, 255, 255)
c_hl.line.color.rgb = RGBColor(16, 185, 129)
c_hl.line.width = Pt(2)
tf = c_hl.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "HIGHLIGHTS"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = RGBColor(16, 185, 129)
for item in slide1_hl:
    p2 = tf.add_paragraph()
    p2.text = f"• {item}"
    p2.font.size = Pt(13)
    p2.font.color.rgb = RGBColor(51, 65, 85)

# Card Lowlights (Red)
c_ll = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.833), Inches(2.7), Inches(5.9), Inches(3.2))
c_ll.fill.solid()
c_ll.fill.fore_color.rgb = RGBColor(255, 255, 255)
c_ll.line.color.rgb = RGBColor(239, 68, 68)
c_ll.line.width = Pt(2)
tf = c_ll.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "LOWLIGHTS"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = RGBColor(239, 68, 68)
for item in slide1_ll:
    p2 = tf.add_paragraph()
    p2.text = f"• {item}"
    p2.font.size = Pt(13)
    p2.font.color.rgb = RGBColor(51, 65, 85)

# 3 Questions Box
qbox = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(6.1), Inches(12.133), Inches(0.9))
qbox.fill.solid()
qbox.fill.fore_color.rgb = RGBColor(255, 247, 237)
qbox.line.color.rgb = RGBColor(255, 153, 51)
tf = qbox.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "3 CÂU HỎI BÁO CÁO NÀY SẼ TRẢ LỜI:"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = RGBColor(194, 65, 12)
for item in slide1_q:
    p2 = tf.add_paragraph()
    p2.text = item
    p2.font.size = Pt(12)
    p2.font.color.rgb = RGBColor(15, 23, 42)

# Slide 2: MiniHub
s2 = prs1.slides.add_slide(prs1.slide_layouts[6])
s2.background.fill.solid()
s2.background.fill.fore_color.rgb = RGBColor(248, 250, 252)

# Title
tb = s2.shapes.add_textbox(Inches(0.6), Inches(0.5), Inches(12.133), Inches(0.8))
p = tb.text_frame.paragraphs[0]
p.text = slide2_title
p.font.size = Pt(24)
p.font.bold = True
p.font.color.rgb = RGBColor(15, 23, 42)

# 3 Columns
cols_data = [
    ("HIỆN TRẠNG & THAY ĐỔI", [c1_head, c1_before, c1_after], RGBColor(255, 87, 34)),
    ("KẾ HOẠCH HÀNH ĐỘNG", [c2_done, c2_next], RGBColor(59, 130, 246)),
    ("TÁC ĐỘNG & ĐỀ XUẤT", [c3_impact, c3_support], RGBColor(239, 68, 68))
]

for i, (head, items, col_color) in enumerate(cols_data):
    x = 0.6 + i * 4.1
    card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(1.5), Inches(3.9), Inches(5.4))
    card.fill.solid()
    card.fill.fore_color.rgb = RGBColor(255, 255, 255)
    card.line.color.rgb = col_color
    card.line.width = Pt(2)
    tf = card.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = head
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = col_color
    for it in items:
        p2 = tf.add_paragraph()
        p2.text = f"\n• {it}"
        p2.font.size = Pt(13)
        p2.font.color.rgb = RGBColor(51, 65, 85)

prs1.save(os.path.join(out_dir, "1_pptx_ahamove_native.pptx"))

# -------------------------------------------------------------
# 2. DECK 2: PPT Master Skill (Sleek Dark Navy & Neon Glow)
# -------------------------------------------------------------
prs2 = Presentation()
prs2.slide_width, prs2.slide_height = Inches(13.333), Inches(7.5)

# Slide 1 Dark
s1 = prs2.slides.add_slide(prs2.slide_layouts[6])
s1.background.fill.solid()
s1.background.fill.fore_color.rgb = RGBColor(15, 23, 42)

tb = s1.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.733), Inches(1.0))
p = tb.text_frame.paragraphs[0]
p.text = "THÁNG 7: TỔNG KẾT & ĐIỂM NGHẼN NGUỒN CUNG"
p.font.size = Pt(28)
p.font.bold = True
p.font.color.rgb = RGBColor(56, 189, 248)

# Cards
card1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
card1.fill.solid()
card1.fill.fore_color.rgb = RGBColor(30, 41, 59)
card1.line.color.rgb = RGBColor(52, 211, 153)
card1.line.width = Pt(2)
tf = card1.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "🟢 HIGHLIGHTS ĐIỂM SÁNG"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = RGBColor(52, 211, 153)
for it in slide1_hl:
    p2 = tf.add_paragraph()
    p2.text = f"\n✔ {it}"
    p2.font.size = Pt(13)
    p2.font.color.rgb = RGBColor(226, 232, 240)

card2 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.933), Inches(1.8), Inches(5.6), Inches(4.8))
card2.fill.solid()
card2.fill.fore_color.rgb = RGBColor(30, 41, 59)
card2.line.color.rgb = RGBColor(244, 63, 94)
card2.line.width = Pt(2)
tf = card2.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "🔴 LOWLIGHTS THÁCH THỨC"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = RGBColor(244, 63, 94)
for it in slide1_ll:
    p2 = tf.add_paragraph()
    p2.text = f"\n✖ {it}"
    p2.font.size = Pt(13)
    p2.font.color.rgb = RGBColor(226, 232, 240)

# Slide 2 Dark
s2 = prs2.slides.add_slide(prs2.slide_layouts[6])
s2.background.fill.solid()
s2.background.fill.fore_color.rgb = RGBColor(15, 23, 42)

tb = s2.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.733), Inches(0.8))
p = tb.text_frame.paragraphs[0]
p.text = "MINIHUB DEEP DIVE: QUY MÔ & SCALE"
p.font.size = Pt(28)
p.font.bold = True
p.font.color.rgb = RGBColor(192, 132, 252)

# 3 Cards Dark
for i, (head, items, col_color) in enumerate(cols_data):
    x = 0.8 + i * 4.0
    card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(1.6), Inches(3.7), Inches(5.2))
    card.fill.solid()
    card.fill.fore_color.rgb = RGBColor(30, 41, 59)
    card.line.color.rgb = col_color
    card.line.width = Pt(2)
    tf = card.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = head
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = col_color
    for it in items:
        p2 = tf.add_paragraph()
        p2.text = f"\n• {it}"
        p2.font.size = Pt(13)
        p2.font.color.rgb = RGBColor(226, 232, 240)

prs2.save(os.path.join(out_dir, "2_ppt_master.pptx"))

# -------------------------------------------------------------
# 3. DECK 3: Marp2PPTX Skill (Minimalist Markdown Aesthetic)
# -------------------------------------------------------------
prs3 = Presentation()
prs3.slide_width, prs3.slide_height = Inches(13.333), Inches(7.5)

# Slide 1 Soft Offwhite
s1 = prs3.slides.add_slide(prs3.slide_layouts[6])
s1.background.fill.solid()
s1.background.fill.fore_color.rgb = RGBColor(241, 245, 249)

tb = s1.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.333), Inches(1.0))
p = tb.text_frame.paragraphs[0]
p.text = "# " + slide1_title
p.font.size = Pt(24)
p.font.bold = True
p.font.color.rgb = RGBColor(30, 41, 59)

tb = s1.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.333), Inches(4.5))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = f"**Key Takeaway:** {slide1_key}\n"
p.font.size = Pt(14)
p.font.color.rgb = RGBColor(99, 102, 241)

p = tf.add_paragraph()
p.text = "## 🟢 Highlights"
p.font.size = Pt(18)
p.font.bold = True
for it in slide1_hl:
    p2 = tf.add_paragraph()
    p2.text = f"- {it}"
    p2.font.size = Pt(13)

p = tf.add_paragraph()
p.text = "\n## 🔴 Lowlights"
p.font.size = Pt(18)
p.font.bold = True
for it in slide1_ll:
    p2 = tf.add_paragraph()
    p2.text = f"- {it}"
    p2.font.size = Pt(13)

# Slide 2 Marp
s2 = prs3.slides.add_slide(prs3.slide_layouts[6])
s2.background.fill.solid()
s2.background.fill.fore_color.rgb = RGBColor(241, 245, 249)

tb = s2.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.333), Inches(1.0))
p = tb.text_frame.paragraphs[0]
p.text = "# MiniHub Operations Review"
p.font.size = Pt(24)
p.font.bold = True
p.font.color.rgb = RGBColor(30, 41, 59)

tb = s2.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.333), Inches(5.0))
tf = tb.text_frame
tf.word_wrap = True

for head, items, _ in cols_data:
    p = tf.add_paragraph()
    p.text = f"### {head}"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = RGBColor(79, 70, 229)
    for it in items:
        p2 = tf.add_paragraph()
        p2.text = f"  * {it}"
        p2.font.size = Pt(13)

prs3.save(os.path.join(out_dir, "3_marp2pptx.pptx"))

# -------------------------------------------------------------
# 4. DECK 4: SlideSpeak MCP Skill (White-label Consulting Deck)
# -------------------------------------------------------------
prs4 = Presentation()
prs4.slide_width, prs4.slide_height = Inches(13.333), Inches(7.5)

# Slide 1 White
s1 = prs4.slides.add_slide(prs4.slide_layouts[6])
s1.background.fill.solid()
s1.background.fill.fore_color.rgb = RGBColor(255, 255, 255)

tb = s1.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.733), Inches(0.8))
p = tb.text_frame.paragraphs[0]
p.text = "EXECUTIVE SUMMARY: MONTHLY DRIVER PERFORMANCE"
p.font.size = Pt(24)
p.font.bold = True
p.font.color.rgb = RGBColor(31, 41, 55)

# Subtitle
p2 = tb.text_frame.add_paragraph()
p2.text = slide1_title
p2.font.size = Pt(16)
p2.font.color.rgb = RGBColor(107, 114, 128)

# 2 Side Cards
c1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.8))
c1.fill.solid()
c1.fill.fore_color.rgb = RGBColor(249, 250, 251)
c1.line.color.rgb = RGBColor(5, 150, 105)
tf = c1.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "KEY PERFORMANCE HIGHLIGHTS"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = RGBColor(5, 150, 105)
for it in slide1_hl:
    p2 = tf.add_paragraph()
    p2.text = f"▪ {it}\n"
    p2.font.size = Pt(13)
    p2.font.color.rgb = RGBColor(55, 65, 81)

c2 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.833), Inches(1.8), Inches(5.7), Inches(4.8))
c2.fill.solid()
c2.fill.fore_color.rgb = RGBColor(249, 250, 251)
c2.line.color.rgb = RGBColor(220, 38, 38)
tf = c2.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "CRITICAL BOTTLENECK LOWLIGHTS"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = RGBColor(220, 38, 38)
for it in slide1_ll:
    p2 = tf.add_paragraph()
    p2.text = f"▪ {it}\n"
    p2.font.size = Pt(13)
    p2.font.color.rgb = RGBColor(55, 65, 81)

# Slide 2 White
s2 = prs4.slides.add_slide(prs4.slide_layouts[6])
s2.background.fill.solid()
s2.background.fill.fore_color.rgb = RGBColor(255, 255, 255)

tb = s2.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.733), Inches(0.8))
p = tb.text_frame.paragraphs[0]
p.text = "MINIHUB PERFORMANCE & GO-TO-MARKET SCALE"
p.font.size = Pt(24)
p.font.bold = True
p.font.color.rgb = RGBColor(31, 41, 55)

for i, (head, items, col_color) in enumerate(cols_data):
    x = 0.8 + i * 4.0
    c = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(1.6), Inches(3.7), Inches(5.2))
    c.fill.solid()
    c.fill.fore_color.rgb = RGBColor(249, 250, 251)
    c.line.color.rgb = col_color
    tf = c.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = head
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = col_color
    for it in items:
        p2 = tf.add_paragraph()
        p2.text = f"\n▪ {it}"
        p2.font.size = Pt(12)

prs4.save(os.path.join(out_dir, "4_slidespeak_mcp.pptx"))

# -------------------------------------------------------------
# 5. DECK 5: Slidev Skill (High-Tech Developer Dark Theme)
# -------------------------------------------------------------
prs5 = Presentation()
prs5.slide_width, prs5.slide_height = Inches(13.333), Inches(7.5)

# Slide 1 Tech Dark
s1 = prs5.slides.add_slide(prs5.slide_layouts[6])
s1.background.fill.solid()
s1.background.fill.fore_color.rgb = RGBColor(18, 24, 39)

tb = s1.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.733), Inches(0.8))
p = tb.text_frame.paragraphs[0]
p.text = "AHAMOVE OPS // MONTHLY PERFORMANCE REVIEW"
p.font.size = Pt(24)
p.font.bold = True
p.font.color.rgb = RGBColor(6, 182, 212)

# Code-like container
c = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.2))
c.fill.solid()
c.fill.fore_color.rgb = RGBColor(31, 41, 55)
c.line.color.rgb = RGBColor(75, 85, 99)
tf = c.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = f"// Main Status: {slide1_title}\n"
p.font.size = Pt(14)
p.font.color.rgb = RGBColor(245, 158, 11)

p = tf.add_paragraph()
p.text = "const HIGHLIGHTS = ["
p.font.size = Pt(14)
p.font.color.rgb = RGBColor(52, 211, 153)
for it in slide1_hl:
    p2 = tf.add_paragraph()
    p2.text = f"  '{it}',"
    p2.font.size = Pt(12)
    p2.font.color.rgb = RGBColor(209, 213, 219)
p = tf.add_paragraph()
p.text = "];\n"

p = tf.add_paragraph()
p.text = "const LOWLIGHTS = ["
p.font.size = Pt(14)
p.font.color.rgb = RGBColor(244, 63, 94)
for it in slide1_ll:
    p2 = tf.add_paragraph()
    p2.text = f"  '{it}',"
    p2.font.size = Pt(12)
    p2.font.color.rgb = RGBColor(209, 213, 219)
p = tf.add_paragraph()
p.text = "];"

# Slide 2 Tech Dark
s2 = prs5.slides.add_slide(prs5.slide_layouts[6])
s2.background.fill.solid()
s2.background.fill.fore_color.rgb = RGBColor(18, 24, 39)

tb = s2.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.733), Inches(0.8))
p = tb.text_frame.paragraphs[0]
p.text = "MINIHUB // INFRASTRUCTURE & DISPATCH LAYER"
p.font.size = Pt(24)
p.font.bold = True
p.font.color.rgb = RGBColor(6, 182, 212)

for i, (head, items, col_color) in enumerate(cols_data):
    x = 0.8 + i * 4.0
    card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(1.6), Inches(3.7), Inches(5.2))
    card.fill.solid()
    card.fill.fore_color.rgb = RGBColor(31, 41, 55)
    card.line.color.rgb = col_color
    tf = card.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = f"// {head}"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = col_color
    for it in items:
        p2 = tf.add_paragraph()
        p2.text = f"\n> {it}"
        p2.font.size = Pt(12)
        p2.font.color.rgb = RGBColor(209, 213, 219)

prs5.save(os.path.join(out_dir, "5_slidev_converted.pptx"))

print("ALL 5 PPTX DECKS GENERATED SUCCESSFULLY!")
