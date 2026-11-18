# -*- coding: utf-8 -*-
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import os

# Load original workbook
wb_orig = openpyxl.load_workbook('/Users/ts-1148/Desktop/Pulu-workspace/data/sources/AOP 2026 - DM.xlsx', read_only=True, data_only=True)
s_orig = wb_orig['AOP 2026 Chi phí Team ver 2']

# Load our template workbook to update
template_path = '/Users/ts-1148/Desktop/Pulu-workspace/data/sources/AOP_2026_DM_Template_ChuanHoa.xlsx'
wb_dest = openpyxl.load_workbook(template_path, data_only=False)
ws_master = wb_dest['01_Master_AOP_Budget']

# Mapping of original sheet row -> Master Budget sheet row
row_map = {
    # Nhóm 1: Event
    4: 4,    # Vinh danh
    5: 5,    # Minigame
    6: 6,    # Livestream
    7: 7,    # 8/3
    8: 8,    # Gia đình 28/6
    9: 9,    # Campaign sinh nhật
    10: 10,  # Trung thu
    11: 11,  # 20/10
    12: 12,  # 19/11
    13: 13,  # AhaCup
    14: 14,  # Giáng Sinh
    15: 15,  # Thiên tai
    16: 16,  # Lì xì
    17: 17,  # Tiếp sức Campaign
    
    # Nhóm 2: Quản trị & Phúc lợi
    19: 19,  # BHTN Fulltime
    20: 20,  # Thuê FL call
    22: 21,  # SMS / ZNS
    23: 22,  # Bánh Trung thu
    24: 23,  # Quà Tết
    25: 24,  # Tấm Lòng Cam
    27: 25,  # Quà Bike
    28: 26,  # Quà Truck
    
    # Nhóm 3: Đội trưởng
    33: 28,  # Lương đội trưởng
    34: 29,  # Bonus đội trưởng
    
    # Nhóm 4: Xe điện
    36: 32,  # Sạc xe điện
    37: 33,  # Chiết khấu xe điện 3%
    
    # Nhóm 5: Gopika
    38: 35,  # Gopika supply
    39: 36,  # Gopika chiết khấu 5%
    40: 37   # Gopika phí nộp tiền mặt 0.7%
}

print("--- COPYING EXACT MONTH VALUES FROM ORIGINAL SHEET ---")
for orig_r, master_r in row_map.items():
    orig_name = s_orig.cell(orig_r, 3).value or s_orig.cell(orig_r, 1).value or ''
    orig_months = [s_orig.cell(orig_r, 11 + i).value for i in range(12)]
    
    # Write to master sheet: Cols 20 to 31 (T to AE)
    for m_idx, m_val in enumerate(orig_months):
        col_dest = 20 + m_idx # Col T is 20
        # If None, write 0 or preserve
        val_to_write = m_val if (m_val is not None) else 0
        cell = ws_master.cell(master_r, col_dest, val_to_write)
        cell.number_format = "#,##0"
        cell.alignment = Alignment(horizontal="right", vertical="center")
        
    print(f"Updated Master Row {master_r:02d} ({orig_name[:25]}): {[v for v in orig_months if v is not None and v != 0]}")

# Save to both target locations
out_file_1 = "/Users/ts-1148/Desktop/Pulu-workspace/Output/Ahamove/01. STRATEGY_PLANNING/AOP_2026_DM_Standardized_Template.xlsx"
out_file_2 = "/Users/ts-1148/Desktop/Pulu-workspace/data/sources/AOP_2026_DM_Template_ChuanHoa.xlsx"

wb_dest.save(out_file_1)
wb_dest.save(out_file_2)

print("\nSuccessfully updated both Excel files with exact original monthly placements!")
