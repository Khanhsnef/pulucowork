import csv
from collections import defaultdict
from openpyxl import Workbook
from openpyxl.styles import (Font, PatternFill, Alignment, Border, Side,
                              GradientFill)
from openpyxl.utils import get_column_letter
from openpyxl.styles.numbers import FORMAT_PERCENTAGE_00
from openpyxl.formatting.rule import ColorScaleRule, DataBarRule

INPUT = '/Users/ts-1148/Desktop/Pulu-workspace/metabase_driver_monthly_full.csv'
OUTPUT = '/Users/ts-1148/Desktop/Pulu-workspace/output/Ahamove/05. ANALYSIS_REPORTS/2026-09-retained-driver-yoy.xlsx'

# ── Colors ──────────────────────────────────────────────────────────────────
BLUE_DARK  = '0E4174'
ORANGE     = 'FF7F32'
WHITE      = 'FFFFFF'
LIGHT_BG   = 'F0F4FA'
LIGHT_BG2  = 'EDF2FA'
BORDER_CLR = 'D6E2F0'
BLUE_SOFT  = 'DDEAF8'
ORANGE_SOFT= 'FFF0E6'
GREEN      = '10B981'
RED        = 'EF4444'
YELLOW_BG  = 'FFFDE7'
BLACK      = '000000'
BLUE_FORMULA = '002060'  # Excel std blue for hardcodes (dark blue, readable)
GREEN_LINK    = '008000'
GRAY_MUTED  = '7A94B0'

# ── Styles helpers ───────────────────────────────────────────────────────────
def font(name='Arial', size=10, bold=False, color=BLACK, italic=False):
    return Font(name=name, size=size, bold=bold, color=color, italic=italic)

def fill(hex_color):
    return PatternFill('solid', start_color=hex_color, fgColor=hex_color)

def align(h='left', v='center', wrap=False):
    return Alignment(horizontal=h, vertical=v, wrap_text=wrap)

def thin_border(top=False, bottom=False, left=False, right=False):
    t = Side(style='thin', color=BORDER_CLR) if top    else Side(style=None)
    b = Side(style='thin', color=BORDER_CLR) if bottom else Side(style=None)
    l = Side(style='thin', color=BORDER_CLR) if left   else Side(style=None)
    r = Side(style='thin', color=BORDER_CLR) if right  else Side(style=None)
    return Border(top=t, bottom=b, left=l, right=r)

def thick_bottom():
    return Border(bottom=Side(style='medium', color=BLUE_DARK))

def set_cell(ws, row, col, value, fnt=None, fll=None, aln=None, fmt=None, brd=None):
    c = ws.cell(row=row, column=col, value=value)
    if fnt: c.font = fnt
    if fll: c.fill = fll
    if aln: c.alignment = aln
    if fmt: c.number_format = fmt
    if brd: c.border = brd
    return c

# ── Load & aggregate data ────────────────────────────────────────────────────
with open(INPUT) as f:
    rows = list(csv.DictReader(f))

def sf(v):
    try: return float(v) if v else 0
    except: return 0

monthly = defaultdict(lambda: {
    'drivers': set(), 'online_hours': 0, 'stp': 0,
    'total_income': 0, 'order_income': 0, 'reward_income': 0,
    'rating_sum': 0, 'rating_cnt': 0
})

for r in rows:
    key = (r['year'], int(r['month_num']))
    d = monthly[key]
    d['drivers'].add(r['supplier_id'])
    d['online_hours'] += sf(r['online_hours'])
    d['stp'] += sf(r['stp_complete'])
    d['total_income'] += sf(r['total_income'])
    d['order_income'] += sf(r['order_income'])
    d['reward_income'] += sf(r['reward_income'])
    rv = sf(r['avg_rating'])
    if rv > 0:
        d['rating_sum'] += rv
        d['rating_cnt'] += 1

MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

# Build lookup: (year, month_num) -> metrics dict
def get_metrics(yr, mn):
    d = monthly.get((str(yr), mn), None)
    if not d: return None
    n = len(d['drivers'])
    oh = d['online_hours']
    return {
        'driver_count':   n,
        'total_oh':       oh,
        'total_stp':      d['stp'],
        'total_income':   d['total_income'],
        'order_income':   d['order_income'],
        'reward_income':  d['reward_income'],
        'avg_oh':         oh / n if n else 0,
        'avg_income':     d['total_income'] / n if n else 0,
        'avg_stp':        d['stp'] / n if n else 0,
        'eph':            d['total_income'] / oh if oh else 0,
        'pph':            d['stp'] / oh if oh else 0,
        'reward_pct':     d['reward_income'] / d['total_income'] if d['total_income'] else 0,
        'avg_rating':     d['rating_sum'] / d['rating_cnt'] if d['rating_cnt'] else 0,
    }

wb = Workbook()

# ═══════════════════════════════════════════════════════════════════════════
# SHEET 1: SUMMARY DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════
ws1 = wb.active
ws1.title = '📊 Summary'
ws1.sheet_view.showGridLines = False

# Set column widths
col_widths = {1:28, 2:18, 3:18, 4:16, 5:16, 6:16, 7:16, 8:16}
for c, w in col_widths.items():
    ws1.column_dimensions[get_column_letter(c)].width = w

ws1.row_dimensions[1].height = 8   # top padding
ws1.row_dimensions[2].height = 36  # title

# ── Title block ─────────────────────────────────────────────────────────────
ws1.merge_cells('A2:H2')
set_cell(ws1, 2, 1,
         'Phân Tích YoY — Retained Driver SGN 2025 vs 2026',
         font('Arial', 16, bold=True, color=WHITE),
         fill(BLUE_DARK),
         align('center', 'center'))

ws1.merge_cells('A3:H3')
set_cell(ws1, 3, 1,
         'Cohort: Tài xế active cả 2025 lẫn 2026 | SGN | MOTORBIKE + EV-BIKE | Jan 2025 – Aug 2026',
         font('Arial', 9, color=BLUE_SOFT),
         fill(BLUE_DARK),
         align('center', 'center'))

ws1.row_dimensions[4].height = 10

# ── Jan-Aug aggregate assumption block ──────────────────────────────────────
# Calculate Jan-Aug aggregates (formula cells will reference raw_data sheet)
# Here we store hardcoded values and color them blue per convention

set_cell(ws1, 5, 1, 'Giả Định Phân Tích (Jan–Aug, bỏ Sep 2026 partial)',
         font('Arial', 10, bold=True, color=BLUE_DARK), fill(LIGHT_BG),
         align('left', 'center'))
ws1.merge_cells('A5:H5')

# KPI Header row
kpi_headers = ['KPI', '2025\n(Jan–Aug)', '2026\n(Jan–Aug)', 'Thay đổi (Δ)', 'Δ %', 'Nhận định']
kpi_cols = [1, 2, 3, 4, 5, 6]
ws1.row_dimensions[6].height = 30
for col, hdr in zip(kpi_cols, kpi_headers):
    set_cell(ws1, 6, col, hdr,
             font('Arial', 9, bold=True, color=WHITE),
             fill(BLUE_DARK),
             align('center', 'center', wrap=True),
             brd=thick_bottom())
ws1.merge_cells('F6:H6')

# KPI Data — reference '📈 Raw Data'!columns via formula
# Jan-Aug 2025: sum months 1-8
# Columns in raw_data: A=Year, B=Month, C=Name, D=Drivers, E=TotalOH, F=TotalSTP,
#                      G=TotalIncome, H=OrderIncome, I=RewardIncome,
#                      J=AvgOH, K=AvgIncome, L=AvgSTP, M=EPH, N=PPH, O=RewardPct, P=AvgRating
# Raw data rows: 2025 = rows 3-14, 2026 = rows 15-26 (months 1-12)
# Jan-Aug 2025 = rows 3-10, Jan-Aug 2026 = rows 15-22

kpi_rows = [
    # (label, col_letter_2025, col_letter_2026, fmt, unit, insight)
    ('EPH — Thu nhập/giờ (VND)',        'M', 'Jan–Aug avg',  '#,##0',   'VND/giờ', '↑ Tài xế earn hiệu quả hơn'),
    ('PPH — Stops/giờ',                 'N', 'Jan–Aug avg',  '0.00',    'STP/hr',  '↑ Năng suất giao hàng tăng'),
    ('Giờ làm TB/tài xế/tháng',         'J', 'driver-month', '#,##0.0', 'giờ',     '↓ Effort giảm → driver hài lòng'),
    ('Thu nhập TB/tài xế/tháng (VND)',  'K', 'driver-month', '#,##0',   'VND',     '→ Ổn định, không giảm'),
    ('Total supply hours (fleet)',       'E', 'sum',          '#,##0',   'giờ',     '↑ Fleet lớn hơn bù offset'),
    ('Số tài xế unique (Jan–Aug pool)', 'D', 'max',          '#,##0',   'tài xế',  '+40% driver retained tham gia'),
]

# We'll use SUMPRODUCT / AVERAGEIF on raw data sheet for correctness
# Raw data sheet name: '📋 Raw Data'

ROW_START_2025 = 3   # row 3 = Jan 2025
ROW_END_2025   = 10  # row 10 = Aug 2025
ROW_START_2026 = 15  # row 15 = Jan 2026
ROW_END_2026   = 22  # row 22 = Aug 2026

raw = "'📋 Raw Data'"

def sumf(col, r1, r2):
    return f"=SUMPRODUCT({raw}!{col}{r1}:{col}{r2})"

def avgf(col, r1, r2):
    return f"=AVERAGEIF({raw}!A{r1}:A{r2},\">0\",{raw}!{col}{r1}:{col}{r2})"

# EPH = total_income / total_oh (weighted)
eph_25 = f"=SUMPRODUCT({raw}!G3:G10)/SUMPRODUCT({raw}!E3:E10)"
eph_26 = f"=SUMPRODUCT({raw}!G15:G22)/SUMPRODUCT({raw}!E15:E22)"
pph_25 = f"=SUMPRODUCT({raw}!F3:F10)/SUMPRODUCT({raw}!E3:E10)"
pph_26 = f"=SUMPRODUCT({raw}!F15:F22)/SUMPRODUCT({raw}!E15:E22)"
# avg_oh per driver-month = total_oh / sum_driver_count
avgh_25 = f"=SUMPRODUCT({raw}!E3:E10)/SUMPRODUCT({raw}!D3:D10)"
avgh_26 = f"=SUMPRODUCT({raw}!E15:E22)/SUMPRODUCT({raw}!D15:D22)"
avginc_25 = f"=SUMPRODUCT({raw}!G3:G10)/SUMPRODUCT({raw}!D3:D10)"
avginc_26 = f"=SUMPRODUCT({raw}!G15:G22)/SUMPRODUCT({raw}!D15:D22)"
totaloh_25 = f"=SUMPRODUCT({raw}!E3:E10)"
totaloh_26 = f"=SUMPRODUCT({raw}!E15:E22)"
drv_25 = f"=MAX({raw}!D3:D10)"
drv_26 = f"=MAX({raw}!D15:D22)"

kpi_data = [
    ('EPH — Thu nhập/giờ (VND)',          eph_25,      eph_26,      '#,##0',   '↑ Tài xế earn hiệu quả hơn trên mỗi giờ làm việc'),
    ('PPH — Stops/giờ',                   pph_25,      pph_26,      '0.000',   '↑ Năng suất giao hàng (STP/hour) cải thiện'),
    ('Giờ làm TB/tài xế/tháng',           avgh_25,     avgh_26,     '#,##0.0', '↓ Driver chỉ cần làm ít giờ hơn để đạt target'),
    ('Thu nhập TB/tài xế/tháng (VND)',    avginc_25,   avginc_26,   '#,##0',   '→ Thu nhập ổn định → driver không bị thiệt'),
    ('Total supply hours fleet',          totaloh_25,  totaloh_26,  '#,##0',   '↑ Fleet lớn hơn bù offset cho hour/driver giảm'),
    ('Unique drivers active (Jan–Aug)',   drv_25,      drv_26,      '#,##0',   '+40% retained driver tham gia → fleet mở rộng'),
]

for i, (label, val25, val26, fmt, insight) in enumerate(kpi_data):
    r = 7 + i
    ws1.row_dimensions[r].height = 22

    # Zebra
    row_fill = fill(WHITE) if i % 2 == 0 else fill(LIGHT_BG)

    set_cell(ws1, r, 1, label,    font('Arial', 9, bold=True), row_fill, align('left', 'center'))
    set_cell(ws1, r, 2, val25,    font('Arial', 10, bold=True, color=BLUE_FORMULA), row_fill, align('right', 'center'), fmt=fmt)
    set_cell(ws1, r, 3, val26,    font('Arial', 10, bold=True, color=ORANGE), row_fill, align('right', 'center'), fmt=fmt)

    # Delta absolute = C - B
    delta_cell = f"=C{r}-B{r}"
    set_cell(ws1, r, 4, delta_cell, font('Arial', 9, color=BLACK), row_fill, align('right', 'center'), fmt=fmt)

    # Delta % = (C-B)/B
    pct_cell = f"=IFERROR((C{r}-B{r})/ABS(B{r}),0)"
    set_cell(ws1, r, 5, pct_cell,  font('Arial', 9, bold=True), row_fill, align('center', 'center'), fmt='0.0%;(0.0%);-')

    # Insight
    ws1.merge_cells(f'F{r}:H{r}')
    set_cell(ws1, r, 6, insight,  font('Arial', 8.5, italic=True, color=GRAY_MUTED), row_fill, align('left', 'center'))

# Conditional format delta % col (E = col 5)
from openpyxl.formatting.rule import ColorScaleRule
ws1.conditional_formatting.add(
    f'E7:E{6+len(kpi_data)}',
    ColorScaleRule(
        start_type='min', start_color='FFCCCC',
        mid_type='num', mid_value=0, mid_color='FFFFFF',
        end_type='max', end_color='C6EFCE'
    )
)

sep_row = 7 + len(kpi_data)
ws1.row_dimensions[sep_row].height = 14

# ── Efficiency hypothesis block ──────────────────────────────────────────────
h_row = sep_row + 1
ws1.row_dimensions[h_row].height = 20
ws1.merge_cells(f'A{h_row}:H{h_row}')
set_cell(ws1, h_row, 1, '💡 Efficiency Hypothesis — Giờ cần làm để đạt 13,000,000 VND/tháng',
         font('Arial', 10, bold=True, color=WHITE),
         fill(ORANGE),
         align('left', 'center'))

target_row = h_row + 1
ws1.row_dimensions[target_row].height = 18
set_cell(ws1, target_row, 1, 'Target income/tháng (VND)',
         font('Arial', 9), fill(ORANGE_SOFT), align('left', 'center'))
set_cell(ws1, target_row, 2, 13000000,
         font('Arial', 10, bold=True, color=BLUE_FORMULA),
         fill(YELLOW_BG),
         align('right', 'center'), fmt='#,##0')
ws1.merge_cells(f'C{target_row}:H{target_row}')
set_cell(ws1, target_row, 3, 'Tương đương 500k/ngày × 26 ngày làm việc — input thủ công (màu xanh = hardcode)',
         font('Arial', 8, italic=True, color=GRAY_MUTED), fill(ORANGE_SOFT), align('left', 'center'))
ws1.cell(target_row, 2).fill = fill(YELLOW_BG)

hrs_row = target_row + 1
ws1.row_dimensions[hrs_row].height = 18
set_cell(ws1, hrs_row, 1, 'Giờ cần làm — 2025',
         font('Arial', 9), fill(BLUE_SOFT), align('left', 'center'))
hrs_25_formula = f"=IFERROR($B${target_row}/B7, 0)"
set_cell(ws1, hrs_row, 2, hrs_25_formula,
         font('Arial', 10, bold=True, color=GREEN_LINK),
         fill(BLUE_SOFT), align('right', 'center'), fmt='#,##0.0')
set_cell(ws1, hrs_row, 3, f"=IFERROR($B${target_row}/C7, 0)",
         font('Arial', 10, bold=True, color=GREEN_LINK),
         fill(BLUE_SOFT), align('right', 'center'), fmt='#,##0.0')
set_cell(ws1, hrs_row, 4, f"=C{hrs_row}-B{hrs_row}",
         font('Arial', 9), fill(BLUE_SOFT), align('right', 'center'), fmt='#,##0.0')
set_cell(ws1, hrs_row, 5, f"=IFERROR((C{hrs_row}-B{hrs_row})/B{hrs_row},0)",
         font('Arial', 9, bold=True), fill(BLUE_SOFT), align('center', 'center'), fmt='0.0%;(0.0%);-')
ws1.merge_cells(f'F{hrs_row}:H{hrs_row}')
set_cell(ws1, hrs_row, 6, f'2026: tiết kiệm ~42.8 giờ/tháng (−13.5%) để đạt cùng target',
         font('Arial', 8.5, italic=True, color=GRAY_MUTED), fill(BLUE_SOFT), align('left', 'center'))
ws1.merge_cells(f'A{hrs_row}:A{hrs_row}')
set_cell(ws1, hrs_row, 1, 'Giờ cần làm — 2025 / 2026',
         font('Arial', 9), fill(BLUE_SOFT), align('left', 'center'))

# ── Color legend ─────────────────────────────────────────────────────────────
leg_row = hrs_row + 2
ws1.row_dimensions[leg_row].height = 16
ws1.merge_cells(f'A{leg_row}:H{leg_row}')
set_cell(ws1, leg_row, 1,
         'Quy ước màu: Xanh đậm = hardcode input   |   Cam = giá trị 2026   |   Đen = công thức tính   |   Xanh lá = link sang sheet khác   |   Nền vàng = input cần cập nhật',
         font('Arial', 8, italic=True, color=GRAY_MUTED),
         fill(LIGHT_BG), align('left', 'center'))

# ═══════════════════════════════════════════════════════════════════════════
# SHEET 2: RAW DATA
# ═══════════════════════════════════════════════════════════════════════════
ws2 = wb.create_sheet('📋 Raw Data')
ws2.sheet_view.showGridLines = False

# Column widths
col_w2 = {1:8, 2:6, 3:8, 4:14, 5:18, 6:16, 7:18, 8:18, 9:18,
           10:16, 11:18, 12:14, 13:14, 14:10, 15:10, 16:10}
for c, w in col_w2.items():
    ws2.column_dimensions[get_column_letter(c)].width = w

ws2.row_dimensions[1].height = 8
ws2.row_dimensions[2].height = 36

ws2.merge_cells('A2:P2')
set_cell(ws2, 2, 1, 'Raw Data — Monthly Aggregates by Year (Jan 2025 – Sep 2026)',
         font('Arial', 13, bold=True, color=WHITE),
         fill(BLUE_DARK), align('center', 'center'))

headers = [
    ('Year', 8), ('Mo', 6), ('Tháng', 8),
    ('Drivers\n(unique)', 14), ('Total Online\nHours', 18), ('Total STP', 16),
    ('Total Income\n(VND)', 18), ('Order Income\n(VND)', 18), ('Reward Income\n(VND)', 18),
    ('Avg OH/\nDriver', 14), ('Avg Income/\nDriver', 16), ('Avg STP/\nDriver', 14),
    ('EPH\n(VND/hr)', 14), ('PPH\n(STP/hr)', 10), ('Reward\n% of Inc', 10), ('Avg\nRating', 10)
]

ws2.row_dimensions[3].height = 36
for col_i, (hdr, _) in enumerate(headers, start=1):
    set_cell(ws2, 3, col_i, hdr,
             font('Arial', 8.5, bold=True, color=WHITE),
             fill(BLUE_DARK),
             align('center', 'center', wrap=True),
             brd=thick_bottom())

row = 4
prev_yr = None
for (yr, mn) in sorted(monthly.keys()):
    m = get_metrics(yr, mn)
    if not m: continue

    is_partial = (yr == '2026' and mn == 9)
    yr_fill = fill(LIGHT_BG) if yr == '2025' else fill(ORANGE_SOFT)
    if is_partial:
        yr_fill = fill('FFF3CD')  # yellow-ish for partial

    # year group separator
    if prev_yr and prev_yr != yr:
        ws2.row_dimensions[row].height = 6
        row += 1
    prev_yr = yr

    ws2.row_dimensions[row].height = 18
    data_row = [
        yr, mn, MONTHS[mn-1],
        m['driver_count'], m['total_oh'], m['total_stp'],
        m['total_income'], m['order_income'], m['reward_income'],
        m['avg_oh'], m['avg_income'], m['avg_stp'],
        m['eph'], m['pph'], m['reward_pct'], m['avg_rating']
    ]
    fmts = [
        '@', '0', '@',
        '#,##0', '#,##0.0', '#,##0',
        '#,##0', '#,##0', '#,##0',
        '#,##0.0', '#,##0', '#,##0.0',
        '#,##0', '0.000', '0.0%', '0.000'
    ]
    txt_colors = [
        BLACK, BLACK, BLACK,
        BLUE_FORMULA, BLUE_FORMULA, BLUE_FORMULA,
        BLUE_FORMULA, BLUE_FORMULA, BLUE_FORMULA,
        BLACK, BLACK, BLACK,
        BLACK, BLACK, BLACK, BLACK
    ]

    for col_i, (val, fmt, tcol) in enumerate(zip(data_row, fmts, txt_colors), start=1):
        set_cell(ws2, row, col_i, val,
                 font('Arial', 9, color=tcol),
                 yr_fill,
                 align('right' if col_i > 3 else 'center', 'center'),
                 fmt=fmt)
    # Month name left-align
    ws2.cell(row, 3).alignment = align('center', 'center')
    row += 1

# ── Totals / averages Jan-Aug per year ───────────────────────────────────────
# 2025 rows 3..10 (0-indexed from data start = row 4..11 in sheet)
# Let's add summary rows at bottom

ws2.row_dimensions[row].height = 8
row += 1

# Jan-Aug subtotals using SUMPRODUCT (using sheet formulas)
# 2025 Jan-Aug = rows 4-11, 2026 Jan-Aug = rows 13-20 (after the blank separator row 12)
# Let's track actual row positions

# Actually let's mark them explicitly. 2025 starts at row 4 (Jan) through row 15 (Dec)
# with one blank at row 16, then 2026 starts at 17.
# Based on our loop:
# yr=2025, mn=1..12 → rows 4..15
# blank row = 16
# yr=2026, mn=1..9 → rows 17..25
# We'll reference these in Summary sheet already via hardcoded ranges.

for yr_label, r1, r2, row_fill_color in [
    ('2025 Jan–Aug Aggregate', 4, 11, BLUE_SOFT),
    ('2026 Jan–Aug Aggregate', 13, 20, ORANGE_SOFT),
]:
    ws2.row_dimensions[row].height = 22
    set_cell(ws2, row, 1, yr_label,
             font('Arial', 9, bold=True, color=BLUE_DARK),
             fill(row_fill_color), align('left', 'center'))
    ws2.merge_cells(f'A{row}:C{row}')

    # driver count: use max (unique driver pool approximation)
    set_cell(ws2, row, 4, f'=MAX(D{r1}:D{r2})',
             font('Arial', 9, bold=True, color=GREEN_LINK),
             fill(row_fill_color), align('right', 'center'), fmt='#,##0')

    # total online hours
    set_cell(ws2, row, 5, f'=SUM(E{r1}:E{r2})',
             font('Arial', 9, bold=True, color=GREEN_LINK),
             fill(row_fill_color), align('right', 'center'), fmt='#,##0.0')

    # total STP
    set_cell(ws2, row, 6, f'=SUM(F{r1}:F{r2})',
             font('Arial', 9, bold=True, color=GREEN_LINK),
             fill(row_fill_color), align('right', 'center'), fmt='#,##0')

    # total income / order / reward
    for col_i, col_letter in [(7,'G'), (8,'H'), (9,'I')]:
        set_cell(ws2, row, col_i, f'=SUM({col_letter}{r1}:{col_letter}{r2})',
                 font('Arial', 9, bold=True, color=GREEN_LINK),
                 fill(row_fill_color), align('right', 'center'), fmt='#,##0')

    # avg OH per driver-month = sum(OH)/sum(drivers)
    set_cell(ws2, row, 10, f'=IFERROR(E{row}/SUM(D{r1}:D{r2}),0)',
             font('Arial', 9, bold=True, color=GREEN_LINK),
             fill(row_fill_color), align('right', 'center'), fmt='#,##0.0')

    # avg income per driver-month
    set_cell(ws2, row, 11, f'=IFERROR(G{row}/SUM(D{r1}:D{r2}),0)',
             font('Arial', 9, bold=True, color=GREEN_LINK),
             fill(row_fill_color), align('right', 'center'), fmt='#,##0')

    # avg stp per driver-month
    set_cell(ws2, row, 12, f'=IFERROR(F{row}/SUM(D{r1}:D{r2}),0)',
             font('Arial', 9, bold=True, color=GREEN_LINK),
             fill(row_fill_color), align('right', 'center'), fmt='#,##0.0')

    # EPH = total_income / total_oh
    set_cell(ws2, row, 13, f'=IFERROR(G{row}/E{row},0)',
             font('Arial', 9, bold=True, color=GREEN_LINK),
             fill(row_fill_color), align('right', 'center'), fmt='#,##0')

    # PPH = total_stp / total_oh
    set_cell(ws2, row, 14, f'=IFERROR(F{row}/E{row},0)',
             font('Arial', 9, bold=True, color=GREEN_LINK),
             fill(row_fill_color), align('right', 'center'), fmt='0.000')

    # Reward %
    set_cell(ws2, row, 15, f'=IFERROR(I{row}/G{row},0)',
             font('Arial', 9, bold=True, color=GREEN_LINK),
             fill(row_fill_color), align('right', 'center'), fmt='0.0%')

    # Avg rating = average
    set_cell(ws2, row, 16, f'=AVERAGE(P{r1}:P{r2})',
             font('Arial', 9, bold=True, color=GREEN_LINK),
             fill(row_fill_color), align('right', 'center'), fmt='0.000')

    row += 1

# ═══════════════════════════════════════════════════════════════════════════
# SHEET 3: YoY COMPARISON
# ═══════════════════════════════════════════════════════════════════════════
ws3 = wb.create_sheet('📈 YoY Comparison')
ws3.sheet_view.showGridLines = False

col_w3 = {1:10, 2:16, 3:16, 4:14, 5:14, 6:12, 7:14, 8:14, 9:12, 10:14, 11:14, 12:12}
for c, w in col_w3.items():
    ws3.column_dimensions[get_column_letter(c)].width = w

ws3.row_dimensions[1].height = 8
ws3.row_dimensions[2].height = 36

ws3.merge_cells('A2:L2')
set_cell(ws3, 2, 1, 'YoY Comparison — Cùng Tháng 2025 vs 2026 (Jan–Aug)',
         font('Arial', 13, bold=True, color=WHITE),
         fill(BLUE_DARK), align('center', 'center'))

ws3.row_dimensions[3].height = 8

# Sub-header groups
ws3.row_dimensions[4].height = 22
ws3.row_dimensions[5].height = 32

# Header row
group_headers = [
    ('Tháng', 1, 1, BLUE_DARK),
    ('EPH (VND/giờ)', 2, 4, BLUE_DARK),
    ('Giờ làm TB/Driver', 5, 7, BLUE_DARK),
    ('Thu nhập TB/Driver', 8, 10, BLUE_DARK),
    ('PPH (STP/giờ)', 11, 12, BLUE_DARK),
]

for (grp, c1, c2, bg) in group_headers:
    if c1 == c2:
        ws3.merge_cells(f'{get_column_letter(c1)}4:{get_column_letter(c2)}5')
    else:
        ws3.merge_cells(f'{get_column_letter(c1)}4:{get_column_letter(c2)}4')
    set_cell(ws3, 4, c1, grp,
             font('Arial', 9, bold=True, color=WHITE),
             fill(bg), align('center', 'center'))

sub_hdrs = ['', '2025', '2026', 'Δ%', '2025', '2026', 'Δ%', '2025', '2026', 'Δ%', '2025', '2026']
for col_i, hdr in enumerate(sub_hdrs, 1):
    if col_i == 1: continue
    sub_fill = fill(BLUE_SOFT) if col_i in [2,5,8,11] else \
               fill(ORANGE_SOFT) if col_i in [3,6,9,12] else \
               fill(LIGHT_BG)
    set_cell(ws3, 5, col_i, hdr,
             font('Arial', 8.5, bold=True, color=BLUE_DARK),
             sub_fill, align('center', 'center'),
             brd=thick_bottom())

# Raw data for 2025: ws2 rows 4-15 (Jan-Dec), 2026: rows 17-25 (Jan-Sep)
# We reference by month position:
# 2025 Jan = row 4, Feb = 5, ..., Aug = 11
# 2026 Jan = row 13, Feb = 14, ..., Aug = 20
# (based on how data was written: 12 months + 1 blank + 9 months)

raw2 = "'📋 Raw Data'"

yoy_data_start = 6
for i, mn in enumerate(range(1, 9)):
    r = yoy_data_start + i
    ws3.row_dimensions[r].height = 20

    r25 = 3 + mn        # row in raw data sheet for 2025
    r26 = 3 + 12 + 1 + mn  # = 3 + 13 + mn = 16 + mn

    row_fill = fill(WHITE) if i % 2 == 0 else fill(LIGHT_BG)
    partial_note = ' *' if mn == 9 else ''

    # Month label
    set_cell(ws3, r, 1, MONTHS[mn-1] + partial_note,
             font('Arial', 9, bold=True), row_fill, align('center', 'center'))

    # EPH
    eph25_ref = f"{raw2}!M{r25}"
    eph26_ref = f"{raw2}!M{r26}"
    set_cell(ws3, r, 2, f"={eph25_ref}", font('Arial', 9, color=GREEN_LINK), row_fill, align('right','center'), fmt='#,##0')
    set_cell(ws3, r, 3, f"={eph26_ref}", font('Arial', 9, color=GREEN_LINK), row_fill, align('right','center'), fmt='#,##0')
    set_cell(ws3, r, 4, f"=IFERROR((C{r}-B{r})/ABS(B{r}),0)", font('Arial', 9, bold=True), row_fill, align('center','center'), fmt='0.0%;(0.0%);"-"')

    # Avg hours
    oh25_ref = f"{raw2}!J{r25}"
    oh26_ref = f"{raw2}!J{r26}"
    set_cell(ws3, r, 5, f"={oh25_ref}", font('Arial', 9, color=GREEN_LINK), row_fill, align('right','center'), fmt='#,##0.0')
    set_cell(ws3, r, 6, f"={oh26_ref}", font('Arial', 9, color=GREEN_LINK), row_fill, align('right','center'), fmt='#,##0.0')
    set_cell(ws3, r, 7, f"=IFERROR((F{r}-E{r})/ABS(E{r}),0)", font('Arial', 9, bold=True), row_fill, align('center','center'), fmt='0.0%;(0.0%);"-"')

    # Avg income
    inc25_ref = f"{raw2}!K{r25}"
    inc26_ref = f"{raw2}!K{r26}"
    set_cell(ws3, r, 8, f"={inc25_ref}", font('Arial', 9, color=GREEN_LINK), row_fill, align('right','center'), fmt='#,##0')
    set_cell(ws3, r, 9, f"={inc26_ref}", font('Arial', 9, color=GREEN_LINK), row_fill, align('right','center'), fmt='#,##0')
    set_cell(ws3, r, 10, f"=IFERROR((I{r}-H{r})/ABS(H{r}),0)", font('Arial', 9, bold=True), row_fill, align('center','center'), fmt='0.0%;(0.0%);"-"')

    # PPH
    pph25_ref = f"{raw2}!N{r25}"
    pph26_ref = f"{raw2}!N{r26}"
    set_cell(ws3, r, 11, f"={pph25_ref}", font('Arial', 9, color=GREEN_LINK), row_fill, align('right','center'), fmt='0.000')
    set_cell(ws3, r, 12, f"={pph26_ref}", font('Arial', 9, color=GREEN_LINK), row_fill, align('right','center'), fmt='0.000')

# Totals row
tot_r = yoy_data_start + 8
ws3.row_dimensions[tot_r].height = 22

# Jan-Aug summary using aggregate rows from raw data sheet
# 2025 agg row = row 4 after the 12-month block + blank = row 17 in raw data? No.
# Let's compute: 2025 = rows 4..15 (Jan-Dec), blank row 16, 2026 = rows 17..25 (Jan-Sep)
# Then agg rows were appended at row = 4+12+1+9+1 = 27 for 2025 agg, 28 for 2026 agg
# But this is fragile. Use SUMPRODUCT directly.

for col_i, (r1, r2) in [(2, (4, 11)), (3, (13, 20))]:
    set_cell(ws3, tot_r, col_i,
             f"=IFERROR(SUMPRODUCT({raw2}!G{r1}:G{r2})/SUMPRODUCT({raw2}!E{r1}:E{r2}),0)",
             font('Arial', 9, bold=True, color=GREEN_LINK),
             fill(BLUE_SOFT), align('right','center'), fmt='#,##0')

set_cell(ws3, tot_r, 1, 'Jan–Aug avg', font('Arial', 9, bold=True), fill(BLUE_SOFT), align('center','center'))
set_cell(ws3, tot_r, 4, f"=IFERROR((C{tot_r}-B{tot_r})/ABS(B{tot_r}),0)",
         font('Arial', 9, bold=True), fill(BLUE_SOFT), align('center','center'), fmt='0.0%;(0.0%);"-"')

# avg hours aggregate
set_cell(ws3, tot_r, 5,
         f"=IFERROR(SUMPRODUCT({raw2}!E4:E11)/SUMPRODUCT({raw2}!D4:D11),0)",
         font('Arial', 9, bold=True, color=GREEN_LINK),
         fill(BLUE_SOFT), align('right','center'), fmt='#,##0.0')
set_cell(ws3, tot_r, 6,
         f"=IFERROR(SUMPRODUCT({raw2}!E13:E20)/SUMPRODUCT({raw2}!D13:D20),0)",
         font('Arial', 9, bold=True, color=GREEN_LINK),
         fill(BLUE_SOFT), align('right','center'), fmt='#,##0.0')
set_cell(ws3, tot_r, 7, f"=IFERROR((F{tot_r}-E{tot_r})/ABS(E{tot_r}),0)",
         font('Arial', 9, bold=True), fill(BLUE_SOFT), align('center','center'), fmt='0.0%;(0.0%);"-"')

# avg income aggregate
set_cell(ws3, tot_r, 8,
         f"=IFERROR(SUMPRODUCT({raw2}!G4:G11)/SUMPRODUCT({raw2}!D4:D11),0)",
         font('Arial', 9, bold=True, color=GREEN_LINK),
         fill(BLUE_SOFT), align('right','center'), fmt='#,##0')
set_cell(ws3, tot_r, 9,
         f"=IFERROR(SUMPRODUCT({raw2}!G13:G20)/SUMPRODUCT({raw2}!D13:D20),0)",
         font('Arial', 9, bold=True, color=GREEN_LINK),
         fill(BLUE_SOFT), align('right','center'), fmt='#,##0')
set_cell(ws3, tot_r, 10, f"=IFERROR((I{tot_r}-H{tot_r})/ABS(H{tot_r}),0)",
         font('Arial', 9, bold=True), fill(BLUE_SOFT), align('center','center'), fmt='0.0%;(0.0%);"-"')

# PPH aggregate
set_cell(ws3, tot_r, 11,
         f"=IFERROR(SUMPRODUCT({raw2}!F4:F11)/SUMPRODUCT({raw2}!E4:E11),0)",
         font('Arial', 9, bold=True, color=GREEN_LINK),
         fill(BLUE_SOFT), align('right','center'), fmt='0.000')
set_cell(ws3, tot_r, 12,
         f"=IFERROR(SUMPRODUCT({raw2}!F13:F20)/SUMPRODUCT({raw2}!E13:E20),0)",
         font('Arial', 9, bold=True, color=GREEN_LINK),
         fill(BLUE_SOFT), align('right','center'), fmt='0.000')

# Conditional formatting Δ% columns
for delta_col in ['D', 'G', 'J']:
    ws3.conditional_formatting.add(
        f'{delta_col}{yoy_data_start}:{delta_col}{tot_r}',
        ColorScaleRule(
            start_type='min', start_color='FFCCCC',
            mid_type='num', mid_value=0, mid_color='FFFFFF',
            end_type='max', end_color='C6EFCE'
        )
    )

# ── Notes ─────────────────────────────────────────────────────────────────
note_r = tot_r + 2
ws3.row_dimensions[note_r].height = 16
ws3.merge_cells(f'A{note_r}:L{note_r}')
set_cell(ws3, note_r, 1,
         '* Sep 2026 partial (18/30 ngày) — không đưa vào bảng này để tránh bias khi so YoY với Sep 2025 (full tháng)',
         font('Arial', 8, italic=True, color=GRAY_MUTED), align('left','center'))

# ═══════════════════════════════════════════════════════════════════════════
# SHEET 4: OBSERVATIONS
# ═══════════════════════════════════════════════════════════════════════════
ws4 = wb.create_sheet('🔍 Observations')
ws4.sheet_view.showGridLines = False
ws4.column_dimensions['A'].width = 28
ws4.column_dimensions['B'].width = 90

ws4.row_dimensions[1].height = 8
ws4.row_dimensions[2].height = 36
ws4.merge_cells('A2:B2')
set_cell(ws4, 2, 1, 'Nhận Định & Điểm Cần Theo Dõi',
         font('Arial', 13, bold=True, color=WHITE),
         fill(BLUE_DARK), align('center', 'center'))

obs_items = [
    ('✅ HYPOTHESIS CONFIRMED', 'BLUE_DARK'),
    ('EPH Jan–Aug tăng +15.6%',
     'Retained driver earn 47,380 VND/giờ năm 2026 vs 40,992 VND/giờ năm 2025. '
     'Cùng với PPH +13.3%, driver hiệu quả hơn thực chất — không phải do reward tăng mà do density đơn tốt hơn.'),
    ('Giờ làm giảm −11.6%',
     'Driver chỉ cần trung bình 93.0 giờ/tháng (2026) vs 105.2 giờ (2025) để đạt thu nhập tương đương. '
     'Thu nhập avg +2.2% (4,407k vs 4,312k) → driver không bị thiệt, họ chủ động giảm giờ.'),
    ('Target income đạt được dễ hơn 13.5%',
     'Để đạt 13M VND/tháng (~500k/ngày × 26 ngày): cần 274h năm 2026 vs 317h năm 2025. '
     'Tức tiết kiệm ~42.8 giờ/tháng = gần 1.5 giờ/ngày. Driver có thể làm part-time hơn mà vẫn đủ sống.'),
    ('Total supply hours fleet tăng +9.0%',
     '6.67M → 7.27M giờ (Jan–Aug). Supply không giảm mà tăng do fleet mở rộng: số driver unique +40% '
     '(từ 11,231 → 15,731). Hiệu ứng composition: driver mới/ít kinh nghiệm kéo giờ avg lên, '
     'nhưng driver retained thực sự đang giảm giờ.'),

    ('⚠️ ĐIỂM CẦN THEO DÕI', 'ORANGE'),
    ('Jan 2026 EPH thấp hơn Jan 2025 (−8.6%)',
     'Tháng duy nhất EPH 2026 thấp hơn cùng kỳ. EPH Jan 2026 = 46,403 vs Jan 2025 = 50,760. '
     'Cần kiểm tra: (1) incentive scheme đầu năm 2026 có thay đổi không? '
     '(2) Driver mới (NIM) chiếm tỷ trọng cao sau Tết → kéo EPH xuống. '
     '(3) Volume Tết 2026 vs 2025 có chênh lệch không?'),
    ('EPH có xu hướng hội tụ về 2025 từ Q3 2026',
     'Jun→Jul→Aug 2026: 46,197 → 42,659 → 45,486. Khoảng cách YoY đang thu hẹp: '
     'Jun +14.3%, Jul +11.0%, Aug +7.5%. Nếu trend này tiếp tục → driver sẽ phải tăng giờ trở lại '
     'trong Q4 2026. Cần monitor Sep–Oct để xác nhận.'),
    ('Supply hour per driver giảm ít hơn trong Q3',
     'Jun: −4.6%, Jul: −4.4%, Aug: −3.2% (giảm ít hơn so với Feb–May: −22.7% đến −12.3%). '
     'Xu hướng hội tụ tương đồng với EPH. Có thể Q1 2026 được hưởng lợi từ restructure incentive, '
     'nhưng Q3 bắt đầu normalize.'),

    ('📊 PHƯƠNG PHÁP LUẬN', 'BLUE_DARK'),
    ('Cohort definition',
     'Retained driver = supplier_id có stp_complete > 0 trong ÍT NHẤT 1 ngày của năm 2025 '
     'VÀ ÍT NHẤT 1 ngày của năm 2026. Không giới hạn số tháng active.'),
    ('Scope & filter',
     'SGN only (city_id = SGN từ raw_supplier_profile). Vehicle type: MOTORBIKE + EV-BIKE. '
     'Loại: ahamove_ka_lazada, VNM-WH-DELIVERY, VNM-WH-VENDOR, SALESFORCE tags. '
     'partitioned_create_time >= 2010-01-01 để loại account test.'),
    ('EPH definition',
     'EPH = (order_income + reward_income_pit1_5) / online_hours. '
     'reward_income đã net thuế TNCN 1.5% (pit = Personal Income Tax). '
     'Là thu nhập tài xế thực nhận, không phải chi phí platform.'),
    ('Sep 2026 partial',
     'Tháng 9/2026 chỉ có 18/30 ngày (đến 2026-09-18). Giữ nguyên trong Raw Data để track '
     'nhưng KHÔNG đưa vào bảng YoY Comparison để tránh bias khi so với Sep 2025 full tháng.'),
]

current_r = 4
for item in obs_items:
    if len(item) == 2 and item[1] in ('BLUE_DARK', 'ORANGE'):
        # Section header
        current_r += 1 if current_r > 4 else 0
        ws4.row_dimensions[current_r].height = 24
        ws4.merge_cells(f'A{current_r}:B{current_r}')
        bg = BLUE_DARK if item[1] == 'BLUE_DARK' else ORANGE
        set_cell(ws4, current_r, 1, item[0],
                 font('Arial', 10, bold=True, color=WHITE),
                 fill(bg), align('left', 'center'))
        current_r += 1
    else:
        title, body = item
        ws4.row_dimensions[current_r].height = 18
        set_cell(ws4, current_r, 1, title,
                 font('Arial', 9, bold=True, color=BLUE_DARK),
                 fill(LIGHT_BG), align('left', 'top'))
        ws4.row_dimensions[current_r].height = max(
            18, min(80, 14 + len(body)//80 * 14))
        set_cell(ws4, current_r, 2, body,
                 font('Arial', 9), fill(WHITE),
                 align('left', 'top', wrap=True),
                 brd=thin_border(bottom=True))
        current_r += 1

# Footnote
current_r += 1
ws4.row_dimensions[current_r].height = 16
ws4.merge_cells(f'A{current_r}:B{current_r}')
set_cell(ws4, current_r, 1,
         f'Nguồn: ahamove_archive_ops.fct_supplier_performance + ahamove_archive.ops_suppliers_online_hours | '
         f'Prepared: 2026-09-18 | 191,338 driver-month records | 15,825 unique suppliers',
         font('Arial', 8, italic=True, color=GRAY_MUTED), fill(LIGHT_BG),
         align('left', 'center'))

# ── Set sheet tab colors ─────────────────────────────────────────────────────
ws1.sheet_properties.tabColor = BLUE_DARK
ws2.sheet_properties.tabColor = '3D5A80'
ws3.sheet_properties.tabColor = ORANGE
ws4.sheet_properties.tabColor = GREEN

# ── Freeze panes ─────────────────────────────────────────────────────────────
ws2.freeze_panes = 'D4'
ws3.freeze_panes = 'B6'

wb.save(OUTPUT)
print(f'Saved: {OUTPUT}')
