# -*- coding: utf-8 -*-
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import json
import os

wb = openpyxl.Workbook()
wb.remove(wb.active) # Remove default sheet

# Brand Colors (Ahamove & Enterprise Slate)
ORANGE_PRIMARY = "FF6B00"       # Ahamove Orange
ORANGE_DARK = "D95A00"
ORANGE_LIGHT = "FFF3EB"         # Soft Orange Tint
DARK_SLATE = "1E293B"           # Slate Dark
MUTED_SLATE = "64748B"          # Slate Muted
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
TOTAL_BG = "FFF7ED"             # Light Amber for Subtotals
GRAND_TOTAL_BG = "FFEDD5"       # Warm Orange for Grand Total

# Styles
font_title = Font(name="Calibri", size=15, bold=True, color="FFFFFF")
font_subtitle = Font(name="Calibri", size=10, italic=True, color="FFFFFF")
font_section = Font(name="Calibri", size=12, bold=True, color=DARK_SLATE)
font_header = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
font_sub_header = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
font_bold = Font(name="Calibri", size=10, bold=True, color=DARK_SLATE)
font_regular = Font(name="Calibri", size=10, color="1E293B")
font_muted = Font(name="Calibri", size=9, italic=True, color=MUTED_SLATE)
font_kpi_num = Font(name="Calibri", size=16, bold=True, color=ORANGE_PRIMARY)
font_kpi_label = Font(name="Calibri", size=9, bold=True, color=MUTED_SLATE)

fill_primary = PatternFill(start_color=ORANGE_PRIMARY, end_color=ORANGE_PRIMARY, fill_type="solid")
fill_dark = PatternFill(start_color=DARK_SLATE, end_color=DARK_SLATE, fill_type="solid")
fill_sub_dark = PatternFill(start_color="334155", end_color="334155", fill_type="solid")
fill_soft_orange = PatternFill(start_color=ORANGE_LIGHT, end_color=ORANGE_LIGHT, fill_type="solid")
fill_zebra = PatternFill(start_color=ZEBRA_ROW, end_color=ZEBRA_ROW, fill_type="solid")
fill_card = PatternFill(start_color=CARD_BG, end_color=CARD_BG, fill_type="solid")
fill_subtotal = PatternFill(start_color=TOTAL_BG, end_color=TOTAL_BG, fill_type="solid")
fill_grand_total = PatternFill(start_color=GRAND_TOTAL_BG, end_color=GRAND_TOTAL_BG, fill_type="solid")

thin_side = Side(border_style="thin", color=BORDER_COLOR)
med_side = Side(border_style="medium", color=ORANGE_PRIMARY)
double_side = Side(border_style="double", color=DARK_SLATE)
card_side = Side(border_style="thin", color=CARD_BORDER)

border_all = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)
border_header = Border(left=thin_side, right=thin_side, top=thin_side, bottom=med_side)
border_subtotal = Border(top=thin_side, bottom=thin_side, left=thin_side, right=thin_side)
border_grand_total = Border(top=thin_side, bottom=double_side, left=thin_side, right=thin_side)
border_card = Border(left=card_side, right=card_side, top=card_side, bottom=card_side)

align_center = Alignment(horizontal="center", vertical="center")
align_left = Alignment(horizontal="left", vertical="center", wrap_text=True)
align_right = Alignment(horizontal="right", vertical="center")
align_header = Alignment(horizontal="center", vertical="center", wrap_text=True)

# Formatters
FMT_CURRENCY = "#,##0 ₫"
FMT_NUMBER = "#,##0"
FMT_PERCENT = "0.0%"

print("Styles initialized successfully.")
