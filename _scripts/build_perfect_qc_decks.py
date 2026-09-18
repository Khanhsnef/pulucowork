import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

out_dir = "/Users/ts-1148/Desktop/Pulu-workspace/output_slides"
os.makedirs(out_dir, exist_ok=True)

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)

# SLIDE 1: Executive Summary
s1 = prs.slides.add_slide(prs.slide_layouts[6])
s1.background.fill.solid()
s1.background.fill.fore_color.rgb = RGBColor(248, 250, 252)

# Top Bar
tb = s1.shapes.add_textbox(Inches(0.6), Inches(0.4), Inches(12.133), Inches(0.4))
tf = tb.text_frame
tf.vertical_anchor = MSO_ANCHOR.MIDDLE
p = tf.paragraphs[0]
p.text = "TỔNG KẾT THÁNG 7 · 3 CÂU HỎI MỞ"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = RGBColor(255, 87, 34)

# Header Title
tb_t = s1.shapes.add_textbox(Inches(0.6), Inches(0.85), Inches(12.133), Inches(0.65))
tf_t = tb_t.text_frame
tf_t.word_wrap = True
tf_t.vertical_anchor = MSO_ANCHOR.MIDDLE
p = tf_t.paragraphs[0]
p.text = "Tháng 7: chất lượng tốt, nhưng quy mô & giữ chân tài xế đang chậm lại"
p.font.size = Pt(24)
p.font.bold = True
p.font.color.rgb = RGBColor(15, 23, 42)

# Key Takeaway Box (Vertically Centered)
kt_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.6), Inches(12.133), Inches(0.75))
kt_box.fill.solid()
kt_box.fill.fore_color.rgb = RGBColor(255, 255, 255)
kt_box.line.color.rgb = RGBColor(255, 87, 34)
kt_box.line.width = Pt(1.5)
tf = kt_box.text_frame
tf.word_wrap = True
tf.vertical_anchor = MSO_ANCHOR.MIDDLE
tf.margin_left = Inches(0.2)
tf.margin_right = Inches(0.2)
p = tf.paragraphs[0]
p.text = "Key Takeaway: CTR/GDR tốt ở cả 2 khu vực, nhưng CR nhóm PT/GR và retention SGN là 2 điểm nghẽn kéo dài cần xử lý trước tháng 8."
p.font.size = Pt(13.5)
p.font.bold = True
p.font.color.rgb = RGBColor(30, 41, 59)

# Highlights & Lowlights Cards (Symmetric Top & Baseline)
hl_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(2.55), Inches(5.9), Inches(3.45))
hl_box.fill.solid()
hl_box.fill.fore_color.rgb = RGBColor(255, 255, 255)
hl_box.line.color.rgb = RGBColor(16, 185, 129)
hl_box.line.width = Pt(2)
tf_hl = hl_box.text_frame
tf_hl.word_wrap = True
tf_hl.vertical_anchor = MSO_ANCHOR.MIDDLE
tf_hl.margin_left = Inches(0.25)
tf_hl.margin_right = Inches(0.25)

p = tf_hl.paragraphs[0]
p.text = "HIGHLIGHTS"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = RGBColor(16, 185, 129)

hl_items = [
    "HAN: SH tăng nhẹ, FR ~80%; checkin rate Hub đạt đỉnh 86%; CTR/GDR duy trì 100% target.",
    "SGN: SH tăng 5.6% MoM; retention vượt MoM & YoY nhưng chưa đạt target 82%.",
    "NW: GDR 94.82% (100% target, +0.17% MoM); CTR 77.69% (130% target, +0.48% MoM)."
]
for item in hl_items:
    p2 = tf_hl.add_paragraph()
    p2.text = f"• {item}"
    p2.font.size = Pt(12.5)
    p2.space_before = Pt(6)
    p2.font.color.rgb = RGBColor(51, 65, 85)

ll_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.833), Inches(2.55), Inches(5.9), Inches(3.45))
ll_box.fill.solid()
ll_box.fill.fore_color.rgb = RGBColor(255, 255, 255)
ll_box.line.color.rgb = RGBColor(239, 68, 68)
ll_box.line.width = Pt(2)
tf_ll = ll_box.text_frame
tf_ll.word_wrap = True
tf_ll.vertical_anchor = MSO_ANCHOR.MIDDLE
tf_ll.margin_left = Inches(0.25)
tf_ll.margin_right = Inches(0.25)

p = tf_ll.paragraphs[0]
p.text = "LOWLIGHTS"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = RGBColor(239, 68, 68)

ll_items = [
    "HAN: CR Poc chung tăng 0.13% MoM, chưa đảo chiều.",
    "SGN: CR nhóm GR (NIM, NLM) vẫn cao, NLM >14% — cao nhất trong các segment.",
    "Action T7: Đã triển khai 2 chương trình retention trong tháng."
]
for item in ll_items:
    p2 = tf_ll.add_paragraph()
    p2.text = f"• {item}"
    p2.font.size = Pt(12.5)
    p2.space_before = Pt(6)
    p2.font.color.rgb = RGBColor(51, 65, 85)

# Bottom Questions Box
q_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(6.15), Inches(12.133), Inches(0.85))
q_box.fill.solid()
q_box.fill.fore_color.rgb = RGBColor(255, 247, 237)
q_box.line.color.rgb = RGBColor(255, 153, 51)
tf_q = q_box.text_frame
tf_q.word_wrap = True
tf_q.vertical_anchor = MSO_ANCHOR.MIDDLE
tf_q.margin_left = Inches(0.2)
tf_q.margin_right = Inches(0.2)
p = tf_q.paragraphs[0]
p.text = "3 CÂU HỎI BÁO CÁO NÀY SẼ TRẢ LỜI:"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = RGBColor(194, 65, 12)
p_qs = tf_q.add_paragraph()
p_qs.text = "1. Vì sao FT active HAN giảm dù retention đã cải thiện?   2. MiniHub có đáng scale tiếp không?   3. Ngân sách EV tháng 8 nên ưu tiên gì?"
p_qs.font.size = Pt(12)
p_qs.space_before = Pt(3)
p_qs.font.color.rgb = RGBColor(15, 23, 42)

# SLIDE 2: MiniHub Deep Dive
s2 = prs.slides.add_slide(prs.slide_layouts[6])
s2.background.fill.solid()
s2.background.fill.fore_color.rgb = RGBColor(248, 250, 252)

tb = s2.shapes.add_textbox(Inches(0.6), Inches(0.5), Inches(12.133), Inches(0.8))
tf = tb.text_frame
tf.vertical_anchor = MSO_ANCHOR.MIDDLE
p = tf.paragraphs[0]
p.text = "MiniHub: chất lượng vận hành tốt, nhưng tốc độ scale đang chậm hơn kế hoạch [ĐỎ]"
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = RGBColor(15, 23, 42)

# 3 Columns with Vertical Centering
cols = [
    ("HIỆN TRẠNG & CHUYỂN ĐỔI", [
        "~2x PPH Hub gấp ~2 lần Mass | Go/no-go PnL trước 15/8.",
        "TRƯỚC 6/7: Zone theo ranh giới cũ; KPI Leader chưa tách riêng từng khu vực; dispatch dùng chung 1 layer.",
        "SAU 6/7: HAN chuyển sang Hub quận, mở Bigzone & Z24; NW áp dụng combine rule mới & dispatch layer riêng."
    ], RGBColor(255, 87, 34)),
    ("KẾ HOẠCH HÀNH ĐỘNG", [
        "1. ĐÃ LÀM GÌ (T7): Mở rộng zone theo mô hình mới; đánh giá KPI Leader theo từng zone.",
        "2. BƯỚC TIẾP THEO: Review target KPI theo baseline zone mới; đánh giá PnL MiniHub Leader (ROI vs chi phí 36-50tr/tháng) trước 15/8."
    ], RGBColor(59, 130, 246)),
    ("TÁC ĐỘNG & ĐỀ XUẤT", [
        "TÁC ĐỘNG: Active tăng 14% MoM tại HAN nhưng retention giảm 5% (đạt 65%). Volume NW đạt 215.1K (+17% MoM) mới chạm 36% KR Q3.",
        "CẦN SUPPORT TỪ: S&P (đánh giá PnL, baseline/control group), OE (theo dõi coverage & chế tài)."
    ], RGBColor(239, 68, 68))
]

for i, (title, points, col_color) in enumerate(cols):
    x = 0.6 + i * 4.1
    card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(1.5), Inches(3.9), Inches(5.4))
    card.fill.solid()
    card.fill.fore_color.rgb = RGBColor(255, 255, 255)
    card.line.color.rgb = col_color
    card.line.width = Pt(1.5)
    tf = card.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.2)
    tf.margin_right = Inches(0.2)
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = col_color
    
    for pt in points:
        p2 = tf.add_paragraph()
        p2.text = f"• {pt}"
        p2.font.size = Pt(12)
        p2.space_before = Pt(8)
        p2.font.color.rgb = RGBColor(51, 65, 85)

out_file = os.path.join(out_dir, "perfect_qc_ahamove_presentation.pptx")
prs.save(out_file)
print(f"Saved Perfect QC PPTX to {out_file}")
