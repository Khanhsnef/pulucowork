import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import json
import os

wb = openpyxl.Workbook()
# remove default sheet
wb.remove(wb.active)

# Color Palette - Ahamove Brand Standards
ORANGE_PRIMARY = "FF6B00"       # Ahamove Orange
ORANGE_LIGHT = "FFF3EB"         # Soft Orange Tint for Key Takeaways/Card
DARK_SLATE = "1E293B"           # Slate Dark for Headers
MUTED_SLATE = "64748B"          # Slate Muted for Subheaders
HEADER_BG = "FF6B00"            # Table Header Background
HEADER_FG = "FFFFFF"            # Table Header Text
SUBHEADER_BG = "0F172A"         # Block Subheader
ZEBRA_ROW = "F8FAFC"            # Light Gray
CARD_BG = "F1F5F9"              # Card Neutral
CARD_BORDER = "CBD5E1"
SUCCESS_BG = "E8F5EC"
SUCCESS_FG = "065F46"
WARNING_BG = "FEF3C7"
WARNING_FG = "92400E"
DANGER_BG = "FEE2E2"
DANGER_FG = "991B1B"
BORDER_COLOR = "E2E8F0"

font_title = Font(name="Calibri", size=16, bold=True, color="FFFFFF")
font_subtitle = Font(name="Calibri", size=11, italic=True, color="FFFFFF")
font_section = Font(name="Calibri", size=13, bold=True, color=DARK_SLATE)
font_header = Font(name="Calibri", size=11, bold=True, color=HEADER_FG)
font_bold = Font(name="Calibri", size=10, bold=True, color=DARK_SLATE)
font_regular = Font(name="Calibri", size=10, color="000000")
font_muted = Font(name="Calibri", size=9, italic=True, color=MUTED_SLATE)
font_kpi_num = Font(name="Calibri", size=18, bold=True, color=ORANGE_PRIMARY)
font_kpi_label = Font(name="Calibri", size=9, bold=True, color=MUTED_SLATE)

fill_primary = PatternFill(start_color=ORANGE_PRIMARY, end_color=ORANGE_PRIMARY, fill_type="solid")
fill_dark = PatternFill(start_color=DARK_SLATE, end_color=DARK_SLATE, fill_type="solid")
fill_sub_dark = PatternFill(start_color=SUBHEADER_BG, end_color=SUBHEADER_BG, fill_type="solid")
fill_soft_orange = PatternFill(start_color=ORANGE_LIGHT, end_color=ORANGE_LIGHT, fill_type="solid")
fill_zebra = PatternFill(start_color=ZEBRA_ROW, end_color=ZEBRA_ROW, fill_type="solid")
fill_card = PatternFill(start_color=CARD_BG, end_color=CARD_BG, fill_type="solid")
fill_total = PatternFill(start_color="FFEAD5", end_color="FFEAD5", fill_type="solid")

thin_border_side = Side(border_style="thin", color=BORDER_COLOR)
med_border_side = Side(border_style="medium", color=ORANGE_PRIMARY)
double_border_side = Side(border_style="double", color=DARK_SLATE)

border_all = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)
border_header = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=med_border_side)
border_subtotal = Border(top=thin_border_side, bottom=thin_border_side)
border_grand_total = Border(top=thin_border_side, bottom=double_border_side)

align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
align_left = Alignment(horizontal="left", vertical="center", wrap_text=True)
align_right = Alignment(horizontal="right", vertical="center")
align_header = Alignment(horizontal="center", vertical="center", wrap_text=True)

# Load raw json
with open('/Users/ts-1148/Desktop/Pulu-workspace/aop_data_extracted.json') as f:
    raw_data = json.load(f)

print("Data loaded, creating sheets...")
