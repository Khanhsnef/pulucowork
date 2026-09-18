"""
Build 2026-09-retained-driver-yoy.xlsx
YoY analysis: Retained driver cohort SGN 2025 vs 2026
"""
import csv
from collections import defaultdict
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import ColorScaleRule

INPUT  = '/Users/ts-1148/Desktop/Pulu-workspace/metabase_driver_monthly_full.csv'
OUTPUT = '/Users/ts-1148/Desktop/Pulu-workspace/output/Ahamove/05. ANALYSIS_REPORTS/2026-09-retained-driver-yoy.xlsx'

# ── Brand colors ─────────────────────────────────────────────────────────────
C = {
    'blue_dark':   '0E4174',
    'orange':      'FF7F32',
    'white':       'FFFFFF',
    'light_bg':    'F0F4FA',
    'blue_soft':   'DDEAF8',
    'orange_soft': 'FFF0E6',
    'green':       '10B981',
    'red':         'EF4444',
    'yellow':      'FFFDE7',
    'black':       '000000',
    'blue_in':     '1F3864',   # hardcoded input color (dark blue)
    'green_link':  '375623',   # cross-sheet formula
    'gray':        '7A94B0',
    'border':      'D6E2F0',
    'orange_dark': 'CC5500',
}

def fnt(size=10, bold=False, color='000000', italic=False):
    return Font(name='Arial', size=size, bold=bold, color=color, italic=italic)

def fll(hex_color):
    return PatternFill('solid', fgColor=hex_color)

def aln(h='left', v='center', wrap=False):
    return Alignment(horizontal=h, vertical=v, wrap_text=wrap)

def border_bottom(color='0E4174', style='medium'):
    return Border(bottom=Side(style=style, color=color))

def border_all(color='D6E2F0'):
    s = Side(style='thin', color=color)
    return Border(top=s, bottom=s, left=s, right=s)

def sc(ws, r, c, val, font=None, fill=None, align=None, fmt=None, border=None):
    cell = ws.cell(row=r, column=c, value=val)
    if font:   cell.font = font
    if fill:   cell.fill = fill
    if align:  cell.alignment = align
    if fmt:    cell.number_format = fmt
    if border: cell.border = border
    return cell

def cw(ws, col, width):
    ws.column_dimensions[get_column_letter(col)].width = width

def rh(ws, row, height):
    ws.row_dimensions[row].height = height

MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

# ── Load CSV ──────────────────────────────────────────────────────────────────
with open(INPUT) as f:
    rows = list(csv.DictReader(f))

def sf(v):
    try: return float(v) if v else 0.0
    except: return 0.0

monthly = defaultdict(lambda: {
    'drivers': set(), 'oh': 0.0, 'stp': 0.0,
    'total_inc': 0.0, 'order_inc': 0.0, 'reward_inc': 0.0,
    'rsum': 0.0, 'rcnt': 0
})

for r in rows:
    k = (r['year'], int(r['month_num']))
    d = monthly[k]
    d['drivers'].add(r['supplier_id'])
    d['oh']         += sf(r['online_hours'])
    d['stp']        += sf(r['stp_complete'])
    d['total_inc']  += sf(r['total_income'])
    d['order_inc']  += sf(r['order_income'])
    d['reward_inc'] += sf(r['reward_income'])
    rv = sf(r['avg_rating'])
    if rv > 0:
        d['rsum'] += rv
        d['rcnt']  += 1

def metrics(yr, mn):
    d = monthly.get((str(yr), mn))
    if not d: return None
    n  = len(d['drivers'])
    oh = d['oh']
    return {
        'n': n, 'oh': oh, 'stp': d['stp'],
        'ti': d['total_inc'], 'oi': d['order_inc'], 'ri': d['reward_inc'],
        'avg_oh':  oh / n if n else 0,
        'avg_inc': d['total_inc'] / n if n else 0,
        'avg_stp': d['stp'] / n if n else 0,
        'eph':  d['total_inc'] / oh if oh else 0,
        'pph':  d['stp'] / oh if oh else 0,
        'rpct': d['reward_inc'] / d['total_inc'] if d['total_inc'] else 0,
        'rating': d['rsum'] / d['rcnt'] if d['rcnt'] else 0,
    }

wb = Workbook()

# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 1 — RAW DATA (hardcoded values, blue = input)
# Raw data lays out: 2025 rows 3-14 (Jan-Dec), blank row 15, 2026 rows 16-24 (Jan-Sep)
# Jan-Aug 2025 = rows 3-10, Jan-Aug 2026 = rows 16-23
# ═══════════════════════════════════════════════════════════════════════════════
ws_raw = wb.active
ws_raw.title = 'Raw Data'
ws_raw.sheet_view.showGridLines = False

# Col widths
for c, w in [(1,8),(2,6),(3,9),(4,14),(5,18),(6,14),(7,19),(8,19),(9,18),
             (10,14),(11,16),(12,14),(13,14),(14,10),(15,10),(16,10)]:
    cw(ws_raw, c, w)

rh(ws_raw, 1, 8)
rh(ws_raw, 2, 34)
ws_raw.merge_cells('A2:P2')
sc(ws_raw, 2, 1, 'Raw Data — Monthly Aggregates | Retained Cohort SGN 2025–2026',
   fnt(13, True, C['white']), fll(C['blue_dark']), aln('center','center'))

# Header
rh(ws_raw, 3, 34)
hdrs = [
    'Year','Mo','Tháng',
    'Drivers\n(unique)','Total Online\nHours','Total\nSTP',
    'Total Income\n(VND)','Order Income\n(VND)','Reward Income\n(VND)',
    'Avg OH/\nDriver','Avg Income/\nDriver','Avg STP/\nDriver',
    'EPH\n(VND/hr)','PPH\n(STP/hr)','Reward\n%','Avg\nRating'
]
for ci, h in enumerate(hdrs, 1):
    sc(ws_raw, 3, ci, h,
       fnt(8.5, True, C['white']),
       fll(C['blue_dark']),
       aln('center','center',True),
       border=border_bottom())

fmts = ['@','0','@',
        '#,##0','#,##0.0','#,##0',
        '#,##0','#,##0','#,##0',
        '#,##0.0','#,##0','#,##0.0',
        '#,##0','0.000','0.0%','0.000']

# Write data rows
row_map = {}  # (yr_str, mn) -> row number in sheet
data_row = 4
for yr in ['2025', '2026']:
    for mn in range(1, 13 if yr == '2025' else 10):
        m = metrics(yr, mn)
        if not m: continue
        is_partial = (yr == '2026' and mn == 9)
        rfill = fll(C['light_bg'] if yr == '2025' else C['orange_soft'])
        if is_partial:
            rfill = fll(C['yellow'])
        rh(ws_raw, data_row, 18)
        vals = [
            int(yr), mn, MONTHS[mn-1],
            m['n'], m['oh'], m['stp'],
            m['ti'], m['oi'], m['ri'],
            m['avg_oh'], m['avg_inc'], m['avg_stp'],
            m['eph'], m['pph'], m['rpct'], m['rating']
        ]
        for ci, (v, fmt) in enumerate(zip(vals, fmts), 1):
            color = C['blue_in'] if ci >= 4 else C['black']
            sc(ws_raw, data_row, ci, v,
               fnt(9, False, color),
               rfill,
               aln('center' if ci <= 3 else 'right','center'),
               fmt=fmt)
        row_map[(yr, mn)] = data_row
        data_row += 1
    if yr == '2025':
        rh(ws_raw, data_row, 8)
        data_row += 1  # blank separator row

# Aggregate summary rows at bottom
agg_start = data_row + 1
rh(ws_raw, data_row, 8)
data_row += 1

for yr_label, yr_str, rfill_color in [
    ('2025 Jan–Aug (8 months aggregate)', '2025', C['blue_soft']),
    ('2026 Jan–Aug (8 months aggregate)', '2026', C['orange_soft']),
]:
    rh(ws_raw, data_row, 22)
    r1 = row_map[(yr_str, 1)]
    r8 = row_map[(yr_str, 8)]
    rfill = fll(rfill_color)

    ws_raw.merge_cells(f'A{data_row}:C{data_row}')
    sc(ws_raw, data_row, 1, yr_label, fnt(9, True, C['blue_dark']), rfill, aln('left','center'))

    # D: max driver count
    sc(ws_raw, data_row, 4,  f'=MAX(D{r1}:D{r8})',     fnt(9,True,C['green_link']), rfill, aln('right','center'), '#,##0')
    # E: sum OH
    sc(ws_raw, data_row, 5,  f'=SUM(E{r1}:E{r8})',     fnt(9,True,C['green_link']), rfill, aln('right','center'), '#,##0.0')
    # F: sum STP
    sc(ws_raw, data_row, 6,  f'=SUM(F{r1}:F{r8})',     fnt(9,True,C['green_link']), rfill, aln('right','center'), '#,##0')
    # G: total income
    sc(ws_raw, data_row, 7,  f'=SUM(G{r1}:G{r8})',     fnt(9,True,C['green_link']), rfill, aln('right','center'), '#,##0')
    # H: order income
    sc(ws_raw, data_row, 8,  f'=SUM(H{r1}:H{r8})',     fnt(9,True,C['green_link']), rfill, aln('right','center'), '#,##0')
    # I: reward income
    sc(ws_raw, data_row, 9,  f'=SUM(I{r1}:I{r8})',     fnt(9,True,C['green_link']), rfill, aln('right','center'), '#,##0')
    # J: avg OH/driver-month = sumOH / sum(driver counts)
    sc(ws_raw, data_row, 10, f'=IFERROR(E{data_row}/SUM(D{r1}:D{r8}),0)', fnt(9,True,C['green_link']), rfill, aln('right','center'), '#,##0.0')
    # K: avg income/driver-month
    sc(ws_raw, data_row, 11, f'=IFERROR(G{data_row}/SUM(D{r1}:D{r8}),0)', fnt(9,True,C['green_link']), rfill, aln('right','center'), '#,##0')
    # L: avg stp/driver-month
    sc(ws_raw, data_row, 12, f'=IFERROR(F{data_row}/SUM(D{r1}:D{r8}),0)', fnt(9,True,C['green_link']), rfill, aln('right','center'), '#,##0.0')
    # M: EPH
    sc(ws_raw, data_row, 13, f'=IFERROR(G{data_row}/E{data_row},0)',  fnt(9,True,C['green_link']), rfill, aln('right','center'), '#,##0')
    # N: PPH
    sc(ws_raw, data_row, 14, f'=IFERROR(F{data_row}/E{data_row},0)',  fnt(9,True,C['green_link']), rfill, aln('right','center'), '0.000')
    # O: reward %
    sc(ws_raw, data_row, 15, f'=IFERROR(I{data_row}/G{data_row},0)', fnt(9,True,C['green_link']), rfill, aln('right','center'), '0.0%')
    # P: avg rating
    sc(ws_raw, data_row, 16, f'=AVERAGE(P{r1}:P{r8})', fnt(9,True,C['green_link']), rfill, aln('right','center'), '0.000')

    data_row += 1

ws_raw.freeze_panes = 'D4'

# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 2 — YoY COMPARISON (formulas linking to Raw Data)
# ═══════════════════════════════════════════════════════════════════════════════
ws_yoy = wb.create_sheet('YoY Comparison')
ws_yoy.sheet_view.showGridLines = False

for c, w in [(1,9),(2,16),(3,16),(4,11),(5,16),(6,16),(7,11),(8,16),(9,16),(10,11),(11,12),(12,12),(13,11)]:
    cw(ws_yoy, c, w)

rh(ws_yoy, 1, 8)
rh(ws_yoy, 2, 34)
ws_yoy.merge_cells('A2:M2')
sc(ws_yoy, 2, 1, 'YoY Comparison — Cùng Tháng 2025 vs 2026 (Jan–Aug only)',
   fnt(13, True, C['white']), fll(C['blue_dark']), aln('center','center'))

rh(ws_yoy, 3, 8)
rh(ws_yoy, 4, 22)
rh(ws_yoy, 5, 28)

# Group headers
groups = [
    ('Tháng', 1, 1),
    ('EPH (VND/giờ)', 2, 4),
    ('Giờ làm TB/Driver/tháng', 5, 7),
    ('Thu nhập TB/Driver/tháng', 8, 10),
    ('PPH (STP/giờ)', 11, 12),
    ('Δ% PPH', 13, 13),
]
for (grp, c1, c2) in groups:
    if c1 == c2:
        ws_yoy.merge_cells(f'{get_column_letter(c1)}4:{get_column_letter(c2)}5')
    else:
        ws_yoy.merge_cells(f'{get_column_letter(c1)}4:{get_column_letter(c2)}4')
    sc(ws_yoy, 4, c1, grp,
       fnt(9, True, C['white']), fll(C['blue_dark']), aln('center','center'))

# Sub-headers row 5
# Sub-headers row 5 — skip cols 1 and 13 (merged with row 4)
sub5 = [(2,'2025',C['blue_soft']), (3,'2026',C['orange_soft']), (4,'Δ%',C['light_bg']),
        (5,'2025',C['blue_soft']), (6,'2026',C['orange_soft']), (7,'Δ%',C['light_bg']),
        (8,'2025',C['blue_soft']), (9,'2026',C['orange_soft']), (10,'Δ%',C['light_bg']),
        (11,'2025',C['blue_soft']), (12,'2026',C['orange_soft'])]
for (ci, h, bg) in sub5:
    sc(ws_yoy, 5, ci, h, fnt(8.5, True, C['blue_dark']),
       fll(bg), aln('center','center'),
       border=border_bottom())

raw = "'Raw Data'"

yoy_r = 6
for i, mn in enumerate(range(1, 9)):  # Jan-Aug only
    r = yoy_r + i
    rh(ws_yoy, r, 20)
    rfill = fll(C['white']) if i % 2 == 0 else fll(C['light_bg'])

    r25 = row_map[('2025', mn)]
    r26 = row_map[('2026', mn)]

    sc(ws_yoy, r, 1, MONTHS[mn-1], fnt(9, True, C['blue_dark']), rfill, aln('center','center'))

    # EPH
    sc(ws_yoy, r, 2, f"={raw}!M{r25}", fnt(9,False,C['green_link']), rfill, aln('right','center'), '#,##0')
    sc(ws_yoy, r, 3, f"={raw}!M{r26}", fnt(9,False,C['green_link']), rfill, aln('right','center'), '#,##0')
    sc(ws_yoy, r, 4, f"=IFERROR((C{r}-B{r})/ABS(B{r}),0)", fnt(9,True,C['black']), rfill, aln('center','center'), '0.0%;[Red](0.0%)')

    # Avg hours/driver
    sc(ws_yoy, r, 5, f"={raw}!J{r25}", fnt(9,False,C['green_link']), rfill, aln('right','center'), '#,##0.0')
    sc(ws_yoy, r, 6, f"={raw}!J{r26}", fnt(9,False,C['green_link']), rfill, aln('right','center'), '#,##0.0')
    sc(ws_yoy, r, 7, f"=IFERROR((F{r}-E{r})/ABS(E{r}),0)", fnt(9,True,C['black']), rfill, aln('center','center'), '0.0%;[Red](0.0%)')

    # Avg income/driver
    sc(ws_yoy, r, 8,  f"={raw}!K{r25}", fnt(9,False,C['green_link']), rfill, aln('right','center'), '#,##0')
    sc(ws_yoy, r, 9,  f"={raw}!K{r26}", fnt(9,False,C['green_link']), rfill, aln('right','center'), '#,##0')
    sc(ws_yoy, r, 10, f"=IFERROR((I{r}-H{r})/ABS(H{r}),0)", fnt(9,True,C['black']), rfill, aln('center','center'), '0.0%;[Red](0.0%)')

    # PPH
    sc(ws_yoy, r, 11, f"={raw}!N{r25}", fnt(9,False,C['green_link']), rfill, aln('right','center'), '0.000')
    sc(ws_yoy, r, 12, f"={raw}!N{r26}", fnt(9,False,C['green_link']), rfill, aln('right','center'), '0.000')
    sc(ws_yoy, r, 13, f"=IFERROR((L{r}-K{r})/ABS(K{r}),0)", fnt(9,True,C['black']), rfill, aln('center','center'), '0.0%;[Red](0.0%)')

# Totals row
tot_r = yoy_r + 8
rh(ws_yoy, tot_r, 24)
tot_fill = fll(C['blue_soft'])

r25_start = row_map[('2025', 1)]
r25_end   = row_map[('2025', 8)]
r26_start = row_map[('2026', 1)]
r26_end   = row_map[('2026', 8)]

sc(ws_yoy, tot_r, 1, 'Jan–Aug\nAvg', fnt(9, True, C['blue_dark']), tot_fill, aln('center','center',True))

# EPH weighted avg
sc(ws_yoy, tot_r, 2,
   f"=IFERROR(SUMPRODUCT({raw}!G{r25_start}:G{r25_end})/SUMPRODUCT({raw}!E{r25_start}:E{r25_end}),0)",
   fnt(9,True,C['green_link']), tot_fill, aln('right','center'), '#,##0')
sc(ws_yoy, tot_r, 3,
   f"=IFERROR(SUMPRODUCT({raw}!G{r26_start}:G{r26_end})/SUMPRODUCT({raw}!E{r26_start}:E{r26_end}),0)",
   fnt(9,True,C['green_link']), tot_fill, aln('right','center'), '#,##0')
sc(ws_yoy, tot_r, 4, f"=IFERROR((C{tot_r}-B{tot_r})/ABS(B{tot_r}),0)", fnt(9,True,C['black']), tot_fill, aln('center','center'), '0.0%;[Red](0.0%)')

# Avg OH per driver-month
sc(ws_yoy, tot_r, 5,
   f"=IFERROR(SUMPRODUCT({raw}!E{r25_start}:E{r25_end})/SUMPRODUCT({raw}!D{r25_start}:D{r25_end}),0)",
   fnt(9,True,C['green_link']), tot_fill, aln('right','center'), '#,##0.0')
sc(ws_yoy, tot_r, 6,
   f"=IFERROR(SUMPRODUCT({raw}!E{r26_start}:E{r26_end})/SUMPRODUCT({raw}!D{r26_start}:D{r26_end}),0)",
   fnt(9,True,C['green_link']), tot_fill, aln('right','center'), '#,##0.0')
sc(ws_yoy, tot_r, 7, f"=IFERROR((F{tot_r}-E{tot_r})/ABS(E{tot_r}),0)", fnt(9,True,C['black']), tot_fill, aln('center','center'), '0.0%;[Red](0.0%)')

# Avg income per driver-month
sc(ws_yoy, tot_r, 8,
   f"=IFERROR(SUMPRODUCT({raw}!G{r25_start}:G{r25_end})/SUMPRODUCT({raw}!D{r25_start}:D{r25_end}),0)",
   fnt(9,True,C['green_link']), tot_fill, aln('right','center'), '#,##0')
sc(ws_yoy, tot_r, 9,
   f"=IFERROR(SUMPRODUCT({raw}!G{r26_start}:G{r26_end})/SUMPRODUCT({raw}!D{r26_start}:D{r26_end}),0)",
   fnt(9,True,C['green_link']), tot_fill, aln('right','center'), '#,##0')
sc(ws_yoy, tot_r, 10, f"=IFERROR((I{tot_r}-H{tot_r})/ABS(H{tot_r}),0)", fnt(9,True,C['black']), tot_fill, aln('center','center'), '0.0%;[Red](0.0%)')

# PPH weighted
sc(ws_yoy, tot_r, 11,
   f"=IFERROR(SUMPRODUCT({raw}!F{r25_start}:F{r25_end})/SUMPRODUCT({raw}!E{r25_start}:E{r25_end}),0)",
   fnt(9,True,C['green_link']), tot_fill, aln('right','center'), '0.000')
sc(ws_yoy, tot_r, 12,
   f"=IFERROR(SUMPRODUCT({raw}!F{r26_start}:F{r26_end})/SUMPRODUCT({raw}!E{r26_start}:E{r26_end}),0)",
   fnt(9,True,C['green_link']), tot_fill, aln('right','center'), '0.000')
sc(ws_yoy, tot_r, 13, f"=IFERROR((L{tot_r}-K{tot_r})/ABS(K{tot_r}),0)", fnt(9,True,C['black']), tot_fill, aln('center','center'), '0.0%;[Red](0.0%)')

# Conditional formatting Δ% columns
for delta_col in ['D','G','J','M']:
    ws_yoy.conditional_formatting.add(
        f'{delta_col}{yoy_r}:{delta_col}{tot_r}',
        ColorScaleRule(
            start_type='min',  start_color='FFCCCC',
            mid_type='num', mid_value=0, mid_color='FFFFFF',
            end_type='max',    end_color='C6EFCE'
        )
    )

note_r = tot_r + 2
ws_yoy.merge_cells(f'A{note_r}:M{note_r}')
sc(ws_yoy, note_r, 1,
   '* Sep 2026 partial (18/30 ngày) — bị loại khỏi bảng này để không bias khi so với Sep 2025 full tháng.',
   fnt(8, italic=True, color=C['gray']), fll(C['light_bg']), aln('left','center'))

ws_yoy.freeze_panes = 'B6'

# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 3 — SUMMARY KPIs
# ═══════════════════════════════════════════════════════════════════════════════
ws_sum = wb.create_sheet('Summary KPIs')
ws_sum.sheet_view.showGridLines = False

for c, w in [(1,30),(2,18),(3,18),(4,14),(5,14),(6,50)]:
    cw(ws_sum, c, w)

rh(ws_sum, 1, 8)
rh(ws_sum, 2, 36)
ws_sum.merge_cells('A2:F2')
sc(ws_sum, 2, 1, 'Summary KPIs — Retained Driver SGN | Jan–Aug YoY (2025 vs 2026)',
   fnt(14, True, C['white']), fll(C['blue_dark']), aln('center','center'))

rh(ws_sum, 3, 8)
rh(ws_sum, 4, 28)

# Column headers
for ci, (h, bg) in enumerate([
    ('KPI', C['blue_dark']),
    ('2025 (Jan–Aug)', C['blue_dark']),
    ('2026 (Jan–Aug)', C['blue_dark']),
    ('Δ (abs)', C['blue_dark']),
    ('Δ %', C['blue_dark']),
    ('Nhận định', C['blue_dark']),
], start=1):
    sc(ws_sum, 4, ci, h, fnt(9,True,C['white']), fll(C['blue_dark']),
       aln('center','center'), border=border_bottom())

yoy = "'YoY Comparison'"

kpis = [
    # (label, val25_formula, val26_formula, abs_fmt, pct_fmt, insight)
    ('EPH — VND/giờ (weighted avg)',
     f"={yoy}!B{tot_r}", f"={yoy}!C{tot_r}",
     '#,##0', '↑ Tài xế kiếm tiền hiệu quả hơn mỗi giờ làm việc'),
    ('PPH — Stops/giờ (weighted avg)',
     f"={yoy}!K{tot_r}", f"={yoy}!L{tot_r}",
     '0.000', '↑ Năng suất giao hàng thực chất tăng, không phải do incentive'),
    ('Giờ làm TB/driver/tháng (driver-weighted)',
     f"={yoy}!E{tot_r}", f"={yoy}!F{tot_r}",
     '#,##0.0', '↓ Driver cần ít giờ hơn → flexibility & work-life balance tốt hơn'),
    ('Thu nhập TB/driver/tháng (VND)',
     f"={yoy}!H{tot_r}", f"={yoy}!I{tot_r}",
     '#,##0', '→ Thu nhập ổn định, driver không bị thiệt khi giảm giờ'),
    ('Total supply hours (Jan–Aug fleet)',
     f"=SUMPRODUCT('Raw Data'!E{r25_start}:E{r25_end})",
     f"=SUMPRODUCT('Raw Data'!E{r26_start}:E{r26_end})",
     '#,##0', '↑ Fleet lớn hơn bù offset cho hour/driver giảm → supply vẫn tăng'),
    ('Tổng STP hoàn thành (Jan–Aug)',
     f"=SUMPRODUCT('Raw Data'!F{r25_start}:F{r25_end})",
     f"=SUMPRODUCT('Raw Data'!F{r26_start}:F{r26_end})",
     '#,##0', '→ Volume đơn hàng tương đương/tăng nhẹ'),
    ('Tổng thu nhập fleet (VND, Jan–Aug)',
     f"=SUMPRODUCT('Raw Data'!G{r25_start}:G{r25_end})",
     f"=SUMPRODUCT('Raw Data'!G{r26_start}:G{r26_end})",
     '#,##0', '↑ Tổng payout tăng do fleet lớn hơn'),
]

kpi_row = 5
for label, f25, f26, afmt, insight in kpis:
    rh(ws_sum, kpi_row, 22)
    rfill = fll(C['white']) if kpi_row % 2 else fll(C['light_bg'])

    sc(ws_sum, kpi_row, 1, label, fnt(9,True,C['blue_dark']), rfill, aln('left','center'))
    sc(ws_sum, kpi_row, 2, f25,   fnt(10,True,C['blue_in']),  rfill, aln('right','center'), afmt)
    sc(ws_sum, kpi_row, 3, f26,   fnt(10,True,C['orange']),   rfill, aln('right','center'), afmt)
    sc(ws_sum, kpi_row, 4, f"=C{kpi_row}-B{kpi_row}",
       fnt(9,False,C['black']), rfill, aln('right','center'), afmt)
    sc(ws_sum, kpi_row, 5, f"=IFERROR((C{kpi_row}-B{kpi_row})/ABS(B{kpi_row}),0)",
       fnt(9,True,C['black']), rfill, aln('center','center'), '0.0%;[Red](0.0%)')
    sc(ws_sum, kpi_row, 6, insight, fnt(8.5,False,C['gray'],True), rfill, aln('left','center'))
    kpi_row += 1

# Conditional color for Δ%
ws_sum.conditional_formatting.add(
    f'E5:E{kpi_row-1}',
    ColorScaleRule(
        start_type='min',  start_color='FFCCCC',
        mid_type='num', mid_value=0, mid_color='FFFFFF',
        end_type='max',    end_color='C6EFCE'
    )
)

# ── Income target block ─────────────────────────────────────────────────────
rh(ws_sum, kpi_row, 10)
kpi_row += 1

rh(ws_sum, kpi_row, 24)
ws_sum.merge_cells(f'A{kpi_row}:F{kpi_row}')
sc(ws_sum, kpi_row, 1,
   'Efficiency Hypothesis — Giờ cần làm để đạt Target Income 13,000,000 VND/tháng',
   fnt(10, True, C['white']), fll(C['orange']), aln('left','center'))
kpi_row += 1

rh(ws_sum, kpi_row, 20)
sc(ws_sum, kpi_row, 1, 'Target income/tháng (VND) — input', fnt(9), fll(C['yellow']), aln('left','center'))
target_cell = f'B{kpi_row}'
sc(ws_sum, kpi_row, 2, 13000000, fnt(10,True,C['blue_in']), fll(C['yellow']),
   aln('right','center'), '#,##0')
ws_sum.merge_cells(f'C{kpi_row}:F{kpi_row}')
sc(ws_sum, kpi_row, 3,
   '≈ 500,000 VND/ngày × 26 ngày | Ô màu vàng = input, thay đổi số này để recalc tự động',
   fnt(8.5,False,C['gray'],True), fll(C['yellow']), aln('left','center'))
kpi_row += 1

rh(ws_sum, kpi_row, 20)
sc(ws_sum, kpi_row, 1, 'Giờ cần làm — 2025', fnt(9), fll(C['blue_soft']), aln('left','center'))
sc(ws_sum, kpi_row, 2, f"=IFERROR({target_cell}/B5,0)", fnt(10,True,C['green_link']),
   fll(C['blue_soft']), aln('right','center'), '#,##0.0')
sc(ws_sum, kpi_row, 3, f"=IFERROR({target_cell}/C5,0)", fnt(10,True,C['orange']),
   fll(C['blue_soft']), aln('right','center'), '#,##0.0')
sc(ws_sum, kpi_row, 4, f"=C{kpi_row}-B{kpi_row}", fnt(9), fll(C['blue_soft']),
   aln('right','center'), '#,##0.0')
sc(ws_sum, kpi_row, 5, f"=IFERROR((C{kpi_row}-B{kpi_row})/ABS(B{kpi_row}),0)",
   fnt(9,True), fll(C['blue_soft']), aln('center','center'), '0.0%;[Red](0.0%)')
ws_sum.merge_cells(f'F{kpi_row}:F{kpi_row}')
sc(ws_sum, kpi_row, 6,
   f'Savings: 2026 tiết kiệm ~42–43 giờ/tháng (~13.5%) để đạt cùng target income',
   fnt(8.5,False,C['gray'],True), fll(C['blue_soft']), aln('left','center'))

# ── Color legend ─────────────────────────────────────────────────────────────
kpi_row += 2
rh(ws_sum, kpi_row, 16)
ws_sum.merge_cells(f'A{kpi_row}:F{kpi_row}')
sc(ws_sum, kpi_row, 1,
   'Quy ước màu:  Xanh đậm = hardcode input  |  Cam = 2026  |  Xanh lá = cross-sheet formula  |  Nền vàng = input thay đổi được  |  Nền đỏ nhạt = giảm',
   fnt(8,False,C['gray'],True), fll(C['light_bg']), aln('left','center'))

ws_sum.freeze_panes = 'B5'

# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 4 — OBSERVATIONS
# ═══════════════════════════════════════════════════════════════════════════════
ws_obs = wb.create_sheet('Observations')
ws_obs.sheet_view.showGridLines = False
cw(ws_obs, 1, 32)
cw(ws_obs, 2, 90)

rh(ws_obs, 1, 8)
rh(ws_obs, 2, 34)
ws_obs.merge_cells('A2:B2')
sc(ws_obs, 2, 1, 'Nhận Định Phân Tích & Điểm Cần Theo Dõi',
   fnt(13,True,C['white']), fll(C['blue_dark']), aln('center','center'))

obs_content = [
    # (type, title, body)
    ('section', '✅ HYPOTHESIS CONFIRMED', 'blue_dark'),
    ('item', 'EPH tăng +15.6% (Jan–Aug avg)',
     'Retained driver earn 47,380 VND/giờ năm 2026 vs 40,992 VND/giờ năm 2025. '
     'Đây là EPH weighted (income/hours), phản ánh thu nhập thực sự tài xế nhận được trên mỗi giờ làm việc. '
     'Kết hợp với PPH +13.3% → tăng hiệu quả là thực chất (nhiều đơn hơn/giờ), không phải do reward giả tạo.'),
    ('item', 'Giờ làm giảm −11.6%/driver',
     'Driver cần trung bình 93.0 giờ/tháng (2026) vs 105.2 giờ (2025). '
     'Thu nhập avg +2.2% (4,407k vs 4,312k) → driver không bị thiệt. '
     'Họ chủ động giảm giờ vì cần ít effort hơn để đạt cùng mức thu nhập → flexibility tăng.'),
    ('item', 'Target 13M VND/tháng: tiết kiệm 42.8 giờ (−13.5%)',
     '2025: cần ~317h/tháng để đạt 13M VND. '
     '2026: chỉ cần ~274h/tháng — tương đương tiết kiệm 1.5 giờ/ngày. '
     'Driver có thể làm part-time nhiều hơn, hoặc giữ target thu nhập với ít effort hơn → retention tự nhiên tăng.'),
    ('item', 'Total supply hours fleet tăng +9.0%',
     '6.67M → 7.27M giờ (Jan–Aug). Supply không giảm vì fleet lớn hơn: unique driver count +40% (11,231 → 15,731). '
     'Hiệu ứng composition: per-driver hours giảm nhưng số lượng driver tăng mạnh bù lại. '
     'Retained cohort đang ngày càng lớn hơn qua từng năm.'),

    ('section', '⚠️ ĐIỂM CẦN THEO DÕI', 'orange'),
    ('item', 'Jan 2026: EPH thấp hơn Jan 2025 (−8.6%)',
     'Tháng duy nhất EPH 2026 < 2025 trong Jan–Aug: 46,403 vs 50,760 VND/hr. '
     'Cần check: (1) Incentive structure đầu năm 2026 có thay đổi không? '
     '(2) Tỷ lệ NIM (driver mới vào sau Tết) cao → EPH thấp là bình thường. '
     '(3) Volume Tết 2026 vs 2025 — Tết 2026 sớm hơn, có thể Jan 2025 benefited from pre-Tết surge. '
     'Action: kiểm tra incentive_log Jan 2026 và breakdown NIM vs retained trong tháng này.'),
    ('item', 'EPH hội tụ về 2025 từ Q3 2026',
     'Khoảng cách YoY đang thu hẹp: Jun +14.3% → Jul +11.0% → Aug +7.5%. '
     'Nếu trend này tiếp tục, Q4 2026 EPH có thể quay về ngang 2025 → driver phải tăng giờ trở lại. '
     'Action: Monitor Sep–Oct 2026 weekly. Set alert nếu EPH Δ% < +5%.'),
    ('item', 'Giờ làm/driver hội tụ trong Q3',
     'Hours reduction từ Feb–May rất mạnh (Feb: −22.7%, Mar: −16.8%) nhưng từ Jun về sau giảm ít hơn '
     '(Jun: −4.6%, Jul: −4.4%, Aug: −3.2%). '
     'Possible cause: effect của restructure incentive đang tắt dần sau 2 quý. '
     'Cần confirm bằng data Q4.'),
    ('item', 'Sep 2026 partial month (18/30 ngày)',
     'Sep 2026 chỉ có data đến 2026-09-18. EPH Sep = 53,600 (full extrapolation chưa chắc). '
     'Không đưa vào YoY table. Khi tháng kết thúc (Sep 30), cần refresh file với data đầy đủ.'),

    ('section', '📋 PHƯƠNG PHÁP LUẬN', 'blue_dark'),
    ('item', 'Retained cohort definition',
     'Retained driver = supplier_id có stp_complete > 0 trong ÍT NHẤT 1 ngày của năm 2025 '
     'VÀ ÍT NHẤT 1 ngày của năm 2026. '
     'Metric: JOIN trên supplier_id giữa 2 năm, không yêu cầu active liên tục.'),
    ('item', 'Vehicle & supplier filter',
     'MOTORBIKE + EV-BIKE. Loại trừ: ahamove_ka_lazada, VNM-WH-DELIVERY, VNM-WH-VENDOR, SALESFORCE tags. '
     'City: SGN only (city_id = SGN từ raw_supplier_profile). '
     'partitioned_create_time >= 2010-01-01 để loại account test.'),
    ('item', 'EPH = Total Income / Online Hours',
     'Total income = order_income + reward_income_pit1_5 (đã net thuế TNCN 1.5%). '
     'Online hours từ bảng ops_suppliers_online_hours (daily aggregates). '
     'EPH trong file này là weighted average (sum income / sum hours), không phải trung bình số học.'),
    ('item', 'Nguồn data',
     'ahamove_archive_ops.fct_supplier_performance + ahamove_archive.ops_suppliers_online_hours. '
     'Query ngày: 2026-09-18. 191,338 driver-month records. 15,825 unique suppliers trong cohort.'),
]

obs_r = 4
for item in obs_content:
    if item[0] == 'section':
        obs_r += 1 if obs_r > 4 else 0
        rh(ws_obs, obs_r, 24)
        ws_obs.merge_cells(f'A{obs_r}:B{obs_r}')
        bg = C['blue_dark'] if item[2] == 'blue_dark' else C['orange']
        sc(ws_obs, obs_r, 1, item[1],
           fnt(10,True,C['white']), fll(bg), aln('left','center'))
        obs_r += 1
    else:
        _, title, body = item
        body_lines = len(body) // 85 + 1
        rh(ws_obs, obs_r, max(18, body_lines * 14))
        sc(ws_obs, obs_r, 1, title,
           fnt(9,True,C['blue_dark']), fll(C['light_bg']), aln('left','top'))
        sc(ws_obs, obs_r, 2, body,
           fnt(9,False,C['black']), fll(C['white']),
           aln('left','top',True),
           border=border_bottom(C['border'],'thin'))
        obs_r += 1

obs_r += 1
ws_obs.merge_cells(f'A{obs_r}:B{obs_r}')
sc(ws_obs, obs_r, 1,
   f'File: 2026-09-retained-driver-yoy.xlsx | Built: 2026-09-18 | Data: Metabase BigQuery',
   fnt(8,False,C['gray'],True), fll(C['light_bg']), aln('left','center'))

# ── Tab colors ────────────────────────────────────────────────────────────────
ws_raw.sheet_properties.tabColor  = '3D5A80'
ws_yoy.sheet_properties.tabColor  = C['orange']
ws_sum.sheet_properties.tabColor  = C['blue_dark']
ws_obs.sheet_properties.tabColor  = C['green']

wb.save(OUTPUT)
print(f'Saved → {OUTPUT}')
print(f'Sheets: {[s.title for s in wb.worksheets]}')
print(f'row_map sample: 2025-Jan={row_map[("2025",1)]}, 2026-Jan={row_map[("2026",1)]}')
