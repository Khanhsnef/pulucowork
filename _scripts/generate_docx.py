import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
import os

doc = Document()

# Set page margins to 0.8 inch
for section in doc.sections:
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

# Color Palette
NAVY = RGBColor(15, 44, 89)       # Primary Accent: #0F2C59
TEAL = RGBColor(13, 148, 136)     # Secondary Accent: #0D9488
CHARCOAL = RGBColor(30, 41, 59)   # Main Text: #1E293B
MUTED = RGBColor(100, 116, 139)   # Subtitle/Muted: #64748B
WHITE = RGBColor(255, 255, 255)   # Header Text
BG_LIGHT = "F8FAFC"
HEADER_BG = "0F2C59"
BORDER_GRAY = "CBD5E1"
ROW_ALT_BG = "F1F5F9"

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=140, bottom=140, left=180, right=180):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="CBD5E1", sz="4", val="single"):
    tblPr = table._element.xpath('w:tblPr')
    if tblPr:
        borders = parse_xml(f'<w:tblBorders {nsdecls("w")}><w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/><w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/><w:left w:val="none"/><w:right w:val="none"/><w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/><w:insideV w:val="none"/></w:tblBorders>')
        tblPr[0].append(borders)

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Arial'
    run.font.size = Pt(15)
    run.bold = True
    run.font.color.rgb = NAVY
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Arial'
    run.font.size = Pt(12.5)
    run.bold = True
    run.font.color.rgb = TEAL
    return p

def add_heading_3(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Arial'
    run.font.size = Pt(11)
    run.bold = True
    run.font.color.rgb = CHARCOAL
    return p

def add_body_p(doc, text, bold_prefix="", italic_text=""):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.name = 'Arial'
        r_pre.font.size = Pt(10)
        r_pre.font.color.rgb = CHARCOAL
    run = p.add_run(text)
    run.font.name = 'Arial'
    run.font.size = Pt(10)
    run.font.color.rgb = CHARCOAL
    if italic_text:
        r_it = p.add_run(italic_text)
        r_it.italic = True
        r_it.font.name = 'Arial'
        r_it.font.size = Pt(10)
        r_it.font.color.rgb = MUTED
    return p

def make_callout_box(doc, text_items, title="", border_color="0F2C59", bg_color="F8FAFC"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=140, bottom=140, left=220, right=180)
    
    tcPr = cell._element.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="none"/><w:bottom w:val="none"/><w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/><w:right w:val="none"/></w:tcBorders>')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    
    if title:
        run_title = p.add_run(title + "\n")
        run_title.bold = True
        run_title.font.name = 'Arial'
        run_title.font.size = Pt(11)
        run_title.font.color.rgb = NAVY
        
    for idx, item in enumerate(text_items):
        if idx > 0 or title:
            p = cell.add_paragraph()
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(3)
        run = p.add_run(item)
        run.font.name = 'Arial'
        run.font.size = Pt(9.5)
        run.font.color.rgb = CHARCOAL

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

# ==================== COVER HEADER ====================
p_title = doc.add_paragraph()
p_title.paragraph_format.space_before = Pt(0)
p_title.paragraph_format.space_after = Pt(2)
r_title = p_title.add_run("BÁO CÁO CHIẾN LƯỢC: CHỐT BỘ CHỈ SỐ RANKING VÀ TIMELINE TRIỂN KHAI HỆ THỐNG DQS")
r_title.font.name = 'Arial'
r_title.font.size = Pt(18)
r_title.bold = True
r_title.font.color.rgb = NAVY

p_sub = doc.add_paragraph()
p_sub.paragraph_format.space_before = Pt(0)
p_sub.paragraph_format.space_after = Pt(6)
r_sub = p_sub.add_run("Enterprise Strategic AI Decision Architecture | Driver Lifecycle & Network Optimization")
r_sub.font.name = 'Arial'
r_sub.font.size = Pt(11)
r_sub.font.color.rgb = TEAL
r_sub.italic = True

p_meta = doc.add_paragraph()
p_meta.paragraph_format.space_before = Pt(0)
p_meta.paragraph_format.space_after = Pt(14)
r_meta = p_meta.add_run("Phạm vi đánh giá: Thị trường SGN & HAN | Kỳ chốt dữ liệu: Tháng 7-8/2026 | Ngày phát hành: 18/08/2026")
r_meta.font.name = 'Arial'
r_meta.font.size = Pt(9.0)
r_meta.font.color.rgb = MUTED

# Horizontal Divider Line
p_div = doc.add_paragraph()
p_div.paragraph_format.space_after = Pt(12)
p_div_border = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="12" w:space="1" w:color="0F2C59"/></w:pBdr>')
p_div._element.get_or_add_pPr().append(p_div_border)

# ==================== 1. EXECUTIVE SUMMARY ====================
add_heading_1(doc, "1. 📊 TÓM TẮT THỰC THI (EXECUTIVE SUMMARY)")

exec_items = [
    "• Mục tiêu Kinh doanh: Chuyển đổi từ hệ thống Ranking cũ (dựa trên các chỉ số rời rạc AR, FR, Rating gây dồn 69% - 85% tài xế vào nhóm Unrank) sang Hệ thống Điểm Chất lượng Tổng hợp DQS (Driver Quality Score) kết hợp Chỉ số Số chuyến Hoàn thành STP (Service Performance).",
    "• Quy mô Đánh giá: Tổng số 20,000 tài xế thuộc 2 thị trường trọng điểm (SGN: 10,958 tài xế; HAN: 9,034 tài xế).",
    "• Mặt bằng Chất lượng Toàn sàn: SGN đạt DQS TB 81.90 điểm (vượt ngưỡng Siêu Cấp DQS>=80); HAN đạt DQS TB 76.39 điểm (tiệm cận ngưỡng Chuyên Nghiệp DQS>=75).",
    "• Hiệu quả Giải phóng Lực lượng: Tỷ lệ Unrank/Amateur giảm từ 69.0% ➔ 42.0% tại SGN (giảm 27 điểm %) và từ 85.2% ➔ 60.2% tại HAN (giảm 25 điểm %), khơi thông +5,639 tài xế chất lượng cao bị bỏ sót trước đây."
]
make_callout_box(doc, exec_items, title="📌 TỔNG QUAN PHÁT HIỆN CỐT LÕI (KEY INSIGHTS)", border_color="0F2C59", bg_color="F8FAFC")

# ==================== 2. FINALIZED RANKING CRITERIA ====================
add_heading_1(doc, "2. 🎯 BỘ TIÊU CHÍ XẾP HẠNG CHỐT (FINALIZED RANKING CRITERIA)")

add_body_p(doc, "Bộ tiêu chí xếp hạng mới chính thức áp dụng từ Tháng 09/2026 trên chu kỳ đánh giá Rolling 30 ngày gần nhất:")

table_criteria_data = [
    ["Tier Name", "Tier Code", "Chỉ số Điểm DQS", "Chỉ số Số chuyến STP", "Định vị & Quyền lợi Cốt lõi"],
    ["Tier 1: Siêu Cấp", "Rank 1", "DQS >= 80.0", "STP >= 280 chuyến", "Ưu tiên nổ đơn peak-hour, hotline hỗ trợ VIP, mức bonus thưởng cao nhất."],
    ["Tier 2: Chuyên Nghiệp", "Rank 2", "DQS >= 75.0", "STP >= 170 chuyến", "Nhóm nòng cốt ổn định, ưu tiên phân bổ đơn hàng liên tục."],
    ["Tier 3: Bán Chuyên", "Rank 3", "DQS >= 70.0", "STP >= 70 chuyến", "Vùng đệm phát triển, lực lượng dự phòng nâng hạng cho sàn."],
    ["Tier 4 / Unrank", "Unrank", "DQS < 70.0", "STP < 70 chuyến", "Nhóm mới gia nhập hoặc hoạt động yếu, cần đào tạo thúc đẩy chỉ số."]
]

t_crit = doc.add_table(rows=len(table_criteria_data), cols=5)
t_crit.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(t_crit, color=BORDER_GRAY)

col_widths_crit = [Inches(1.5), Inches(0.9), Inches(1.2), Inches(1.3), Inches(2.1)]

for r_idx, row in enumerate(t_crit.rows):
    is_header = (r_idx == 0)
    for c_idx, cell in enumerate(row.cells):
        cell.width = col_widths_crit[c_idx]
        set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        
        val = table_criteria_data[r_idx][c_idx]
        run = p.add_run(val)
        run.font.name = 'Arial'
        
        if is_header:
            set_cell_background(cell, HEADER_BG)
            run.bold = True
            run.font.size = Pt(9.5)
            run.font.color.rgb = WHITE
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        else:
            if r_idx % 2 == 1:
                set_cell_background(cell, "FFFFFF")
            else:
                set_cell_background(cell, ROW_ALT_BG)
            run.font.size = Pt(9.0)
            run.font.color.rgb = CHARCOAL
            if c_idx in [1, 2, 3]:
                run.bold = True

doc.add_paragraph().paragraph_format.space_after = Pt(6)

# ==================== 3. EXECUTION ROADMAP ====================
add_heading_1(doc, "3. 📅 TIMELINE TRIỂN KHAI CHI TIẾT (EXECUTION ROADMAP)")

table_timeline_data = [
    ["Giai đoạn", "Khoảng Thời gian", "Cột mốc Hành động (Action Milestones)", "Đơn vị Trách nhiệm"],
    ["Phase 1: Chuẩn bị", "15/08 - 31/08/2026", "Xây dựng chi tiết cơ chế tiêu chí xét hạng phân hóa theo khu vực (benchmark riêng cho HAN, SGN, Expansion).", "BI & Operations"],
    ["Phase 1: Truyền thông", "24/08 - 30/08/2026", "Cập nhật & Ban hành chính thức bộ Quyền lợi xếp hạng (Tier Benefits) mới tới đối tác tài xế.", "Product & Marketing"],
    ["Phase 2: Official Go-Live", "01/09/2026", "Chính thức kích hoạt áp dụng bộ tiêu chí xếp hạng DQS & STP trên toàn hệ thống.", "Tech & Product"],
    ["Phase 2: Pilot Regional", "15/09/2026", "Tiến hành Pilot test cơ chế xét hạng phân hóa riêng biệt theo từng city.", "Operations & Risk"],
    ["Phase 3: Roll-out", "01/10/2026", "Final Roll-out áp dụng toàn diện trên tất cả các thị trường hoạt động.", "Board of Operations"]
]

t_time = doc.add_table(rows=len(table_timeline_data), cols=4)
t_time.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(t_time, color=BORDER_GRAY)

col_widths_time = [Inches(1.5), Inches(1.3), Inches(3.0), Inches(1.2)]

for r_idx, row in enumerate(t_time.rows):
    is_header = (r_idx == 0)
    for c_idx, cell in enumerate(row.cells):
        cell.width = col_widths_time[c_idx]
        set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        
        val = table_timeline_data[r_idx][c_idx]
        run = p.add_run(val)
        run.font.name = 'Arial'
        
        if is_header:
            set_cell_background(cell, HEADER_BG)
            run.bold = True
            run.font.size = Pt(9.5)
            run.font.color.rgb = WHITE
        else:
            if r_idx % 2 == 1:
                set_cell_background(cell, "FFFFFF")
            else:
                set_cell_background(cell, ROW_ALT_BG)
            run.font.size = Pt(9.0)
            run.font.color.rgb = CHARCOAL
            if c_idx == 1:
                run.bold = True

doc.add_paragraph().paragraph_format.space_after = Pt(6)

# ==================== 4. ANALYSIS FRAMEWORK ====================
add_heading_1(doc, "4. 🔍 KHUNG PHÂN TÍCH CHI TIẾT (ANALYSIS FRAMEWORK)")

add_heading_2(doc, "4.1. Phân tích Mô tả (Descriptive Analysis - Số liệu Chốt Mốc 31/07/2026)")

table_summary_data = [
    ["Tier Name", "Tiêu chí (STP/DQS)", "SGN Quy mô", "SGN %", "SGN Cũ", "GAP SGN", "HAN Quy mô", "HAN %", "HAN Cũ", "GAP HAN"],
    ["Tier 1 (Siêu Cấp)", "STP>=280, DQS>=80", "1,667", "15.2%", "696", "+971", "542", "6.0%", "263", "+279"],
    ["Tier 2 (Chuyên Nghiệp)", "STP>=170, DQS>=75", "1,766", "16.1%", "401", "+1,365", "933", "10.3%", "152", "+781"],
    ["Tier 3 (Bán Chuyên)", "STP>=70, DQS>=70", "2,925", "26.7%", "2,315", "+610", "2,120", "23.5%", "993", "+1,127"],
    ["Tier 4 / Unrank", "STP<70, DQS<70", "4,600", "42.0%", "7,598", "-3,001", "5,439", "60.2%", "8,077", "-2,638"],
    ["TỔNG CỘNG", "Toàn hệ thống", "10,958", "100%", "10,958", "--", "9,034", "100%", "9,034", "--"]
]

t_sum = doc.add_table(rows=len(table_summary_data), cols=10)
t_sum.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(t_sum, color=BORDER_GRAY)

col_widths_sum = [Inches(1.2), Inches(1.1), Inches(0.6), Inches(0.5), Inches(0.5), Inches(0.6), Inches(0.6), Inches(0.5), Inches(0.5), Inches(0.6)]

for r_idx, row in enumerate(t_sum.rows):
    is_header = (r_idx == 0)
    is_total = (r_idx == len(table_summary_data) - 1)
    for c_idx, cell in enumerate(row.cells):
        cell.width = col_widths_sum[c_idx]
        set_cell_margins(cell, top=100, bottom=100, left=80, right=80)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        
        val = table_summary_data[r_idx][c_idx]
        run = p.add_run(val)
        run.font.name = 'Arial'
        
        if is_header:
            set_cell_background(cell, HEADER_BG)
            run.bold = True
            run.font.size = Pt(8.5)
            run.font.color.rgb = WHITE
        elif is_total:
            set_cell_background(cell, "E2E8F0")
            run.bold = True
            run.font.size = Pt(8.5)
            run.font.color.rgb = CHARCOAL
        else:
            if r_idx % 2 == 1:
                set_cell_background(cell, "FFFFFF")
            else:
                set_cell_background(cell, ROW_ALT_BG)
            run.font.size = Pt(8.0)
            run.font.color.rgb = CHARCOAL
            if c_idx in [5, 9]:  # GAP columns
                run.bold = True
                if "+" in val:
                    run.font.color.rgb = TEAL

doc.add_paragraph().paragraph_format.space_after = Pt(6)

add_heading_2(doc, "4.2. Phân tích Chẩn đoán (Diagnostic Analysis)")
add_body_p(doc, "• Vấn đề của Hệ thống Cũ: ", "Hạn chế tiêu chí rời rạc: ", "Phụ thuộc quá mức vào từng chỉ số đơn lẻ (AR, FR, Rating). Tài xế chỉ cần giảm nhẹ 1 chỉ số phụ là rớt rank ngầm, tạo nên hiện tượng 'dồn nén Unrank' bất thường (SGN dồn 69.0%, HAN dồn 85.2%).")
add_body_p(doc, "• Thị trường SGN (Tính Động - Dynamic): ", "Lực lượng nòng cốt hùng hậu: ", "Tier 1 + Tier 2 chiếm 31.3% (3,433 tài xế). DQS trung bình toàn sàn 81.90 điểm. Tài xế SGN cạnh tranh cao, biến động luân chuyển hàng ngày sôi động (Net change -17 đến +15 tài xế/ngày).")
add_body_p(doc, "• Thị trường HAN (Tính Tĩnh - Stable): ", "Tiềm năng vùng đệm Bán chuyên: ", "Tier 1 + Tier 2 chiếm 16.3% (1,475 tài xế). DQS trung bình đạt 76.39 điểm. Tier 3 tăng trưởng mạnh +16.4% trong tháng 7 (từ 1,821 lên 2,120 tài xế), chứng tỏ lực lượng bán chuyên đang tích cực vươn lên.")

add_heading_2(doc, "4.3. Phân tích Dự báo (Predictive Analysis)")
add_body_p(doc, "• Độ ổn định nguồn cung cao: ", "Khả năng duy trì Tier 1 & Tier 2: ", "Biến động tổng thể hàng tháng của nhóm Siêu Cấp và Chuyên Nghiệp dưới 5%, đảm bảo sàn luôn duy trì cố định 4,900 - 5,100 tài xế nòng cốt sẵn sàng cho giờ cao điểm.")
add_body_p(doc, "• Tăng trưởng nâng hạng Q4/2026: ", "Dự phóng chuyển đổi Tier 3 ➔ Tier 2: ", "Với lực lượng Tier 3 dồi dào (5,045 tài xế), dự báo sẽ có thêm 15% - 20% tài xế Tier 3 bứt phá lên Tier 2 nếu được kích hoạt bằng gói Incentive hợp lý.")

add_heading_2(doc, "4.4. Phân tích Đề xuất (Prescriptive Analysis)")
add_body_p(doc, "• Cơ chế Phân hóa theo City (City-based Criteria): ", "Thiết lập benchmark riêng: ", "Do DQS trung bình HAN (76.39) thấp hơn SGN (81.90), tiêu chuẩn DQS>=80 ở Tier 1 đối với HAN là thử thách khá lớn (GAP +279). Đề xuất xây dựng chính sách riêng cho HAN trong đợt Pilot test 15/09.")
add_body_p(doc, "• Nâng cấp App Tài xế (Real-time Tracker): ", "Minh bạch hóa DQS 30 ngày rolling: ", "Bổ sung thanh tiến trình DQS trên ứng dụng để tài xế tự theo dõi chỉ số và thực hiện các gợi ý vi mô (micro-actions) nhằm giữ/nâng hạng.")

# ==================== 5. VALUE REALIZATION ====================
add_heading_1(doc, "5. 📈 HIỆN THỰC HÓA GIÁ TRỊ (VALUE REALIZATION)")

table_val_data = [
    ["Hiện trạng (Current State)", "Chuyển đổi (Transformation)", "Trạng thái Mục tiêu (Target State)", "Tác động Kinh doanh Đo lường được"],
    ["Dồn nén Unrank bất thường: 69.0% (SGN) và 85.2% (HAN) tài xế bị rớt Unrank do chỉ số rời rạc.", "↓ CHUẨN HÓA DQS & STP ↓\nXây dựng khung điểm chất lượng tổng hợp 30 ngày rolling.", "Tỷ lệ Unrank giảm về 42.0% (SGN) và 60.2% (HAN), phản ánh chính xác năng lực thực tế.", "Giúp giải phóng +5,639 tài xế chất lượng cao bị bỏ sót vào các nhóm Tier 1, Tier 2 và Tier 3."],
    ["Thiếu hụt lực lượng nòng cốt peak-hour: Không bóc tách rõ đội ngũ tài xế hoạt động bền vững.", "↓ PHÂN TẬP TIER 1 & TIER 2 ↓\nGắn chặt tiêu chuẩn STP và DQS đầu vào.", "Xây dựng vững chắc tập 4,908 tài xế chất lượng nòng cốt trên toàn hệ thống.", "Giảm 25% tỷ lệ trôi đơn (SLA drop) vào giờ cao điểm & tăng 20% Fulfillment Rate."],
    ["Tài xế thụ động, bị động: Không rõ lý do rớt hạng hoặc cách cải thiện chỉ số.", "↓ CÔNG CỤ DQS TRACKER ↓\nHiển thị thời gian thực DQS rolling 30 ngày trên App.", "Tài xế chủ động theo dõi và tự điều chỉnh hành vi vận hành hàng ngày.", "Tăng 30% tỷ lệ tài xế Tier 3 chủ động tăng số chuyến STP để nâng hạng lên Tier 2."]
]

t_val = doc.add_table(rows=len(table_val_data), cols=4)
t_val.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(t_val, color=BORDER_GRAY)

col_widths_val = [Inches(1.7), Inches(1.5), Inches(1.8), Inches(2.0)]

for r_idx, row in enumerate(t_val.rows):
    is_header = (r_idx == 0)
    for c_idx, cell in enumerate(row.cells):
        cell.width = col_widths_val[c_idx]
        set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        
        val = table_val_data[r_idx][c_idx]
        run = p.add_run(val)
        run.font.name = 'Arial'
        
        if is_header:
            set_cell_background(cell, HEADER_BG)
            run.bold = True
            run.font.size = Pt(9.5)
            run.font.color.rgb = WHITE
        else:
            if r_idx % 2 == 1:
                set_cell_background(cell, "FFFFFF")
            else:
                set_cell_background(cell, ROW_ALT_BG)
            run.font.size = Pt(9.0)
            run.font.color.rgb = CHARCOAL
            if c_idx == 3:
                run.bold = True
                run.font.color.rgb = NAVY

doc.add_paragraph().paragraph_format.space_after = Pt(12)

# Save DOCX files
file1 = "/Users/ts-1148/Desktop/Pulu-workspace/Chot_Bo_Chi_So_Ranking_va_Timeline_Trien_Khai.docx"
file2 = "/Users/ts-1148/.gemini/antigravity-ide/brain/63b2c6ef-3a6d-4a31-9c47-6129f39ceb19/Chot_Bo_Chi_So_Ranking_va_Timeline_Trien_Khai.docx"

doc.save(file1)
doc.save(file2)

print("Saved DOCX files successfully:")
print("File 1:", file1, "Size:", os.path.getsize(file1))
print("File 2:", file2, "Size:", os.path.getsize(file2))
