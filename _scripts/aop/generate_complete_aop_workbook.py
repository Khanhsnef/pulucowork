# -*- coding: utf-8 -*-
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import os

wb = openpyxl.Workbook()
wb.remove(wb.active) # Remove default blank sheet

# -------------------------------------------------------------
# PALETTE & STYLES (Ahamove Brand Standards)
# -------------------------------------------------------------
ORANGE_PRIMARY = "FF6B00"       # Primary Orange
ORANGE_DARK = "D95A00"
ORANGE_LIGHT = "FFF3EB"         # Soft Orange Tint for Highlights / Cards
DARK_SLATE = "1E293B"           # Slate Dark for Headers
MUTED_SLATE = "64748B"          # Slate Muted for Subtitles
BORDER_COLOR = "CBD5E1"
ZEBRA_ROW = "F8FAFC"            # Light Gray
CARD_BG = "F8FAFC"              # Card Neutral
TOTAL_BG = "FFF7ED"             # Light Amber for Subtotals
GRAND_TOTAL_BG = "FFEDD5"       # Warm Orange for Grand Total
BLOCK_A_BG = "0284C7"           # Sky Blue for Core Ops
BLOCK_B_BG = "B45309"           # Amber for Strategic

font_title = Font(name="Segoe UI", size=14, bold=True, color="FFFFFF")
font_subtitle = Font(name="Segoe UI", size=9, italic=True, color="FFFFFF")
font_section = Font(name="Segoe UI", size=11, bold=True, color=DARK_SLATE)
font_tbl_header = Font(name="Segoe UI", size=9, bold=True, color="FFFFFF")
font_subtotal = Font(name="Segoe UI", size=9, bold=True, color=DARK_SLATE)
font_grand = Font(name="Segoe UI", size=10, bold=True, color="9A3412")
font_bold = Font(name="Segoe UI", size=9, bold=True, color="1E293B")
font_regular = Font(name="Segoe UI", size=9, color="1E293B")
font_muted = Font(name="Segoe UI", size=8, italic=True, color=MUTED_SLATE)

fill_primary = PatternFill(start_color=ORANGE_PRIMARY, end_color=ORANGE_PRIMARY, fill_type="solid")
fill_dark = PatternFill(start_color=DARK_SLATE, end_color=DARK_SLATE, fill_type="solid")
fill_zebra = PatternFill(start_color=ZEBRA_ROW, end_color=ZEBRA_ROW, fill_type="solid")
fill_subtotal = PatternFill(start_color=TOTAL_BG, end_color=TOTAL_BG, fill_type="solid")
fill_grand = PatternFill(start_color=GRAND_TOTAL_BG, end_color=GRAND_TOTAL_BG, fill_type="solid")
fill_card = PatternFill(start_color=CARD_BG, end_color=CARD_BG, fill_type="solid")
fill_card_head = PatternFill(start_color=ORANGE_LIGHT, end_color=ORANGE_LIGHT, fill_type="solid")

thin_side = Side(border_style="thin", color=BORDER_COLOR)
med_side = Side(border_style="medium", color=ORANGE_PRIMARY)
double_side = Side(border_style="double", color=DARK_SLATE)

border_all = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)
border_header = Border(left=thin_side, right=thin_side, top=thin_side, bottom=med_side)
border_subtotal = Border(top=thin_side, bottom=thin_side, left=thin_side, right=thin_side)
border_grand = Border(top=thin_side, bottom=double_side, left=thin_side, right=thin_side)

align_center = Alignment(horizontal="center", vertical="center")
align_left = Alignment(horizontal="left", vertical="center", wrap_text=True)
align_right = Alignment(horizontal="right", vertical="center")
align_header = Alignment(horizontal="center", vertical="center", wrap_text=True)

# ==============================================================================
# SHEET 1: 01_Master_AOP_Budget (Create First to ensure safe cross-referencing)
# ==============================================================================
ws1 = wb.create_sheet(title="01_Master_AOP_Budget")
ws1.views.sheetView[0].showGridLines = True

ws1.merge_cells("A1:AE1")
ws1["A1"] = "AHAMOVE - MASTER AOP 2026: KẾ HOẠCH CHI TIẾT NGÂN SÁCH ĐỘI NGŨ TÀI XẾ (DRIVER MANAGEMENT NATIONWIDE)"
ws1["A1"].font = font_title
ws1["A1"].fill = fill_primary
ws1["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
ws1.row_dimensions[1].height = 30

ws1.merge_cells("A2:AE2")
ws1["A2"] = "Chuẩn hóa từ Sheet [AOP 2026] Chi phí Team ver 2 | Tách biệt Core Ops vs Strategic Transformation | Đơn vị: VNĐ"
ws1["A2"].font = font_subtitle
ws1["A2"].fill = fill_dark
ws1["A2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
ws1.row_dimensions[2].height = 18

master_headers = [
    "Mã ID", "Khối & Nhóm Chi Phí", "Hạng Mục Chi Tiết / Chương Trình", "Mục Tiêu Chiến Lược (Aim)", 
    "Mã AOP (FA)", "PIC", "Khu Vực", "Dòng Xe", "Mức Ưu Tiên", "Chỉ Số Đo Lường (KPIs)", 
    "Cơ Sở Tính Toán (Drivers & Assumptions)", "Ghi Chú Điều Chỉnh (Notes)", "Actual 2025", 
    "AOP 2026 Budget", "Quý 1 (Q1)", "Quý 2 (Q2)", "Quý 3 (Q3)", "Quý 4 (Q4)", "Chênh Lệch vs 2025",
    "Tháng 1", "Tháng 2", "Tháng 3", "Tháng 4", "Tháng 5", "Tháng 6", 
    "Tháng 7", "Tháng 8", "Tháng 9", "Tháng 10", "Tháng 11", "Tháng 12"
]

ws1.row_dimensions[3].height = 28
for c_idx, h in enumerate(master_headers, start=1):
    cell = ws1.cell(3, c_idx, h)
    cell.font = font_tbl_header
    cell.fill = fill_dark
    cell.alignment = align_header
    cell.border = border_header

master_items = [
    # NHÓM 1: EVENT & VINH DANH (Rows 4 to 17)
    ("DM-EVT-01", "1. Event & Vinh Danh", "Vinh danh (Offline) mỗi quý", "Maintain retention & chất lượng Fulltime", "1401_C493_4802", "DS", "NW", "Fulltime", "Must have", "High driver capacity & GDR", "Gộp chi phí vinh danh + Phụ nữ VN + Ahacup; +30% quy mô (500 HAN, 700 SGN)", "Đề xuất 2027: Làm 2 lần/năm (T4 & T10)", 0, [0, 0, 120000000, 0, 0, 120000000, 0, 0, 120000000, 0, 0, 0]),
    ("DM-EVT-02", "1. Event & Vinh Danh", "Minigame online / Mini Contest đua đơn", "Maintain retention & GDR", "1401_C493_4802", "DS", "NW", "All Fleet", "Must have", "GDR, CTR, CR", "Duy trì tương tác trực tuyến thường xuyên hàng tháng (trừ T3, T6, T9 dồn vinh danh)", "10M/tháng cho 9 tháng", 0, [10000000, 10000000, 0, 10000000, 10000000, 0, 10000000, 10000000, 0, 10000000, 10000000, 10000000]),
    ("DM-EVT-03", "1. Event & Vinh Danh", "Livestream tổng kết năm + Tổng kết Quý", "Driver Loyalty & Engagement", "1401_C493_4802", "DS", "NW", "All Fleet", "Must have", "Capacity all segments", "Tri ân toàn quốc trước dịp Tết Nguyên Đán", "+15% theo GSV", 0, [100000000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    ("DM-EVT-04", "1. Event & Vinh Danh", "Quốc Tế Phụ Nữ (08/03)", "Driver Loyalty & Engagement", "1401_C493_4802", "DS", "NW", "Female Drivers", "Should have", "Engagement (CSAT), Retention", "SGN: 20M, HAN: 20M tri ân đối tác nữ", "+15% theo GSV", 0, [0, 0, 40000000, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    ("DM-EVT-05", "1. Event & Vinh Danh", "Ngày hội gia đình (28/6) & Quốc Tế Thiếu Nhi", "Driver Loyalty & Engagement", "1401_C493_4802", "DS", "NW", "All Fleet", "Should have", "Engagement (CSAT), Retention", "Tổ chức ngày hội gia đình cho con em tài xế", "Chuyển hình thức làm Online để tối ưu chi phí", 0, [0, 0, 0, 0, 0, 60000000, 0, 0, 0, 0, 0, 0]),
    ("DM-EVT-06", "1. Event & Vinh Danh", "Campaign sinh nhật Ahamove (10 tuổi)", "Driver Loyalty & Engagement", "1401_C493_4802", "DS", "NW", "All Fleet", "Must have", "Capacity all segments", "Đại lễ kỷ niệm 10 năm thành lập Ahamove", "Cần kết hợp với Marketing để đồng bộ", 0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 100000000, 0, 0]),
    ("DM-EVT-07", "1. Event & Vinh Danh", "Sự kiện Trung thu", "Driver Loyalty & Engagement", "1401_C493_4802", "DS", "NW", "All Fleet", "Must have", "Engagement (CSAT)", "SGN: 25M, HAN: 25M trao quà cho con tài xế", "Tăng tập tài xế năng suất của mỗi miền", 0, [0, 0, 0, 0, 0, 0, 0, 0, 50000000, 0, 0, 0]),
    ("DM-EVT-08", "1. Event & Vinh Danh", "Chương trình 20/10 - Phụ nữ Việt Nam", "Driver Loyalty & Engagement", "1401_C493_4802", "DS", "NW", "Female Drivers", "Must have", "Engagement (CSAT)", "Tri ân nữ tài xế đợt 2 trong năm", "Đề xuất đẩy cost vào sự kiện vinh danh", 0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 40000000, 0, 0]),
    ("DM-EVT-09", "1. Event & Vinh Danh", "Quốc tế Đàn ông (19/11)", "Driver Loyalty & Engagement", "1401_C493_4802", "DS", "NW", "Male Drivers", "Nice to have", "Engagement (CSAT)", "SGN: 20M, HAN: 20M tôn vinh tài xế nam", "Có thể cắt giảm nếu cần tối ưu ngân sách", 0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 40000000, 0]),
    ("DM-EVT-10", "1. Event & Vinh Danh", "AhaCup (Giải bóng đá tài xế)", "Driver Loyalty & Engagement", "1401_C493_4802", "DS", "NW", "Community", "Must have", "Engagement (CSAT), Retention", "SGN: 60M, HAN: 60M giải đấu thể thao thường niên", "Gắn kết các câu lạc bộ tài xế địa phương", 0, [0, 0, 0, 0, 0, 0, 60000000, 60000000, 0, 0, 0, 0]),
    ("DM-EVT-11", "1. Event & Vinh Danh", "Giáng Sinh - Tết Dương Lịch", "Driver Loyalty & Engagement", "1401_C493_4802", "DS", "NW", "All Fleet", "Must have", "Capacity all segments", "Hoạt động truyền thông, quà tặng cuối năm", "+15% theo GSV tăng trưởng", 0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 60000000]),
    ("DM-EVT-12", "1. Event & Vinh Danh", "Tiếp sức, hỗ trợ thiên tai bão lũ", "Driver Loyalty & Trách nhiệm xã hội", "1401_C493_4802", "DS", "HAN & EXP", "All Fleet", "Must have", "Retention, CSAT", "70M hỗ trợ tài xế miền Bắc và miền Trung (bão lũ M7-M10)", "Dựa theo dữ liệu lịch sử bão lũ 2025", 0, [0, 0, 0, 0, 0, 0, 10000000, 20000000, 20000000, 20000000, 0, 0]),
    ("DM-EVT-13", "1. Event & Vinh Danh", "Lì xì kéo active sau Tết", "Đảm bảo performance sau Tết", "1401_C493_4802", "DS", "NW", "Active Drivers", "Should have", "Active drivers, Retention", "SGN: 5M, HAN: 10M lì xì đầu xuân kích hoạt nguồn cung", "Cần review lại số thực tế 2025", 0, [0, 15000000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    ("DM-EVT-14", "1. Event & Vinh Danh", "Tiếp sức Campaign (All sectors / Door gift)", "Đảm bảo capacity mùa cao điểm", "1401_C493_4802", "DS", "NW", "All Fleet", "Should have", "Active drivers, WH Capacity", "Dự phòng hỗ trợ các campaign đột xuất", "Hiện để 0, linh hoạt điều phối từ quỹ chung", 0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),

    # NHÓM 2: QUẢN TRỊ & PHÚC LỢI (Rows 19 to 26)
    ("DM-OPS-01", "2. Quản Trị & Phúc Lợi", "Bảo hiểm tai nạn tài xế Fulltime", "Phúc lợi nòng cốt giữ chân Fulltime", "1401_A112_4603", "DS", "NW", "Fulltime", "Must have", "Capacity segment", "Mua gói BHTN hàng tháng cho tài xế chuyên trách", "Tiết kiệm 37% vs 2025 (474.6M) nhờ danh sách chuẩn", 474600000, [24261135, 24260257, 22787400, 29162444, 22787400, 32475194, 26322344, 22881334, 23350474, 23365424, 22973644, 23913857]),
    ("DM-OPS-02", "2. Quản Trị & Phúc Lợi", "Chi phí thuê nhân sự ngoài (FL Call)", "Hỗ trợ onboarding, GDR, CTR", "1401_C493_4802", "DS", "NW", "New Drivers", "Must have", "Good driver rate, CTR, Retention", "Thuê nhân sự call push active, dự kiến contribute 70% cap", "Chuyển dần sang đội ngũ đội trưởng", 0, [30000000, 20000000, 20000000, 20000000, 20000000, 20000000, 20000000, 20000000, 20000000, 30000000, 30000000, 30000000]),
    ("DM-OPS-03", "2. Quản Trị & Phúc Lợi", "Chi phí SMS / ZNS push active & thông tin", "Truyền thông vận hành daily", "1401_C5_5608", "DS", "NW", "All Fleet", "Must have", "Active drivers, Response rate", "SMS push thông báo cuốc, incentive, chính sách", "Chi phí mới 2026 cho các mô hình tài xế mới", 0, [20000000, 20000000, 15000000, 15000000, 15000000, 15000000, 15000000, 15000000, 15000000, 20000000, 20000000, 20000000]),
    ("DM-OPS-04", "2. Quản Trị & Phúc Lợi", "Sản xuất bánh Trung thu tri ân tài xế", "Driver Loyalty & Thâm niên", "1401_C494_5607", "DS", "NW", "VIP & Senior", "Must have", "Engagement, Retention", "Mua quà tặng bánh Trung thu cho tài xế VIP/thâm niên", "+15% theo GSV (80M * 115% = 92M)", 0, [0, 0, 0, 0, 0, 0, 0, 0, 80000000, 0, 0, 0]),
    ("DM-OPS-05", "2. Quản Trị & Phúc Lợi", "Sản xuất quà Tết tri ân tài xế", "Driver Loyalty & Thâm niên", "1401_C494_5607", "DS", "NW", "VIP & Senior", "Must have", "Engagement, Retention", "Mua quà tặng Tết cho tài xế nòng cốt dịp cuối năm", "+15% theo GSV", 0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 140000000]),
    ("DM-OPS-06", "2. Quản Trị & Phúc Lợi", "Quỹ Hỗ trợ Tấm Lòng Cam", "Hỗ trợ tài xế gặp rủi ro tai nạn", "1401_C493_4802", "DS", "NW", "All Fleet", "Should have", "Engagement (CSAT)", "Quỹ hỗ trợ nhân văn khẩn cấp 5M/tháng cho cả 2 miền", "Giữ nguyên mức chi 5M/tháng", 0, [5000000, 5000000, 5000000, 5000000, 5000000, 5000000, 5000000, 5000000, 5000000, 5000000, 5000000, 5000000]),
    ("DM-OPS-07", "2. Quản Trị & Phúc Lợi", "Xuất kho quà tặng Tài xế (2-Wheel / Bike)", "Khen thưởng theo campaign lớn", "1401_C494_5607", "DS", "NW", "Bike Fleet", "Must have", "Capacity segment", "Phân bổ theo kế hoạch sử dụng quà tặng các sự kiện lớn", "Tập trung các tháng chiến dịch, tránh dàn trải", 269700000, [50000000, 20000000, 50000000, 20000000, 20000000, 50000000, 20000000, 50000000, 50000000, 20000000, 20000000, 50000000]),
    ("DM-OPS-08", "2. Quản Trị & Phúc Lợi", "Xuất kho quà tặng & Trang thiết bị (4-Wheel / Truck)", "Hỗ trợ trang bị đội xe tải", "1401_C494_5607", "DS", "NW", "Truck Fleet", "Must have", "Capacity segment", "Xe đẩy, thang, móc kéo, bạt xe tải, đồng phục", "Dự phòng mở rộng phân khúc xe tải", 0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),

    # NHÓM 3: ĐỘI TRƯỞNG (Rows 28 to 29)
    ("DM-CAP-01", "3. Đội Ngũ Đội Trưởng", "Lương cơ bản Đội trưởng (04 Đội trưởng)", "Quản trị & điều phối đội ngũ tại Hub", "1401_C493_4802", "DM", "NW", "Captains", "Must have", "Capacity đội, Lead driver", "Lương base chi trả hàng tháng cho 4 đội trưởng nòng cốt", "T1: 18M, T2-T12: 24M/tháng", 105270000, [18000000, 24000000, 24000000, 24000000, 24000000, 24000000, 24000000, 24000000, 24000000, 24000000, 24000000, 24000000]),
    ("DM-CAP-02", "3. Đội Ngũ Đội Trưởng", "Bonus hiệu suất Đội trưởng", "Khích lệ năng suất & phát triển fleet", "1401_C493_4802", "DM", "NW", "Captains", "Must have", "Capacity đội", "Commission sau đánh giá năng suất", "Đã gộp thẳng vào lương cơ bản", 0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),

    # NHÓM 4: CHUYỂN ĐỔI XE ĐIỆN (Rows 32 to 33)
    ("DM-STR-01", "4. Chuyển Đổi Xe Điện", "Hỗ trợ chi phí sạc điện theo km hoạt động", "Khuyến khích chuyển đổi xe máy điện", "TBC", "DM", "HAN", "Electric Bike", "Must have", "EV Active Drivers, Transition Rate", "Hỗ trợ chi phí sạc cho tháng hoạt động đầu tiên & theo km", "Chính sách trọng điểm 2026 đảm bảo active xe điện T7/2026", 0, [0, 397052020, 681942830, 1161073157, 1376145946, 1669696697, 1964042128, 0, 0, 0, 0, 0]),
    ("DM-STR-02", "4. Chuyển Đổi Xe Điện", "Supply Costs - Hỗ trợ chiết khấu 3-5%", "Bảo đảm thu nhập tài xế chuyển đổi xe điện", "TBC", "DM", "HAN", "Electric Bike", "Must have", "EV Active Drivers, GDR", "Giảm chiết khấu 3% - 5% theo lộ trình từng tháng", "Lộ trình chuyển đổi dần đảm bảo cung ứng", 0, [0, 189706304, 230029941, 207467400, 206786762, 198039935, 199351725, 226574838, 221024949, 329499719, 327646445, 375967737]),

    # NHÓM 5: GOPIKA PROJECT (Rows 35 to 37)
    ("DM-STR-03", "5. Gopika Station Fleet", "Supply cost (Gopika Dedicated Station)", "Vận hành đội xe chuyên trách Hub/Station", "TBC2", "DM", "HAN", "Station Fleet", "Must have", "Fulfillment Rate Station, SLA", "Chi phí cung ứng xe chuyên trách phục vụ đơn hàng trạm", "Dự án hợp tác chiến lược mới năm 2026", 0, [621105748, 549287372, 685482168, 794747535, 984882208, 1087393722, 1263270048, 1588568736, 1631351861, 1755698037, 1470513630, 1656315244]),
    ("DM-STR-04", "5. Gopika Station Fleet", "Chiết khấu 5% (Gopika Station)", "Khuyến khích tài xế nhận đơn trạm", "TBC2", "DM", "HAN", "Station Fleet", "Must have", "Acceptance Rate Station", "Mức chiết khấu 5% cho đội xe nhận đơn Station", "Chi phí phát sinh mới cho Gopika Project", 0, [38819109, 34330461, 42842636, 49671721, 61555138, 67962108, 78954378, 99285546, 101959491, 109731127, 91907102, 103519703]),
    ("DM-STR-05", "5. Gopika Station Fleet", "Hỗ trợ phí nộp tiền mặt 0.7% (Gopika COD)", "Giảm chi phí giao dịch tiền mặt", "TBC2", "DM", "HAN", "Station Fleet", "Must have", "COD Reconcile SLA", "0.7% chi phí nộp tiền mặt COD của đội xe trạm", "Hỗ trợ tài xế trạm nộp COD hàng ngày", 0, [1739096, 1538005, 1919350, 2225293, 2757670, 3044702, 3537156, 4447992, 4567785, 4915955, 4117438, 4637683]),
]

def write_master_row(ws, r_idx, item_tuple):
    (m_id, grp, name, aim, code, pic, city, fleet, prio, kpis, basis, notes, act2025, months) = item_tuple
    ws.row_dimensions[r_idx].height = 20
    ws.cell(r_idx, 1, m_id).alignment = align_center
    ws.cell(r_idx, 2, grp).alignment = align_left
    ws.cell(r_idx, 3, name).alignment = align_left
    ws.cell(r_idx, 4, aim).alignment = align_left
    ws.cell(r_idx, 5, code).alignment = align_center
    ws.cell(r_idx, 6, pic).alignment = align_center
    ws.cell(r_idx, 7, city).alignment = align_center
    ws.cell(r_idx, 8, fleet).alignment = align_center
    ws.cell(r_idx, 9, prio).alignment = align_center
    ws.cell(r_idx, 10, kpis).alignment = align_left
    ws.cell(r_idx, 11, basis).alignment = align_left
    ws.cell(r_idx, 12, notes).alignment = align_left
    
    c_act = ws.cell(r_idx, 13, act2025)
    c_act.number_format = "#,##0"
    c_act.alignment = align_right
    
    ws.cell(r_idx, 14, f"=SUM(T{r_idx}:AE{r_idx})").number_format = "#,##0"
    ws.cell(r_idx, 15, f"=SUM(T{r_idx}:V{r_idx})").number_format = "#,##0"
    ws.cell(r_idx, 16, f"=SUM(W{r_idx}:Y{r_idx})").number_format = "#,##0"
    ws.cell(r_idx, 17, f"=SUM(Z{r_idx}:AB{r_idx})").number_format = "#,##0"
    ws.cell(r_idx, 18, f"=SUM(AC{r_idx}:AE{r_idx})").number_format = "#,##0"
    ws.cell(r_idx, 19, f"=N{r_idx}-M{r_idx}").number_format = "#,##0"
    
    for m_idx, m_val in enumerate(months, start=20):
        cell_m = ws.cell(r_idx, m_idx, m_val)
        cell_m.number_format = "#,##0"
        cell_m.alignment = align_right
        
    for c in range(1, 32):
        cell = ws.cell(r_idx, c)
        cell.border = border_all
        cell.font = font_bold if c in [1, 3, 14] else font_regular
        if r_idx % 2 == 1:
            cell.fill = fill_zebra

def write_subtotal_row(ws, r_idx, label, start_r, end_r, is_block=False, block_letter=""):
    ws.row_dimensions[r_idx].height = 22
    ws.cell(r_idx, 1, block_letter if is_block else "SUB").alignment = align_center
    ws.cell(r_idx, 2, label).alignment = align_left
    ws.cell(r_idx, 3, "").alignment = align_left
    
    fill_to_use = fill_grand if is_block else fill_subtotal
    font_to_use = font_grand if is_block else font_subtotal
    border_to_use = border_grand if is_block else border_subtotal
    
    ws.cell(r_idx, 13, f"=SUM(M{start_r}:M{end_r})").number_format = "#,##0"
    ws.cell(r_idx, 14, f"=SUM(N{start_r}:N{end_r})").number_format = "#,##0"
    ws.cell(r_idx, 15, f"=SUM(O{start_r}:O{end_r})").number_format = "#,##0"
    ws.cell(r_idx, 16, f"=SUM(P{start_r}:P{end_r})").number_format = "#,##0"
    ws.cell(r_idx, 17, f"=SUM(Q{start_r}:Q{end_r})").number_format = "#,##0"
    ws.cell(r_idx, 18, f"=SUM(R{start_r}:R{end_r})").number_format = "#,##0"
    ws.cell(r_idx, 19, f"=N{r_idx}-M{r_idx}").number_format = "#,##0"
    
    for c in range(20, 32):
        col_l = get_column_letter(c)
        ws.cell(r_idx, c, f"=SUM({col_l}{start_r}:{col_l}{end_r})").number_format = "#,##0"
        
    for c in range(1, 32):
        cell = ws.cell(r_idx, c)
        cell.border = border_to_use
        cell.font = font_to_use
        cell.fill = fill_to_use
        if c >= 13:
            cell.alignment = align_right

# 1. Nhóm 1: Event (Items 0..13) -> rows 4..17
r = 4
for item in master_items[0:14]:
    write_master_row(ws1, r, item)
    r += 1
# Subtotal Nhóm 1 at row 18
write_subtotal_row(ws1, 18, "TỔNG NHÓM 1: CHI PHÍ EVENT & VINH DANH", 4, 17)
r = 19

# 2. Nhóm 2: Quản trị & Phúc lợi (Items 14..21) -> rows 19..26
for item in master_items[14:22]:
    write_master_row(ws1, r, item)
    r += 1
# Subtotal Nhóm 2 at row 27
write_subtotal_row(ws1, 27, "TỔNG NHÓM 2: CHI PHÍ QUẢN TRỊ & PHÚC LỢI VẬN HÀNH", 19, 26)
r = 28

# 3. Nhóm 3: Đội trưởng (Items 22..23) -> rows 28..29
for item in master_items[22:24]:
    write_master_row(ws1, r, item)
    r += 1
# Subtotal Nhóm 3 at row 30
write_subtotal_row(ws1, 30, "TỔNG NHÓM 3: CHI PHÍ ĐỘI NGŨ ĐỘI TRƯỞNG", 28, 29)

# BLOCK A TOTAL at row 31
r = 31
ws1.row_dimensions[r].height = 24
ws1.cell(r, 1, "BLOCK A").alignment = align_center
ws1.cell(r, 2, "TỔNG KHỐI A: CHI PHÍ VẬN HÀNH THƯỜNG NHẬT TEAM DM (CORE OPEX)").alignment = align_left
for c in range(13, 32):
    col_l = get_column_letter(c)
    ws1.cell(r, c, f"={col_l}18+{col_l}27+{col_l}30").number_format = "#,##0"
for c in range(1, 32):
    cell = ws1.cell(r, c)
    cell.border = border_grand
    cell.font = Font(name="Segoe UI", size=10, bold=True, color="0369A1")
    cell.fill = PatternFill(start_color="E0F2FE", end_color="E0F2FE", fill_type="solid")
    if c >= 13:
        cell.alignment = align_right

# 4. Nhóm 4: Xe điện (Items 24..25) -> rows 32..33
r = 32
for item in master_items[24:26]:
    write_master_row(ws1, r, item)
    r += 1
# Subtotal Nhóm 4 at row 34
write_subtotal_row(ws1, 34, "TỔNG NHÓM 4: DỰ ÁN CHUYỂN ĐỔI XE MÁY ĐIỆN", 32, 33)
r = 35

# 5. Nhóm 5: Gopika (Items 26..28) -> rows 35..37
for item in master_items[26:29]:
    write_master_row(ws1, r, item)
    r += 1
# Subtotal Nhóm 5 at row 38
write_subtotal_row(ws1, 38, "TỔNG NHÓM 5: DỰ ÁN GOPIKA - DEDICATED STATION FLEET", 35, 37)

# BLOCK B TOTAL at row 39
r = 39
ws1.row_dimensions[r].height = 24
ws1.cell(r, 1, "BLOCK B").alignment = align_center
ws1.cell(r, 2, "TỔNG KHỐI B: DỰ ÁN CHIẾN LƯỢC CHUYỂN ĐỔI MÔ HÌNH").alignment = align_left
for c in range(13, 32):
    col_l = get_column_letter(c)
    ws1.cell(r, c, f"={col_l}34+{col_l}38").number_format = "#,##0"
for c in range(1, 32):
    cell = ws1.cell(r, c)
    cell.border = border_grand
    cell.font = Font(name="Segoe UI", size=10, bold=True, color="B45309")
    cell.fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
    if c >= 13:
        cell.alignment = align_right

# GRAND TOTAL at row 40
r = 40
ws1.row_dimensions[r].height = 28
ws1.cell(r, 1, "★").alignment = align_center
ws1.cell(r, 2, "TỔNG CỘNG TOÀN BỘ NGÂN SÁCH AOP 2026 (KHỐI A + KHỐI B)").alignment = align_left
for c in range(13, 32):
    col_l = get_column_letter(c)
    ws1.cell(r, c, f"={col_l}31+{col_l}39").number_format = "#,##0"
for c in range(1, 32):
    cell = ws1.cell(r, c)
    cell.border = border_grand
    cell.font = Font(name="Segoe UI", size=11, bold=True, color="7C2D12")
    cell.fill = fill_grand
    if c >= 13:
        cell.alignment = align_right

ws1.freeze_panes = "D4"
col_widths_1 = {
    "A": 12, "B": 24, "C": 35, "D": 28, "E": 14, "F": 8, "G": 10, "H": 12, "I": 12,
    "J": 25, "K": 35, "L": 30, "M": 14, "N": 16, "O": 13, "P": 13, "Q": 13, "R": 13, "S": 14,
    "T": 12, "U": 12, "V": 12, "W": 12, "X": 12, "Y": 12, "Z": 12, "AA": 12, "AB": 12, "AC": 12, "AD": 12, "AE": 12
}
for col_l, w in col_widths_1.items():
    ws1.column_dimensions[col_l].width = w

# ==============================================================================
# SHEET 0: 00_Executive_Dashboard
# ==============================================================================
ws0 = wb.create_sheet(title="00_Executive_Dashboard", index=0)
ws0.views.sheetView[0].showGridLines = True

ws0.merge_cells("A1:K1")
ws0["A1"] = "AHAMOVE - BẢNG ĐIỀU HÀNH KẾ HOẠCH NGÂN SÁCH AOP 2026 (DRIVER MANAGEMENT)"
ws0["A1"].font = font_title
ws0["A1"].fill = fill_primary
ws0["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
ws0.row_dimensions[1].height = 32

ws0.merge_cells("A2:K2")
ws0["A2"] = "Driver Operations & Strategic Transformation Budget | Đơn vị tính: VNĐ | Nguồn: [AOP 2026] Chi phí Team ver 2"
ws0["A2"].font = font_subtitle
ws0["A2"].fill = fill_dark
ws0["A2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
ws0.row_dimensions[2].height = 20

cards = [
    ("B4:C4", "B5:C5", "B6:C6", "TỔNG NGÂN SÁCH TOÀN BỘ (FY2026)", "=01_Master_AOP_Budget!N40", "Gồm Core Ops + Xe điện + Gopika"),
    ("D4:E4", "D5:E5", "D6:E6", "NGÂN SÁCH VẬN HÀNH CORE TEAM DM", "=01_Master_AOP_Budget!N31", "+29.7% vs Actual 2025 (2.24 tỷ)"),
    ("F4:G4", "F5:G5", "F6:G6", "DỰ ÁN CHIẾN LƯỢC (EV & GOPIKA)", "=01_Master_AOP_Budget!N39", "Chiếm 89.5% tổng ngân sách AOP"),
    ("H4:I4", "H5:I5", "H6:I6", "TỶ TRỌNG MUST-HAVE (CORE TEAM)", "=01_Master_AOP_Budget!N31-175000000-40000000", "2.70 tỷ (92.6% ngân sách Core)"),
]

for top_r, mid_r, bot_r, label, val_formula, note in cards:
    ws0.merge_cells(top_r)
    c_top = ws0[top_r.split(":")[0]]
    c_top.value = label
    c_top.font = Font(name="Segoe UI", size=8, bold=True, color=MUTED_SLATE)
    c_top.fill = fill_card_head
    c_top.alignment = align_center
    
    ws0.merge_cells(mid_r)
    c_mid = ws0[mid_r.split(":")[0]]
    c_mid.value = val_formula
    c_mid.font = Font(name="Segoe UI", size=14, bold=True, color=ORANGE_PRIMARY)
    c_mid.fill = fill_card
    c_mid.alignment = align_center
    c_mid.number_format = "#,##0"
    
    ws0.merge_cells(bot_r)
    c_bot = ws0[bot_r.split(":")[0]]
    c_bot.value = note
    c_bot.font = Font(name="Segoe UI", size=8, italic=True, color="64748B")
    c_bot.fill = fill_card
    c_bot.alignment = align_center

ws0.row_dimensions[4].height = 20
ws0.row_dimensions[5].height = 28
ws0.row_dimensions[6].height = 18

ws0["A8"] = "I. TIẾN ĐỘ PHÂN BỔ NGÂN SÁCH THEO PHÂN KỲ & QUÝ (QUARTERLY PHASING)"
ws0["A8"].font = font_section

headers_t1 = ["STT", "Khối Ngân Sách & Nhóm Chi Phí", "PIC", "Actual 2025", "AOP 2026 Budget", "Quý 1 (Q1)", "Quý 2 (Q2)", "Quý 3 (Q3)", "Quý 4 (Q4)", "% Tăng Trưởng", "Tỷ Trọng (%)"]
ws0.row_dimensions[9].height = 24
for col_idx, h in enumerate(headers_t1, start=1):
    cell = ws0.cell(9, col_idx, h)
    cell.font = font_tbl_header
    cell.fill = fill_dark
    cell.alignment = align_header
    cell.border = border_header

rows_t1 = [
    ("1", "Nhóm 1: Chi phí Event & Vinh danh cộng đồng", "DS", 1429372193, "=01_Master_AOP_Budget!N18", "=01_Master_AOP_Budget!O18", "=01_Master_AOP_Budget!P18", "=01_Master_AOP_Budget!Q18", "=01_Master_AOP_Budget!R18", "=(E10-D10)/D10", "=E10/$E$17"),
    ("2", "Nhóm 2: Chi phí Quản trị, Phúc lợi & Vận hành", "DS", 744300000, "=01_Master_AOP_Budget!N27", "=01_Master_AOP_Budget!O27", "=01_Master_AOP_Budget!P27", "=01_Master_AOP_Budget!Q27", "=01_Master_AOP_Budget!R27", "=(E11-D11)/D11", "=E11/$E$17"),
    ("3", "Nhóm 3: Chi phí Đội ngũ Đội trưởng (Fleet Lead)", "DM", 105270000, "=01_Master_AOP_Budget!N30", "=01_Master_AOP_Budget!O30", "=01_Master_AOP_Budget!P30", "=01_Master_AOP_Budget!Q30", "=01_Master_AOP_Budget!R30", "=(E12-D12)/D12", "=E12/$E$17"),
    ("A", "TỔNG KHỐI A: VẬN HÀNH THƯỜNG NHẬT TEAM DM (CORE OPEX)", "DM/DS", 2278942193, "=01_Master_AOP_Budget!N31", "=01_Master_AOP_Budget!O31", "=01_Master_AOP_Budget!P31", "=01_Master_AOP_Budget!Q31", "=01_Master_AOP_Budget!R31", "=(E13-D13)/D13", "=E13/$E$17"),
    ("4", "Nhóm 4: Dự án Chuyển đổi Xe máy điện (EV Fleet)", "DM", 0, "=01_Master_AOP_Budget!N34", "=01_Master_AOP_Budget!O34", "=01_Master_AOP_Budget!P34", "=01_Master_AOP_Budget!Q34", "=01_Master_AOP_Budget!R34", "Mới 100%", "=E14/$E$17"),
    ("5", "Nhóm 5: Dự án Gopika - Dedicated Station Fleet", "DM", 0, "=01_Master_AOP_Budget!N38", "=01_Master_AOP_Budget!O38", "=01_Master_AOP_Budget!P38", "=01_Master_AOP_Budget!Q38", "=01_Master_AOP_Budget!R38", "Mới 100%", "=E15/$E$17"),
    ("B", "TỔNG KHỐI B: DỰ ÁN CHIẾN LƯỢC CHUYỂN ĐỔI MÔ HÌNH", "DM", 0, "=01_Master_AOP_Budget!N39", "=01_Master_AOP_Budget!O39", "=01_Master_AOP_Budget!P39", "=01_Master_AOP_Budget!Q39", "=01_Master_AOP_Budget!R39", "Mới 100%", "=E16/$E$17"),
    ("★", "TỔNG CỘNG TOÀN BỘ NGÂN SÁCH AOP 2026 (A + B)", "ALL", 2278942193, "=01_Master_AOP_Budget!N40", "=01_Master_AOP_Budget!O40", "=01_Master_AOP_Budget!P40", "=01_Master_AOP_Budget!Q40", "=01_Master_AOP_Budget!R40", "=(E17-D17)/D17", "=E17/$E$17"),
]

for r_offset, r_data in enumerate(rows_t1, start=10):
    ws0.row_dimensions[r_offset].height = 20
    is_subtotal = r_data[0] in ["A", "B"]
    is_grand = r_data[0] == "★"
    
    for c_idx, val in enumerate(r_data, start=1):
        cell = ws0.cell(r_offset, c_idx, val)
        cell.border = border_grand if is_grand else (border_subtotal if is_subtotal else border_all)
        if is_grand:
            cell.font = font_grand
            cell.fill = fill_grand
        elif is_subtotal:
            cell.font = font_subtotal
            cell.fill = fill_subtotal
        else:
            cell.font = font_bold if c_idx == 2 else font_regular
            if r_offset % 2 == 1:
                cell.fill = fill_zebra
                
        if c_idx in [1, 3]:
            cell.alignment = align_center
        elif c_idx == 2:
            cell.alignment = align_left
        elif 4 <= c_idx <= 9:
            cell.alignment = align_right
            cell.number_format = "#,##0"
        elif c_idx == 10:
            cell.alignment = align_center
            if isinstance(val, str) and val.startswith("="):
                cell.number_format = "0.0%"
        elif c_idx == 11:
            cell.alignment = align_right
            cell.number_format = "0.0%"

ws0["A19"] = "II. ĐỐI CHIẾU MÃ TÀI KHOẢN KẾ TOÁN (AOP COST CODE ROLLUP - FA VIEW)"
ws0["A19"].font = font_section

headers_t2 = ["Mã AOP", "Tên Tài Khoản / Hạng Mục Kế Toán", "Actual 2025", "AOP 2026 Budget", "Chênh Lệch (+/-)", "% Tăng Trưởng", "Phân Loại", "Ghi Chú Thuyết Minh Cốt Lõi Của Team"]
ws0.row_dimensions[20].height = 24
for col_idx, h in enumerate(headers_t2, start=1):
    cell = ws0.cell(20, col_idx, h)
    cell.font = font_tbl_header
    cell.fill = fill_dark
    cell.alignment = align_header
    cell.border = border_header

rows_t2 = [
    ("1401_A112_4603", "Bảo hiểm tai nạn tài xế Fulltime", 474600000, "=01_Master_AOP_Budget!N19", "=D21-C21", "=(D21-C21)/C21", "Core Ops", "Tối ưu -37% chi phí bảo hiểm nhờ chuẩn hóa chính sách trang bị theo danh sách thực tế"),
    ("1401_C493_4802", "Chi phí hoạt động Community, Event, Đội trưởng & FL call", 1429372193, "=01_Master_AOP_Budget!N18+01_Master_AOP_Budget!N20+01_Master_AOP_Budget!N24+01_Master_AOP_Budget!N28", "=D22-C22", "=(D22-C22)/C22", "Core Ops", "+23.6% để tăng quy mô vinh danh (500 HAN, 700 SGN), hỗ trợ thiên tai 70M và thuê FL call 280M"),
    ("1401_C494_5607", "Đồng phục xuất bán & Quà tặng tài xế (Trung thu, Tết, Bike)", 269700000, "=01_Master_AOP_Budget!N22+01_Master_AOP_Budget!N23+01_Master_AOP_Budget!N25", "=D23-C23", "=(D23-C23)/C23", "Core Ops", "+137% do tập trung quà tặng cho các chiến dịch lớn, bánh Trung thu 80M, quà Tết 140M, quà Bike 420M"),
    ("1401_C5_5608", "Chi phí SMS / ZNS push active & truyền thông", 0, "=01_Master_AOP_Budget!N21", "=D24-C24", "Mới 100%", "Core Ops", "Chi phí phát sinh mới 2026 phục vụ truyền thông trực tiếp, push active hàng ngày cho mô hình mới"),
    ("TBC", "Chính sách hỗ trợ chuyển đổi xe máy điện (Sạc điện & Chiết khấu)", 0, "=01_Master_AOP_Budget!N34", "=D25-C25", "Mới 100%", "Strategic", "Hỗ trợ phí sạc điện theo km (7.25 tỷ) và chiết khấu 3-5% (2.71 tỷ) đảm bảo active xe điện"),
    ("TBC2", "Dự án Gopika - Dedicated Hub/Station Fleet", 0, "=01_Master_AOP_Budget!N38", "=D26-C26", "Mới 100%", "Strategic", "Chi phí cung ứng xe chuyên trách Hub/Station (14.09 tỷ), chiết khấu 5% (880.5M), phí COD 0.7% (39.4M)"),
    ("TỔNG CỘNG", "Toàn bộ danh mục chi phí phòng ban & dự án", 2173672193, "=SUM(D21:D26)", "=D27-C27", "=(D27-C27)/C27", "Total", "Khớp 100% với số liệu tổng hợp trong Master Budget"),
]

for r_offset, r_data in enumerate(rows_t2, start=21):
    ws0.row_dimensions[r_offset].height = 22
    is_tot = r_data[0] == "TỔNG CỘNG"
    for c_idx, val in enumerate(r_data, start=1):
        cell = ws0.cell(r_offset, c_idx, val)
        cell.border = border_grand if is_tot else border_all
        if is_tot:
            cell.font = font_grand
            cell.fill = fill_grand
        else:
            cell.font = font_bold if c_idx in [1, 2] else font_regular
            if r_offset % 2 == 1:
                cell.fill = fill_zebra
        
        if c_idx == 1:
            cell.alignment = align_center
        elif c_idx in [2, 8]:
            cell.alignment = align_left
        elif c_idx in [3, 4, 5]:
            cell.alignment = align_right
            cell.number_format = "#,##0"
        elif c_idx == 6:
            cell.alignment = align_center
            if isinstance(val, str) and val.startswith("="):
                cell.number_format = "0.0%"
        elif c_idx == 7:
            cell.alignment = align_center

ws0["A29"] = "III. MA TRẬN MỨC ĐỘ ƯU TIÊN & KỊCH BẢN TỐI ƯU NGÂN SÁCH (SCENARIOS FOR BOD REVIEW)"
ws0["A29"].font = font_section

headers_t3 = ["Mức Độ Ưu Tiên", "Ngân Sách Core DM (VNĐ)", "Ngân Sách Toàn Bộ (VNĐ)", "Tỷ Trọng Core", "Tác Động Vận Hành & Khả Năng Cắt Giảm", "Khuyến Nghị Phê Duyệt Của Kiến Trúc Sư"]
ws0.row_dimensions[30].height = 24
for col_idx, h in enumerate(headers_t3, start=1):
    cell = ws0.cell(30, col_idx, h)
    cell.font = font_tbl_header
    cell.fill = fill_dark
    cell.alignment = align_header
    cell.border = border_header

rows_t3 = [
    ("Must have (Bắt buộc)", "=01_Master_AOP_Budget!N31-175000000-40000000", "=01_Master_AOP_Budget!N40-175000000-40000000", "=B31/$B$34", "Chi phí sống còn: Bảo hiểm fulltime, lương đội trưởng, vinh danh nòng cốt, quà tặng đối tác, xe điện & Gopika. Cắt giảm sẽ gây sụt giảm trực tiếp Active Drivers & vỡ SLA.", "BẢO VỆ 100%: Không cắt giảm. Đây là điều kiện tiên quyết để giữ vững mạng lưới cung ứng."),
    ("Should have (Nên có)", 175000000, 175000000, "=B32/$B$34", "Gồm: 8/3 (40M), Gia đình & Thiếu nhi (60M), Lì xì Tết (15M), Tấm lòng cam (60M). Tác động gián tiếp đến gắn kết (CSAT) và tinh thần cộng đồng.", "TỐI ƯU CÓ ĐIỀU KIỆN: Chuyển ngày hội gia đình sang Online (tiết kiệm ~30-40M), gộp lì xì vào incentive."),
    ("Nice to have (Có thể giãn)", 40000000, 40000000, "=B33/$B$34", "Gồm: Quốc tế Đàn ông 19/11 (40M). Hoạt động mang tính chất phong trào nội bộ, không ảnh hưởng đến số cuốc hoàn thành.", "CẮT GIẢM ĐẦU TIÊN: Sẵn sàng cắt bỏ 100% (tiết kiệm 40M) nếu BOD yêu cầu siết trần ngân sách."),
    ("TỔNG CỘNG", "=SUM(B31:B33)", "=SUM(C31:C33)", "=SUM(D31:D33)", "Cấu trúc ngân sách Core lành mạnh với 92.6% là chi phí nòng cốt tạo năng lực cạnh tranh.", "Tổng biên độ có thể tối ưu linh hoạt: 40M - 100M VND mà không gây rủi ro vận hành.")
]

for r_offset, r_data in enumerate(rows_t3, start=31):
    ws0.row_dimensions[r_offset].height = 26
    is_tot = r_data[0] == "TỔNG CỘNG"
    for c_idx, val in enumerate(r_data, start=1):
        cell = ws0.cell(r_offset, c_idx, val)
        cell.border = border_grand if is_tot else border_all
        if is_tot:
            cell.font = font_grand
            cell.fill = fill_grand
        else:
            cell.font = font_bold if c_idx == 1 else font_regular
            if r_offset % 2 == 1:
                cell.fill = fill_zebra
        
        if c_idx == 1:
            cell.alignment = align_center
        elif c_idx in [2, 3]:
            cell.alignment = align_right
            cell.number_format = "#,##0"
        elif c_idx == 4:
            cell.alignment = align_center
            cell.number_format = "0.0%"
        else:
            cell.alignment = align_left

col_widths_0 = {
    "A": 8, "B": 38, "C": 10, "D": 16, "E": 18, "F": 15, "G": 15, "H": 15, "I": 15, "J": 14, "K": 14
}
for col_l, w in col_widths_0.items():
    ws0.column_dimensions[col_l].width = w

# ==============================================================================
# SHEET 2: 02_Phan_Bo_Chi_Phi (Allocation Engine)
# ==============================================================================
ws2 = wb.create_sheet(title="02_Phan_Bo_Chi_Phi")
ws2.views.sheetView[0].showGridLines = True

ws2.merge_cells("A1:K1")
ws2["A1"] = "AHAMOVE - MA TRẬN PHÂN BỔ CHI PHÍ (ALLOCATION ENGINE: CITY, FLEET & UNIT ECONOMICS)"
ws2["A1"].font = font_title
ws2["A1"].fill = fill_primary
ws2["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
ws2.row_dimensions[1].height = 30

ws2.merge_cells("A2:K2")
ws2["A2"] = "Phân bổ minh bạch theo Khu vực (SGN, HAN, EXP) và Dòng xe (Bike, Truck, EV, Station) | Tối ưu kiểm soát Budget"
ws2["A2"].font = font_subtitle
ws2["A2"].fill = fill_dark
ws2["A2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
ws2.row_dimensions[2].height = 18

ws2["A4"] = "I. MA TRẬN PHÂN BỔ THEO THỊ TRƯỜNG & KHU VỰC (REGIONAL ALLOCATION)"
ws2["A4"].font = font_section

headers_alloc_city = ["STT", "Hạng Mục Chi Phí Cốt Lõi", "Mã AOP", "Tổng Ngân Sách", "TP. Hồ Chí Minh (SGN)", "Hà Nội (HAN)", "Thị Trường Tỉnh (EXP)", "Tỷ Lệ SGN (%)", "Tỷ Lệ HAN (%)", "Tỷ Lệ EXP (%)", "Cơ Sở / Logic Phân Bổ"]
ws2.row_dimensions[5].height = 24
for col_idx, h in enumerate(headers_alloc_city, start=1):
    cell = ws2.cell(5, col_idx, h)
    cell.font = font_tbl_header
    cell.fill = fill_dark
    cell.alignment = align_header
    cell.border = border_header

city_alloc_rows = [
    ("1", "Vinh danh Quý (Offline)", "1401_C493_4802", "=01_Master_AOP_Budget!N4", "=D6*H6", "=D6*I6", "=D6*J6", 0.583, 0.417, 0.000, "Tỷ lệ quy mô tài xế vinh danh: 700 SGN vs 500 HAN (58.3% : 41.7%)"),
    ("2", "Minigame online & Contest", "1401_C493_4802", "=01_Master_AOP_Budget!N5", "=D7*H7", "=D7*I7", "=D7*J7", 0.500, 0.400, 0.100, "Tỷ trọng tài xế tham gia cộng đồng trên app & Zalo"),
    ("3", "Livestream tổng kết năm", "1401_C493_4802", "=01_Master_AOP_Budget!N6", "=D8*H8", "=D8*I8", "=D8*J8", 0.550, 0.350, 0.100, "Quy mô Active Drivers theo thị trường toàn quốc"),
    ("4", "Sự kiện ngày lễ (8/3, Trung thu, 20/10)", "1401_C493_4802", "=01_Master_AOP_Budget!N7+01_Master_AOP_Budget!N10+01_Master_AOP_Budget!N11", "=D9*H9", "=D9*I9", "=D9*J9", 0.500, 0.500, 0.000, "Chia đều ngân sách 50-50 cho 2 miền trọng điểm"),
    ("5", "AhaCup (Giải bóng đá tài xế)", "1401_C493_4802", "=01_Master_AOP_Budget!N13", "=D10*H10", "=D10*I10", "=D10*J10", 0.500, 0.500, 0.000, "Mỗi miền 60M (SGN 60M, HAN 60M) theo kế hoạch giải"),
    ("6", "Hỗ trợ thiên tai bão lũ", "1401_C493_4802", "=01_Master_AOP_Budget!N15", "=D11*H11", "=D11*I11", "=D11*J11", 0.000, 0.571, 0.429, "HAN 40M (57%), các tỉnh Expansion miền Trung/Bắc 30M (43%)"),
    ("7", "Bảo hiểm tài xế Fulltime", "1401_A112_4603", "=01_Master_AOP_Budget!N19", "=D12*H12", "=D12*I12", "=D12*J12", 0.520, 0.480, 0.000, "Dựa theo số lượng tài xế Fulltime đăng ký tại từng Hub"),
    ("8", "Thuê nhân sự ngoài (FL call)", "1401_C493_4802", "=01_Master_AOP_Budget!N20", "=D13*H13", "=D13*I13", "=D13*J13", 0.500, 0.500, 0.000, "Phân bổ 50-50 để call push active 2 đầu cầu"),
    ("9", "Quà tặng tài xế (Bánh TT, Tết, Bike)", "1401_C494_5607", "=01_Master_AOP_Budget!N22+01_Master_AOP_Budget!N23+01_Master_AOP_Budget!N25", "=D14*H14", "=D14*I14", "=D14*J14", 0.550, 0.350, 0.100, "55% SGN, 35% HAN, 10% các tỉnh mở rộng"),
    ("10", "Lương đội trưởng (04 Đội trưởng)", "1401_C493_4802", "=01_Master_AOP_Budget!N28", "=D15*H15", "=D15*I15", "=D15*J15", 0.500, 0.500, 0.000, "2 Đội trưởng SGN (50%) & 2 Đội trưởng HAN (50%)"),
    ("11", "Chuyển đổi xe máy điện (Sạc & Chiết khấu)", "TBC", "=01_Master_AOP_Budget!N34", "=D16*H16", "=D16*I16", "=D16*J16", 0.200, 0.800, 0.000, "Thử nghiệm tập trung tại HAN (80%), sau mở rộng SGN (20%)"),
    ("12", "Dự án Gopika Dedicated Station", "TBC2", "=01_Master_AOP_Budget!N38", "=D17*H17", "=D17*I17", "=D17*J17", 0.000, 1.000, 0.000, "100% triển khai tại các Hub/Station khu vực Hà Nội"),
    ("★", "TỔNG PHÂN BỔ THEO KHU VỰC", "ALL", "=SUM(D6:D17)", "=SUM(E6:E17)", "=SUM(F6:F17)", "=SUM(G6:G17)", "=E18/$D$18", "=F18/$D$18", "=G18/$D$18", "Tự động rollup từ các công thức phân bổ")
]

for r_offset, r_data in enumerate(city_alloc_rows, start=6):
    ws2.row_dimensions[r_offset].height = 20
    is_tot = r_data[0] == "★"
    for c_idx, val in enumerate(r_data, start=1):
        cell = ws2.cell(r_offset, c_idx, val)
        cell.border = border_grand if is_tot else border_all
        if is_tot:
            cell.font = font_grand
            cell.fill = fill_grand
        else:
            cell.font = font_bold if c_idx in [1, 2] else font_regular
            if r_offset % 2 == 1:
                cell.fill = fill_zebra
                
        if c_idx in [1, 3]:
            cell.alignment = align_center
        elif c_idx in [2, 11]:
            cell.alignment = align_left
        elif 4 <= c_idx <= 7:
            cell.alignment = align_right
            cell.number_format = "#,##0"
        elif 8 <= c_idx <= 10:
            cell.alignment = align_center
            cell.number_format = "0.0%"

ws2["A20"] = "II. MA TRẬN PHÂN BỔ THEO DÒNG PHƯƠNG TIỆN & MÔ HÌNH FLEET"
ws2["A20"].font = font_section

headers_alloc_fleet = ["Mô Hình Phương Tiện", "Phạm Vi Áp Dụng", "Ngân Sách Phân Bổ (VNĐ)", "Tỷ Trọng (%)", "Đối Tượng Hưởng Lợi", "Đơn Vị Kinh Tế Mục Tiêu (Unit Economics)"]
ws2.row_dimensions[21].height = 24
for col_idx, h in enumerate(headers_alloc_fleet, start=1):
    cell = ws2.cell(21, col_idx, h)
    cell.font = font_tbl_header
    cell.fill = fill_dark
    cell.alignment = align_header
    cell.border = border_header

fleet_alloc_rows = [
    ("Xe 2 bánh truyền thống (Bike - Xăng)", "NW (SGN, HAN, EXP)", 2628540907, "=C22/$C$26", "Tài xế giao hàng xe máy nòng cốt", "Ước tính ~45,000 đ/Active Driver/năm"),
    ("Xe tải & Bán tải (4-Wheel / Truck)", "NW (SGN, HAN)", 0, "=C23/$C$26", "Đội ngũ tài xế xe tải (Dự phòng mở rộng)", "Khai thác tối đa nguồn lực trang thiết bị"),
    ("Đội xe máy điện (EV Fleet)", "HAN & SGN", 9962048533, "=C24/$C$26", "Tài xế chuyển đổi mô hình xanh", "Bù đắp chi phí sạc & chiết khấu thu nhập"),
    ("Đội xe chuyên trách Trạm (Gopika Station)", "HAN Station / Hubs", 14969154831, "=C25/$C$26", "Tài xế cam kết đơn hàng Hub/Station", "Đảm bảo SLA & Fulfillment rate > 98%"),
    ("TỔNG CỘNG", "Toàn mạng lưới", "=SUM(C22:C25)", "=SUM(D22:D25)", "Toàn bộ tài xế Ahamove", "Tối ưu hóa tổng thể chi phí trên từng đơn hàng")
]

for r_offset, r_data in enumerate(fleet_alloc_rows, start=22):
    ws2.row_dimensions[r_offset].height = 22
    is_tot = r_data[0] == "TỔNG CỘNG"
    for c_idx, val in enumerate(r_data, start=1):
        cell = ws2.cell(r_offset, c_idx, val)
        cell.border = border_grand if is_tot else border_all
        if is_tot:
            cell.font = font_grand
            cell.fill = fill_grand
        else:
            cell.font = font_bold if c_idx == 1 else font_regular
            if r_offset % 2 == 1:
                cell.fill = fill_zebra
                
        if c_idx in [1, 2]:
            cell.alignment = align_left
        elif c_idx == 3:
            cell.alignment = align_right
            cell.number_format = "#,##0"
        elif c_idx == 4:
            cell.alignment = align_center
            cell.number_format = "0.0%"
        else:
            cell.alignment = align_left

col_widths_2 = {
    "A": 8, "B": 36, "C": 14, "D": 18, "E": 18, "F": 18, "G": 18, "H": 13, "I": 13, "J": 13, "K": 38
}
for col_l, w in col_widths_2.items():
    ws2.column_dimensions[col_l].width = w

# ==============================================================================
# SHEET 3: 03_Theo_Doi_Thuc_Chi (Monthly Budget Tracker)
# ==============================================================================
ws3 = wb.create_sheet(title="03_Theo_Doi_Thuc_Chi")
ws3.views.sheetView[0].showGridLines = True

ws3.merge_cells("A1:K1")
ws3["A1"] = "AHAMOVE - BẢNG THEO DÕI THỰC CHI NGÂN SÁCH HÀNG THÁNG (BUDGET VS ACTUAL TRACKER)"
ws3["A1"].font = font_title
ws3["A1"].fill = fill_primary
ws3["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
ws3.row_dimensions[1].height = 30

ws3.merge_cells("A2:K2")
ws3["A2"] = "Công cụ kiểm soát tiến độ giải ngân (Burn Rate) & Cảnh báo vượt ngân sách | Đối chiếu hàng tháng với Finance/FA"
ws3["A2"].font = font_subtitle
ws3["A2"].fill = fill_dark
ws3["A2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
ws3.row_dimensions[2].height = 18

tracker_headers = [
    "Mã ID", "Hạng Mục Chi Phí", "Mã AOP", "PIC", "Ngân Sách Được Duyệt (Planned)", 
    "Thực Chi Lũy Kế (Actual YTD)", "Cam Kết Chưa Claim (Committed PO)", "Ngân Sách Còn Lại (Remaining)", 
    "Tỷ Lệ Giải Ngân (% Burn Rate)", "Trạng Thái Kiểm Soát (Status)", "Phương Án Bù Trừ / Hành Động"
]

ws3.row_dimensions[4].height = 24
for col_idx, h in enumerate(tracker_headers, start=1):
    cell = ws3.cell(4, col_idx, h)
    cell.font = font_tbl_header
    cell.fill = fill_dark
    cell.alignment = align_header
    cell.border = border_header

tracker_items = [
    ("DM-EVT-01", "Vinh danh (Offline) mỗi quý", "1401_C493_4802", "DS", "=01_Master_AOP_Budget!N4", 120000000, 0),
    ("DM-EVT-02", "Minigame online / Mini Contest", "1401_C493_4802", "DS", "=01_Master_AOP_Budget!N5", 20000000, 5000000),
    ("DM-EVT-03", "Livestream tổng kết năm", "1401_C493_4802", "DS", "=01_Master_AOP_Budget!N6", 98500000, 0),
    ("DM-EVT-04", "Quốc Tế Phụ Nữ (08/03)", "1401_C493_4802", "DS", "=01_Master_AOP_Budget!N7", 38200000, 0),
    ("DM-EVT-05", "Ngày hội gia đình (28/6)", "1401_C493_4802", "DS", "=01_Master_AOP_Budget!N8", 0, 0),
    ("DM-EVT-06", "Campaign sinh nhật Ahamove", "1401_C493_4802", "DS", "=01_Master_AOP_Budget!N9", 0, 0),
    ("DM-EVT-07", "Sự kiện Trung thu", "1401_C493_4802", "DS", "=01_Master_AOP_Budget!N10", 0, 0),
    ("DM-EVT-08", "Chương trình 20/10", "1401_C493_4802", "DS", "=01_Master_AOP_Budget!N11", 0, 0),
    ("DM-EVT-09", "Quốc tế Đàn ông (19/11)", "1401_C493_4802", "DS", "=01_Master_AOP_Budget!N12", 0, 0),
    ("DM-EVT-10", "AhaCup (Giải bóng đá tài xế)", "1401_C493_4802", "DS", "=01_Master_AOP_Budget!N13", 0, 0),
    ("DM-EVT-11", "Giáng Sinh - Tết Dương Lịch", "1401_C493_4802", "DS", "=01_Master_AOP_Budget!N14", 0, 0),
    ("DM-EVT-12", "Tiếp sức hỗ trợ thiên tai bão lũ", "1401_C493_4802", "DS", "=01_Master_AOP_Budget!N15", 0, 0),
    ("DM-EVT-13", "Lì xì kéo active sau Tết", "1401_C493_4802", "DS", "=01_Master_AOP_Budget!N16", 14800000, 0),
    ("DM-OPS-01", "Bảo hiểm tài xế Fulltime", "1401_A112_4603", "DS", "=01_Master_AOP_Budget!N19", 71308792, 0),
    ("DM-OPS-02", "Chi phí thuê nhân sự FL call", "1401_C493_4802", "DS", "=01_Master_AOP_Budget!N20", 70000000, 10000000),
    ("DM-OPS-03", "Chi phí SMS / ZNS push active", "1401_C5_5608", "DS", "=01_Master_AOP_Budget!N21", 55000000, 0),
    ("DM-OPS-04", "Sản xuất bánh Trung thu", "1401_C494_5607", "DS", "=01_Master_AOP_Budget!N22", 0, 0),
    ("DM-OPS-05", "Sản xuất quà Tết", "1401_C494_5607", "DS", "=01_Master_AOP_Budget!N23", 0, 0),
    ("DM-OPS-06", "Quỹ Hỗ trợ Tấm Lòng Cam", "1401_C493_4802", "DS", "=01_Master_AOP_Budget!N24", 15000000, 0),
    ("DM-OPS-07", "Quà tặng Tài xế (Bike)", "1401_C494_5607", "DS", "=01_Master_AOP_Budget!N25", 120000000, 0),
    ("DM-CAP-01", "Lương cơ bản Đội trưởng", "1401_C493_4802", "DM", "=01_Master_AOP_Budget!N28", 66000000, 0),
    ("DM-STR-01", "Hỗ trợ sạc xe máy điện", "TBC", "DM", "=01_Master_AOP_Budget!N32", 1078994850, 0),
    ("DM-STR-02", "Chiết khấu xe máy điện 3%", "TBC", "DM", "=01_Master_AOP_Budget!N33", 419736245, 0),
    ("DM-STR-03", "Gopika Station Supply cost", "TBC2", "DM", "=01_Master_AOP_Budget!N35", 1855875288, 0),
    ("DM-STR-04", "Gopika Station Chiết khấu 5%", "TBC2", "DM", "=01_Master_AOP_Budget!N36", 115992206, 0),
    ("DM-STR-05", "Gopika Hỗ trợ phí COD 0.7%", "TBC2", "DM", "=01_Master_AOP_Budget!N37", 5196451, 0),
    ("TỔNG CỘNG", "Toàn bộ danh mục AOP 2026", "ALL", "ALL", "=SUM(E5:E30)", "=SUM(F5:F30)", "=SUM(G5:G30)", "=E31-F31-G31", "=(F31+G31)/E31", '="🟢 An Toàn"', '="Duy trì kiểm soát giải ngân định kỳ hàng tháng"')
]

for r_offset, r_data in enumerate(tracker_items, start=5):
    ws3.row_dimensions[r_offset].height = 20
    is_tot = r_data[0] == "TỔNG CỘNG"
    
    ws3.cell(r_offset, 1, r_data[0]).alignment = align_center
    ws3.cell(r_offset, 2, r_data[1]).alignment = align_left
    ws3.cell(r_offset, 3, r_data[2]).alignment = align_center
    ws3.cell(r_offset, 4, r_data[3]).alignment = align_center
    
    ws3.cell(r_offset, 5, r_data[4]).number_format = "#,##0"
    ws3.cell(r_offset, 6, r_data[5]).number_format = "#,##0"
    ws3.cell(r_offset, 7, r_data[6]).number_format = "#,##0"
    
    if is_tot:
        ws3.cell(r_offset, 8, f"=E{r_offset}-F{r_offset}-G{r_offset}").number_format = "#,##0"
        ws3.cell(r_offset, 9, f"=(F{r_offset}+G{r_offset})/E{r_offset}").number_format = "0.0%"
        ws3.cell(r_offset, 10, "🟢 An Toàn").alignment = align_center
        ws3.cell(r_offset, 11, "Tổng giải ngân toàn mạng lưới trong tầm kiểm soát").alignment = align_left
    else:
        ws3.cell(r_offset, 8, f"=E{r_offset}-F{r_offset}-G{r_offset}").number_format = "#,##0"
        ws3.cell(r_offset, 9, f"=IF(E{r_offset}>0, (F{r_offset}+G{r_offset})/E{r_offset}, 0)").number_format = "0.0%"
        ws3.cell(r_offset, 10, f'=IF(I{r_offset}>1, "🔴 Vượt Ngân Sách", IF(I{r_offset}>0.9, "🟡 Sắp Chạm Trần", "🟢 Bình Thường"))').alignment = align_center
        ws3.cell(r_offset, 11, '="Theo dõi sát hóa đơn chứng từ tháng này"').alignment = align_left
        
    for c in range(1, 12):
        cell = ws3.cell(r_offset, c)
        cell.border = border_grand if is_tot else border_all
        if is_tot:
            cell.font = font_grand
            cell.fill = fill_grand
        else:
            cell.font = font_bold if c in [1, 2] else font_regular
            if r_offset % 2 == 1:
                cell.fill = fill_zebra
        if 5 <= c <= 8:
            cell.alignment = align_right
        elif c == 9:
            cell.alignment = align_center

col_widths_3 = {
    "A": 12, "B": 34, "C": 15, "D": 8, "E": 18, "F": 18, "G": 18, "H": 18, "I": 15, "J": 18, "K": 35
}
for col_l, w in col_widths_3.items():
    ws3.column_dimensions[col_l].width = w

# ==============================================================================
# SHEET 4: 04_Tu_Dien_Ma_AOP (Cost Code Dictionary)
# ==============================================================================
ws4 = wb.create_sheet(title="04_Tu_Dien_Ma_AOP")
ws4.views.sheetView[0].showGridLines = True

ws4.merge_cells("A1:G1")
ws4["A1"] = "AHAMOVE - TỪ ĐIỂN MÃ TÀI KHOẢN KẾ TOÁN AOP (AOP COST CODE DICTIONARY & COMPLIANCE)"
ws4["A1"].font = font_title
ws4["A1"].fill = fill_primary
ws4["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
ws4.row_dimensions[1].height = 30

ws4.merge_cells("A2:G2")
ws4["A2"] = "Hướng dẫn chuẩn hóa hồ sơ chứng từ, phạm vi chi tiêu hợp lệ & ma trận phê duyệt | Phòng chống rủi ro Fraud"
ws4["A2"].font = font_subtitle
ws4["A2"].fill = fill_dark
ws4["A2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
ws4.row_dimensions[2].height = 18

dict_headers = [
    "Mã AOP", "Tên Mã Kế Toán / Diễn Giải", "Tài Khoản Hạch Toán", "Phạm Vi Chi Tiêu HỢP LỆ (Allowed)", 
    "Chi Tiêu KHÔNG HỢP LỆ (Disallowed)", "Hồ Sơ Chứng Từ Bắt Buộc", "Cấp Phê Duyệt"
]

ws4.row_dimensions[4].height = 24
for col_idx, h in enumerate(dict_headers, start=1):
    cell = ws4.cell(4, col_idx, h)
    cell.font = font_tbl_header
    cell.fill = fill_dark
    cell.alignment = align_header
    cell.border = border_header

dict_rows = [
    ("1401_A112_4603", "Bảo hiểm tai nạn tài xế", "Chi phí phúc lợi tài xế", 
     "Mua bảo hiểm tai nạn (BHTN), hoàn tiền/cashback bảo hiểm cho tài xế Fulltime và tài xế chuyên trách có ký cam kết.", 
     "Không chi cho tài xế part-time chưa đạt chuẩn năng suất, không chi bảo hiểm xe cơ giới cá nhân của tài xế.", 
     "1. Hợp đồng bảo hiểm với công ty bảo hiểm\n2. Hóa đơn GTGT (VAT)\n3. Danh sách tài xế thụ hưởng kèm mã ID\n4. Bảng tính đối chiếu số lượng thực tế", 
     "Head of Ops & Finance Manager"),

    ("1401_C493_4802", "Chi phí hoạt động Community, Event & Đội trưởng", "Chi phí tiếp thị & chăm sóc đối tác", 
     "Chi phí tổ chức sự kiện offline (vinh danh, AhaCup, sinh nhật), minigame, quỹ Tấm lòng cam, thuê nhân sự ngoài FL call, phụ cấp đội trưởng.", 
     "Không chi ăn uống cá nhân ngoài phạm vi teabreak sự kiện, không chi thưởng tiền mặt không có danh sách ký nhận.", 
     "1. Kế hoạch / Tờ trình sự kiện được duyệt\n2. Hợp đồng thuê địa điểm / âm thanh / teabreak\n3. Hóa đơn VAT hợp lệ\n4. Danh sách tài xế check-in / ký nhận quà\n5. Hình ảnh nghiệm thu thực tế", 
     "Head of Ops & BOD"),

    ("1401_C494_5607", "Đồng phục & Quà tặng tài xế", "Chi phí vật phẩm & quà tặng đối tác", 
     "Mua bánh Trung thu, quà Tết cho tài xế VIP, xuất kho áo thun, nón bảo hiểm, áo khoác tặng tài xế, trang thiết bị xe tải.", 
     "Không xuất quà tặng không rõ mục đích, không mua quà tặng cho nhân viên văn phòng từ mã này.", 
     "1. Phiếu xuất kho quà tặng / đồng phục\n2. Hóa đơn GTGT từ nhà cung cấp\n3. Danh sách tài xế nhận quà kèm chữ ký / OTP nhận hàng\n4. Báo cáo nghiệm thu trao quà", 
     "Head of Ops & Supply Lead"),

    ("1401_C5_5608", "Chi phí SMS & ZNS Push Active", "Chi phí viễn thông & công nghệ vận hành", 
     "Chi phí gửi tin nhắn SMS Brandname, Zalo ZNS thông báo cuốc xe, cảnh báo vận hành, push active hàng ngày cho tài xế.", 
     "Không dùng cho các chiến dịch quảng cáo marketing tìm khách hàng (phải do MKT chi trả).", 
     "1. Hợp đồng dịch vụ SMS/Zalo\n2. Đối chiếu CDR (Call Detail Record) / Log tin nhắn thành công\n3. Hóa đơn VAT nhà mạng\n4. Nghiệm thu kỹ thuật", 
     "Head of Ops & Tech Lead"),

    ("TBC", "Chính sách hỗ trợ Chuyển đổi Xe máy điện", "Chi phí chiến lược phát triển xe điện", 
     "Chi phí hỗ trợ sạc điện theo km thực tế, hỗ trợ giảm chiết khấu 3-5% cho tài xế chuyển sang dùng xe máy điện.", 
     "Không chi cho xe xăng, không chi khống km không có dữ liệu GPS định vị trên app Ahamove.", 
     "1. Chính sách hỗ trợ xe điện được BOD ký duyệt\n2. Log dữ liệu cuốc xe & km chạy bằng xe điện trên hệ thống\n3. Bảng tính đối soát sạc điện / chiết khấu hàng tuần\n4. Lệnh thanh toán ví tài xế", 
     "Chief Executive Officer & Head of Ops"),

    ("TBC2", "Dự án Gopika Dedicated Station Fleet", "Chi phí vận hành trạm chuyên trách Hub", 
     "Supply cost trả cho đội xe chuyên trách trạm, chiết khấu 5% đơn hàng Station, hỗ trợ 0.7% phí nộp COD tiền mặt.", 
     "Không chi cho tài xế tự do ngoài mô hình trạm, không chi ngoài các trạm/hub trong danh mục dự án Gopika.", 
     "1. Hợp đồng hợp tác mô hình trạm Gopika\n2. Bảng kê đối soát cuốc xe hoàn thành tại từng Station\n3. Bảng đối soát phí nộp tiền mặt với ngân hàng\n4. Biên bản nghiệm thu SLA hàng tháng", 
     "Head of Station Ops & Finance Director")
]

for r_offset, r_data in enumerate(dict_rows, start=5):
    ws4.row_dimensions[r_offset].height = 54
    for c_idx, val in enumerate(r_data, start=1):
        cell = ws4.cell(r_offset, c_idx, val)
        cell.border = border_all
        cell.font = font_bold if c_idx in [1, 2] else font_regular
        if r_offset % 2 == 1:
            cell.fill = fill_zebra
        
        if c_idx in [1, 3, 7]:
            cell.alignment = align_center
        else:
            cell.alignment = align_left

col_widths_4 = {
    "A": 16, "B": 28, "C": 22, "D": 38, "E": 34, "F": 38, "G": 24
}
for col_l, w in col_widths_4.items():
    ws4.column_dimensions[col_l].width = w

# -------------------------------------------------------------
# SAVE WORKBOOK
# -------------------------------------------------------------
out_dir_1 = "/Users/ts-1148/Desktop/Pulu-workspace/Output/Ahamove/01. STRATEGY_PLANNING"
os.makedirs(out_dir_1, exist_ok=True)
out_file_1 = os.path.join(out_dir_1, "AOP_2026_DM_Standardized_Template.xlsx")
wb.save(out_file_1)

out_file_2 = "/Users/ts-1148/Desktop/Pulu-workspace/data/sources/AOP_2026_DM_Template_ChuanHoa.xlsx"
wb.save(out_file_2)

print(f"Saved successfully to:\n1. {out_file_1}\n2. {out_file_2}")
