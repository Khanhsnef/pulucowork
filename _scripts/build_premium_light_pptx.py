import sys
import os
import datetime
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# Sleek Executive Light Palette (Clean & Bright)
COLOR_BG_LIGHT = RGBColor(248, 250, 252)     # #F8FAFC Soft Slate White
COLOR_CARD_BG = RGBColor(255, 255, 255)      # #FFFFFF Pure White
COLOR_CARD_BORDER = RGBColor(226, 232, 240)  # #E2E8F0 Subtle Border Stroke
COLOR_NAVY_PRIMARY = RGBColor(14, 65, 116)   # #0E4174 Ahamove Navy
COLOR_NAVY_DARK = RGBColor(10, 46, 82)      # #0A2E52

COLOR_TEXT_DARK = RGBColor(15, 23, 42)       # #0F172A Slate Dark Text
COLOR_TEXT_MUTED = RGBColor(100, 116, 139)   # #64748B Slate Muted Text
COLOR_WHITE = RGBColor(255, 255, 255)

# Accent Palette
COLOR_ORANGE = RGBColor(255, 127, 50)        # #FF7F32 Ahamove Orange
COLOR_GREEN = RGBColor(16, 185, 129)         # #10B981 Success Green
COLOR_RED = RGBColor(239, 68, 68)            # #EF4444 Danger Red
COLOR_YELLOW = RGBColor(245, 158, 11)        # #F59E0B Warning Yellow

# Background Fills for Impact Boxes
COLOR_RED_BG = RGBColor(254, 242, 242)       # #FEF2F2 Light Red
COLOR_YELLOW_BG = RGBColor(254, 243, 199)    # #FEF3C7 Light Yellow
COLOR_GREEN_BG = RGBColor(236, 253, 245)     # #ECFDF5 Light Green

def set_flat_style(shape, fill_rgb, border_rgb=None, border_pt=1, radius=0.015):
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_rgb
    if border_rgb:
        shape.line.color.rgb = border_rgb
        shape.line.width = Pt(border_pt)
    else:
        shape.line.fill.background()
    
    # Adjust corner radius if applicable (subtle barely rounded corners)
    try:
        if hasattr(shape, 'adjustments') and len(shape.adjustments) > 0:
            shape.adjustments[0] = radius
    except Exception:
        pass

def add_light_slide_bg(slide):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    set_flat_style(bg, COLOR_BG_LIGHT)
    return bg

def add_header(slide, title_text, category_tag="AHAMOVE DRIVER OPS"):
    # Top Accent Line
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.1))
    set_flat_style(top_bar, COLOR_ORANGE)

    # Category Tag Badge
    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.35), Inches(2.2), Inches(0.35))
    set_flat_style(badge, RGBColor(238, 242, 246), COLOR_NAVY_PRIMARY, radius=0.02)
    p_b = badge.text_frame.paragraphs[0]
    p_b.text = f"✦ {category_tag}"
    p_b.font.name = 'Inter'
    p_b.font.size = Pt(9.5)
    p_b.font.bold = True
    p_b.font.color.rgb = COLOR_NAVY_PRIMARY
    p_b.alignment = PP_ALIGN.CENTER

    # Title Text Box
    h_box = slide.shapes.add_textbox(Inches(3.2), Inches(0.3), Inches(9.3), Inches(0.6))
    htf = h_box.text_frame
    htf.word_wrap = True
    hp = htf.paragraphs[0]
    hp.text = title_text
    hp.font.name = 'Outfit'
    hp.font.size = Pt(22)
    hp.font.bold = True
    hp.font.color.rgb = COLOR_NAVY_PRIMARY

def add_footer(slide, current_slide, total_slides):
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    f_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.95), Inches(11.733), Inches(0.35))
    ftf = f_box.text_frame
    fp = ftf.paragraphs[0]
    fp.text = f"📅 {date_str}  │  Ahamove Operations Report — Confidential  │  Slide {current_slide} / {total_slides}"
    fp.font.name = 'Inter'
    fp.font.size = Pt(9.5)
    fp.font.color.rgb = COLOR_TEXT_MUTED

def build_light_presentation(output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    TOTAL_SLIDES = 8

    # ----------------------------------------------------
    # SLIDE 1: Cover Slide (Sleek Clean Header)
    # ----------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    add_light_slide_bg(s1)

    # Top Dark Navy Banner Card
    banner1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(4.2))
    set_flat_style(banner1, COLOR_NAVY_PRIMARY, radius=0.015)

    # Tag Badge
    badge1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.3), Inches(1.3), Inches(4.5), Inches(0.4))
    set_flat_style(badge1, COLOR_NAVY_DARK, COLOR_ORANGE, radius=0.02)
    p = badge1.text_frame.paragraphs[0]
    p.text = "AHAMOVE DRIVER MANAGEMENT NETWORK"
    p.font.name = 'Inter'
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_ORANGE
    p.alignment = PP_ALIGN.CENTER

    tb1 = s1.shapes.add_textbox(Inches(1.3), Inches(1.9), Inches(10.7), Inches(2.8))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "MASTER DRIVER OPERATIONS PERFORMANCE REPORT"
    p0.font.name = 'Outfit'
    p0.font.size = Pt(32)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_WHITE

    p1 = tf1.add_paragraph()
    p1.text = "\nStrategic Operational Diagnostic Framework (WHAT → WHERE → WHO → IMPACT → WHY → ACTION → RECOVERY)"
    p1.font.name = 'Inter'
    p1.font.size = Pt(13)
    p1.font.color.rgb = RGBColor(203, 213, 225)

    # 3 Bottom Info Cards (Clean White with borders)
    info_data = [
        ("LEAD AUTHOR", "Strategy & BI Operations Team"),
        ("SCOPE", "DM NW Performance Diagnostic"),
        ("DATA SOURCE", "11 Metabase Cards Audit")
    ]
    for idx, (lbl, val) in enumerate(info_data):
        card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + idx * 3.95), Inches(5.2), Inches(3.8), Inches(1.4))
        set_flat_style(card, COLOR_CARD_BG, COLOR_CARD_BORDER, radius=0.015)
        
        # Left Accent Line
        acc = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8 + idx * 3.95), Inches(5.2), Inches(0.08), Inches(1.4))
        set_flat_style(acc, COLOR_ORANGE if idx==0 else COLOR_NAVY_PRIMARY)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_top = Inches(0.2)
        
        p_lbl = tf.paragraphs[0]
        p_lbl.text = lbl
        p_lbl.font.name = 'Inter'
        p_lbl.font.size = Pt(9.5)
        p_lbl.font.bold = True
        p_lbl.font.color.rgb = COLOR_TEXT_MUTED
        
        p_val = tf.add_paragraph()
        p_val.text = val
        p_val.font.name = 'Outfit'
        p_val.font.size = Pt(13)
        p_val.font.bold = True
        p_val.font.color.rgb = COLOR_NAVY_PRIMARY

    # ----------------------------------------------------
    # SLIDE 2: KPI Health Overview (Clean White Bento Cards)
    # ----------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    add_light_slide_bg(s2)
    add_header(s2, "1.1. KPI Health Overview Dashboard", "EXECUTIVE BRIEF")
    add_footer(s2, 2, TOTAL_SLIDES)

    kpis = [
        ("🟢 COMPLIANCE TRUE RATE", "74.15%", "▲ Kỷ lục mới toàn quốc\nĐảm bảo tuân thủ tiêu chuẩn.", COLOR_GREEN),
        ("🟡 FULFILLMENT RATE NW", "81.38%", "SGN bứt phá 86.2%\nHAN sụt giảm còn 75.8%", COLOR_YELLOW),
        ("🟡 SGN RETENTION NLM", "65.15%", "▼ -5.45% MoM (Sụt 718 tx)\nCần can thiệp nhóm Tân binh.", COLOR_YELLOW),
        ("🔴 CITYZONE NO-SHOW", "32.2%", "163 ca No-show\n(39% ca ảo vẫn chạy 401 đơn)", COLOR_RED)
    ]

    for idx, (title, num, sub, color) in enumerate(kpis):
        left = Inches(0.8 + idx * 2.95)
        top = Inches(1.2)
        width = Inches(2.75)
        height = Inches(2.1)

        # Card Container (Sharp subtle rounded corner)
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        set_flat_style(card, COLOR_CARD_BG, COLOR_CARD_BORDER, radius=0.015)

        # Perfectly Fitted Left Accent Strip
        strip = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, Inches(0.1), height)
        set_flat_style(strip, color)

        tb = s2.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.3), height - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.name = 'Inter'
        p0.font.size = Pt(9)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_TEXT_MUTED

        p1 = tf.add_paragraph()
        p1.text = num
        p1.font.name = 'Outfit'
        p1.font.size = Pt(28)
        p1.font.bold = True
        p1.font.color.rgb = color

        p2 = tf.add_paragraph()
        p2.text = sub
        p2.font.name = 'Inter'
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = COLOR_TEXT_DARK

    # Key Takeaways Bento Card
    t_left = Inches(0.8)
    t_top = Inches(3.55)
    t_width = Inches(11.733)
    t_height = Inches(3.2)

    takeaway_card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, t_left, t_top, t_width, t_height)
    set_flat_style(takeaway_card, COLOR_CARD_BG, COLOR_ORANGE, border_pt=1.5, radius=0.015)

    # Fitted Top Accent Bar
    t_bar = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, t_left, t_top, t_width, Inches(0.08))
    set_flat_style(t_bar, COLOR_ORANGE)

    tb_t = s2.shapes.add_textbox(t_left + Inches(0.3), t_top + Inches(0.2), t_width - Inches(0.6), t_height - Inches(0.4))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True

    p = tf_t.paragraphs[0]
    p.text = "🏆 KEY TAKEAWAYS BÁO CÁO BAN GIÁM ĐỐC"
    p.font.name = 'Outfit'
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_PRIMARY

    takeaways = [
        "1. Hà Nội nghẽn cung ca cao điểm: FR HAN chạm đáy 75.8%, Surge Rate vọt 48.3% (Hệ số 1.31x) làm thất thoát ~95,000 đơn hoàn thành/tháng.",
        "2. Chất lượng SGN duy trì kỷ lục: Compliance True Rate toàn quốc đạt 74.15% & Good Driver Rate SGN chạm mốc tối đa 96.51% (Max Score 1.20x).",
        "3. Sự cố UX CityZone Hub: 39% ca No-show (99/254 ca) VẪN CÓ 401 ĐƠN HOÀN THÀNH do quên bấm Check-in ca làm thủ công."
    ]
    for t_line in takeaways:
        p = tf_t.add_paragraph()
        p.text = f"\n{t_line}"
        p.font.name = 'Inter'
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT_DARK

    # ----------------------------------------------------
    # SLIDE 3: Top 3 Problem Statements (Sleek Clean Columns)
    # ----------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    add_light_slide_bg(s3)
    add_header(s3, "1.2. Top 3 Problem Statements (Prioritization P0 / P1)", "PROBLEMS AUDIT")
    add_footer(s3, 3, TOTAL_SLIDES)

    problems = [
        ("PRIORITY P0", "PROB-01: FR HAN Sụt Ca Cao Điểm", 
         "Fulfillment Rate Hà Nội sụt về 75.8% trong ca trưa (11h-13h) và chiều (17h-19h). Surge Rate vọt 48.3% (Hệ số 1.31x), RPH 2.07.",
         "Thất thoát ~95,000 đơn/tháng", COLOR_RED, COLOR_RED_BG),
        ("PRIORITY P0", "PROB-02: UX CityZone Check-in Sót Đơn", 
         "163 ca No-show (32.2% ca). Tuy nhiên 39% số ca No-show đó (99 ca) vẫn hoàn thành 401 đơn do tài xế quên bấm Check-in.",
         "Sót đơn tính thưởng & khiếu nại +50%", COLOR_RED, COLOR_RED_BG),
        ("PRIORITY P1", "PROB-03: Shopee Reverse Cancel Rate Vọt", 
         "Tỷ lệ hủy đơn dịch vụ Shopee Reverse tăng lên mốc 37.61% do quy trình gán đơn đổi trả phức tạp và thông tin địa chỉ nhiễu.",
         "Tăng 3.5x tỷ lệ hủy & sụt SLA SPX", COLOR_YELLOW, COLOR_YELLOW_BG)
    ]

    for idx, (prio, title, desc, impact, color, bg_color) in enumerate(problems):
        left = Inches(0.8 + idx * 3.95)
        top = Inches(1.2)
        width = Inches(3.7)
        height = Inches(5.5)

        card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        set_flat_style(card, COLOR_CARD_BG, COLOR_CARD_BORDER, radius=0.015)

        # Perfectly Fitted Top Accent Bar
        top_accent = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, Inches(0.1))
        set_flat_style(top_accent, color)

        # Priority Badge
        pill = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.3), Inches(1.5), Inches(1.6), Inches(0.35))
        set_flat_style(pill, color, radius=0.02)
        p = pill.text_frame.paragraphs[0]
        p.text = prio
        p.font.name = 'Inter'
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER

        # Content Textbox
        tb = s3.shapes.add_textbox(left + Inches(0.3), Inches(2.0), Inches(3.1), Inches(3.2))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.name = 'Outfit'
        p0.font.size = Pt(13.5)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_NAVY_PRIMARY

        p1 = tf.add_paragraph()
        p1.text = f"\n{desc}"
        p1.font.name = 'Inter'
        p1.font.size = Pt(11)
        p1.font.color.rgb = COLOR_TEXT_MUTED

        # Perfectly Fitted Bottom Impact Box
        imp_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.2), Inches(5.45), Inches(3.3), Inches(1.0))
        set_flat_style(imp_box, bg_color, color, radius=0.015)

        tf_i = imp_box.text_frame
        tf_i.word_wrap = True
        tf_i.margin_left = Inches(0.15)
        tf_i.margin_right = Inches(0.15)
        
        pi0 = tf_i.paragraphs[0]
        pi0.text = "TÁC ĐỘNG KINH DOANH:"
        pi0.font.name = 'Inter'
        pi0.font.size = Pt(8.5)
        pi0.font.bold = True
        pi0.font.color.rgb = color

        pi1 = tf_i.add_paragraph()
        pi1.text = impact
        pi1.font.name = 'Inter'
        pi1.font.size = Pt(11)
        pi1.font.bold = True
        pi1.font.color.rgb = color

    # ----------------------------------------------------
    # SLIDE 4: Deep Diagnostics & Localization
    # ----------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    add_light_slide_bg(s4)
    add_header(s4, "2.2. Localization & Contribution Analysis", "DEEP DIAGNOSTICS")
    add_footer(s4, 4, TOTAL_SLIDES)

    # Card 1: Churn Breakdown
    c1 = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.2), Inches(5.7), Inches(5.5))
    set_flat_style(c1, COLOR_CARD_BG, COLOR_CARD_BORDER, radius=0.015)
    
    # Left Accent Line
    acc1 = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.2), Inches(0.08), Inches(5.5))
    set_flat_style(acc1, COLOR_ORANGE)

    tb1 = s4.shapes.add_textbox(Inches(1.1), Inches(1.4), Inches(5.2), Inches(5.1))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "📉 Lý Do Sụt Giảm Retention Tân Binh\n(NLM SGN: 718 TX Churn)"
    p.font.name = 'Outfit'
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_PRIMARY

    churn_items = [
        ("🔴 44% Contribution (316 tx)", "Thu nhập & chi phí xăng tăng cao trong mùa mưa nắng cực đoan."),
        ("🟡 31% Contribution (222 tx)", "Lỗi thao tác app / chưa quen quy trình thu hộ COD."),
        ("⚪ 25% Contribution (180 tx)", "Chuyển sang ứng dụng đối thủ (Grab/Be/XanhSM).")
    ]
    for tag, desc in churn_items:
        p = tf1.add_paragraph()
        p.text = f"\n{tag}"
        p.font.name = 'Inter'
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_DARK

        p_sub = tf1.add_paragraph()
        p_sub.text = desc
        p_sub.font.name = 'Inter'
        p_sub.font.size = Pt(10.5)
        p_sub.font.color.rgb = COLOR_TEXT_MUTED

    # Card 2: CityZone Checkin Breakdown
    c2 = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.2), Inches(5.733), Inches(5.5))
    set_flat_style(c2, COLOR_CARD_BG, COLOR_CARD_BORDER, radius=0.015)

    # Left Accent Line
    acc2 = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(1.2), Inches(0.08), Inches(5.5))
    set_flat_style(acc2, COLOR_NAVY_PRIMARY)

    tb2 = s4.shapes.add_textbox(Inches(7.1), Inches(1.4), Inches(5.2), Inches(5.1))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "📍 Phân Phối Ca Check-in CityZone Hub\n(Tổng 506 Ca Đăng Ký)"
    p.font.name = 'Outfit'
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_PRIMARY

    cz_items = [
        ("🟢 67.8% (343 Ca)", "Check-in hợp lệ đúng vị trí & khung giờ quy định."),
        ("🔴 19.6% (99 Ca)", "No-show thực sự (Không có mặt & không chạy đơn nào)."),
        ("🟠 12.6% (64 Ca)", "No-show ẢO — Vẫn dịch chuyển đến Hub và hoàn thành 401 đơn!")
    ]
    for tag, desc in cz_items:
        p = tf2.add_paragraph()
        p.text = f"\n{tag}"
        p.font.name = 'Inter'
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_DARK

        p_sub = tf2.add_paragraph()
        p_sub.text = desc
        p_sub.font.name = 'Inter'
        p_sub.font.size = Pt(10.5)
        p_sub.font.color.rgb = COLOR_TEXT_MUTED

    # ----------------------------------------------------
    # SLIDE 5: 5 Whys Root Cause Diagnosis
    # ----------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    add_light_slide_bg(s5)
    add_header(s5, "3.1. 5 Whys Root Cause Diagnosis", "ROOT CAUSE AUDIT")
    add_footer(s5, 5, TOTAL_SLIDES)

    steps = [
        ("Why #1", "Tại sao FR HAN bị sụt về 75.8%?", "Vì tỷ lệ đơn tăng giá (Surge Rate) vọt lên 48.3% (Hệ số 1.31x) và RPH chạm mốc 2.07 đơn/giờ gây nghẽn mạng lưới."),
        ("Why #2", "Tại sao Surge Rate và RPH vọt cao?", "Vì nguồn cung giờ online của tài xế thiếu hụt -15.4% so với nhu cầu ca cao điểm (11h-13h & 17h-19h)."),
        ("Why #3", "Tại sao giờ online tài xế sụt hụt?", "Vì tài xế Part-time (PT) giảm -6.46% giờ online và Tân binh (NIM) giảm -38.71% do thời tiết mưa nắng cực đoan.")
    ]

    for idx, (w_num, w_q, w_a) in enumerate(steps):
        card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.2 + idx * 1.3), Inches(11.733), Inches(1.15))
        set_flat_style(card, COLOR_CARD_BG, COLOR_CARD_BORDER, radius=0.015)

        # Left fitted accent strip
        acc_s = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.2 + idx * 1.3), Inches(0.08), Inches(1.15))
        set_flat_style(acc_s, COLOR_NAVY_PRIMARY)

        tb = s5.shapes.add_textbox(Inches(1.1), Inches(1.25 + idx * 1.3), Inches(11.133), Inches(1.05))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = f"✦ {w_num}: {w_q}"
        p0.font.name = 'Outfit'
        p0.font.size = Pt(13)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_NAVY_PRIMARY

        p1 = tf.add_paragraph()
        p1.text = w_a
        p1.font.name = 'Inter'
        p1.font.size = Pt(11)
        p1.font.color.rgb = COLOR_TEXT_DARK

    # Root Cause Highlight Card
    rc_card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.2), Inches(11.733), Inches(1.5))
    set_flat_style(rc_card, COLOR_RED_BG, COLOR_RED, border_pt=1.5, radius=0.015)

    # Fitted Left Accent Strip
    rc_acc = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(5.2), Inches(0.1), Inches(1.5))
    set_flat_style(rc_acc, COLOR_RED)

    tb_rc = s5.shapes.add_textbox(Inches(1.1), Inches(5.3), Inches(11.133), Inches(1.3))
    tf_rc = tb_rc.text_frame
    tf_rc.word_wrap = True

    p0 = tf_rc.paragraphs[0]
    p0.text = "★ ROOT CAUSE XÁC MINH (CONFIRMED ROOT CAUSE):"
    p0.font.name = 'Outfit'
    p0.font.size = Pt(12.5)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_RED

    p1 = tf_rc.add_paragraph()
    p1.text = "Hạn chế trang bị Baga/Áo mưa tiêu chuẩn và rào cản hạn mức COD Balance (10M) khiến tài xế PT/NIM không đủ điều kiện gánh đơn Bulky ca cao điểm."
    p1.font.name = 'Inter'
    p1.font.size = Pt(13)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TEXT_DARK

    # ----------------------------------------------------
    # SLIDE 6: Execution Roadmap (Styled Table)
    # ----------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    add_light_slide_bg(s6)
    add_header(s6, "4.1. Execution Roadmap & Action Matrix", "ACTION PLAN")
    add_footer(s6, 6, TOTAL_SLIDES)

    headers = ["Mã Action", "Tên Giải Pháp Chi Tiết", "Nhóm Ưu Tiên", "PIC Đảm Nhận", "Thời Gian"]
    rows = [
        ["ACT-01", "Tự động hóa Geofencing Check-in qua vị trí GPS cho CityZone Hub", "P0 High", "Product & Operations", "Tuần 1 - Tuần 2"],
        ["ACT-02", "Tăng hạn mức COD linh hoạt từ 10M lên 15M cho tài xế Tân binh đủ điểm", "P0 High", "Risk & DM Lead", "Tuần 2"],
        ["ACT-03", "Tài trợ 50% chi phí Baga Bulky & Áo mưa cho 500 tài xế PT Hà Nội", "P1 Med", "Driver Comms & Ops", "Tuần 2 - Tuần 3"],
        ["ACT-04", "Tối ưu UI gán đơn Shopee Reverse kèm bản đồ định vị chính xác", "P1 Med", "Product & SPX Lead", "Tuần 3"]
    ]

    tbl_shape = s6.shapes.add_table(5, 5, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.2))
    tbl = tbl_shape.table
    tbl.columns[0].width = Inches(1.3)
    tbl.columns[1].width = Inches(4.5)
    tbl.columns[2].width = Inches(1.5)
    tbl.columns[3].width = Inches(2.4)
    tbl.columns[4].width = Inches(2.033)

    for c_idx, h_text in enumerate(headers):
        cell = tbl.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.name = 'Outfit'
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE

    for r_idx, r_data in enumerate(rows):
        for c_idx, val in enumerate(r_data):
            cell = tbl.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_BG_LIGHT if r_idx % 2 == 0 else COLOR_CARD_BG
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = 'Inter'
            p.font.size = Pt(11)
            p.font.color.rgb = COLOR_TEXT_DARK
            if c_idx == 2:
                p.font.bold = True
                p.font.color.rgb = COLOR_RED if "P0" in val else COLOR_YELLOW

    # ----------------------------------------------------
    # SLIDE 7: Value Realization & ROI
    # ----------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    add_light_slide_bg(s7)
    add_header(s7, "5.1. Value Realization & ROI Transformation", "EXPECTED IMPACT")
    add_footer(s7, 7, TOTAL_SLIDES)

    headers_roi = ["Chỉ Số Vận Hành (KPI)", "Hiện Trạng (Current)", "Mục Tiêu Sau Chuyển Đổi", "Tác Động Kinh Doanh (Business Impact)"]
    rows_roi = [
        ["Fulfillment Rate (HAN)", "75.8% (Surge 48.3%)", "83.5% (Surge < 25%)", "Khôi phục +15,000 đơn hoàn thành/tháng tại Hà Nội."],
        ["Tỷ lệ No-show CityZone", "32.2% (163 ca)", "< 5.0% (Tự động Check-in)", "Triệt tiêu 100% khiếu nại sót đơn tính thưởng."],
        ["Retention Tân Binh NLM SGN", "65.15% (Sụt 718 tx)", "72.0% (+6.85% MoM)", "Giữ chân +500 tài xế active, giảm chi phí tuyển mới."]
    ]

    tbl_roi = s7.shapes.add_table(4, 4, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.2)).table
    tbl_roi.columns[0].width = Inches(2.8)
    tbl_roi.columns[1].width = Inches(2.2)
    tbl_roi.columns[2].width = Inches(2.5)
    tbl_roi.columns[3].width = Inches(4.233)

    for c_idx, h_text in enumerate(headers_roi):
        cell = tbl_roi.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.name = 'Outfit'
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE

    for r_idx, r_data in enumerate(rows_roi):
        for c_idx, val in enumerate(r_data):
            cell = tbl_roi.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_BG_LIGHT if r_idx % 2 == 0 else COLOR_CARD_BG
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = 'Inter'
            p.font.size = Pt(11)
            p.font.color.rgb = COLOR_TEXT_DARK
            if c_idx == 2:
                p.font.bold = True
                p.font.color.rgb = COLOR_GREEN

    # ----------------------------------------------------
    # SLIDE 8: 60-Sec Executive Storyline
    # ----------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    add_light_slide_bg(s8)
    add_header(s8, "60-Second BOD Executive Storyline", "MANAGEMENT BRIEF")
    add_footer(s8, 8, TOTAL_SLIDES)

    b_card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.2), Inches(11.733), Inches(5.5))
    set_flat_style(b_card, COLOR_CARD_BG, COLOR_ORANGE, border_pt=1.5, radius=0.015)

    # Fitted Top Accent Bar
    b_acc = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.2), Inches(11.733), Inches(0.08))
    set_flat_style(b_acc, COLOR_ORANGE)

    tb = s8.shapes.add_textbox(Inches(1.1), Inches(1.4), Inches(11.133), Inches(5.1))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "🏆 TÓM TẮT DÀNH CHO BAN GIÁM ĐỐC (PYRAMID PRINCIPLE)"
    p0.font.name = 'Outfit'
    p0.font.size = Pt(16)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_NAVY_PRIMARY

    story = [
        ("1. Điểm Khởi Sắc:", "Tuân thủ tiêu chuẩn vận hành toàn quốc (Compliance True Rate) đạt kỷ lục mới 74.15%; SGN giữ vững chất lượng dịch vụ ở mốc tối đa (Good Driver Rate 96.51%)."),
        ("2. Điểm Nghẽn Cốt Lõi:", "Nguồn cung Hà Nội trong ca cao điểm thiếu hụt làm FR sụt về 75.8%; sự cố thao tác Check-in thủ công tại CityZone Hub gây lãng phí 25.6% lượng đơn."),
        ("3. Quyết Định Đề Xuất:", "Phê duyệt ngay giải pháp Geofencing Auto-Checkin cho Hub và mở rộng hạn mức COD linh hoạt 15M cho tài xế Tân binh trong tuần tới.")
    ]

    for s_title, s_desc in story:
        p = tf.add_paragraph()
        p.text = f"\n{s_title}"
        p.font.name = 'Outfit'
        p.font.size = Pt(13.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY_PRIMARY

        p_d = tf.add_paragraph()
        p_d.text = s_desc
        p_d.font.name = 'Inter'
        p_d.font.size = Pt(12)
        p_d.font.color.rgb = COLOR_TEXT_DARK

    prs.save(output_path)
    print(f"✅ Created Clean Premium Light Deck at: {output_path}")

if __name__ == "__main__":
    out_file = "/Users/ts-1148/Desktop/Pulu-workspace/Output/Ahamove/04. OPS_METRICS/ahamove_master_ops_performance_report-editable.pptx"
    build_light_presentation(out_file)
