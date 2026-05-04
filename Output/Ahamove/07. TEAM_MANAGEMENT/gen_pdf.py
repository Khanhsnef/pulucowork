#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate Claude Guide PDF for Ahamove Driver Management Team"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus.flowables import Flowable
import os

# ── Fonts ─────────────────────────────────────────────────────────────────────
FONT_PATH = "/Library/Fonts/Arial Unicode.ttf"
pdfmetrics.registerFont(TTFont("ArialUni", FONT_PATH))
pdfmetrics.registerFont(TTFont("ArialUni", FONT_PATH))

# ── Brand Colors ───────────────────────────────────────────────────────────────
BLUE       = colors.HexColor("#0E4174")
ORANGE     = colors.HexColor("#FF7F32")
SUCCESS    = colors.HexColor("#10B981")
DANGER     = colors.HexColor("#EF4444")
BG_GRAY    = colors.HexColor("#F8FAFC")
BG_BLUE_LT = colors.HexColor("#EEF4FB")
BG_ORANGE  = colors.HexColor("#FFF4EC")
BORDER     = colors.HexColor("#E2E8F0")
TEXT_DARK  = colors.HexColor("#1E293B")
TEXT_MID   = colors.HexColor("#475569")
TEXT_LIGHT = colors.HexColor("#94A3B8")
CODE_BG    = colors.HexColor("#F1F5F9")
CODE_TEXT  = colors.HexColor("#0F172A")
WHITE      = colors.white

PAGE_W, PAGE_H = A4
MARGIN = 18 * mm

# ── Styles ─────────────────────────────────────────────────────────────────────
def S(name, **kw):
    defaults = dict(fontName="ArialUni", fontSize=10, leading=15,
                    textColor=TEXT_DARK, spaceAfter=4)
    defaults.update(kw)
    return ParagraphStyle(name, **defaults)

ST = {
    "h1"       : S("h1", fontSize=22, leading=28, textColor=WHITE,
                   fontName="ArialUni", spaceBefore=0, spaceAfter=0),
    "h2"       : S("h2", fontSize=14, leading=20, textColor=WHITE,
                   fontName="ArialUni", spaceBefore=0, spaceAfter=0),
    "h3"       : S("h3", fontSize=11, leading=16, textColor=BLUE,
                   fontName="ArialUni", spaceBefore=8, spaceAfter=4),
    "h4"       : S("h4", fontSize=10, leading=15, textColor=ORANGE,
                   fontName="ArialUni", spaceBefore=6, spaceAfter=3),
    "body"     : S("body", fontSize=9.5, leading=15, textColor=TEXT_DARK,
                   spaceAfter=6, alignment=TA_JUSTIFY),
    "body_sm"  : S("body_sm", fontSize=9, leading=14, textColor=TEXT_MID,
                   spaceAfter=4),
    "bullet"   : S("bullet", fontSize=9.5, leading=14, textColor=TEXT_DARK,
                   leftIndent=12, firstLineIndent=0, spaceAfter=3,
                   bulletIndent=4),
    "code"     : S("code", fontSize=8.5, leading=13, textColor=CODE_TEXT,
                   fontName="Courier", backColor=CODE_BG,
                   leftIndent=8, rightIndent=8, spaceBefore=4, spaceAfter=6),
    "callout"  : S("callout", fontSize=9.5, leading=14, textColor=BLUE,
                   backColor=BG_BLUE_LT, leftIndent=10, rightIndent=10,
                   spaceBefore=4, spaceAfter=6),
    "warn"     : S("warn", fontSize=9.5, leading=14, textColor="#7C2D12",
                   backColor="#FEF3C7", leftIndent=10, rightIndent=10,
                   spaceBefore=4, spaceAfter=6),
    "toc_item" : S("toc_item", fontSize=10, leading=18, textColor=TEXT_DARK,
                   leftIndent=8),
    "toc_num"  : S("toc_num", fontSize=10, leading=18, textColor=ORANGE,
                   fontName="ArialUni"),
    "cover_sub": S("cover_sub", fontSize=11, leading=18, textColor=WHITE,
                   alignment=TA_CENTER),
    "cover_tag": S("cover_tag", fontSize=9, leading=14,
                   textColor=colors.HexColor("#CBD5E1"),
                   alignment=TA_CENTER),
    "footer"   : S("footer", fontSize=8, leading=10,
                   textColor=TEXT_LIGHT, alignment=TA_CENTER),
    "th"       : S("th", fontSize=9, leading=13, textColor=WHITE,
                   fontName="ArialUni", alignment=TA_CENTER),
    "td"       : S("td", fontSize=9, leading=13, textColor=TEXT_DARK,
                   spaceAfter=0),
    "td_code"  : S("td_code", fontSize=8.5, leading=12, textColor=ORANGE,
                   fontName="Courier"),
    "label"    : S("label", fontSize=8, leading=12, textColor=WHITE,
                   fontName="ArialUni", alignment=TA_CENTER),
}

# ── Helpers ────────────────────────────────────────────────────────────────────
def p(text, style="body"):
    return Paragraph(text, ST[style])

def sp(h=4):
    return Spacer(1, h * mm)

def hr(color=BORDER, thickness=0.5):
    return HRFlowable(width="100%", thickness=thickness, color=color,
                      spaceBefore=2*mm, spaceAfter=2*mm)

def section_header(number, title, icon=""):
    tbl = Table(
        [[Paragraph(f"{icon} {number}. {title}", ST["h2"])]],
        colWidths=[PAGE_W - 2*MARGIN],
    )
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), BLUE),
        ("ROUNDEDCORNERS", [6]),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 12),
        ("RIGHTPADDING",  (0,0), (-1,-1), 12),
    ]))
    return KeepTogether([sp(3), tbl, sp(4)])

def sub_header(title):
    return KeepTogether([sp(2), p(title, "h3"), sp(1)])

def sub2_header(title):
    return p(title, "h4")

def bullet(items):
    """items: list of str"""
    out = []
    for item in items:
        out.append(Paragraph(f"• {item}", ST["bullet"]))
    return out

def code_block(text):
    lines = text.strip().split("\n")
    content = "<br/>".join(l.replace(" ", "&nbsp;").replace("<","&lt;").replace(">","&gt;") for l in lines)
    tbl = Table(
        [[Paragraph(content, ST["code"])]],
        colWidths=[PAGE_W - 2*MARGIN - 4*mm],
    )
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), CODE_BG),
        ("ROUNDEDCORNERS", [4]),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("BOX",           (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
    ]))
    return KeepTogether([tbl, sp(2)])

def callout(text, style="callout"):
    icon = "💡" if style == "callout" else "⚠️"
    tbl = Table(
        [[Paragraph(f"{icon}  {text}", ST[style])]],
        colWidths=[PAGE_W - 2*MARGIN - 4*mm],
    )
    bg = BG_BLUE_LT if style == "callout" else colors.HexColor("#FEF3C7")
    bd = colors.HexColor("#93C5FD") if style == "callout" else colors.HexColor("#FCD34D")
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), bg),
        ("ROUNDEDCORNERS", [4]),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("BOX",           (0,0), (-1,-1), 1, bd),
    ]))
    return KeepTogether([tbl, sp(2)])

def make_table(headers, rows, col_widths=None, highlight_col=None):
    usable = PAGE_W - 2*MARGIN - 4*mm
    if col_widths is None:
        col_widths = [usable / len(headers)] * len(headers)

    header_row = [Paragraph(h, ST["th"]) for h in headers]
    data = [header_row]
    for i, row in enumerate(rows):
        data.append([Paragraph(str(c), ST["td"]) for c in row])

    tbl = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ("BACKGROUND",    (0, 0), (-1, 0), BLUE),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, BG_GRAY]),
        ("GRID",          (0, 0), (-1, -1), 0.4, BORDER),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 7),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 7),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("ROUNDEDCORNERS",[4]),
    ]
    if highlight_col is not None:
        for r in range(1, len(data)):
            style.append(("TEXTCOLOR", (highlight_col, r), (highlight_col, r), ORANGE))
    tbl.setStyle(TableStyle(style))
    return KeepTogether([tbl, sp(3)])

def badge(text, color=BLUE):
    tbl = Table([[Paragraph(text, ST["label"])]], colWidths=[28*mm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), color),
        ("TOPPADDING",    (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ("ROUNDEDCORNERS",[8]),
    ]))
    return tbl

# ── Page template ──────────────────────────────────────────────────────────────
class PageTemplate:
    def __init__(self, total_pages=None):
        self.total = total_pages

    def __call__(self, canvas_obj, doc):
        canvas_obj.saveState()
        w, h = A4
        # Header bar
        canvas_obj.setFillColor(BLUE)
        canvas_obj.rect(0, h - 10*mm, w, 10*mm, fill=1, stroke=0)
        canvas_obj.setFillColor(ORANGE)
        canvas_obj.rect(0, h - 11.5*mm, w, 1.5*mm, fill=1, stroke=0)
        # Header text
        canvas_obj.setFillColor(WHITE)
        canvas_obj.setFont("ArialUni", 7.5)
        canvas_obj.drawString(MARGIN, h - 6.5*mm, "AHAMOVE  •  DRIVER MANAGEMENT TEAM")
        canvas_obj.setFont("ArialUni", 7)
        canvas_obj.drawRightString(w - MARGIN, h - 6.5*mm, "Claude AI — Huong Dan Toan Dien")
        # Footer bar
        canvas_obj.setFillColor(BG_GRAY)
        canvas_obj.rect(0, 0, w, 10*mm, fill=1, stroke=0)
        canvas_obj.setFillColor(BORDER)
        canvas_obj.rect(0, 10*mm, w, 0.5, fill=1, stroke=0)
        # Footer text
        canvas_obj.setFillColor(TEXT_LIGHT)
        canvas_obj.setFont("ArialUni", 7.5)
        canvas_obj.drawString(MARGIN, 3.5*mm, "khanhlp@ahamove.com  •  2026-05-04")
        page_num = doc.page
        canvas_obj.drawRightString(w - MARGIN, 3.5*mm, f"Trang {page_num}")
        canvas_obj.restoreState()

# ── Cover Page ─────────────────────────────────────────────────────────────────
def cover_page():
    elements = []

    # Big blue background card
    cover_tbl = Table(
        [[Paragraph("CLAUDE AI", ParagraphStyle("ct", fontName="ArialUni",
                    fontSize=36, leading=44, textColor=WHITE,
                    alignment=TA_CENTER)),
          ]],
        colWidths=[PAGE_W - 2*MARGIN],
    )
    cover_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), BLUE),
        ("TOPPADDING",    (0,0), (-1,-1), 24),
        ("BOTTOMPADDING", (0,0), (-1,-1), 24),
        ("ROUNDEDCORNERS",[12]),
    ]))

    subtitle_tbl = Table(
        [[Paragraph("Huong Dan Toan Dien Cho Team", ST["cover_sub"])]],
        colWidths=[PAGE_W - 2*MARGIN],
    )
    subtitle_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), colors.HexColor("#0A2E56")),
        ("TOPPADDING",    (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("ROUNDEDCORNERS",[8]),
    ]))

    elements += [
        sp(20),
        cover_tbl,
        sp(4),
        subtitle_tbl,
        sp(8),
    ]

    # Tag row
    tags = [
        ("Danh cho nguoi moi bat dau", BLUE),
        ("10 Phan Chi Tiet", ORANGE),
        ("Ung dung thuc te", SUCCESS),
    ]
    tag_cells = [[badge(t, c) for t, c in tags]]
    tag_tbl = Table(tag_cells, colWidths=[62*mm, 52*mm, 52*mm])
    tag_tbl.setStyle(TableStyle([
        ("ALIGN",    (0,0), (-1,-1), "CENTER"),
        ("VALIGN",   (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING",  (0,0), (-1,-1), 4),
        ("RIGHTPADDING", (0,0), (-1,-1), 4),
    ]))
    elements += [tag_tbl, sp(12)]

    # Meta info box
    meta_rows = [
        ["Danh cho",   "Thanh vien team chua tung dung AI / Claude"],
        ["Muc tieu",   "Hieu Claude la gi, dung duoc ngay, ap dung vao cong viec"],
        ["Cap nhat",   "2026-05-04"],
        ["Bien soan",  "Khanh (Driver Management Leader) — Ahamove"],
    ]
    meta_data = []
    for k, v in meta_rows:
        meta_data.append([
            Paragraph(k, ParagraphStyle("mk", fontName="ArialUni", fontSize=9,
                       textColor=ORANGE)),
            Paragraph(v, ParagraphStyle("mv", fontName="ArialUni", fontSize=9,
                       textColor=TEXT_DARK)),
        ])
    meta_tbl = Table(meta_data, colWidths=[38*mm, PAGE_W - 2*MARGIN - 42*mm])
    meta_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), BG_GRAY),
        ("BOX",           (0,0), (-1,-1), 0.5, BORDER),
        ("INNERGRID",     (0,0), (-1,-1), 0.3, BORDER),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("ROUNDEDCORNERS",[6]),
    ]))
    elements += [meta_tbl, PageBreak()]
    return elements

# ── TOC ────────────────────────────────────────────────────────────────────────
def toc():
    items = [
        ("1", "AI La Gi? — Giai thich khong can ky thuat"),
        ("2", "Claude La Ai? — Anthropic La Ai?"),
        ("3", "Nguyen Ly Hoat Dong"),
        ("4", "Cac Nen Tang Claude — Dung o dau, khac gi nhau?"),
        ("5", "Bat Dau Dung Claude — Step by step"),
        ("6", "Cach Viet Prompt Hieu Qua"),
        ("7", "Ap Dung Vao Cong Viec Thuc Te"),
        ("8", "Nhung Dieu Claude KHONG Lam Duoc"),
        ("9", "Bao Mat & Luu Y Quan Trong"),
        ("10", "Tu Dien Thuat Ngu"),
    ]
    tbl_data = []
    for num, title in items:
        tbl_data.append([
            Paragraph(num, ST["toc_num"]),
            Paragraph(title, ST["toc_item"]),
        ])

    tbl = Table(tbl_data, colWidths=[12*mm, PAGE_W - 2*MARGIN - 16*mm])
    tbl.setStyle(TableStyle([
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [WHITE, BG_GRAY]),
        ("TOPPADDING",     (0,0), (-1,-1), 7),
        ("BOTTOMPADDING",  (0,0), (-1,-1), 7),
        ("LEFTPADDING",    (0,0), (-1,-1), 8),
        ("BOX",            (0,0), (-1,-1), 0.5, BORDER),
        ("LINEBELOW",      (0,0), (-1,-2), 0.3, BORDER),
        ("VALIGN",         (0,0), (-1,-1), "MIDDLE"),
    ]))

    header_tbl = Table(
        [[Paragraph("MUC LUC", ParagraphStyle("toch",
            fontName="ArialUni", fontSize=16, leading=22,
            textColor=WHITE, alignment=TA_CENTER))]],
        colWidths=[PAGE_W - 2*MARGIN],
    )
    header_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), BLUE),
        ("TOPPADDING",    (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("ROUNDEDCORNERS",[8]),
    ]))

    return [header_tbl, sp(4), tbl, PageBreak()]

# ── Section 1 — AI La Gi ──────────────────────────────────────────────────────
def section1():
    el = [section_header("1", "AI La Gi?", "")]
    el.append(p("Hay nghi AI (Tri tue nhan tao) nhu mot <b>nhan vien da doc gan nhu toan bo internet</b> — sach, bai bao, code, tai lieu khoa hoc, Wikipedia, dien dan... — roi hoc cach <b>tra loi cau hoi, viet van ban, phan tich du lieu va ly luan</b> dua tren tat ca kien thuc do."))
    el.append(p("Khac voi phan mem thong thuong (ban bam nut → no lam dung 1 viec co dinh), AI <b>hieu ngon ngu tu nhien</b> — tuc la ban noi chuyen binh thuong voi no nhu noi chuyen voi nguoi."))
    el.append(sub_header("AI ≠ Robot trong phim"))
    headers = ["Dieu nhieu nguoi nghi", "Thuc te"]
    rows = [
        ["AI co y thuc, cam xuc nhu nguoi", "AI khong co y thuc. No xu ly van ban theo xac suat thong ke"],
        ["AI biet het moi thu", "AI chi biet nhung gi da duoc hoc. Co the sai, co the bia"],
        ["AI se thay the toan bo con nguoi", "AI thay the <b>tac vu</b>, khong thay the <b>tu duy & judgement</b>"],
        ["Phai biet code moi dung duoc", "Ai cung dung duoc — chi can biet go chu"],
    ]
    el.append(make_table(headers, rows, col_widths=[80*mm, PAGE_W-2*MARGIN-84*mm]))
    return el

# ── Section 2 — Claude La Ai ──────────────────────────────────────────────────
def section2():
    el = [section_header("2", "Claude La Ai? Anthropic La Ai?", "")]
    el.append(sub_header("Anthropic — Cong ty tao ra Claude"))
    el.append(p("<b>Anthropic</b> la cong ty AI thanh lap nam 2021 tai My, tach ra tu OpenAI (cong ty tao ChatGPT). Anthropic tap trung vao <b>AI an toan va dang tin cay</b> — triet ly cua ho la tao ra AI giup ich cho con nguoi ma khong gay hai."))
    el.append(p("<b>Claude</b> la san pham AI chinh cua Anthropic, ra mat nam 2023. Hien tai (2026) dang o the he <b>Claude 4</b>."))
    el.append(sub_header("Claude vs ChatGPT — Khac nhau the nao?"))
    headers = ["Tieu chi", "Claude (Anthropic)", "ChatGPT (OpenAI)"]
    rows = [
        ["Do an toan", "Thiet ke tu dau voi tieu chi an toan", "Them vao sau"],
        ["Van phong", "Tu nhien, co chieu sau, it 'robot' hon", "Doi khi cung, cong thuc"],
        ["Ly luan dai", "Rat manh — xu ly tai lieu dai tot", "Tot nhung doi khi lac de"],
        ["Code", "Xuat sac", "Xuat sac"],
        ["Phan tich", "Manh, trung thuc ve gioi han", "Tot"],
        ["Gia", "Free / Pro $20/thang", "Free / Plus $20/thang"],
    ]
    w = (PAGE_W - 2*MARGIN - 4*mm)
    el.append(make_table(headers, rows, col_widths=[40*mm, (w-40*mm)/2, (w-40*mm)/2]))
    el.append(callout("Tom lai: Ca hai deu manh. Claude thuong duoc danh gia cao hon ve van ban chuyen sau, phan tich, va do trung thuc — Claude hay noi thang khi khong chac, thay vi bia."))
    return el

# ── Section 3 — Nguyen Ly ─────────────────────────────────────────────────────
def section3():
    el = [section_header("3", "Nguyen Ly Hoat Dong", "")]
    el.append(sub_header("Claude 'nghi' nhu the nao? (Khong can biet ky thuat)"))
    el.append(p("Hay tuong tuong Claude nhu nguoi da <b>doc hang ty cau van</b> trong suot qua trinh training (huan luyen). Tu do, Claude hoc duoc:"))
    el += bullet(["Khi A thi thuong tiep theo la B",
                  "Cau hoi dang X thuong duoc tra loi theo cau truc Y",
                  "Van ban tot trong nhu the nao"])
    el.append(p("Khi ban go cau hoi, Claude <b>du doan tung tu tiep theo</b> theo xac suat cao nhat de tao ra cau tra loi co nghia. Khong co 'nao bo' that su — nhung ket qua tao ra rat giong voi suy nghi con nguoi."))
    el.append(sub_header("Context Window — 'Bo nho lam viec' cua Claude"))
    el.append(p("<b>Context window</b> la luong van ban Claude co the 'nhin thay' va xu ly trong 1 lan tro chuyen."))
    el.append(code_block(
        "Ban go:          [Cau hoi cua ban]\n"
        "Claude nhin thay: [Toan bo lich su hoi thoai tu dau den gio]\n"
        "→ Tra loi dua tren TAT CA context do"
    ))
    el.append(callout("Quan trong: Khi ban tat tab / mo cuoc tro chuyen moi → Claude quen het. Moi conversation la mot trang giay trang moi."))
    el.append(sub_header("Claude KHONG co kha nang:"))
    el += bullet([
        "<b>Nho ban</b> sau khi dong hoi thoai (tru khi dung tinh nang Memory)",
        "<b>Truy cap internet real-time</b> (tru khi duoc cai tool tim kiem)",
        "<b>Luu file vao may ban</b> tu dong",
        "<b>Tu hanh dong</b> ma khong co lenh tu ban",
    ])
    return el

# ── Section 4 — Cac Nen Tang ─────────────────────────────────────────────────
def section4():
    el = [section_header("4", "Cac Nen Tang Claude", "")]
    el.append(p("Claude khong chi co mot cach dung — co nhieu 'cua vao' khac nhau, phu hop voi nhu cau khac nhau. Phan nay giai thich ro tung nen tang."))

    # Overview diagram
    el.append(sub_header("Ban do tong quan"))
    el.append(code_block(
        "CLAUDE CO THE DUNG QUA:\n"
        "│\n"
        "├── claude.ai (Web)    → Trinh duyet web (ai cung dung duoc, khong cai gi)\n"
        "├── Claude Desktop     → App cai tren may Mac/Windows\n"
        "├── Claude Code        → Cong cu cho lap trinh vien (chay trong terminal)\n"
        "│       ├── CLI (terminal)\n"
        "│       ├── Web: claude.ai/code\n"
        "│       └── IDE Extension (VS Code, JetBrains)\n"
        "└── Cowork             → Moi truong lam viec day du xay tren Claude Code"
    ))

    # Claude.ai Web
    el.append(sub2_header("claude.ai (Web) — Danh cho moi nguoi"))
    el.append(p("<b>La gi:</b> Trang web tai claude.ai — cach don gian nhat de dung Claude. Mo trinh duyet, go claude.ai, dang nhap la xong."))
    el += bullet([
        "Chat hoi dap, viet van ban, phan tich",
        "Upload file (PDF, Word, Excel, anh) de Claude doc",
        "Tao <b>Projects</b> (workspace) de luu ngu canh tai su dung",
        "Dung tren moi thiet bi: laptop, dien thoai, may tinh bang",
    ])
    el.append(p("<b>Gioi han:</b> Chi la chat — khong the tu dong hoa, khong ket noi sau voi email/lich, khong thao tac file tren may ban."))
    el.append(sp(2))

    # Claude Desktop
    el.append(sub2_header("Claude Desktop — App may tinh"))
    el.append(p("<b>La gi:</b> Ung dung cai dat tren may tinh (Mac hoac Windows), giao dien giong claude.ai nhung chay nhu mot app rieng."))
    headers = ["Tieu chi", "Claude.ai Web", "Claude Desktop"]
    rows = [
        ["Can mo trinh duyet", "Co", "Khong (app doc lap)"],
        ["Giao dien", "Giong nhau", "Giong nhau"],
        ["Tinh nang", "Nhu nhau", "Nhu nhau + tich hop MCP"],
        ["Offline", "Khong", "Khong (van can internet)"],
        ["MCP Tools", "Khong", "Co the cai them"],
    ]
    w = PAGE_W - 2*MARGIN - 4*mm
    el.append(make_table(headers, rows, col_widths=[55*mm, (w-55*mm)/2, (w-55*mm)/2]))
    el.append(callout("<b>MCP (Model Context Protocol)</b> = Chuan ket noi cho phep Claude 'voi tay' sang cac app khac: Google Calendar, Gmail, Notion, Slack... Desktop cho phep cai them cac ket noi nay, con web thi khong."))

    # Claude Code
    el.append(sub2_header("Claude Code — Danh cho cong viec chuyen sau"))
    el.append(p("<b>La gi:</b> Phien ban Claude chay <b>trong terminal (cua so dong lenh)</b> cua may tinh — khong phai chat web thong thuong."))
    headers = ["claude.ai / Desktop", "Claude Code"]
    rows = [
        ["Chat qua giao dien web/app", "Chay truc tiep trong may tinh"],
        ["Claude chi tra loi van ban", "Claude thao tac duoc file that tren may ban"],
        ["Khong tu chay lenh", "Tu chay lenh, viet code, doc/sua file"],
        ["Khong nho project qua session", "Nho toan bo codebase/project"],
        ["Dung tay, tung cau", "Co the chay task dai tu dong"],
    ]
    w = PAGE_W - 2*MARGIN - 4*mm
    el.append(make_table(headers, rows, col_widths=[w/2, w/2]))
    el += bullet([
        "Doc toan bo thu muc file bao cao → tong hop thanh 1 file duy nhat",
        "Tu dong tao file Excel tu du lieu ban cung cap → luu thang vao may",
        "Chay script xu ly 1000 dong CSV ma khong can copy-paste tung phan",
    ])

    # Cowork
    el.append(sub2_header("Cowork — Moi Truong Lam Viec Day Du"))
    el.append(p("<b>La gi:</b> Cowork la mot <b>bo cau hinh va mo rong</b> xay tren nen Claude Code, bien Claude tu 'chatbot thong minh' thanh mot <b>tro ly lam viec thuc thu</b> duoc ket noi voi toan bo cong cu van phong."))
    el.append(callout("Hinh dung don gian: claude.ai = xe may di duoc. Cowork = xe may da duoc lap them GPS, hop chua do, ket noi Bluetooth, camera hanh trinh, tich hop app giao hang — cung mot 'dong co' nhung manh hon nhieu."))

    headers = ["Tinh nang", "claude.ai", "Claude Desktop", "Cowork"]
    rows = [
        ["Chat hoi dap",              "Co", "Co", "Co"],
        ["Doc/viet file tren may",    "Khong", "Khong", "Co"],
        ["Ket noi Gmail",             "Khong", "Co the", "Co"],
        ["Ket noi Google Calendar",   "Khong", "Co the", "Co"],
        ["Ket noi Google Drive",      "Khong", "Co the", "Co"],
        ["Memory (nho qua session)",  "Khong", "Khong", "Co"],
        ["Skills (lenh tat)",         "Khong", "Khong", "Co"],
        ["Chay task tu dong",         "Khong", "Khong", "Co"],
    ]
    w = PAGE_W - 2*MARGIN - 4*mm
    el.append(make_table(headers, rows, col_widths=[68*mm, (w-68*mm)/3, (w-68*mm)/3, (w-68*mm)/3]))

    # Memory & Skills
    el.append(sub2_header("Memory trong Cowork — Claude 'nho' ban"))
    el.append(p("Khi dung Cowork, Claude co he thong <b>memory file</b> — moi lan lam viec, Claude hoc them ve ban, luu lai: ban la ai, lam gi, can gi / feedback va so thich lam viec / cac du an dang chay / nguon tai lieu tham khao."))
    el.append(p("→ Lan sau mo lai, Claude <b>khong can ban giai thich lai tu dau</b>."))

    el.append(sub2_header("Skills trong Cowork — Lenh tat thong minh"))
    el.append(p("<b>Skills</b> la cac 'lenh chuyen dung' duoc lap trinh san de lam nhung viec phuc tap voi 1 lenh ngan. Go <b>/ten-skill</b> la Claude tu biet can lam gi."))
    headers = ["Skill", "Lenh", "Lam gi"]
    rows = [
        ["xlsx",     "/xlsx",     "Tao/sua file Excel chuyen nghiep"],
        ["pptx",     "/pptx",     "Tao slide PowerPoint"],
        ["html",     "/html",     "Tao bao cao HTML dep"],
        ["pdf",      "/pdf",      "Doc, tao, ghep file PDF"],
        ["okr",      "/okr",      "Xay OKR theo chuan"],
        ["schedule", "/schedule", "Dat lich chay task tu dong"],
    ]
    w = PAGE_W - 2*MARGIN - 4*mm
    el.append(make_table(headers, rows, col_widths=[35*mm, 30*mm, w-65*mm-4*mm]))

    # Projects vs Cowork
    el.append(sub2_header("Projects / Workspace trong claude.ai"))
    el.append(p("Ben trong claude.ai, ban co the tao <b>Projects</b> — mot khong gian rieng cho tung mang cong viec. Project cho phep: dat System Prompt co dinh, upload tai lieu nen (SOP, brand guide), tat ca hoi thoai trong Project deu ke thua ngu canh do."))

    headers = ["Tieu chi", "Projects (claude.ai)", "Cowork"]
    rows = [
        ["Ban chat",     "Khong gian chat co ngu canh co dinh", "Moi truong lam viec tich hop day du"],
        ["Memory",       "Trong project do thoi",               "Xuyen suot moi session"],
        ["Tools",        "Chat + upload file",                  "Ket noi Gmail, Calendar, Drive, tu dong hoa"],
        ["Skills",       "Khong co",                            "Co san hang chuc skill"],
        ["Tu dong hoa",  "Khong",                               "Co (schedule, cron)"],
        ["Thao tac file","Claude doc file ban upload",          "Claude doc/ghi file thang tren may ban"],
        ["Do phuc tap",  "Don gian, dung ngay",                 "Can setup, nhung manh hon nhieu"],
    ]
    w = PAGE_W - 2*MARGIN - 4*mm
    el.append(make_table(headers, rows, col_widths=[38*mm, (w-38*mm)/2, (w-38*mm)/2]))
    el.append(callout("Tom lai: Projects la nang cap nho cua claude.ai thuong. Cowork la buoc nhay vot — tu chatbot thanh tro ly lam viec tich hop thuc su."))

    # Decision guide
    el.append(sub_header("Chon nen tang nao?"))
    el.append(code_block(
        "Toi moi dung lan dau\n"
        "→ claude.ai (web)\n\n"
        "Toi dung Claude moi ngay, muon app rieng\n"
        "→ Claude Desktop\n\n"
        "Toi co nhieu mang cong viec, muon luu context\n"
        "→ claude.ai + Projects\n\n"
        "Toi la developer hoac muon Claude thao tac file truc tiep\n"
        "→ Claude Code (CLI)\n\n"
        "Toi muon Claude ket noi Gmail/Calendar/Drive, nho toi, chay task tu dong\n"
        "→ Cowork (lien he Khanh de duoc huong dan setup)"
    ))
    return el

# ── Section 5 — Bat Dau ───────────────────────────────────────────────────────
def section5():
    el = [section_header("5", "Bat Dau Dung Claude", "")]
    el.append(sub_header("Buoc 1 — Tao tai khoan"))
    el += bullet([
        "Vao <b>claude.ai</b> (tren trinh duyet bat ky)",
        "Nhan <b>Sign Up</b>",
        "Dang ky bang email hoac Google account",
        "Chon goi <b>Free</b> de bat dau (du dung cho hau het tac vu)",
    ])
    el.append(callout("<b>Goi Pro ($20/thang):</b> Dung nhieu hon, model manh hon (Opus), upload file lon hon — can nhac neu dung hang ngay cho cong viec."))
    el.append(sub_header("Buoc 2 — Giao dien co ban"))
    el.append(code_block(
        "+------------------------------------------+\n"
        "|  Claude                           [New]  |\n"
        "|------------------------------------------|\n"
        "| [Danh sach cac cuoc hoi thoai cu]        |\n"
        "|------------------------------------------|\n"
        "|                                          |\n"
        "|         Khu vuc tro chuyen               |\n"
        "|                                          |\n"
        "|------------------------------------------|\n"
        "|  [ Go cau hoi cua ban o day...    ]  [→] |\n"
        "+------------------------------------------+"
    ))
    el += bullet([
        "<b>New conversation:</b> Bat dau hoi thoai moi (Claude quen het lich su cu)",
        "<b>O go phia duoi:</b> Go yeu cau → Enter hoac nhan nut gui",
        "<b>Upload file:</b> Dinh kem PDF, Excel, Word, anh de Claude doc va phan tich",
    ])
    el.append(sub_header("Buoc 3 — Thu ngay"))
    el.append(p("Go thu cau nay de lam quen:"))
    el.append(code_block(
        "Xin chao! Toi vua moi bat dau dung Claude.\n"
        "Ban co the gioi thieu ngan gon ban co the\n"
        "giup gi cho toi trong cong viec van phong khong?"
    ))
    return el

# ── Section 6 — Prompt ────────────────────────────────────────────────────────
def section6():
    el = [section_header("6", "Cach Viet Prompt Hieu Qua", "")]
    el.append(p("<b>Prompt</b> = Lenh/cau hoi ban gui cho Claude. Viet prompt tot = Claude tra loi dung y hon, tiet kiem thoi gian hon."))
    el.append(sub_header("Cong thuc COAT (De nho)"))
    headers = ["Chu", "Y nghia", "Vi du"]
    rows = [
        ["<b>C</b>ontext",     "Boi canh la gi",        "Toi la team leader quan ly 5 nguoi..."],
        ["<b>O</b>bjective",   "Muc tieu muon dat",     "...can viet email tu choi ung vien..."],
        ["<b>A</b>udience",    "Doi tuong nhan",        "...gui cho ung vien da phong van..."],
        ["<b>T</b>one/Format", "Giong & dinh dang",     "...lich su, ngan gon duoi 100 tu"],
    ]
    w = PAGE_W - 2*MARGIN - 4*mm
    el.append(make_table(headers, rows, col_widths=[22*mm, 45*mm, w-67*mm-4*mm]))

    el.append(sub_header("So sanh Prompt kem vs tot"))
    # Bad prompt
    bad_tbl = Table(
        [[Paragraph("Prompt KEM", ParagraphStyle("bh", fontName="ArialUni",
                    fontSize=9, textColor=DANGER)),
          Paragraph("Claude khong biet email ve gi, gui cho ai, muc dich gi", ST["td"])]],
        colWidths=[35*mm, PAGE_W-2*MARGIN-39*mm],
    )
    bad_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), colors.HexColor("#FFF5F5")),
        ("BOX",           (0,0), (-1,-1), 1,   DANGER),
        ("LINEAFTER",     (0,0), (0,-1), 0.5, DANGER),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("ROUNDEDCORNERS",[4]),
    ]))
    el += [bad_tbl, sp(2)]
    el.append(code_block("viet email"))

    good_tbl = Table(
        [[Paragraph("Prompt TOT", ParagraphStyle("gh", fontName="ArialUni",
                    fontSize=9, textColor=SUCCESS)),
          Paragraph("Day du boi canh, muc tieu, doi tuong, giong van, gioi han do dai", ST["td"])]],
        colWidths=[35*mm, PAGE_W-2*MARGIN-39*mm],
    )
    good_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), colors.HexColor("#F0FDF4")),
        ("BOX",           (0,0), (-1,-1), 1,   SUCCESS),
        ("LINEAFTER",     (0,0), (0,-1), 0.5, SUCCESS),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("ROUNDEDCORNERS",[4]),
    ]))
    el += [good_tbl, sp(2)]
    el.append(code_block(
        "Toi dang lam HR tai cong ty logistics. Viet email\n"
        "tu choi lich su cho ung vien vi tri Operations\n"
        "Executive sau vong phong van. Ly do: ung vien\n"
        "thieu kinh nghiem thuc te. Giong van chuyen nghiep,\n"
        "am ap, khong vuot qua 120 tu. Tieng Viet."
    ))

    el.append(sub_header("5 ky thuat prompt pho bien"))
    techniques = [
        ("1. Giao vai (Role-playing)",
         "Ban la chuyen gia phan tich du lieu voi 10 nam kinh nghiem.\nHay review bang so lieu nay va chi ra cac diem bat thuong."),
        ("2. Cho vi du mau",
         "Tom tat noi dung cuoc hop theo format sau:\n- Quyet dinh: [...]\n- Action item: [Ai] lam [gi] truoc [ngay]\n- Van de con mo: [...]"),
        ("3. Yeu cau step-by-step",
         "Giai thich tung buoc cach doc bao cao P&L cho nguoi moi,\nkhong dung thuat ngu ky thuat phuc tap."),
        ("4. Phe binh & cai thien",
         "Day la email toi vua draft. Hay chi ra 3 diem yeu\nva de xuat cai thien cu the:\n[paste email vao]"),
        ("5. Hoi lai khi chua ung",
         "Cau tra loi truoc qua dai. Rut gon con 5 bullet\npoint chinh, moi cai toi da 1 dong."),
    ]
    for title, code in techniques:
        el.append(sub2_header(title))
        el.append(code_block(code))

    el.append(callout("<b>Meo quan trong:</b> Claude nho toan bo hoi thoai trong cung 1 tab. Ban co the noi 'sua lai doan 2', 'them vi du', 'dich sang tieng Anh' ma khong can giai thich lai tu dau."))
    return el

# ── Section 7 — Ap dung cong viec ────────────────────────────────────────────
def section7():
    el = [section_header("7", "Ap Dung Vao Cong Viec", "")]

    el.append(sub_header("7.1 Viet lach & Soan thao"))
    headers = ["Tac vu", "Prompt mau"]
    rows = [
        ["Viet email",           "Viet email [muc dich] gui [ai], giong [chuyen nghiep/than thien], duoi [X] tu"],
        ["Soan thong bao noi bo","Soan thong bao cho toan team ve [noi dung], format ngan gon duoi 200 tu"],
        ["Viet JD tuyen dung",   "Viet JD cho vi tri [ten vi tri], yeu cau [ky nang chinh], tai [cong ty/nganh]"],
        ["Tom tat tai lieu",     "Upload file PDF/Word + 'Tom tat tai lieu nay thanh 5 diem chinh'"],
    ]
    w = PAGE_W - 2*MARGIN - 4*mm
    el.append(make_table(headers, rows, col_widths=[45*mm, w-45*mm-4*mm]))

    el.append(sub_header("7.2 Phan tich & Bao cao"))
    rows = [
        ["Phan tich so lieu",     "Upload Excel + 'Phan tich xu huong, chi ra top 3 insight quan trong nhat'"],
        ["Root cause analysis",   "Du lieu: [chi so] giam [X%] trong [khoang thoi gian]. De xuat 5 nguyen nhan tiem an"],
        ["Tom tat cuoc hop",      "Paste noi dung meeting + 'Tom tat: Quyet dinh / Action item / Van de con mo'"],
        ["Chuan bi slide",        "Tao outline slide presentation ve [chu de], 10 slides, doi tuong la [ai]"],
    ]
    el.append(make_table(headers, rows, col_widths=[45*mm, w-45*mm-4*mm]))

    el.append(sub_header("7.3 Nghien cuu & Hoc tap"))
    rows = [
        ["Giai thich khai niem",  "Giai thich [khai niem] don gian nhu toi chua biet gi ve linh vuc nay"],
        ["So sanh lua chon",      "So sanh [option A] vs [option B] theo tieu chi: chi phi, thoi gian, rui ro"],
        ["Brainstorm y tuong",    "Brainstorm 10 cach de [muc tieu]. Sang tao, khong gioi han"],
        ["Chuan bi cau hoi PV",   "Tao 20 cau hoi phong van cho vi tri [ten vi tri], tap trung vao [ky nang X]"],
    ]
    el.append(make_table(headers, rows, col_widths=[45*mm, w-45*mm-4*mm]))

    el.append(sub_header("7.4 Use Cases cho Team Driver Management"))
    headers = ["Tinh huong", "Cach dung Claude"]
    rows = [
        ["Soan thong bao chinh sach moi cho tai xe",
         "Viet thong bao chinh sach [X] bang ngon ngu don gian, tai xe de hieu, duoi 150 chu"],
        ["Phan tich bao cao AR/FR tuan",
         "Upload bao cao + 'Tom tat va chi ra khu vuc nao can uu tien can thiep'"],
        ["Chuan bi noi dung hop team weekly",
         "Tao agenda hop team ops tuan, dua tren cac van de sau: [list van de]"],
        ["Viet script training tai xe moi",
         "Viet script giai thich quy trinh [X] cho tai xe moi, dung ngon ngu don gian, co vi du"],
        ["Phan tich feedback tai xe",
         "Paste feedback + 'Phan loai theo chu de, chi ra top 3 van de duoc de cap nhieu nhat'"],
    ]
    el.append(make_table(headers, rows, col_widths=[55*mm, w-55*mm-4*mm]))
    return el

# ── Section 8 — Gioi han ─────────────────────────────────────────────────────
def section8():
    el = [section_header("8", "Nhung Dieu Claude KHONG Lam Duoc", "")]
    el.append(sub_header("Claude co the noi sai — va ban can biet dieu nay"))
    el.append(p('Claude doi khi <b>"hallucinate"</b> (bia ra thong tin nghe co ve dung nhung sai). Dac biet voi:'))
    el += bullet([
        "So lieu cu the, thong ke (luon verify)",
        "Ten nguoi, ngay thang, su kien lich su cu the",
        "Thong tin phap ly, y te (khong dung thay cho chuyen gia)",
        "Thong tin moi sau ngay Claude duoc training (knowledge cutoff)",
    ])
    el.append(callout("<b>Nguyen tac vang:</b> Claude la <b>assistant thong minh</b>, khong phai <b>nguon su that</b>. Luon verify thong tin quan trong."))
    el.append(sub_header("Nen vs Khong nen dung Claude"))
    headers = ["NEN dung Claude", "KHONG dung Claude thay the"]
    rows = [
        ["Draft van ban, email, bao cao",       "Quyet dinh chien luoc quan trong (khong verify)"],
        ["Brainstorm y tuong",                  "So lieu tai chinh chinh xac (phai kiem tra)"],
        ["Tom tat tai lieu dai",                "Tu van phap ly, y te"],
        ["Giai thich khai niem",                "Thay the judgement cua con nguoi"],
        ["Viet code, cong thuc",                "Thong tin real-time (gia co phieu, tin tuc hom nay)"],
    ]
    w = PAGE_W - 2*MARGIN - 4*mm
    tbl_data = [[Paragraph("NEN dung Claude", ST["th"]),
                 Paragraph("KHONG dung Claude thay the", ST["th"])]]
    for r in rows:
        tbl_data.append([
            Paragraph(f"✓  {r[0]}", ParagraphStyle("ok", fontName="ArialUni",
                       fontSize=9, leading=13, textColor=SUCCESS)),
            Paragraph(f"✗  {r[1]}", ParagraphStyle("no", fontName="ArialUni",
                       fontSize=9, leading=13, textColor=DANGER)),
        ])
    tbl = Table(tbl_data, colWidths=[w/2, w/2])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0), BLUE),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, BG_GRAY]),
        ("GRID",          (0, 0), (-1, -1), 0.4, BORDER),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]))
    el += [tbl, sp(3)]
    return el

# ── Section 9 — Bao mat ──────────────────────────────────────────────────────
def section9():
    el = [section_header("9", "Bao Mat & Luu Y Quan Trong", "")]

    warn_tbl = Table(
        [[Paragraph("TUYET DOI KHONG chia se voi Claude:", ParagraphStyle("wt",
            fontName="ArialUni", fontSize=10, textColor=colors.HexColor("#7C2D12"))),]],
        colWidths=[PAGE_W-2*MARGIN],
    )
    warn_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), colors.HexColor("#FEF3C7")),
        ("BOX",           (0,0), (-1,-1), 1.5, colors.HexColor("#F59E0B")),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 12),
        ("ROUNDEDCORNERS",[6]),
    ]))
    el += [warn_tbl, sp(1)]
    el += bullet([
        "<b>Mat khau, tai khoan ngan hang</b>",
        "<b>Thong tin ca nhan nhay cam cua tai xe/khach hang</b> (CMND, SDT, dia chi nha)",
        "<b>Du lieu kinh doanh mat</b> (doanh thu noi bo, chien luoc chua cong bo)",
        "<b>Hop dong, thoa thuan bao mat</b>",
    ])
    el.append(sub_header("Tai sao?"))
    el.append(p("Khi ban go noi dung vao claude.ai, du lieu do duoc gui len server cua Anthropic. Mac du Anthropic co chinh sach bao mat tot, nhung <b>best practice</b> la khong dua thong tin nhay cam len bat ky nen tang AI cloud nao."))
    el.append(sub_header("Tips an toan khi dung cho cong viec"))
    el.append(code_block(
        "SAI: 'Phan tich du lieu tai xe cua Ahamove:\n"
        "       Nguyen Van A - SDT 0901234567 - AR 45%...'\n\n"
        "DUNG: 'Phan tich du lieu tai xe an danh:\n"
        "        Tai xe X - AR 45%, tai xe Y - AR 62%...\n"
        "        Chi ra pattern va de xuat cai thien.'"
    ))
    el.append(callout("<b>Anonymize (an danh hoa) truoc khi hoi</b> — thay ten that bang Tai xe A, B, C hoac dung ID gia."))
    return el

# ── Section 10 — Tu dien ─────────────────────────────────────────────────────
def section10():
    el = [section_header("10", "Tu Dien Thuat Ngu", "")]
    terms = [
        ("AI (Artificial Intelligence)", "Tri tue nhan tao — phan mem co kha nang xu ly ngon ngu va ly luan"),
        ("LLM (Large Language Model)", "'Mo hinh ngon ngu lon' — loai AI duoc train tren luong van ban khong lo. Claude va ChatGPT deu la LLM"),
        ("Prompt", "Cau lenh/cau hoi ban gui cho Claude"),
        ("Context Window", "'Bo nho lam viec' — luong text Claude xu ly duoc trong 1 hoi thoai"),
        ("Hallucination", "Khi AI tu bia ra thong tin sai nhung trinh bay tu tin nhu that"),
        ("Training / Training Data", "Qua trinh 'hoc' cua AI — doc hang ty tai lieu de hieu ngon ngu"),
        ("Knowledge Cutoff", "Ngay Claude ngung duoc cap nhat kien thuc moi (sau do khong biet tin tuc moi)"),
        ("Model", "Phien ban AI cu the. Claude co: Haiku (nhanh/nhe), Sonnet (can bang), Opus (manh nhat)"),
        ("Token", "Don vi do van ban cua AI. Gioi han context window tinh bang token"),
        ("Agent", "Claude duoc trang bi them tools (tim kiem web, doc file, chay code) de tu thuc hien tac vu phuc tap"),
        ("API", "Cach ket noi Claude vao phan mem/app khac (danh cho developer)"),
        ("Claude Code", "Phien ban Claude chay trong terminal/IDE, co the doc/ghi file that tren may tinh"),
        ("Claude Desktop", "App cai dat tren may Mac/Windows, giao dien nhu claude.ai nhung ho tro ket noi MCP"),
        ("Cowork", "Moi truong lam viec day du xay tren Claude Code — co Memory, Skills, ket noi Gmail/Calendar/Drive"),
        ("Projects (Workspace)", "Khong gian lam viec trong claude.ai — luu system prompt va tai lieu nen de dung lai nhieu lan"),
        ("MCP (Model Context Protocol)", "Chuan ket noi cho phep Claude 'voi tay' sang app khac: Google Workspace, Notion, Slack..."),
        ("Skills", "Lenh tat chuyen dung trong Cowork — go /ten-skill de Claude thuc hien task phuc tap theo quy trinh dinh san"),
        ("Memory", "He thong luu tru thong tin qua nhieu session trong Cowork — Claude nho ban la ai, so thich, du an dang chay"),
        ("Anthropic", "Cong ty tao ra Claude, thanh lap 2021 tai My, tap trung vao AI an toan"),
        ("System Prompt", "Lenh nen duoc cai san de dinh hinh cach Claude phan hoi (ban thuong khong thay)"),
    ]
    headers = ["Thuat ngu", "Giai thich don gian"]
    rows = [[t, d] for t, d in terms]
    w = PAGE_W - 2*MARGIN - 4*mm
    el.append(make_table(headers, rows, col_widths=[60*mm, w-60*mm-4*mm]))
    return el

# ── Closing page ──────────────────────────────────────────────────────────────
def closing_page():
    el = [sp(10)]
    tbl = Table(
        [[Paragraph("Bat Dau Ngay Hom Nay", ParagraphStyle("ct2",
            fontName="ArialUni", fontSize=18, leading=24,
            textColor=WHITE, alignment=TA_CENTER))]],
        colWidths=[PAGE_W - 2*MARGIN],
    )
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), ORANGE),
        ("TOPPADDING",    (0,0), (-1,-1), 16),
        ("BOTTOMPADDING", (0,0), (-1,-1), 16),
        ("ROUNDEDCORNERS",[10]),
    ]))
    el += [tbl, sp(6)]

    checklist_items = [
        "Tao tai khoan tai claude.ai",
        "Gui 1 cau hoi bat ky de lam quen giao dien",
        "Thu upload 1 file PDF/Word va hoi Claude tom tat",
        "Thu viet 1 email theo COAT formula",
        "Hoi Claude 1 dieu ban dang thac mac trong cong viec",
    ]
    cl_data = [[
        Paragraph("CHECKLIST 15 PHUT DAU TIEN", ParagraphStyle("clh",
            fontName="ArialUni", fontSize=11, textColor=BLUE)),
    ]]
    for item in checklist_items:
        cl_data.append([
            Paragraph(f"[ ]  {item}", ParagraphStyle("cli",
                fontName="ArialUni", fontSize=10, leading=18,
                textColor=TEXT_DARK, leftIndent=8)),
        ])
    cl_tbl = Table(cl_data, colWidths=[PAGE_W - 2*MARGIN - 4*mm])
    cl_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), BG_GRAY),
        ("BOX",           (0,0), (-1,-1), 0.5, BORDER),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 16),
        ("ROUNDEDCORNERS",[8]),
        ("LINEBELOW",     (0,0), (0,0), 0.5, BORDER),
    ]))
    el += [cl_tbl, sp(6)]

    el.append(callout("Cau hoi co dap an ro rang, khong nhay cam → Hoi Claude truoc\nCau hoi can judgement, context noi bo → Hoi dong nghiep/quan ly\nCau hoi quan trong → Claude draft truoc, dong nghiep review sau"))
    el += [sp(6), hr(ORANGE, 1.5), sp(3)]
    el.append(p("Tai lieu nay duoc soan boi Driver Management Team — Ahamove  |  2026-05-04", "footer"))
    el.append(p("Cau hoi hoac gop y: lien he Khanh — khanhlp@ahamove.com", "footer"))
    return el

# ── Build PDF ─────────────────────────────────────────────────────────────────
def build():
    out_path = os.path.join(
        os.path.dirname(__file__),
        "2026-05-claude-guide-for-team.pdf"
    )
    doc = SimpleDocTemplate(
        out_path,
        pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=14*mm, bottomMargin=14*mm,
        title="Claude AI — Huong Dan Toan Dien Cho Team",
        author="Ahamove Driver Management Team",
        subject="Claude AI Guide",
    )

    story = []
    story += cover_page()
    story += toc()
    story += section1()
    story += [PageBreak()]
    story += section2()
    story += [PageBreak()]
    story += section3()
    story += [PageBreak()]
    story += section4()
    story += [PageBreak()]
    story += section5()
    story += section6()
    story += [PageBreak()]
    story += section7()
    story += [PageBreak()]
    story += section8()
    story += section9()
    story += [PageBreak()]
    story += section10()
    story += [PageBreak()]
    story += closing_page()

    template = PageTemplate()
    doc.build(story, onFirstPage=lambda c, d: None, onLaterPages=template)
    print(f"PDF saved: {out_path}")
    return out_path

if __name__ == "__main__":
    build()
