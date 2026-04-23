"""
Fix 2 bugs:
1. Period stored as datetime objects (not strings) so MAX/SUMIF work
2. Replace MAXIFS with LARGE+COUNTIF (compatible with all Excel versions)
"""
import pandas as pd, warnings, os, datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import ColorScaleRule, CellIsRule
warnings.filterwarnings('ignore')

SRC = '/Users/ts-1148/Downloads/[S&P] Supply data report - Weekly.xlsx'
OUT = '/Users/ts-1148/Desktop/Cowork/output/Ahamove/04. OPS_METRICS/weekly-ops-dashboard.xlsx'

BLUE='0E4174'; ORANGE='FF7F32'; GREEN='10B981'; RED='EF4444'
WHITE='FFFFFF'; BL='E8EFF8'; GL='E6FAF4'; RL='FEE9E9'
GRAY='94A3B8'; DARK='1E293B'; BDR='E2E8F0'; YELLOW='FFF9C4'; BG='F8F9FA'

def mf(h): return PatternFill('solid', fgColor=h)
def mb(c=BDR): s=Side(border_style='thin',color=c); return Border(left=s,right=s,top=s,bottom=s)
def fn(bold=False,color=DARK,size=10,name='Arial',italic=False):
    return Font(bold=bold,color=color,size=size,name=name,italic=italic)
def al(h='center',v='center',wrap=False): return Alignment(horizontal=h,vertical=v,wrap_text=wrap)

# ── LOAD DATA ─────────────────────────────────────────────────────────────────
raw = pd.ExcelFile(SRC).parse('data import', header=None)

def to_num(df, cols):
    for c in cols: df[c] = pd.to_numeric(df[c], errors='coerce')
    return df

def to_pydate(val):
    """Convert pandas Timestamp to Python date for openpyxl (stores as Excel serial number)."""
    if pd.isna(val): return None
    return pd.Timestamp(val).date()

# SVC DATA
svc = raw.iloc[2:,0:8].copy()
svc.columns = ['period','region','service_type','requested','accept','completed','ar','fr']
svc = svc.dropna(subset=['period','region'])
svc['period'] = pd.to_datetime(svc['period'])
svc = to_num(svc, ['requested','accept','completed','ar','fr'])
svc = svc[svc['region'].isin(['SGN','HAN','EXP','NW'])].sort_values(['period','region','service_type'],ascending=[False,True,True])

# DFD DATA
dfd = raw.iloc[2:,[0,1,9,10,11,12,17]].copy()
dfd.columns = ['period','region','total_dfd','referral','digital_ads','others','organic']
dfd = dfd.dropna(subset=['total_dfd'])
dfd['period'] = pd.to_datetime(dfd['period'])
dfd = to_num(dfd, ['total_dfd','referral','digital_ads','others','organic'])
dfd = dfd.sort_values(['period','region'], ascending=[False,True])

# DRIVER DATA
ad_meta = raw.iloc[2:,82:90].copy()
ad_meta.columns = ['period','ranking_driver','busy_hours','order_income','city_id','gdr_driver','bad_rating_order','total_driver']
ad_drv = raw.iloc[2:,67:82].copy()
ad_drv.columns = ['cancel_order','driver_segment','rating_order','total_stp','lcd_driver','hard_driver',
                   'online_hours','accept_order','cancel_poc','accept_noti','rating_star','reward_income',
                   'lcd_driver_kpi','total_noti','total_aa_driver']
adr = pd.concat([ad_meta[['period','city_id','total_driver','gdr_driver']],
                  ad_drv[['driver_segment','online_hours','accept_order','reward_income','total_aa_driver']]], axis=1)
adr = adr.dropna(subset=['period'])
adr['period'] = pd.to_datetime(adr['period'])
adr = to_num(adr, ['total_driver','gdr_driver','online_hours','accept_order','reward_income','total_aa_driver'])
adr = adr.sort_values(['period','city_id','driver_segment'], ascending=[False,True,True])

# CANCEL DATA
can = raw.iloc[2:,91:98].copy()
can.columns = ['period','type_','reason_type','service_type','city_id','segment','total_cancel']
can = can.dropna(subset=['period','type_'])
can['period'] = pd.to_datetime(can['period'])
can = to_num(can, ['total_cancel'])
can = can.sort_values(['period','total_cancel'], ascending=[False,False])

print(f"SVC:{len(svc)} DFD:{len(dfd)} DRV:{len(adr)} CAN:{len(can)}")

# ── WORKBOOK ──────────────────────────────────────────────────────────────────
wb = Workbook()

# ─────────────────────────────────────────────────────────────────────────────
# DATA SHEETS  (period stored as datetime.date → Excel serial number)
# ─────────────────────────────────────────────────────────────────────────────
def make_data_sheet(sheet, title, headers, col_widths, fmt_map, rows, note_text):
    sheet.sheet_view.showGridLines = False
    for col,w in zip('ABCDEFGHIJ', col_widths): sheet.column_dimensions[col].width = w
    sheet.row_dimensions[1].height = 8
    sheet.row_dimensions[2].height = 30
    n = len(headers)+1
    sheet.merge_cells(f'B2:{chr(65+n)}2')
    for c in range(2, n+2): sheet.cell(row=2,column=c).fill = mf(BLUE)
    sheet['B2'] = title
    sheet['B2'].font = fn(bold=True,color=WHITE,size=11)
    sheet['B2'].alignment = al('left')
    sheet.row_dimensions[3].height = 22
    for ci,h in enumerate(headers,2):
        c = sheet.cell(row=3,column=ci,value=h)
        c.font = fn(bold=True,color=WHITE,size=9); c.fill = mf(BLUE)
        c.alignment = al(); c.border = mb(BLUE)
    for i, row_vals in enumerate(rows):
        row = 4+i; sheet.row_dimensions[row].height = 16
        fc = BL if i%2==0 else WHITE
        for ci, (val, fmt) in enumerate(zip(row_vals, [fmt_map[j] for j in range(2,len(row_vals)+2)]), 2):
            c = sheet.cell(row=row, column=ci, value=val)
            c.font = fn(size=9); c.fill = mf(fc)
            c.number_format = fmt; c.alignment = al('left' if ci==3 else 'center'); c.border = mb()
    sheet.auto_filter.ref = f'B3:{chr(65+n)}{3+len(rows)}'
    sheet.freeze_panes = 'B4'
    nr = 4+len(rows)+2
    sheet.merge_cells(f'B{nr}:{chr(65+n)}{nr}')
    sheet.cell(row=nr,column=2,value=note_text).font = fn(italic=True,color=GRAY,size=8)
    sheet.cell(row=nr,column=2).alignment = al('left')

# SVC DATA
ws_svc = wb.active; ws_svc.title = 'SVC DATA'
ws_svc.sheet_properties.tabColor = ORANGE
svc_rows = []
for _, r in svc.iterrows():
    svc_rows.append([
        to_pydate(r['period']), str(r['region']), str(r['service_type']),
        int(r['requested']) if pd.notna(r['requested']) else 0,
        int(r['accept']) if pd.notna(r['accept']) else 0,
        int(r['completed']) if pd.notna(r['completed']) else 0,
        float(r['ar']) if pd.notna(r['ar']) else 0,
        float(r['fr']) if pd.notna(r['fr']) else 0,
    ])
make_data_sheet(ws_svc,
    'SVC DATA — Paste new weekly data here (replace from row 4 down)',
    ['Period','Region','Service','Requested','Accept','Completed','AR %','FR %'],
    [2,14,10,12,14,14,14,10,10],
    {2:'DD/MM/YYYY',3:'@',4:'@',5:'#,##0',6:'#,##0',7:'#,##0',8:'0.0%',9:'0.0%'},
    svc_rows,
    'UPDATE: Xóa từ row 4 xuống → Paste data mới. Period = date value (format DD/MM/YYYY). AR/FR = decimal 0.875.')

# DFD DATA
ws_dfd = wb.create_sheet('DFD DATA')
ws_dfd.sheet_properties.tabColor = GREEN
dfd_rows = []
for _, r in dfd.iterrows():
    dfd_rows.append([
        to_pydate(r['period']), str(r['region']),
        int(r['total_dfd']) if pd.notna(r['total_dfd']) else 0,
        int(r['organic']) if pd.notna(r['organic']) else 0,
        int(r['referral']) if pd.notna(r['referral']) else 0,
        int(r['digital_ads']) if pd.notna(r['digital_ads']) else 0,
    ])
make_data_sheet(ws_dfd,
    'DFD DATA — Paste new weekly DFD data here (replace from row 4 down)',
    ['Period','Region','Total DFD','Organic','Referral','Digital Ads'],
    [2,14,10,12,12,12,14],
    {2:'DD/MM/YYYY',3:'@',4:'#,##0',5:'#,##0',6:'#,##0',7:'#,##0'},
    dfd_rows,
    'UPDATE: Xóa từ row 4 xuống → Paste data mới. Period = date value.')

# DRIVER DATA
ws_drv = wb.create_sheet('DRIVER DATA')
ws_drv.sheet_properties.tabColor = '1D4ED8'
drv_rows = []
for _, r in adr.iterrows():
    drv_rows.append([
        to_pydate(r['period']),
        str(r['city_id']) if pd.notna(r['city_id']) else '',
        str(r['driver_segment']) if pd.notna(r['driver_segment']) else '',
        int(r['total_driver']) if pd.notna(r['total_driver']) else 0,
        int(r['gdr_driver']) if pd.notna(r['gdr_driver']) else 0,
        round(float(r['online_hours']),1) if pd.notna(r['online_hours']) else 0,
        int(r['accept_order']) if pd.notna(r['accept_order']) else 0,
        int(r['reward_income']) if pd.notna(r['reward_income']) else 0,
        int(r['total_aa_driver']) if pd.notna(r['total_aa_driver']) else 0,
    ])
make_data_sheet(ws_drv,
    'DRIVER DATA — Paste new weekly driver data here (replace from row 4 down)',
    ['Period','City','Segment','Total Driver','GDR Driver','Online Hrs','Accept Orders','Reward (VND)','AA Driver'],
    [2,14,10,12,12,12,14,14,16,12],
    {2:'DD/MM/YYYY',3:'@',4:'@',5:'#,##0',6:'#,##0',7:'#,##0.0',8:'#,##0',9:'#,##0',10:'#,##0'},
    drv_rows,
    'UPDATE: Xóa từ row 4 xuống → Paste data mới. Period = date value.')

# CANCEL DATA
ws_can = wb.create_sheet('CANCEL DATA')
ws_can.sheet_properties.tabColor = RED
can_rows = []
for i, (_, r) in enumerate(can.iterrows()):
    if i >= 3000: break
    can_rows.append([
        to_pydate(r['period']),
        str(r['type_'])[:60] if pd.notna(r['type_']) else '',
        str(r['reason_type']) if pd.notna(r['reason_type']) else '',
        str(r['service_type']) if pd.notna(r['service_type']) else '',
        str(r['city_id']) if pd.notna(r['city_id']) else '',
        str(r['segment']) if pd.notna(r['segment']) else '',
        int(r['total_cancel']) if pd.notna(r['total_cancel']) else 0,
    ])
make_data_sheet(ws_can,
    'CANCEL DATA — Paste new weekly cancel data here (replace from row 4 down)',
    ['Period','Cancel Reason','Type','Service','City','Segment','Total Cancel'],
    [2,14,40,12,10,10,12,12],
    {2:'DD/MM/YYYY',3:'@',4:'@',5:'@',6:'@',7:'@',8:'#,##0'},
    can_rows,
    'UPDATE: Xóa từ row 4 xuống → Paste data mới. Period = date value. C = Cancel Reason text.')

# ─────────────────────────────────────────────────────────────────────────────
# WEEKLY DASHBOARD  (all formula-driven)
# ─────────────────────────────────────────────────────────────────────────────
ws = wb.create_sheet('WEEKLY DASHBOARD', 0)
ws.sheet_view.showGridLines = False
ws.sheet_properties.tabColor = BLUE

for col,w in zip('ABCDEFGHIJKLMNOPQ',[2,16,14,14,14,2,14,14,14,14,2,14,14,14,14,2,2]):
    ws.column_dimensions[col].width = w

# ── PARAMS ROWS (hidden, rows 1-4) ───────────────────────────────────────────
# Row 2 B:G = 6 latest SVC weeks using LARGE+COUNTIF (works all Excel versions)
# Row 2 H:M = 6 latest DFD weeks
# Row 3 = intermediate totals for KPI delta sub-texts
# Row 4 = latest periods (B=DFD, C=DRIVER, D=CANCEL)

# SVC week chain: W1=latest, W2=2nd latest, ...
# W2 = LARGE(array, count_of_W1 + 1)
# W3 = LARGE(array, count_of_W1 + count_of_W2 + 1)  etc.
ws['B2'] = "=MAX('SVC DATA'!$B:$B)"
ws['B2'].number_format = 'DD/MM/YYYY'
ws['C2'] = "=LARGE('SVC DATA'!$B:$B,COUNTIF('SVC DATA'!$B:$B,$B$2)+1)"
ws['C2'].number_format = 'DD/MM/YYYY'
ws['D2'] = "=LARGE('SVC DATA'!$B:$B,COUNTIF('SVC DATA'!$B:$B,$B$2)+COUNTIF('SVC DATA'!$B:$B,$C$2)+1)"
ws['D2'].number_format = 'DD/MM/YYYY'
ws['E2'] = "=LARGE('SVC DATA'!$B:$B,COUNTIF('SVC DATA'!$B:$B,$B$2)+COUNTIF('SVC DATA'!$B:$B,$C$2)+COUNTIF('SVC DATA'!$B:$B,$D$2)+1)"
ws['E2'].number_format = 'DD/MM/YYYY'
ws['F2'] = "=LARGE('SVC DATA'!$B:$B,COUNTIF('SVC DATA'!$B:$B,$B$2)+COUNTIF('SVC DATA'!$B:$B,$C$2)+COUNTIF('SVC DATA'!$B:$B,$D$2)+COUNTIF('SVC DATA'!$B:$B,$E$2)+1)"
ws['F2'].number_format = 'DD/MM/YYYY'
ws['G2'] = "=LARGE('SVC DATA'!$B:$B,COUNTIF('SVC DATA'!$B:$B,$B$2)+COUNTIF('SVC DATA'!$B:$B,$C$2)+COUNTIF('SVC DATA'!$B:$B,$D$2)+COUNTIF('SVC DATA'!$B:$B,$E$2)+COUNTIF('SVC DATA'!$B:$B,$F$2)+1)"
ws['G2'].number_format = 'DD/MM/YYYY'

# DFD week chain (H:M)
ws['H2'] = "=MAX('DFD DATA'!$B:$B)"
ws['H2'].number_format = 'DD/MM/YYYY'
ws['I2'] = "=LARGE('DFD DATA'!$B:$B,COUNTIF('DFD DATA'!$B:$B,$H$2)+1)"
ws['I2'].number_format = 'DD/MM/YYYY'
ws['J2'] = "=LARGE('DFD DATA'!$B:$B,COUNTIF('DFD DATA'!$B:$B,$H$2)+COUNTIF('DFD DATA'!$B:$B,$I$2)+1)"
ws['J2'].number_format = 'DD/MM/YYYY'
ws['K2'] = "=LARGE('DFD DATA'!$B:$B,COUNTIF('DFD DATA'!$B:$B,$H$2)+COUNTIF('DFD DATA'!$B:$B,$I$2)+COUNTIF('DFD DATA'!$B:$B,$J$2)+1)"
ws['K2'].number_format = 'DD/MM/YYYY'
ws['L2'] = "=LARGE('DFD DATA'!$B:$B,COUNTIF('DFD DATA'!$B:$B,$H$2)+COUNTIF('DFD DATA'!$B:$B,$I$2)+COUNTIF('DFD DATA'!$B:$B,$J$2)+COUNTIF('DFD DATA'!$B:$B,$K$2)+1)"
ws['L2'].number_format = 'DD/MM/YYYY'
ws['M2'] = "=LARGE('DFD DATA'!$B:$B,COUNTIF('DFD DATA'!$B:$B,$H$2)+COUNTIF('DFD DATA'!$B:$B,$I$2)+COUNTIF('DFD DATA'!$B:$B,$J$2)+COUNTIF('DFD DATA'!$B:$B,$K$2)+COUNTIF('DFD DATA'!$B:$B,$L$2)+1)"
ws['M2'].number_format = 'DD/MM/YYYY'

# Row 3: pre-computed KPI values for W1 and W2 (used in delta sub-texts)
ws['B3'] = "=SUMIF('SVC DATA'!$B:$B,$B$2,'SVC DATA'!$E:$E)"   # W1 Requested
ws['C3'] = "=SUMIF('SVC DATA'!$B:$B,$C$2,'SVC DATA'!$E:$E)"   # W2 Requested
ws['D3'] = "=IFERROR(SUMIF('SVC DATA'!$B:$B,$B$2,'SVC DATA'!$F:$F)/B3,0)"  # W1 AR
ws['E3'] = "=IFERROR(SUMIF('SVC DATA'!$B:$B,$C$2,'SVC DATA'!$F:$F)/C3,0)"  # W2 AR
ws['F3'] = "=IFERROR(SUMIF('SVC DATA'!$B:$B,$B$2,'SVC DATA'!$G:$G)/SUMIF('SVC DATA'!$B:$B,$B$2,'SVC DATA'!$F:$F),0)"  # W1 FR
ws['G3'] = "=IFERROR(SUMIF('SVC DATA'!$B:$B,$C$2,'SVC DATA'!$G:$G)/SUMIF('SVC DATA'!$B:$B,$C$2,'SVC DATA'!$F:$F),0)"  # W2 FR
ws['H3'] = "=SUMIF('SVC DATA'!$B:$B,$B$2,'SVC DATA'!$G:$G)"   # W1 Completed
ws['I3'] = "=SUMIF('SVC DATA'!$B:$B,$C$2,'SVC DATA'!$G:$G)"   # W2 Completed
ws['J3'] = "=SUMIF('DFD DATA'!$B:$B,$H$2,'DFD DATA'!$D:$D)"   # W1 DFD
ws['K3'] = "=SUMIF('DFD DATA'!$B:$B,$I$2,'DFD DATA'!$D:$D)"   # W2 DFD

# Row 4: latest periods per sheet
ws['B4'] = "=MAX('DFD DATA'!$B:$B)"
ws['C4'] = "=MAX('DRIVER DATA'!$B:$B)"
ws['D4'] = "=MAX('CANCEL DATA'!$B:$B)"
ws['E4'] = "=SUMIF('CANCEL DATA'!$B:$B,$D$4,'CANCEL DATA'!$H:$H)"  # total cancel latest

# Hide PARAMS rows
for r in [1,2,3,4]: ws.row_dimensions[r].height = 0.1

# ── FORMULA HELPERS ───────────────────────────────────────────────────────────
SVC = "'SVC DATA'"
DFD = "'DFD DATA'"
DRV = "'DRIVER DATA'"
CAN = "'CANCEL DATA'"

def sumif(sheet, lookup_col, lookup_val, sum_col):
    return f"=SUMIF({sheet}!${lookup_col}:${lookup_col},{lookup_val},{sheet}!${sum_col}:${sum_col})"

def sumproduct2(sheet, col1, val1, col2, val2, sum_col, max_row=500):
    r = f"$4:${max_row}"
    return (f"=SUMPRODUCT(({sheet}!${col1}{r}={val1})*"
            f"({sheet}!${col2}{r}={val2}),"
            f"{sheet}!${sum_col}{r})")

def svc_ar(period_cell):
    return (f"=IFERROR(SUMIF({SVC}!$B:$B,{period_cell},{SVC}!$F:$F)/"
            f"SUMIF({SVC}!$B:$B,{period_cell},{SVC}!$E:$E),0)")

def svc_fr(period_cell):
    return (f"=IFERROR(SUMIF({SVC}!$B:$B,{period_cell},{SVC}!$G:$G)/"
            f"SUMIF({SVC}!$B:$B,{period_cell},{SVC}!$F:$F),0)")

def svc_reg_ar(period_cell, region):
    return (f"=IFERROR(SUMPRODUCT(({SVC}!$B$4:$B$500={period_cell})*"
            f"({SVC}!$C$4:$C$500=\"{region}\"),{SVC}!$F$4:$F$500)/"
            f"SUMPRODUCT(({SVC}!$B$4:$B$500={period_cell})*"
            f"({SVC}!$C$4:$C$500=\"{region}\"),{SVC}!$E$4:$E$500),0)")

def svc_reg_fr(period_cell, region):
    return (f"=IFERROR(SUMPRODUCT(({SVC}!$B$4:$B$500={period_cell})*"
            f"({SVC}!$C$4:$C$500=\"{region}\"),{SVC}!$G$4:$G$500)/"
            f"SUMPRODUCT(({SVC}!$B$4:$B$500={period_cell})*"
            f"({SVC}!$C$4:$C$500=\"{region}\"),{SVC}!$F$4:$F$500),0)")

def svc_reg_col(metric_col, period_cell, region):
    return (f"=SUMPRODUCT(({SVC}!$B$4:$B$500={period_cell})*"
            f"({SVC}!$C$4:$C$500=\"{region}\"),{SVC}!${metric_col}$4:${metric_col}$500)")

def svc_svc_ar(period_cell, service):
    return (f"=IFERROR(SUMPRODUCT(({SVC}!$B$4:$B$500={period_cell})*"
            f"({SVC}!$D$4:$D$500=\"{service}\"),{SVC}!$F$4:$F$500)/"
            f"SUMPRODUCT(({SVC}!$B$4:$B$500={period_cell})*"
            f"({SVC}!$D$4:$D$500=\"{service}\"),{SVC}!$E$4:$E$500),0)")

def svc_svc_fr(period_cell, service):
    return (f"=IFERROR(SUMPRODUCT(({SVC}!$B$4:$B$500={period_cell})*"
            f"({SVC}!$D$4:$D$500=\"{service}\"),{SVC}!$G$4:$G$500)/"
            f"SUMPRODUCT(({SVC}!$B$4:$B$500={period_cell})*"
            f"({SVC}!$D$4:$D$500=\"{service}\"),{SVC}!$F$4:$F$500),0)")

def svc_svc_col(metric_col, period_cell, service):
    return (f"=SUMPRODUCT(({SVC}!$B$4:$B$500={period_cell})*"
            f"({SVC}!$D$4:$D$500=\"{service}\"),{SVC}!${metric_col}$4:${metric_col}$500)")

def drv_seg(metric_col, period_cell, segment):
    return (f"=SUMPRODUCT(({DRV}!$B$4:$B$300={period_cell})*"
            f"({DRV}!$D$4:$D$300=\"{segment}\"),{DRV}!${metric_col}$4:${metric_col}$300)")

def can_reason(period_cell, reason):
    esc = reason.replace('"','""')
    return (f"=SUMPRODUCT(({CAN}!$B$4:$B$3500={period_cell})*"
            f"({CAN}!$C$4:$C$3500=\"{esc}\"),{CAN}!$H$4:$H$3500)")

# ── CELL WRITE HELPERS ────────────────────────────────────────────────────────
def rh(r, h): ws.row_dimensions[r].height = h

def cell(row, col, value, bold=False, color=DARK, size=9, fmt=None,
         fill=WHITE, h_align='center', border=True, italic=False):
    c = ws.cell(row=row, column=col, value=value)
    c.font = fn(bold=bold,color=color,size=size,italic=italic)
    c.fill = mf(fill); c.alignment = al(h_align)
    if border: c.border = mb()
    if fmt: c.number_format = fmt
    return c

def hdr(row, col, value, end_col=None):
    if end_col:
        ws.merge_cells(start_row=row,start_column=col,end_row=row,end_column=end_col)
    c = ws.cell(row=row, column=col, value=value)
    c.font = fn(bold=True,color=WHITE,size=9)
    c.fill = mf(BLUE); c.alignment = al(); c.border = mb(BLUE)

def section(row, text):
    rh(row, 22)
    ws.merge_cells(f'B{row}:P{row}')
    ws[f'B{row}'] = f'  {text}'
    ws[f'B{row}'].font = fn(bold=True,color=BLUE,size=10)
    ws[f'B{row}'].fill = mf(BL)
    ws[f'B{row}'].alignment = al('left')
    for col in range(2,17): ws.cell(row=row,column=col).fill = mf(BL)

def kpi(r, cs, title, val_fml, sub_fml, val_fmt, vcolor=BLUE):
    ce = cs+2
    rh(r,20); rh(r+1,32); rh(r+2,18)
    for rr in range(r,r+3):
        for cc in range(cs,ce+1):
            ws.cell(row=rr,column=cc).fill = mf(WHITE)
            ws.cell(row=rr,column=cc).border = mb()
    ws.merge_cells(start_row=r,start_column=cs,end_row=r,end_column=ce)
    c = ws.cell(row=r,column=cs,value=title)
    c.font=fn(bold=True,color=GRAY,size=8); c.alignment=al(); c.fill=mf(WHITE)
    ws.merge_cells(start_row=r+1,start_column=cs,end_row=r+1,end_column=ce)
    c = ws.cell(row=r+1,column=cs,value=val_fml)
    c.font=fn(bold=True,color=vcolor,size=22); c.alignment=al(); c.fill=mf(WHITE); c.number_format=val_fmt
    ws.merge_cells(start_row=r+2,start_column=cs,end_row=r+2,end_column=ce)
    c = ws.cell(row=r+2,column=cs,value=sub_fml)
    c.font=fn(color=GRAY,size=8); c.alignment=al(); c.fill=mf(WHITE)

# ═══════════════════════ VISIBLE DASHBOARD ═══════════════════════════════════
rh(5,8)

# HEADER
rh(6,40); rh(7,20); rh(8,8)
for row in [6,7]:
    for col in range(2,17): ws.cell(row=row,column=col).fill=mf(BLUE)
ws.merge_cells('B6:J6'); ws['B6']='AHAMOVE — WEEKLY OPS DASHBOARD'
ws['B6'].font=fn(bold=True,color=WHITE,size=20); ws['B6'].alignment=al('left')
ws.merge_cells('K6:P6')
ws['K6']='=IFERROR("W/E "&TEXT($B$2,"DD/MM/YYYY"),"No data")'
ws['K6'].font=fn(bold=True,color=ORANGE,size=12); ws['K6'].alignment=al('right')
ws.merge_cells('B7:P7')
ws['B7']='Driver Management  |  Bike Instant  |  SGN · HAN · EXP · NW'
ws['B7'].font=fn(color='AACCEE',size=10,italic=True); ws['B7'].alignment=al('left')

# ── KPI SNAPSHOT ─────────────────────────────────────────────────────────────
section(9, 'KPI SNAPSHOT  —  Latest Week  (auto-refresh from SVC DATA)')

# Sub-text formulas using PARAMS row 3 (pre-computed)
kpi(10,2,  'TOTAL REQUESTED',
    "=SUMIF('SVC DATA'!$B:$B,$B$2,'SVC DATA'!$E:$E)",
    '="vs prev: "&IF($B$3>$C$3,"▲","▼")&TEXT(ABS($B$3-$C$3),"#,##0")',
    '#,##0', BLUE)

kpi(10,6,  'ACCEPTANCE RATE',
    "=$D$3",
    '="vs prev: "&IF($D$3>=$E$3,"▲","▼")&TEXT(ABS($D$3-$E$3)*100,"0.0")&"pp"',
    '0.0%', GREEN)

kpi(10,10, 'FULFILLMENT RATE',
    "=$F$3",
    '="vs prev: "&IF($F$3>=$G$3,"▲","▼")&TEXT(ABS($F$3-$G$3)*100,"0.0")&"pp"',
    '0.0%', GREEN)

kpi(10,14, 'COMPLETED ORDERS',
    "=SUMIF('SVC DATA'!$B:$B,$B$2,'SVC DATA'!$G:$G)",
    '="vs prev: "&IF($H$3>$I$3,"▲","▼")&TEXT(ABS($H$3-$I$3),"#,##0")',
    '#,##0', BLUE)

rh(13,8)

kpi(14,2,  'ACTIVE DRIVERS (AA)',
    "=SUMIF('DRIVER DATA'!$B:$B,$C$4,'DRIVER DATA'!$J:$J)",
    '="Period: "&TEXT($C$4,"DD/MM/YYYY")',
    '#,##0', BLUE)

kpi(14,6,  'DFD — NEW DRIVERS',
    "=$J$3",
    '="vs prev: "&IF($J$3>=$K$3,"▲","▼")&TEXT(ABS($J$3-$K$3),"#,##0")',
    '#,##0', GREEN)

kpi(14,10, 'SGN ACCEPTANCE RATE',
    svc_reg_ar('$B$2','SGN'),
    '"Target ≥ 85%"',
    '0.0%', GREEN)

kpi(14,14, 'HAN ACCEPTANCE RATE',
    svc_reg_ar('$B$2','HAN'),
    '"Target ≥ 85%"',
    '0.0%', GREEN)

# ── 6-WEEK TREND ─────────────────────────────────────────────────────────────
section(18, '6-WEEK PERFORMANCE TREND')
rh(19,22)
for h,c in zip(['Week','Requested','Accepted','Completed','AR %','FR %','WoW Req %','WoW AR pp'],[2,3,4,5,6,7,8,9]):
    hdr(19,c,h)

week_params = ['$B$2','$C$2','$D$2','$E$2','$F$2','$G$2']
for i, wc in enumerate(week_params):
    row=20+i; rh(row,18)
    bg = YELLOW if i==0 else (BL if i%2==0 else WHITE)
    nwc = week_params[i+1] if i<5 else None

    req_w = f"=SUMIF({SVC}!$B:$B,{wc},{SVC}!$E:$E)"
    acc_w = f"=SUMIF({SVC}!$B:$B,{wc},{SVC}!$F:$F)"
    cmp_w = f"=SUMIF({SVC}!$B:$B,{wc},{SVC}!$G:$G)"
    ar_w  = f"=IFERROR({acc_w[1:]}/{req_w[1:]},0)"
    fr_w  = f"=IFERROR({cmp_w[1:]}/{acc_w[1:]},0)"

    if nwc:
        req_nw = f"SUMIF({SVC}!$B:$B,{nwc},{SVC}!$E:$E)"
        acc_nw = f"SUMIF({SVC}!$B:$B,{nwc},{SVC}!$F:$F)"
        wow_req = f"=IFERROR({req_w[1:]}/{req_nw}-1,\"—\")"
        wow_ar  = f"=IFERROR(({acc_w[1:]}/{req_w[1:]})-({acc_nw}/{req_nw}),\"—\")"
    else:
        wow_req = '"—"'
        wow_ar  = '"—"'

    for val,fmt,col in zip(
        [f'=TEXT({wc},"W/E DD/MM/YY")',req_w,acc_w,cmp_w,ar_w,fr_w,wow_req,wow_ar],
        ['@','#,##0','#,##0','#,##0','0.0%','0.0%','0.0%','0.00%'],
        [2,3,4,5,6,7,8,9]):
        c = ws.cell(row=row,column=col,value=val)
        c.font=fn(bold=(i==0),color=DARK,size=9)
        c.fill=mf(bg); c.number_format=fmt; c.alignment=al(); c.border=mb()

# ── REGION BREAKDOWN ─────────────────────────────────────────────────────────
section(27,'REGION BREAKDOWN  —  Latest Week vs Prev Week')
rh(28,22)
for h,c in zip(['Region','Requested','Completed','AR% Cur','AR% Prev','AR Δ pp','FR% Cur','FR% Prev','FR Δ pp'],[2,3,4,5,6,7,8,9,10]):
    hdr(28,c,h)

for i,region in enumerate(['SGN','HAN','EXP','NW']):
    row=29+i; rh(row,18); fc=BL if i%2==0 else WHITE
    ar_c = svc_reg_ar('$B$2',region)
    ar_p = svc_reg_ar('$C$2',region)
    fr_c = svc_reg_fr('$B$2',region)
    fr_p = svc_reg_fr('$C$2',region)
    ar_d = f"={ar_c[1:]}-{ar_p[1:]}"
    fr_d = f"={fr_c[1:]}-{fr_p[1:]}"
    for val,fmt,col in zip(
        [region, svc_reg_col('E','$B$2',region), svc_reg_col('G','$B$2',region),
         ar_c, ar_p, ar_d, fr_c, fr_p, fr_d],
        ['@','#,##0','#,##0','0.0%','0.0%','+0.00%;-0.00%;"-"','0.0%','0.0%','+0.00%;-0.00%;"-"'],
        [2,3,4,5,6,7,8,9,10]):
        c = ws.cell(row=row,column=col,value=val)
        c.font=fn(bold=(col==2),color=DARK,size=9)
        c.fill=mf(fc); c.number_format=fmt
        c.alignment=al('left' if col==2 else 'center'); c.border=mb()

# ── SERVICE BREAKDOWN ─────────────────────────────────────────────────────────
section(34,'SERVICE BREAKDOWN  —  Latest Week')
rh(35,22)
for h,c in zip(['Service','Requested','Accepted','Completed','AR %','FR %','Volume Mix %'],[2,3,4,5,6,7,8]):
    hdr(35,c,h)

for i,service in enumerate(['1H','2H','4H','BULKY','AIFOOD']):
    row=36+i; rh(row,18); fc=BL if i%2==0 else WHITE
    req_s = svc_svc_col('E','$B$2',service)
    mix   = f"=IFERROR({req_s[1:]}/SUMIF({SVC}!$B:$B,$B$2,{SVC}!$E:$E),0)"
    for val,fmt,col in zip(
        [service, req_s, svc_svc_col('F','$B$2',service),
         svc_svc_col('G','$B$2',service), svc_svc_ar('$B$2',service),
         svc_svc_fr('$B$2',service), mix],
        ['@','#,##0','#,##0','#,##0','0.0%','0.0%','0.0%'],
        [2,3,4,5,6,7,8]):
        c = ws.cell(row=row,column=col,value=val)
        c.font=fn(bold=(col==2),color=DARK,size=9)
        c.fill=mf(fc); c.number_format=fmt
        c.alignment=al('left' if col==2 else 'center'); c.border=mb()

# ── ACTIVE DRIVER BY SEGMENT ─────────────────────────────────────────────────
section(42,'ACTIVE DRIVER BY SEGMENT  (DRIVER DATA latest period)')
rh(43,22)
for h,c in zip(['Segment','Total Driver','AA Driver','GDR Driver','Online Hrs','Accept Orders','Reward (K VND)','GDR Rate %'],[2,3,4,5,6,7,8,9]):
    hdr(43,c,h)

seg_colors={'FT':GREEN,'NIM':BLUE,'NLM':'1D4ED8','PT':'7C3AED','Return':ORANGE}
for i,seg in enumerate(['FT','NIM','NLM','PT','Return']):
    row=44+i; rh(row,18); fc=BL if i%2==0 else WHITE
    total = drv_seg('E','$C$4',seg)
    aa    = drv_seg('J','$C$4',seg)
    gdr   = drv_seg('F','$C$4',seg)
    oh    = drv_seg('G','$C$4',seg)
    ao    = drv_seg('H','$C$4',seg)
    rew   = f"=IFERROR({drv_seg('I','$C$4',seg)[1:]}/1000,0)"
    gdr_r = f"=IFERROR({gdr[1:]}/{total[1:]},0)"
    for val,fmt,col in zip(
        [seg,total,aa,gdr,oh,ao,rew,gdr_r],
        ['@','#,##0','#,##0','#,##0','#,##0.0','#,##0','#,##0','0.0%'],
        [2,3,4,5,6,7,8,9]):
        c = ws.cell(row=row,column=col,value=val)
        c.font=fn(bold=(col==2),color=seg_colors.get(seg,DARK) if col==2 else DARK,size=9)
        c.fill=mf(fc); c.number_format=fmt
        c.alignment=al('left' if col==2 else 'center'); c.border=mb()

# ── CANCEL REASONS ───────────────────────────────────────────────────────────
section(50,'TOP CANCEL REASONS  —  Latest Week')
rh(51,22)
hdr(51,2,'#'); hdr(51,3,'Cancel Reason'); hdr(51,4,'Total Cancels'); hdr(51,5,'Share %')
# Total cancel (E4 in params)
rh(52,18)
cell(52,6, '=IFERROR("Total: "&TEXT($E$4,"#,##0")&" cancels","")',
     bold=True, color=BLUE, size=8, fill=BL, fmt='@')
ws.cell(row=52,column=6).border = mb()

known_reasons = [
    "Driver's not ready",
    "Can not contact sender/recipient",
    "user cancel (pos, partner)",
    "Reschedule",
    "Recipient cancel booking",
    "User changes something/Wrong information",
    "Fake order, wrong address",
    "Driver asked to cancel",
]
for i,reason in enumerate(known_reasons):
    row=52+i; rh(row,18); fc=BL if i%2==0 else WHITE
    tot = can_reason('$D$4',reason)
    pct = f"=IFERROR({tot[1:]}/$E$4,0)"
    for val,fmt,col in zip([i+1, reason, tot, pct],['@','@','#,##0','0.0%'],[2,3,4,5]):
        c = ws.cell(row=row,column=col,value=val)
        c.font=fn(bold=(i<3 and col==4),color=DARK,size=9)
        c.fill=mf(fc); c.number_format=fmt
        c.alignment=al('left' if col==3 else 'center'); c.border=mb()
    ws.cell(row=row,column=6).fill=mf(fc); ws.cell(row=row,column=6).border=mb()

ws.conditional_formatting.add(f'E52:E{52+len(known_reasons)-1}', ColorScaleRule(
    start_type='min',start_color='63BE7B',
    mid_type='percentile',mid_value=50,mid_color='FFEB84',
    end_type='max',end_color='F8696B'))

# ── DFD TREND ────────────────────────────────────────────────────────────────
section(61,'DFD (NEW DRIVER) WEEKLY TREND')
rh(62,22)
for h,c in zip(['Week','Total DFD','Organic','Referral','Digital Ads','WoW %'],[2,3,4,5,6,7]):
    hdr(62,c,h)

dfd_params = ['$H$2','$I$2','$J$2','$K$2','$L$2','$M$2']
for i,wc in enumerate(dfd_params):
    row=63+i; rh(row,18)
    bg=YELLOW if i==0 else (BL if i%2==0 else WHITE)
    nwc=dfd_params[i+1] if i<5 else None
    dfd_tot = f"=SUMIF({DFD}!$B:$B,{wc},{DFD}!$D:$D)"
    wow = f"=IFERROR({dfd_tot[1:]}/SUMIF({DFD}!$B:$B,{nwc},{DFD}!$D:$D)-1,\"—\")" if nwc else '"—"'
    for val,fmt,col in zip(
        [f'=TEXT({wc},"W/E DD/MM/YY")', dfd_tot,
         f"=SUMIF({DFD}!$B:$B,{wc},{DFD}!$E:$E)",
         f"=SUMIF({DFD}!$B:$B,{wc},{DFD}!$F:$F)",
         f"=SUMIF({DFD}!$B:$B,{wc},{DFD}!$G:$G)", wow],
        ['@','#,##0','#,##0','#,##0','#,##0','0.0%'],[2,3,4,5,6,7]):
        c = ws.cell(row=row,column=col,value=val)
        c.font=fn(bold=(i==0),color=DARK,size=9)
        c.fill=mf(bg); c.number_format=fmt; c.alignment=al(); c.border=mb()

# ── UPDATE GUIDE ─────────────────────────────────────────────────────────────
rh(70,8); section(71,'HOW TO UPDATE WEEKLY')
guide = [
    '1. SVC DATA   — Xóa từ row 4 xuống, paste data mới. Giữ nguyên header row 3. Cột Period phải là giá trị date (không phải text).',
    '2. DFD DATA   — Tương tự. Period = date value.',
    '3. DRIVER DATA — Tương tự. Cột J = AA Driver (active drivers count).',
    '4. CANCEL DATA — Tương tự. Cột C = Cancel Reason (text chính xác, case-sensitive).',
    '5. Dashboard tự recalculate. Không cần Python. Tất cả dùng SUMIF / SUMPRODUCT / LARGE.',
]
for i,text in enumerate(guide):
    row=72+i; rh(row,18)
    ws.merge_cells(f'B{row}:P{row}')
    ws[f'B{row}']=text
    ws[f'B{row}'].font=fn(size=8,color=DARK,italic=(i==4))
    ws[f'B{row}'].fill=mf(BL if i%2==0 else WHITE)
    ws[f'B{row}'].alignment=al('left')
    for col in range(3,17):
        ws.cell(row=row,column=col).fill=mf(BL if i%2==0 else WHITE)

ws.freeze_panes='B9'

wb._sheets=[ws,ws_svc,ws_dfd,ws_drv,ws_can]
os.makedirs(os.path.dirname(OUT),exist_ok=True)
wb.save(OUT)
print(f'Saved: {OUT}  ({os.path.getsize(OUT):,} bytes)')
