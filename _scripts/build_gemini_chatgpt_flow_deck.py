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

# SLIDE 1: Executive Summary (Gemini & ChatGPT Asymmetric Hero Flow)
s1 = prs.slides.add_slide(prs.slide_layouts[6])
s1.background.fill.solid()
s1.background.fill.fore_color.rgb = RGBColor(248, 250, 252) # Soft slate background

# Top Bar
tb = s1.shapes.add_textbox(Inches(0.6), Inches(0.35), Inches(12.133), Inches(0.4))
tf = tb.text_frame
tf.vertical_anchor = MSO_ANCHOR.MIDDLE
p = tf.paragraphs[0]
p.text = "TỔNG KẾT THÁNG 7 · BÁO CÁO NGUỒN CUNG AHAMOVE"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = RGBColor(255, 87, 34)

# Headline Title (Hero Focal Point Top)
tb_t = s1.shapes.add_textbox(Inches(0.6), Inches(0.75), Inches(12.133), Inches(0.65))
tf_t = tb_t.text_frame
tf_t.word_wrap = True
tf_t.vertical_anchor = MSO_ANCHOR.MIDDLE
p = tf_t.paragraphs[0]
p.text = "Tháng 7: chất lượng tốt, nhưng quy mô & giữ chân tài xế đang chậm lại"
p.font.size = Pt(24)
p.font.bold = True
p.font.color.rgb = RGBColor(15, 23, 42)

# Key Takeaway Banner
kt_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.5), Inches(12.133), Inches(0.7))
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
p.text = "💡 KEY TAKEAWAY: CTR/GDR tốt ở cả 2 khu vực, nhưng CR nhóm PT/GR và retention SGN là 2 điểm nghẽn kéo dài cần xử lý trước tháng 8."
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = RGBColor(30, 41, 59)

# 1. HERO FOCAL CARD (Left 60% Width) - Asymmetric Dominance
hero = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(2.35), Inches(7.2), Inches(3.7))
hero.fill.solid()
hero.fill.fore_color.rgb = RGBColor(255, 255, 255)
hero.line.color.rgb = RGBColor(16, 185, 129)
hero.line.width = Pt(2)
tf_h = hero.text_frame
tf_h.word_wrap = True
tf_h.vertical_anchor = MSO_ANCHOR.MIDDLE
tf_h.margin_left = Inches(0.25)
tf_h.margin_right = Inches(0.25)

p = tf_h.paragraphs[0]
p.text = "🟢 HIGHLIGHTS ĐIỂM SÁNG VẬN HÀNH"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = RGBColor(16, 185, 129)

hl_items = [
    "HAN: SH tăng nhẹ, FR ~80%; checkin rate Hub đạt đỉnh 86%; CTR/GDR duy trì 100% target.",
    "SGN: SH tăng 5.6% MoM; retention vượt MoM & YoY nhưng chưa đạt target 82%.",
    "NW: GDR 94.82% (100% target, +0.17% MoM); CTR 77.69% (130% target, +0.48% MoM)."
]
for item in hl_items:
    p2 = tf_h.add_paragraph()
    p2.text = f"📈  {item}"
    p2.font.size = Pt(12.5)
    p2.space_before = Pt(8)
    p2.font.color.rgb = RGBColor(51, 65, 85)

# 2. SIDE CARD (Right 40% Width) - Bottlenecks & Lowlights
side = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.0), Inches(2.35), Inches(4.733), Inches(3.7))
side.fill.solid()
side.fill.fore_color.rgb = RGBColor(255, 255, 255)
side.line.color.rgb = RGBColor(239, 68, 68)
side.line.width = Pt(2)
tf_s = side.text_frame
tf_s.word_wrap = True
tf_s.vertical_anchor = MSO_ANCHOR.MIDDLE
tf_s.margin_left = Inches(0.25)
tf_s.margin_right = Inches(0.25)

p = tf_s.paragraphs[0]
p.text = "🔴 LOWLIGHTS THÁCH THỨC"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = RGBColor(239, 68, 68)

ll_items = [
    "HAN: CR Poc chung tăng 0.13% MoM, chưa đảo chiều.",
    "SGN: CR nhóm GR (NIM, NLM) vẫn cao, NLM >14% — cao nhất trong các segment.",
    "Action T7 ➔ Đã triển khai 2 chương trình retention trong tháng."
]
for item in ll_items:
    p2 = tf_s.add_paragraph()
    p2.text = f"🎯  {item}"
    p2.font.size = Pt(12)
    p2.space_before = Pt(8)
    p2.font.color.rgb = RGBColor(51, 65, 85)

# 3. BOTTOM PROCESS FLOW BANNER (3 Questions Connected Flow)
q_banner = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(6.2), Inches(12.133), Inches(0.8))
q_banner.fill.solid()
q_banner.fill.fore_color.rgb = RGBColor(255, 247, 237)
q_banner.line.color.rgb = RGBColor(255, 153, 51)
tf_q = q_banner.text_frame
tf_q.word_wrap = True
tf_q.vertical_anchor = MSO_ANCHOR.MIDDLE
tf_q.margin_left = Inches(0.2)
tf_q.margin_right = Inches(0.2)

p = tf_q.paragraphs[0]
p.text = "❓ 3 CÂU HỎI BÁO CÁO NÀY SẼ TRẢ LỜI:"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = RGBColor(194, 65, 12)

p_qs = tf_q.add_paragraph()
p_qs.text = "01. Vì sao FT active HAN giảm dù retention đã cải thiện?   ➔   02. MiniHub có đáng scale tiếp không?   ➔   03. Ngân sách EV tháng 8 nên ưu tiên gì?"
p_qs.font.size = Pt(12)
p_qs.space_before = Pt(2)
p_qs.font.color.rgb = RGBColor(15, 23, 42)


# SLIDE 2: MiniHub Deep Dive (Gemini Dual-Pane & Action Pipeline Flow)
s2 = prs.slides.add_slide(prs.slide_layouts[6])
s2.background.fill.solid()
s2.background.fill.fore_color.rgb = RGBColor(248, 250, 252)

# Top Bar Title
tb2 = s2.shapes.add_textbox(Inches(0.6), Inches(0.4), Inches(12.133), Inches(0.8))
tf2 = tb2.text_frame
tf2.word_wrap = True
tf2.vertical_anchor = MSO_ANCHOR.MIDDLE
p = tf2.paragraphs[0]
p.text = "MiniHub: chất lượng vận hành tốt, nhưng tốc độ scale đang chậm hơn kế hoạch [TRẠNG THÁI: ĐỎ]"
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = RGBColor(15, 23, 42)

# LEFT PANE (Hero Giant Stat & Before/After Timeline) - Width 4.5"
left_pane = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.4), Inches(4.5), Inches(5.5))
left_pane.fill.solid()
left_pane.fill.fore_color.rgb = RGBColor(255, 255, 255)
left_pane.line.color.rgb = RGBColor(255, 87, 34)
left_pane.line.width = Pt(2)
tf_lp = left_pane.text_frame
tf_lp.word_wrap = True
tf_lp.vertical_anchor = MSO_ANCHOR.MIDDLE
tf_lp.margin_left = Inches(0.25)
tf_lp.margin_right = Inches(0.25)

p = tf_lp.paragraphs[0]
p.text = "~2X PPH"
p.font.size = Pt(36)
p.font.bold = True
p.font.color.rgb = RGBColor(255, 87, 34)

p_sub = tf_lp.add_paragraph()
p_sub.text = "PPH của Hub cao gấp ~2 lần Mass ở cả 2 thành phố.\nMỤC TIÊU: Go/no-go PnL trước 15/8"
p_sub.font.size = Pt(13)
p_sub.font.bold = True
p_sub.space_before = Pt(4)
p_sub.font.color.rgb = RGBColor(30, 41, 59)

p_div = tf_lp.add_paragraph()
p_div.text = "──────────────────────────"
p_div.font.size = Pt(10)
p_div.font.color.rgb = RGBColor(203, 213, 225)

p_before = tf_lp.add_paragraph()
p_before.text = "⏳ TRƯỚC 6/7:"
p_before.font.size = Pt(13)
p_before.font.bold = True
p_before.font.color.rgb = RGBColor(239, 68, 68)
p_bt = tf_lp.add_paragraph()
p_bt.text = "Zone theo ranh giới cũ; KPI Leader chưa tách riêng từng khu vực; dispatch dùng chung 1 layer."
p_bt.font.size = Pt(12)
p_bt.font.color.rgb = RGBColor(71, 85, 105)

p_after = tf_lp.add_paragraph()
p_after.text = "🚀 SAU 6/7:"
p_after.font.size = Pt(13)
p_after.font.bold = True
p_after.space_before = Pt(6)
p_after.font.color.rgb = RGBColor(16, 185, 129)
p_at = tf_lp.add_paragraph()
p_at.text = "HAN chuyển sang Hub quận, mở Bigzone & Z24; NW áp dụng combine rule mới & dispatch layer riêng."
p_at.font.size = Pt(12)
p_at.font.color.rgb = RGBColor(71, 85, 105)


# RIGHT PANE TOP (Action Pipeline) - Width 7.433"
act_card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.3), Inches(1.4), Inches(7.433), Inches(2.6))
act_card.fill.solid()
act_card.fill.fore_color.rgb = RGBColor(255, 255, 255)
act_card.line.color.rgb = RGBColor(59, 130, 246)
act_card.line.width = Pt(1.5)
tf_ac = act_card.text_frame
tf_ac.word_wrap = True
tf_ac.vertical_anchor = MSO_ANCHOR.MIDDLE
tf_ac.margin_left = Inches(0.25)
tf_ac.margin_right = Inches(0.25)

p = tf_ac.paragraphs[0]
p.text = "⚡ KẾ HOẠCH HÀNH ĐỘNG PIPELINE"
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = RGBColor(59, 130, 246)

p1 = tf_ac.add_paragraph()
p1.text = "01. ĐÃ LÀM GÌ (T7): Mở rộng zone theo mô hình mới; đánh giá KPI Leader theo từng zone."
p1.font.size = Pt(12.5)
p1.space_before = Pt(6)
p1.font.color.rgb = RGBColor(51, 65, 85)

p2 = tf_ac.add_paragraph()
p2.text = "02. BƯỚC TIẾP THEO: Review target KPI theo baseline zone mới; đánh giá PnL MiniHub Leader (ROI vs chi phí 36-50tr/tháng) để quyết định go/no-go trước 15/8."
p2.font.size = Pt(12.5)
p2.space_before = Pt(6)
p2.font.color.rgb = RGBColor(51, 65, 85)


# RIGHT PANE BOTTOM (Impact & Support) - Width 7.433"
imp_card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.3), Inches(4.2), Inches(7.433), Inches(2.7))
imp_card.fill.solid()
imp_card.fill.fore_color.rgb = RGBColor(255, 255, 255)
imp_card.line.color.rgb = RGBColor(239, 68, 68)
imp_card.line.width = Pt(1.5)
tf_ic = imp_card.text_frame
tf_ic.word_wrap = True
tf_ic.vertical_anchor = MSO_ANCHOR.MIDDLE
tf_ic.margin_left = Inches(0.25)
tf_ic.margin_right = Inches(0.25)

p = tf_ic.paragraphs[0]
p.text = "💥 TÁC ĐỘNG & HỖ TRỢ CẦN THIẾT"
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = RGBColor(239, 68, 68)

p_i = tf_ic.add_paragraph()
p_i.text = "⚡ TÁC ĐỘNG: Active tăng 14% MoM tại HAN nhưng retention giảm 5% (chỉ đạt 65%). Volume NW đạt 215.1K (+17% MoM) nhưng mới chạm 36% KR Q3; Cityzone chỉ 30% KR. Cơ chế: zone mới rộng kéo giãn mật độ tương tác."
p_i.font.size = Pt(12)
p_i.space_before = Pt(6)
p_i.font.color.rgb = RGBColor(51, 65, 85)

p_s = tf_ic.add_paragraph()
p_s.text = "♦ CẦN SUPPORT TỪ: S&P (đánh giá PnL, baseline/control group), OE (theo dõi coverage & chế tài)."
p_s.font.size = Pt(12)
p_s.space_before = Pt(6)
p_s.font.bold = True
p_s.font.color.rgb = RGBColor(30, 41, 59)


out_file = os.path.join(out_dir, "gemini_chatgpt_flow_presentation.pptx")
prs.save(out_file)
print(f"Saved Gemini & ChatGPT Flow PPTX to {out_file}")
