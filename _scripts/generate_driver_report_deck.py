import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION

out_dir = "/Users/ts-1148/Desktop/Pulu-workspace/Output"
os.makedirs(out_dir, exist_ok=True)
pptx_path = os.path.join(out_dir, "BaoCao_VanHanh_Driver_Management_T34.pptx")

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)

# --- VIBRANT COLOR PALETTE ---
BG_COLOR = RGBColor(248, 250, 252)       # Light Slate
CARD_BG = RGBColor(255, 255, 255)        # Pure White Card
TEXT_MAIN = RGBColor(15, 23, 42)         # Deep Slate
TEXT_MUTED = RGBColor(71, 85, 105)       # Muted Slate
ORANGE_PRIMARY = RGBColor(249, 115, 22)  # Primary Orange
BLUE_ACCENT = RGBColor(37, 99, 235)      # Royal Blue
GREEN_POS = RGBColor(16, 185, 129)       # Emerald Green
RED_NEG = RGBColor(239, 68, 68)          # Alert Red
PURPLE_ACCENT = RGBColor(147, 51, 234)   # Violet
BORDER_COLOR = RGBColor(226, 232, 240)   # Light Gray Border

def apply_background(slide):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = BG_COLOR

def add_header(slide, title_text, category_badge, icon_emoji="📊"):
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(0.35), Inches(0.12), Inches(0.85))
    line.fill.solid()
    line.fill.fore_color.rgb = ORANGE_PRIMARY
    line.line.fill.background()

    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.85), Inches(0.35), Inches(3.4), Inches(0.32))
    badge.fill.solid()
    badge.fill.fore_color.rgb = RGBColor(254, 243, 199)
    badge.line.color.rgb = ORANGE_PRIMARY
    badge.line.width = Pt(1)
    tf_b = badge.text_frame
    tf_b.margin_left = Inches(0.1)
    tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf_b.paragraphs[0]
    p.text = f"  {icon_emoji}  {category_badge.upper()}"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = ORANGE_PRIMARY

    tb_t = slide.shapes.add_textbox(Inches(0.85), Inches(0.7), Inches(11.883), Inches(0.55))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
    p2 = tf_t.paragraphs[0]
    p2.text = title_text
    p2.font.size = Pt(21)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_MAIN

def add_card(slide, left, top, width, height, border_color=BORDER_COLOR, bg_color=CARD_BG):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1.5)
    return card

# ==========================================
# SLIDE 1: TỔNG QUAN DASHBOARD TUẦN 34 + PYRAMID DIAGRAM
# ==========================================
s1 = prs.slides.add_slide(prs.slide_layouts[6])
apply_background(s1)
add_header(s1, "BÁO CÁO VẬN HÀNH DRIVER MANAGEMENT — TUẦN 34 (10/08 - 16/08/2026)", "EXECUTIVE DASHBOARD & STRATEGY PYRAMID", "📈")

# 4 GIANT KPI CARDS
kpis = [
    {"num": "69%", "title": "HAN RETENTION", "sub": "CTR đạt 78.49% (130% target)", "icon": "🎯", "color": GREEN_POS, "bg": RGBColor(236, 253, 245)},
    {"num": "120%", "title": "NW GDR TARGET", "sub": "Đạt target, quan tâm tài xế cao", "icon": "🚀", "color": GREEN_POS, "bg": RGBColor(236, 253, 245)},
    {"num": "-2%", "title": "HAN FR DEFICIT", "sub": "SGN SH hụt 2% so với kế hoạch", "icon": "🔻", "color": RED_NEG, "bg": RGBColor(254, 242, 242)},
    {"num": "13%", "title": "CANCEL RATE", "sub": "CR PoM giảm 0.6%, khớp đơn tốt", "icon": "📉", "color": BLUE_ACCENT, "bg": RGBColor(239, 246, 255)}
]

for idx, k in enumerate(kpis):
    left_pos = 0.6 + idx * 3.05
    c = add_card(s1, left_pos, 1.35, 2.9, 1.45, k["color"], k["bg"])
    tf = c.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.15)
    
    p = tf.paragraphs[0]
    p.text = f"{k['icon']}  {k['num']}"
    p.font.size = Pt(30)
    p.font.bold = True
    p.font.color.rgb = k["color"]
    
    p2 = tf.add_paragraph()
    p2.text = k["title"]
    p2.font.size = Pt(10.5)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_MAIN
    
    p3 = tf.add_paragraph()
    p3.text = k["sub"]
    p3.font.size = Pt(9.5)
    p3.font.color.rgb = TEXT_MUTED

# Left Box: Executive Highlights
c_left = add_card(s1, 0.6, 2.95, 6.2, 4.1, GREEN_POS)
tf_l = c_left.text_frame
tf_l.word_wrap = True
tf_l.margin_left = tf_l.margin_right = Inches(0.2)
p = tf_l.paragraphs[0]
p.text = "🟢 HIGHLIGHTS — ĐIỂM SÁNG VẬN HÀNH"
p.font.size = Pt(13.5)
p.font.bold = True
p.font.color.rgb = GREEN_POS

items_l = [
    ("📊", "NW GDR 94.82%", "100% target (+0.17% MoM); CTR 77.69% (130% target)."),
    ("🟢", "Driver Journey RAG Xanh", "Top 2 toàn khu vực, duy nhất đạt trạng thái tốt nhất."),
    ("📉", "Hủy Đơn Giảm 0.6% PoM", "Nhờ siết RBC_counter (từ >=4 xuống >=2) & chặn TTS thấp."),
    ("👥", "Đội Core 2H Duy Trì 80 Tv", "Tỷ lệ Active đạt 96% (77 tài xế hoạt động)."),
    ("📦", "Truyền Thông Baga Bulky", "Tiếp cận 11k tài xế, thu về 87 ĐK HAN & 79 ĐK SGN.")
]
for icon, title, desc in items_l:
    p = tf_l.add_paragraph()
    p.text = f"{icon}  {title}: {desc}"
    p.font.size = Pt(10.5)
    p.space_before = Pt(4)
    p.font.color.rgb = TEXT_MAIN

# Right Box: Vector Pyramid Diagram (Sơ đồ phân tầng chiến lược)
pyr_card = add_card(s1, 7.0, 2.95, 5.733, 4.1, ORANGE_PRIMARY, RGBColor(255, 255, 255))
tf_p = pyr_card.text_frame
tf_p.word_wrap = True
tf_p.margin_left = Inches(0.2)
p = tf_p.paragraphs[0]
p.text = "🔺 SƠ ĐỒ PHÂN TẦNG CHIẾN LƯỢC VẬN HÀNH"
p.font.size = Pt(13.5)
p.font.bold = True
p.font.color.rgb = ORANGE_PRIMARY

# Pyramid Level 1 (Top Peak)
p_top = s1.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, Inches(8.8), Inches(3.5), Inches(2.2), Inches(0.85))
p_top.fill.solid()
p_top.fill.fore_color.rgb = ORANGE_PRIMARY
p_top.line.fill.background()
tf = p_top.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "LEVEL 1: SCALE BẮT BUỘC ĐI KÈM CHẤT LƯỢNG\n(Target PnL MiniHub 36-50M)"
p.font.size = Pt(9)
p.font.bold = True
p.font.color.rgb = CARD_BG
p.alignment = PP_ALIGN.CENTER

# Pyramid Level 2 (Middle Tier)
p_mid = s1.shapes.add_shape(MSO_SHAPE.TRAPEZOID, Inches(8.1), Inches(4.4), Inches(3.6), Inches(1.0))
p_mid.fill.solid()
p_mid.fill.fore_color.rgb = BLUE_ACCENT
p_mid.line.fill.background()
tf = p_mid.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "LEVEL 2: NÒNG CỐT GIỮ CHÂN & ĐIỀU PHỐI\n(FT Retention >95% | Core 2H 80 Member | RBC_counter >=2)"
p.font.size = Pt(9.5)
p.font.bold = True
p.font.color.rgb = CARD_BG
p.alignment = PP_ALIGN.CENTER

# Pyramid Level 3 (Base Layer)
p_base = s1.shapes.add_shape(MSO_SHAPE.TRAPEZOID, Inches(7.4), Inches(5.45), Inches(5.0), Inches(1.15))
p_base.fill.solid()
p_base.fill.fore_color.rgb = GREEN_POS
p_base.line.fill.background()
tf = p_base.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "LEVEL 3: THỰC THI THỰC ĐỊA & NGUỒN CUNG\n(Giờ SH 453.8k | Dat Bike EV 164 xe | Baga Bulky 11k Reached)"
p.font.size = Pt(10)
p.font.bold = True
p.font.color.rgb = CARD_BG
p.alignment = PP_ALIGN.CENTER


# ==========================================
# SLIDE 2: NATIVE POWERPOINT COLUMN CHART (CUNG CẦU SGN VS HAN)
# ==========================================
s2 = prs.slides.add_slide(prs.slide_layouts[6])
apply_background(s2)
add_header(s2, "Phân Tích Giờ Cung Ứng (SH) & Chỉ Số RPH Giữa 2 Miền", "SUPPLY & DEMAND NATIVE CHART", "📊")

# Left Column: Native Column Chart (Giờ Cung Ứng & RPH)
chart_card = add_card(s2, 0.6, 1.35, 6.2, 5.7)
tf_c = chart_card.text_frame
tf_c.word_wrap = True
tf_c.margin_left = Inches(0.2)
p = tf_c.paragraphs[0]
p.text = "📊 ĐỒ THỊ SO SÁNH GIỜ CUNG ỨNG SH (NGÀN GIỜ)"
p.font.size = Pt(13.5)
p.font.bold = True
p.font.color.rgb = BLUE_ACCENT

# Add Native Bar Chart
cdata = CategoryChartData()
cdata.categories = ['TP.HCM (SGN)', 'Hà Nội (HAN)']
cdata.add_series('Giờ Cung Ứng (k giờ)', (275.823, 178.000))

cx, cy, cw, ch = Inches(0.8), Inches(1.9), Inches(5.8), Inches(4.9)
chart_shape = s2.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, cx, cy, cw, ch, cdata)
chart = chart_shape.chart
chart.has_legend = True
chart.legend.position = XL_LEGEND_POSITION.TOP
chart.legend.include_in_layout = False

# Right Column Cards: Performance Analysis
r_card1 = add_card(s2, 7.0, 1.35, 5.733, 2.7, BLUE_ACCENT)
tf_r1 = r_card1.text_frame
tf_r1.word_wrap = True
tf_r1.margin_left = Inches(0.2)
p = tf_r1.paragraphs[0]
p.text = "🌆 TP. HỒ CHÍ MINH (SGN) — 275,823 GIỜ SH"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = BLUE_ACCENT

sgn_items = [
    ("📊", "Giờ SH đạt", "275,823 giờ (chỉ hụt 2.6% so với KH)."),
    ("📉", "Chỉ số RPH", "1.47 Revenue Per Hour (-3.3% WoW)."),
    ("🔻", "Tỷ lệ giữ chân (RR)", "Giảm nhẹ 1.4% MoM và 13.13% YoY."),
    ("🛵", "Nhu cầu Xe Điện (EV)", "Đạt 112 xe (gấp 2.15 lần Hà Nội).")
]
for ic, tt, dc in sgn_items:
    p = tf_r1.add_paragraph()
    p.text = f"{ic}  {tt}: {dc}"
    p.font.size = Pt(11)
    p.space_before = Pt(3)
    p.font.color.rgb = TEXT_MAIN

r_card2 = add_card(s2, 7.0, 4.2, 5.733, 2.85, ORANGE_PRIMARY)
tf_r2 = r_card2.text_frame
tf_r2.word_wrap = True
tf_r2.margin_left = Inches(0.2)
p = tf_r2.paragraphs[0]
p.text = "🏛️ HÀ NỘI (HAN) — 178,000 GIỜ SH"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = ORANGE_PRIMARY

han_items = [
    ("⚠️", "Giờ SH đạt", "178,000 giờ (hụt 10.51%, tập trung ở FT & PT)."),
    ("🚀", "Chỉ số RPH Bức Phá", "2.07 Revenue Per Hour (+11.9% WoW, rất tốt)."),
    ("🟢", "Tỷ lệ giữ chân (RR)", "RR MoM ghi nhận cải thiện tích cực."),
    ("🌧️", "Thời tiết Mưa lớn", "Làm AR-FR giảm ~2%, nhu cầu Bulky tăng mạnh.")
]
for ic, tt, dc in han_items:
    p = tf_r2.add_paragraph()
    p.text = f"{ic}  {tt}: {dc}"
    p.font.size = Pt(11)
    p.space_before = Pt(3)
    p.font.color.rgb = TEXT_MAIN


# ==========================================
# SLIDE 3: NATIVE STEPPER FLOW DIAGRAM (SƠ ĐỒ LUỒNG XỬ LÝ HỦY ĐƠN)
# ==========================================
s3 = prs.slides.add_slide(prs.slide_layouts[6])
apply_background(s3)
add_header(s3, "Quy Trình Siết Đơn Hủy & Driver Journey RAG Xanh", "CANCEL RATE CONTROL & FLOW STEPPER", "🛠️")

# Top Banner Card
b_top = add_card(s3, 0.6, 1.35, 12.133, 1.1, BLUE_ACCENT, RGBColor(239, 246, 255))
tf_bt = b_top.text_frame
tf_bt.word_wrap = True
tf_bt.margin_left = Inches(0.2)
p = tf_bt.paragraphs[0]
p.text = "📉 TỶ LỆ HỦY ĐƠN (CR PoM) GIẢM VỀ MỐC 13% (GIẢM 0.6% PoM)"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = BLUE_ACCENT

p2 = tf_bt.add_paragraph()
p2.text = "Xu hướng giảm xuất hiện đồng đều trên tất cả các tập tài xế, khẳng định hiệu quả khớp đơn đang cải thiện rõ rệt."
p2.font.size = Pt(11)
p2.space_before = Pt(2)
p2.font.color.rgb = TEXT_MAIN

# Flow Stepper Title
st_card = add_card(s3, 0.6, 2.6, 12.133, 4.45)
tf_st = st_card.text_frame
tf_st.word_wrap = True
tf_st.margin_left = Inches(0.2)
p = tf_st.paragraphs[0]
p.text = "🔄 SƠ ĐỒ QUY TRÌNH 4 BƯỚC SIẾT ĐƠN HỦY & TỐI ƯU DISPATCH"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = ORANGE_PRIMARY

# 4 STEP VECTOR CARDS WITH ARROWS
steps = [
    {"num": "STEP 01", "title": "Tiếp Nhận Đơn", "desc": "Lọc đơn phát sinh & ghi nhận lý do hủy 'Không liên lạc được người nhận'", "color": BLUE_ACCENT},
    {"num": "STEP 02", "title": "Siết RBC Counter", "desc": "Áp dụng Logic mới: Siết ngưỡng đơn hủy từ >=4 đơn xuống >=2 đơn", "color": ORANGE_PRIMARY},
    {"num": "STEP 03", "title": "Lọc Điểm TTS", "desc": "Chặn Dispatch tự động cho các tài xế có điểm Thỏa Mãn (TTS) thấp", "color": PURPLE_ACCENT},
    {"num": "STEP 04", "title": "Phân Đơn Chuẩn", "desc": "Tối ưu khớp đơn, giảm tỷ lệ hủy về 13% & nâng Driver Journey lên RAG Xanh", "color": GREEN_POS}
]

for idx, st in enumerate(steps):
    left_p = 0.85 + idx * 2.85
    # Step Box
    s_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left_p), Inches(3.3), Inches(2.45), Inches(3.3))
    s_box.fill.solid()
    s_box.fill.fore_color.rgb = RGBColor(248, 250, 252)
    s_box.line.color.rgb = st["color"]
    s_box.line.width = Pt(2)
    
    tf = s_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.15)
    
    p = tf.paragraphs[0]
    p.text = st["num"]
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = st["color"]
    
    p2 = tf.add_paragraph()
    p2.text = st["title"]
    p2.font.size = Pt(13)
    p2.font.bold = True
    p2.space_before = Pt(4)
    p2.font.color.rgb = TEXT_MAIN
    
    p3 = tf.add_paragraph()
    p3.text = st["desc"]
    p3.font.size = Pt(10.5)
    p3.space_before = Pt(6)
    p3.font.color.rgb = TEXT_MUTED

    # Arrow Connector between steps
    if idx < 3:
        arr = s3.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(left_p + 2.5), Inches(4.7), Inches(0.3), Inches(0.3))
        arr.fill.solid()
        arr.fill.fore_color.rgb = ORANGE_PRIMARY
        arr.line.fill.background()


# ==========================================
# SLIDE 4: NATIVE BAR CHART & INSIGHTS (MINIHUB & CITYZONE)
# ==========================================
s4 = prs.slides.add_slide(prs.slide_layouts[6])
apply_background(s4)
add_header(s4, "Dự Án MiniHub & Cityzone — So Sánh Thu Nhập/Giờ (EPH)", "ZONE PERFORMANCE CLUSTERED CHART", "🏙️")

# Left Column Insights Card
c_mh = add_card(s4, 0.6, 1.35, 5.5, 5.7, ORANGE_PRIMARY)
tf_mh = c_mh.text_frame
tf_mh.word_wrap = True
tf_mh.margin_left = Inches(0.2)
p = tf_mh.paragraphs[0]
p.text = "💡 INSIGHTS MINIHUB & SANCTION"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = ORANGE_PRIMARY

mh_txt = [
    ("💵", "EPH Hà Nội Cao Hơn", "HAN (59.6K) cao vượt trội so với SGN (48.5K)."),
    ("⚠️", "Sanction HAN (86.89%)", "Lỗi phổ biến nhất là 'Không hoạt động'."),
    ("🔻", "Sanction SGN (23.68%)", "Lỗi phổ biến nhất là 'Fail Online'."),
    ("📍", "Cityzone Check-in", "Đạt 49.8% (233/770 lead check-in, 231 tài xế có đơn)."),
    ("⚖️", "Target PnL & ROI", "Chốt Go/No-Go trước 15/8 (Target 36-50tr/tháng).")
]
for ic, tt, dc in mh_txt:
    p = tf_mh.add_paragraph()
    p.text = f"{ic}  {tt}: {dc}"
    p.font.size = Pt(11)
    p.space_before = Pt(6)
    p.font.color.rgb = TEXT_MAIN

# Right Column Native Bar Chart Box
c_chart_bg = add_card(s4, 6.3, 1.35, 6.433, 5.7)
tf_cbg = c_chart_bg.text_frame
tf_cbg.word_wrap = True
tf_cbg.margin_left = Inches(0.2)
p = tf_cbg.paragraphs[0]
p.text = "📊 ĐỒ THỊ SO SÁNH THU NHẬP/GIỜ (EPH - VNĐ)"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = BLUE_ACCENT

# Add Native Horizontal Bar Chart
eph_data = CategoryChartData()
eph_data.categories = ['SGN - Zone 1', 'SGN - Zone 6', 'HAN - Thanh Xuân', 'HAN - Cầu Giấy']
eph_data.add_series('Thu nhập EPH (K VNĐ)', (49.5, 50.7, 72.6, 73.3))

cx, cy, cw, ch = Inches(6.5), Inches(1.9), Inches(6.0), Inches(4.9)
chart_shape2 = s4.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, cx, cy, cw, ch, eph_data)
chart2 = chart_shape2.chart
chart2.has_legend = False


# ==========================================
# SLIDE 5: DONUT CHART & ACTION ROADMAP THÁNG 8
# ==========================================
s5 = prs.slides.add_slide(prs.slide_layouts[6])
apply_background(s5)
add_header(s5, "Dự Án Xe Điện (EV) & Kế Hoạch Trọng Tâm Tháng 8", "EV DONUT CHART & STRATEGIC ROADMAP", "🎯")

# Left Column Donut Chart Box (Tỷ lệ thuê xe điện SGN vs HAN)
c_ev = add_card(s5, 0.6, 1.35, 5.5, 5.7, GREEN_POS)
tf_ev = c_ev.text_frame
tf_ev.word_wrap = True
tf_ev.margin_left = Inches(0.2)
p = tf_ev.paragraphs[0]
p.text = "⚡ TY LE THUE XE ĐIỆN (EV): SGN 112 vs HAN 52"
p.font.size = Pt(13.5)
p.font.bold = True
p.font.color.rgb = GREEN_POS

# Add Native Donut Chart
ev_data = CategoryChartData()
ev_data.categories = ['SGN (112 xe - 68%)', 'HAN (52 xe - 32%)']
ev_data.add_series('Số lượng xe điện', (112, 52))

cx, cy, cw, ch = Inches(0.8), Inches(1.9), Inches(5.1), Inches(3.5)
chart_shape3 = s5.shapes.add_chart(XL_CHART_TYPE.DOUGHNUT, cx, cy, cw, ch, ev_data)
chart3 = chart_shape3.chart
chart3.has_legend = True
chart3.legend.position = XL_LEGEND_POSITION.BOTTOM

# EV Sub-text
tb_ev = s5.shapes.add_textbox(Inches(0.8), Inches(5.4), Inches(5.1), Inches(1.5))
tf_sub = tb_ev.text_frame
tf_sub.word_wrap = True
p = tf_sub.paragraphs[0]
p.text = "• SGN cao gấp 2.15 lần HAN. Dat Bike chiếm tỷ trọng lớn nhất.\n• Duyệt ngân sách CTT từ S&P cho chương trình 'Đua Top Thuê Xe'."
p.font.size = Pt(10.5)
p.font.color.rgb = TEXT_MAIN

# Right Column Strategic Roadmap Actions
c_m8 = add_card(s5, 6.3, 1.35, 6.433, 5.7, ORANGE_PRIMARY)
tf_m8 = c_m8.text_frame
tf_m8.word_wrap = True
tf_m8.margin_left = Inches(0.2)
p = tf_m8.paragraphs[0]
p.text = "🎯 KẾ HOẠCH HÀNH ĐỘNG TRỌNG TÂM THÁNG 8"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = ORANGE_PRIMARY

m8_list = [
    ("📌", "KIM CHỈ NAM OPERATIONAL", "'Đẩy tốc độ scale mà không đánh đổi chất lượng'."),
    ("⚖️", "Quyết Định Go/No-Go MiniHub", "Chốt trước 15/8 dựa trên PnL & ROI (Target 36-50tr/tháng)."),
    ("⚡", "Cải Thiện Nguồn Cung", "Khắc phục hụt SH tại HAN (-10.51%) & SGN (-2.6%)."),
    ("📞", "Tối Ưu Tỷ Lệ Hủy Đơn", "Duy trì RBC_counter mới & giải quyết khâu liên lạc người nhận."),
    ("📦", "Mở Rộng Baga Bulky", "Đẩy mạnh duyệt 166 tài xế đăng ký tại HAN & SGN.")
]
for ic, tt, dc in m8_list:
    p = tf_m8.add_paragraph()
    p.text = f"{ic}  {tt}: {dc}"
    p.font.size = Pt(11.5)
    p.space_before = Pt(8)
    p.font.color.rgb = TEXT_MAIN

# Save Presentation
prs.save(pptx_path)
print(f"Successfully generated full native vector charts & diagrams deck at: {pptx_path}")
