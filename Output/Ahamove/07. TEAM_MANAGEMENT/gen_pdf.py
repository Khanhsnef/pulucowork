#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate Claude Guide PDF for Ahamove Driver Management Team — Tiếng Việt có dấu"""

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
import os

# ── Fonts ─────────────────────────────────────────────────────────────────────
FONT_PATH = "/Library/Fonts/Arial Unicode.ttf"
pdfmetrics.registerFont(TTFont("ArialUni", FONT_PATH))

# ── Brand Colors ───────────────────────────────────────────────────────────────
BLUE       = colors.HexColor("#0E4174")
ORANGE     = colors.HexColor("#FF7F32")
SUCCESS    = colors.HexColor("#10B981")
DANGER     = colors.HexColor("#EF4444")
BG_GRAY    = colors.HexColor("#F8FAFC")
BG_BLUE_LT = colors.HexColor("#EEF4FB")
BORDER     = colors.HexColor("#E2E8F0")
TEXT_DARK  = colors.HexColor("#1E293B")
TEXT_MID   = colors.HexColor("#475569")
TEXT_LIGHT = colors.HexColor("#94A3B8")
CODE_BG    = colors.HexColor("#F1F5F9")
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
    "h2"      : S("h2", fontSize=14, leading=20, textColor=WHITE,
                  spaceBefore=0, spaceAfter=0),
    "h3"      : S("h3", fontSize=11, leading=16, textColor=BLUE,
                  spaceBefore=8, spaceAfter=4),
    "h4"      : S("h4", fontSize=10, leading=15, textColor=ORANGE,
                  spaceBefore=6, spaceAfter=3),
    "body"    : S("body", fontSize=9.5, leading=15, textColor=TEXT_DARK,
                  spaceAfter=6, alignment=TA_JUSTIFY),
    "bullet"  : S("bullet", fontSize=9.5, leading=14, textColor=TEXT_DARK,
                  leftIndent=12, spaceAfter=3),
    "code"    : S("code", fontSize=8.5, leading=13, textColor=TEXT_DARK,
                  fontName="Courier", leftIndent=8, spaceBefore=4, spaceAfter=6),
    "callout" : S("callout", fontSize=9.5, leading=14, textColor=BLUE,
                  leftIndent=10, rightIndent=10, spaceBefore=4, spaceAfter=6),
    "toc_item": S("toc_item", fontSize=10, leading=18, textColor=TEXT_DARK,
                  leftIndent=8),
    "toc_num" : S("toc_num", fontSize=10, leading=18, textColor=ORANGE),
    "cover_sub": S("cover_sub", fontSize=11, leading=18, textColor=WHITE,
                   alignment=TA_CENTER),
    "footer"  : S("footer", fontSize=8, leading=10,
                  textColor=TEXT_LIGHT, alignment=TA_CENTER),
    "th"      : S("th", fontSize=9, leading=13, textColor=WHITE,
                  alignment=TA_CENTER),
    "td"      : S("td", fontSize=9, leading=13, textColor=TEXT_DARK, spaceAfter=0),
    "label"   : S("label", fontSize=8, leading=12, textColor=WHITE,
                  alignment=TA_CENTER),
}

# ── Helpers ────────────────────────────────────────────────────────────────────
def p(text, style="body"):
    return Paragraph(text, ST[style])

def sp(h=4):
    return Spacer(1, h * mm)

def hr(color=BORDER, thickness=0.5):
    return HRFlowable(width="100%", thickness=thickness, color=color,
                      spaceBefore=2*mm, spaceAfter=2*mm)

def section_header(number, title):
    tbl = Table(
        [[Paragraph(f"{number}. {title}", ST["h2"])]],
        colWidths=[PAGE_W - 2*MARGIN],
    )
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), BLUE),
        ("ROUNDEDCORNERS",[6]),
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

def bullets(items):
    return [Paragraph(f"• {item}", ST["bullet"]) for item in items]

def code_block(text):
    lines = text.strip().split("\n")
    content = "<br/>".join(
        l.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace(" ","&nbsp;")
        for l in lines
    )
    tbl = Table(
        [[Paragraph(content, ST["code"])]],
        colWidths=[PAGE_W - 2*MARGIN - 4*mm],
    )
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), CODE_BG),
        ("ROUNDEDCORNERS",[4]),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("BOX",           (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
    ]))
    return KeepTogether([tbl, sp(2)])

def callout(text, warn=False):
    icon = "⚠" if warn else "💡"
    bg  = colors.HexColor("#FEF3C7") if warn else BG_BLUE_LT
    bd  = colors.HexColor("#FCD34D") if warn else colors.HexColor("#93C5FD")
    tc  = colors.HexColor("#92400E") if warn else BLUE
    style = ParagraphStyle("cb", fontName="ArialUni", fontSize=9.5, leading=14,
                            textColor=tc, leftIndent=10, rightIndent=10)
    tbl = Table(
        [[Paragraph(f"{icon}  {text}", style)]],
        colWidths=[PAGE_W - 2*MARGIN - 4*mm],
    )
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), bg),
        ("ROUNDEDCORNERS",[4]),
        ("TOPPADDING",    (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("BOX",           (0,0), (-1,-1), 1, bd),
    ]))
    return KeepTogether([tbl, sp(2)])

def make_table(headers, rows, col_widths=None):
    usable = PAGE_W - 2*MARGIN - 4*mm
    if col_widths is None:
        col_widths = [usable / len(headers)] * len(headers)
    data = [[Paragraph(h, ST["th"]) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), ST["td"]) for c in row])
    tbl = Table(data, colWidths=col_widths, repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), BLUE),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, BG_GRAY]),
        ("GRID",          (0,0), (-1,-1), 0.4, BORDER),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 7),
        ("RIGHTPADDING",  (0,0), (-1,-1), 7),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("ROUNDEDCORNERS",[4]),
    ]))
    return KeepTogether([tbl, sp(3)])

def badge(text, color=BLUE):
    tbl = Table([[Paragraph(text, ST["label"])]], colWidths=[60*mm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), color),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("ROUNDEDCORNERS",[8]),
    ]))
    return tbl

# ── Page Template ──────────────────────────────────────────────────────────────
def page_template(canvas_obj, doc):
    canvas_obj.saveState()
    w, h = A4
    canvas_obj.setFillColor(BLUE)
    canvas_obj.rect(0, h - 10*mm, w, 10*mm, fill=1, stroke=0)
    canvas_obj.setFillColor(ORANGE)
    canvas_obj.rect(0, h - 11.5*mm, w, 1.5*mm, fill=1, stroke=0)
    canvas_obj.setFillColor(WHITE)
    canvas_obj.setFont("ArialUni", 7.5)
    canvas_obj.drawString(MARGIN, h - 6.5*mm, "AHAMOVE  •  DRIVER MANAGEMENT TEAM")
    canvas_obj.setFont("ArialUni", 7)
    canvas_obj.drawRightString(w - MARGIN, h - 6.5*mm, "Claude AI — Hướng Dẫn Toàn Diện")
    canvas_obj.setFillColor(BG_GRAY)
    canvas_obj.rect(0, 0, w, 10*mm, fill=1, stroke=0)
    canvas_obj.setFillColor(BORDER)
    canvas_obj.rect(0, 10*mm, w, 0.5, fill=1, stroke=0)
    canvas_obj.setFillColor(TEXT_LIGHT)
    canvas_obj.setFont("ArialUni", 7.5)
    canvas_obj.drawString(MARGIN, 3.5*mm, "khanhlp@ahamove.com  •  2026-05-04")
    canvas_obj.drawRightString(w - MARGIN, 3.5*mm, f"Trang {doc.page}")
    canvas_obj.restoreState()

# ── Cover Page ─────────────────────────────────────────────────────────────────
def cover_page():
    el = []
    title_tbl = Table(
        [[Paragraph("CLAUDE AI", ParagraphStyle("ct", fontName="ArialUni",
            fontSize=40, leading=50, textColor=WHITE, alignment=TA_CENTER))]],
        colWidths=[PAGE_W - 2*MARGIN],
    )
    title_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), BLUE),
        ("TOPPADDING",    (0,0), (-1,-1), 26),
        ("BOTTOMPADDING", (0,0), (-1,-1), 26),
        ("ROUNDEDCORNERS",[12]),
    ]))
    sub_tbl = Table(
        [[Paragraph("Hướng Dẫn Toàn Diện Cho Team", ST["cover_sub"])]],
        colWidths=[PAGE_W - 2*MARGIN],
    )
    sub_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), colors.HexColor("#0A2E56")),
        ("TOPPADDING",    (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("ROUNDEDCORNERS",[8]),
    ]))
    el += [sp(20), title_tbl, sp(4), sub_tbl, sp(8)]

    tag_data = [[
        badge("Dành cho người mới bắt đầu", BLUE),
        badge("10 Phần Chi Tiết", ORANGE),
        badge("Ứng dụng thực tế", SUCCESS),
    ]]
    tag_tbl = Table(tag_data, colWidths=[66*mm, 56*mm, 56*mm])
    tag_tbl.setStyle(TableStyle([
        ("ALIGN",        (0,0), (-1,-1), "CENTER"),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING",  (0,0), (-1,-1), 3),
        ("RIGHTPADDING", (0,0), (-1,-1), 3),
    ]))
    el += [tag_tbl, sp(12)]

    meta = [
        ["Dành cho",  "Thành viên team chưa từng dùng AI / Claude"],
        ["Mục tiêu",  "Hiểu Claude là gì, dùng được ngay, áp dụng vào công việc"],
        ["Cập nhật",  "2026-05-04"],
        ["Biên soạn", "Khanh — Driver Management Leader, Ahamove"],
    ]
    meta_data = [[
        Paragraph(k, ParagraphStyle("mk", fontName="ArialUni", fontSize=9, textColor=ORANGE)),
        Paragraph(v, ParagraphStyle("mv", fontName="ArialUni", fontSize=9, textColor=TEXT_DARK)),
    ] for k, v in meta]
    meta_tbl = Table(meta_data, colWidths=[38*mm, PAGE_W-2*MARGIN-42*mm])
    meta_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), BG_GRAY),
        ("BOX",           (0,0), (-1,-1), 0.5, BORDER),
        ("INNERGRID",     (0,0), (-1,-1), 0.3, BORDER),
        ("TOPPADDING",    (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("ROUNDEDCORNERS",[6]),
    ]))
    el += [meta_tbl, PageBreak()]
    return el

# ── Mục lục ───────────────────────────────────────────────────────────────────
def toc():
    items = [
        ("1",  "AI Là Gì? — Giải thích không cần kỹ thuật"),
        ("2",  "Claude Là Ai? — Anthropic Là Ai?"),
        ("3",  "Nguyên Lý Hoạt Động"),
        ("4",  "Các Nền Tảng Claude — Dùng ở đâu, khác gì nhau?"),
        ("5",  "Bắt Đầu Dùng Claude — Step by step"),
        ("6",  "Cách Viết Prompt Hiệu Quả"),
        ("7",  "Áp Dụng Vào Công Việc Thực Tế"),
        ("8",  "Những Điều Claude KHÔNG Làm Được"),
        ("9",  "Bảo Mật & Lưu Ý Quan Trọng"),
        ("10", "Từ Điển Thuật Ngữ"),
    ]
    header_tbl = Table(
        [[Paragraph("MỤC LỤC", ParagraphStyle("toch", fontName="ArialUni",
            fontSize=16, leading=22, textColor=WHITE, alignment=TA_CENTER))]],
        colWidths=[PAGE_W - 2*MARGIN],
    )
    header_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), BLUE),
        ("TOPPADDING",    (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("ROUNDEDCORNERS",[8]),
    ]))
    data = [[Paragraph(n, ST["toc_num"]), Paragraph(t, ST["toc_item"])] for n, t in items]
    tbl = Table(data, colWidths=[12*mm, PAGE_W-2*MARGIN-16*mm])
    tbl.setStyle(TableStyle([
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [WHITE, BG_GRAY]),
        ("TOPPADDING",     (0,0), (-1,-1), 7),
        ("BOTTOMPADDING",  (0,0), (-1,-1), 7),
        ("LEFTPADDING",    (0,0), (-1,-1), 8),
        ("BOX",            (0,0), (-1,-1), 0.5, BORDER),
        ("LINEBELOW",      (0,0), (-1,-2), 0.3, BORDER),
        ("VALIGN",         (0,0), (-1,-1), "MIDDLE"),
    ]))
    return [header_tbl, sp(4), tbl, PageBreak()]

# ── Phần 1 — AI là gì ─────────────────────────────────────────────────────────
def section1():
    el = [section_header("1", "AI Là Gì?")]
    el.append(p("Hãy nghĩ AI (Trí tuệ nhân tạo) như một <b>nhân viên đã đọc gần như toàn bộ internet</b> — sách, bài báo, code, tài liệu khoa học, Wikipedia, diễn đàn... — rồi học cách <b>trả lời câu hỏi, viết văn bản, phân tích dữ liệu và lý luận</b> dựa trên tất cả kiến thức đó."))
    el.append(p("Khác với phần mềm thông thường (bạn bấm nút → nó làm đúng 1 việc cố định), AI <b>hiểu ngôn ngữ tự nhiên</b> — tức là bạn nói chuyện bình thường với nó như nói chuyện với người."))
    el.append(sub_header("AI ≠ Robot trong phim"))
    rows = [
        ["AI có ý thức, cảm xúc như người",      "AI không có ý thức. Nó xử lý văn bản theo xác suất thống kê"],
        ["AI biết hết mọi thứ",                  "AI chỉ biết những gì đã được học. Có thể sai, có thể bịa"],
        ["AI sẽ thay thế toàn bộ con người",     "AI thay thế <b>tác vụ</b>, không thay thế <b>tư duy &amp; judgement</b>"],
        ["Phải biết code mới dùng được",         "Ai cũng dùng được — chỉ cần biết gõ chữ"],
    ]
    w = PAGE_W - 2*MARGIN - 4*mm
    el.append(make_table(["Điều nhiều người nghĩ", "Thực tế"], rows,
                         col_widths=[80*mm, w-80*mm]))
    return el

# ── Phần 2 — Claude là ai ─────────────────────────────────────────────────────
def section2():
    el = [section_header("2", "Claude Là Ai? Anthropic Là Ai?")]
    el.append(sub_header("Anthropic — Công ty tạo ra Claude"))
    el.append(p("<b>Anthropic</b> là công ty AI thành lập năm 2021 tại Mỹ, tách ra từ OpenAI (công ty tạo ChatGPT). Anthropic tập trung vào <b>AI an toàn và đáng tin cậy</b> — triết lý của họ là tạo ra AI giúp ích cho con người mà không gây hại."))
    el.append(p("<b>Claude</b> là sản phẩm AI chính của Anthropic, ra mắt năm 2023. Hiện tại (2026) đang ở thế hệ <b>Claude 4</b>."))
    el.append(sub_header("Claude vs ChatGPT — Khác nhau thế nào?"))
    rows = [
        ["Độ an toàn",  "Thiết kế từ đầu với tiêu chí an toàn", "Thêm vào sau"],
        ["Văn phong",   "Tự nhiên, có chiều sâu, ít 'robot' hơn", "Đôi khi cứng, công thức"],
        ["Lý luận dài", "Rất mạnh — xử lý tài liệu dài tốt",    "Tốt nhưng đôi khi lạc đề"],
        ["Code",        "Xuất sắc",                              "Xuất sắc"],
        ["Phân tích",   "Mạnh, trung thực về giới hạn",          "Tốt"],
        ["Giá",         "Free / Pro $20/tháng",                  "Free / Plus $20/tháng"],
    ]
    w = PAGE_W - 2*MARGIN - 4*mm
    el.append(make_table(["Tiêu chí", "Claude (Anthropic)", "ChatGPT (OpenAI)"], rows,
                         col_widths=[38*mm, (w-38*mm)/2, (w-38*mm)/2]))
    el.append(callout("Tóm lại: Cả hai đều mạnh. Claude thường được đánh giá cao hơn về <b>văn bản chuyên sâu, phân tích, và độ trung thực</b> — Claude hay nói thẳng khi không chắc, thay vì bịa."))
    return el

# ── Phần 3 — Nguyên lý ────────────────────────────────────────────────────────
def section3():
    el = [section_header("3", "Nguyên Lý Hoạt Động")]
    el.append(sub_header("Claude 'nghĩ' như thế nào? (Không cần biết kỹ thuật)"))
    el.append(p("Hãy tưởng tượng Claude như người đã <b>đọc hàng tỷ câu văn</b> trong suốt quá trình training (huấn luyện). Từ đó, Claude học được:"))
    el += bullets(["Khi A thì thường tiếp theo là B",
                   "Câu hỏi dạng X thường được trả lời theo cấu trúc Y",
                   "Văn bản tốt trông như thế nào"])
    el.append(p("Khi bạn gõ câu hỏi, Claude <b>dự đoán từng từ tiếp theo</b> theo xác suất cao nhất để tạo ra câu trả lời có nghĩa. Không có 'não bộ' thật sự — nhưng kết quả tạo ra rất giống với suy nghĩ con người."))
    el.append(sub_header("Context Window — 'Bộ nhớ làm việc' của Claude"))
    el.append(p("<b>Context window</b> là lượng văn bản Claude có thể 'nhìn thấy' và xử lý trong 1 lần trò chuyện."))
    el.append(code_block(
        "Bạn gõ:           [Câu hỏi của bạn]\n"
        "Claude nhìn thấy: [Toàn bộ lịch sử hội thoại từ đầu đến giờ]\n"
        "→ Trả lời dựa trên TẤT CẢ context đó"
    ))
    el.append(callout("Quan trọng: Khi bạn tắt tab / mở cuộc trò chuyện mới → Claude quên hết. Mỗi conversation là một trang giấy trắng mới."))
    el.append(sub_header("Claude KHÔNG có khả năng:"))
    el += bullets([
        "<b>Nhớ bạn</b> sau khi đóng hội thoại (trừ khi dùng tính năng Memory)",
        "<b>Truy cập internet real-time</b> (trừ khi được cài tool tìm kiếm)",
        "<b>Lưu file vào máy bạn</b> tự động",
        "<b>Tự hành động</b> mà không có lệnh từ bạn",
    ])
    return el

# ── Phần 4 — Các nền tảng ─────────────────────────────────────────────────────
def section4():
    el = [section_header("4", "Các Nền Tảng Claude")]
    el.append(p("Claude không chỉ có một cách dùng — có nhiều 'cửa vào' khác nhau, phù hợp với nhu cầu khác nhau. Phần này giải thích rõ từng nền tảng để bạn chọn đúng công cụ cho đúng việc."))
    el.append(sub_header("Bản đồ tổng quan"))
    el.append(code_block(
        "CLAUDE CÓ THỂ DÙNG QUA:\n"
        "│\n"
        "├── claude.ai (Web)   → Trình duyệt web (ai cũng dùng được, không cài gì)\n"
        "├── Claude Desktop    → App cài trên máy Mac/Windows\n"
        "├── Claude Code       → Công cụ chuyên sâu (chạy trong terminal)\n"
        "│       ├── CLI (terminal)\n"
        "│       ├── Web: claude.ai/code\n"
        "│       └── IDE Extension (VS Code, JetBrains)\n"
        "└── Pulu-workspace            → Môi trường làm việc đầy đủ xây trên Claude Code"
    ))

    # claude.ai web
    el.append(sub2_header("claude.ai (Web) — Dành cho mọi người"))
    el.append(p("<b>Là gì:</b> Trang web tại claude.ai — cách đơn giản nhất để dùng Claude. Mở trình duyệt, gõ claude.ai, đăng nhập là xong."))
    el += bullets([
        "Chat hỏi đáp, viết văn bản, phân tích",
        "Upload file (PDF, Word, Excel, ảnh) để Claude đọc",
        "Tạo <b>Projects</b> (workspace) để lưu ngữ cảnh tái sử dụng",
        "Dùng trên mọi thiết bị: laptop, điện thoại, máy tính bảng",
    ])
    el.append(p("<b>Giới hạn:</b> Chỉ là chat — không thể tự động hóa, không kết nối sâu với email/lịch, không thao tác file trên máy bạn."))
    el.append(sp(2))

    # Claude Desktop
    el.append(sub2_header("Claude Desktop — App máy tính"))
    el.append(p("<b>Là gì:</b> Ứng dụng cài đặt trên máy tính (Mac hoặc Windows), giao diện giống claude.ai nhưng chạy như một app riêng. Tải về tại claude.ai/download."))
    w = PAGE_W - 2*MARGIN - 4*mm
    rows = [
        ["Cần mở trình duyệt", "Có", "Không (app độc lập)"],
        ["Giao diện",          "Giống nhau", "Giống nhau"],
        ["Tính năng",          "Như nhau", "Như nhau + tích hợp MCP"],
        ["Offline",            "Không", "Không (vẫn cần internet)"],
        ["MCP Tools",          "Không", "Có thể cài thêm"],
    ]
    el.append(make_table(["Tiêu chí", "Claude.ai Web", "Claude Desktop"], rows,
                         col_widths=[55*mm, (w-55*mm)/2, (w-55*mm)/2]))
    el.append(callout("<b>MCP (Model Context Protocol)</b> = Chuẩn kết nối cho phép Claude 'với tay' sang các app khác: Google Calendar, Gmail, Notion, Slack... Desktop cho phép cài thêm các kết nối này, còn web thì không."))

    # Claude Code
    el.append(sub2_header("Claude Code — Dành cho công việc chuyên sâu"))
    el.append(p("<b>Là gì:</b> Phiên bản Claude chạy <b>trong terminal (cửa sổ dòng lệnh)</b> của máy tính — không phải chat web thông thường."))
    rows = [
        ["Chat qua giao diện web/app",       "Chạy trực tiếp trong máy tính"],
        ["Claude chỉ trả lời văn bản",       "Claude <b>thao tác được file thật</b> trên máy bạn"],
        ["Không tự chạy lệnh",               "Tự chạy lệnh, viết code, đọc/sửa file"],
        ["Không nhớ project qua session",    "Nhớ toàn bộ codebase/project"],
        ["Dùng tay, từng câu",               "Có thể chạy task dài tự động"],
    ]
    el.append(make_table(["claude.ai / Desktop", "Claude Code"], rows,
                         col_widths=[w/2, w/2]))
    el += bullets([
        "Đọc toàn bộ thư mục file báo cáo → tổng hợp thành 1 file duy nhất",
        "Tự động tạo file Excel từ dữ liệu bạn cung cấp → lưu thẳng vào máy",
        "Chạy script xử lý 1000 dòng CSV mà không cần copy-paste từng phần",
    ])

    # Pulu-workspace
    el.append(sub2_header("Pulu-workspace — Môi Trường Làm Việc Đầy Đủ"))
    el.append(p("<b>Là gì:</b> Pulu-workspace là một <b>bộ cấu hình và mở rộng</b> xây trên nền Claude Code, biến Claude từ 'chatbot thông minh' thành một <b>trợ lý làm việc thực thụ</b> được kết nối với toàn bộ công cụ văn phòng."))
    el.append(callout("Hình dung đơn giản: claude.ai = xe máy đi được. Pulu-workspace = xe máy đã được lắp thêm GPS, hộp chứa đồ, kết nối Bluetooth, camera hành trình, tích hợp app giao hàng — cùng một 'động cơ' nhưng mạnh hơn nhiều."))
    rows = [
        ["Chat hỏi đáp",                "Có",       "Có",       "Có"],
        ["Đọc/viết file trên máy",      "Không",    "Không",    "Có"],
        ["Kết nối Gmail",               "Không",    "Có thể",   "Có"],
        ["Kết nối Google Calendar",     "Không",    "Có thể",   "Có"],
        ["Kết nối Google Drive",        "Không",    "Có thể",   "Có"],
        ["Memory (nhớ qua session)",    "Không",    "Không",    "Có"],
        ["Skills (lệnh tắt)",           "Không",    "Không",    "Có"],
        ["Chạy task tự động",           "Không",    "Không",    "Có"],
    ]
    el.append(make_table(["Tính năng", "claude.ai", "Claude Desktop", "Pulu-workspace"], rows,
                         col_widths=[68*mm, (w-68*mm)/3, (w-68*mm)/3, (w-68*mm)/3]))

    el.append(sub2_header("Memory trong Pulu-workspace — Claude 'nhớ' bạn"))
    el.append(p("Khi dùng Pulu-workspace, Claude có hệ thống <b>memory file</b> — mỗi lần làm việc, Claude học thêm về bạn và lưu lại: bạn là ai, làm gì, cần gì / feedback và sở thích làm việc / các dự án đang chạy / nguồn tài liệu tham khảo."))
    el.append(p("→ Lần sau mở lại, Claude <b>không cần bạn giải thích lại từ đầu</b>."))

    el.append(sub2_header("Skills trong Pulu-workspace — Lệnh tắt thông minh"))
    el.append(p("<b>Skills</b> là các 'lệnh chuyên dụng' được lập trình sẵn để làm những việc phức tạp với 1 lệnh ngắn. Gõ <b>/tên-skill</b> là Claude tự biết cần làm gì."))
    rows = [
        ["xlsx",     "/xlsx",     "Tạo/sửa file Excel chuyên nghiệp"],
        ["pptx",     "/pptx",     "Tạo slide PowerPoint"],
        ["html",     "/html",     "Tạo báo cáo HTML đẹp"],
        ["pdf",      "/pdf",      "Đọc, tạo, ghép file PDF"],
        ["okr",      "/okr",      "Xây OKR theo chuẩn"],
        ["schedule", "/schedule", "Đặt lịch chạy task tự động"],
    ]
    el.append(make_table(["Skill", "Lệnh", "Làm gì"], rows,
                         col_widths=[35*mm, 30*mm, w-65*mm-4*mm]))

    # Projects vs Pulu-workspace
    el.append(sub2_header("Projects / Workspace trong claude.ai"))
    el.append(p("Bên trong claude.ai, bạn có thể tạo <b>Projects</b> — một không gian riêng cho từng mảng công việc. Project cho phép: đặt System Prompt cố định, upload tài liệu nền (SOP, brand guide), tất cả hội thoại trong Project đều kế thừa ngữ cảnh đó."))
    rows = [
        ["Bản chất",     "Không gian chat có ngữ cảnh cố định",  "Môi trường làm việc tích hợp đầy đủ"],
        ["Memory",       "Trong project đó thôi",                "Xuyên suốt mọi session"],
        ["Tools",        "Chat + upload file",                   "Kết nối Gmail, Calendar, Drive, tự động hóa"],
        ["Skills",       "Không có",                             "Có sẵn hàng chục skill"],
        ["Tự động hóa",  "Không",                                "Có (schedule, cron)"],
        ["Thao tác file","Claude đọc file bạn upload",           "Claude đọc/ghi file thẳng trên máy bạn"],
        ["Độ phức tạp",  "Đơn giản, dùng ngay",                  "Cần setup, nhưng mạnh hơn nhiều"],
    ]
    el.append(make_table(["Tiêu chí", "Projects (claude.ai)", "Pulu-workspace"], rows,
                         col_widths=[38*mm, (w-38*mm)/2, (w-38*mm)/2]))
    el.append(callout("Tóm lại: Projects là <b>nâng cấp nhỏ</b> của claude.ai thông thường. Pulu-workspace là <b>bước nhảy vọt</b> — từ chatbot thành trợ lý làm việc tích hợp thực sự."))

    el.append(sub_header("Chọn nền tảng nào?"))
    el.append(code_block(
        "Tôi mới dùng lần đầu\n"
        "→ claude.ai (web)\n\n"
        "Tôi dùng Claude mỗi ngày, muốn app riêng\n"
        "→ Claude Desktop\n\n"
        "Tôi có nhiều mảng công việc, muốn lưu context\n"
        "→ claude.ai + Projects\n\n"
        "Tôi là developer hoặc muốn Claude thao tác file trực tiếp\n"
        "→ Claude Code (CLI)\n\n"
        "Tôi muốn Claude kết nối Gmail/Calendar/Drive, nhớ tôi, chạy task tự động\n"
        "→ Pulu-workspace (liên hệ Khanh để được hướng dẫn setup)"
    ))
    return el

# ── Phần 5 — Bắt đầu ─────────────────────────────────────────────────────────
def section5():
    el = [section_header("5", "Bắt Đầu Dùng Claude")]
    el.append(sub_header("Bước 1 — Tạo tài khoản"))
    el += bullets([
        "Vào <b>claude.ai</b> (trên trình duyệt bất kỳ)",
        "Nhấn <b>Sign Up</b>",
        "Đăng ký bằng email hoặc Google account",
        "Chọn gói <b>Free</b> để bắt đầu (đủ dùng cho hầu hết tác vụ)",
    ])
    el.append(callout("<b>Gói Pro ($20/tháng):</b> Dùng nhiều hơn, model mạnh hơn (Opus), upload file lớn hơn — cân nhắc nếu dùng hàng ngày cho công việc."))
    el.append(sub_header("Bước 2 — Giao diện cơ bản"))
    el.append(code_block(
        "+------------------------------------------+\n"
        "|  Claude                           [New]  |\n"
        "|------------------------------------------|\n"
        "| [Danh sách các cuộc hội thoại cũ]        |\n"
        "|------------------------------------------|\n"
        "|                                          |\n"
        "|         Khu vực trò chuyện               |\n"
        "|                                          |\n"
        "|------------------------------------------|\n"
        "|  [ Gõ câu hỏi của bạn ở đây...    ] [→] |\n"
        "+------------------------------------------+"
    ))
    el += bullets([
        "<b>New conversation:</b> Bắt đầu hội thoại mới (Claude quên hết lịch sử cũ)",
        "<b>Ô gõ phía dưới:</b> Gõ yêu cầu → Enter hoặc nhấn nút gửi",
        "<b>Upload file:</b> Đính kèm PDF, Excel, Word, ảnh để Claude đọc và phân tích",
    ])
    el.append(sub_header("Bước 3 — Thử ngay"))
    el.append(code_block(
        "Xin chào! Tôi vừa mới bắt đầu dùng Claude.\n"
        "Bạn có thể giới thiệu ngắn gọn bạn có thể\n"
        "giúp gì cho tôi trong công việc văn phòng không?"
    ))
    return el

# ── Phần 6 — Prompt ───────────────────────────────────────────────────────────
def section6():
    el = [section_header("6", "Cách Viết Prompt Hiệu Quả")]
    el.append(p("<b>Prompt</b> = Lệnh/câu hỏi bạn gửi cho Claude. Viết prompt tốt = Claude trả lời đúng ý hơn, tiết kiệm thời gian hơn."))
    el.append(sub_header("Công thức COAT (Dễ nhớ)"))
    w = PAGE_W - 2*MARGIN - 4*mm
    rows = [
        ["<b>C</b>ontext",     "Bối cảnh là gì",      "Tôi là team leader quản lý 5 người..."],
        ["<b>O</b>bjective",   "Mục tiêu muốn đạt",   "...cần viết email từ chối ứng viên..."],
        ["<b>A</b>udience",    "Đối tượng nhận",       "...gửi cho ứng viên đã phỏng vấn..."],
        ["<b>T</b>one/Format", "Giọng &amp; định dạng","...lịch sự, ngắn gọn dưới 100 từ"],
    ]
    el.append(make_table(["Chữ", "Ý nghĩa", "Ví dụ"], rows,
                         col_widths=[22*mm, 44*mm, w-66*mm-4*mm]))

    el.append(sub_header("So sánh Prompt kém vs tốt"))
    # Bad
    bad_data = [[
        Paragraph("Prompt KÉM", ParagraphStyle("bh", fontName="ArialUni",
                  fontSize=9, textColor=DANGER)),
        Paragraph("Claude không biết email về gì, gửi cho ai, mục đích gì", ST["td"]),
    ]]
    bad_tbl = Table(bad_data, colWidths=[35*mm, w-35*mm])
    bad_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), colors.HexColor("#FFF5F5")),
        ("BOX",           (0,0), (-1,-1), 1, DANGER),
        ("LINEAFTER",     (0,0), (0,-1), 0.5, DANGER),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("ROUNDEDCORNERS",[4]),
    ]))
    el += [bad_tbl, sp(1)]
    el.append(code_block("viết email"))

    # Good
    good_data = [[
        Paragraph("Prompt TỐT", ParagraphStyle("gh", fontName="ArialUni",
                  fontSize=9, textColor=SUCCESS)),
        Paragraph("Đầy đủ bối cảnh, mục tiêu, đối tượng, giọng văn, giới hạn độ dài", ST["td"]),
    ]]
    good_tbl = Table(good_data, colWidths=[35*mm, w-35*mm])
    good_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), colors.HexColor("#F0FDF4")),
        ("BOX",           (0,0), (-1,-1), 1, SUCCESS),
        ("LINEAFTER",     (0,0), (0,-1), 0.5, SUCCESS),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("ROUNDEDCORNERS",[4]),
    ]))
    el += [good_tbl, sp(1)]
    el.append(code_block(
        "Tôi đang làm HR tại công ty logistics. Viết email\n"
        "từ chối lịch sự cho ứng viên vị trí Operations\n"
        "Executive sau vòng phỏng vấn. Lý do: ứng viên\n"
        "thiếu kinh nghiệm thực tế. Giọng văn chuyên nghiệp,\n"
        "ấm áp, không vượt quá 120 từ. Tiếng Việt."
    ))

    el.append(sub_header("5 kỹ thuật prompt phổ biến"))
    techniques = [
        ("1. Giao vai (Role-playing)",
         "Bạn là chuyên gia phân tích dữ liệu với 10 năm kinh nghiệm.\nHãy review bảng số liệu này và chỉ ra các điểm bất thường."),
        ("2. Cho ví dụ mẫu",
         "Tóm tắt nội dung cuộc họp theo format sau:\n- Quyết định: [...]\n- Action item: [Ai] làm [gì] trước [ngày]\n- Vấn đề còn mở: [...]"),
        ("3. Yêu cầu step-by-step",
         "Giải thích từng bước cách đọc báo cáo P&L cho người mới,\nkhông dùng thuật ngữ kỹ thuật phức tạp."),
        ("4. Phê bình & cải thiện",
         "Đây là email tôi vừa draft. Hãy chỉ ra 3 điểm yếu\nvà đề xuất cải thiện cụ thể:\n[paste email vào]"),
        ("5. Hỏi lại khi chưa ưng",
         "Câu trả lời trước quá dài. Rút gọn còn 5 bullet\npoint chính, mỗi cái tối đa 1 dòng."),
    ]
    for title, code in techniques:
        el.append(sub2_header(title))
        el.append(code_block(code))
    el.append(callout("<b>Mẹo quan trọng:</b> Claude nhớ toàn bộ hội thoại trong cùng 1 tab. Bạn có thể nói 'sửa lại đoạn 2', 'thêm ví dụ', 'dịch sang tiếng Anh' mà không cần giải thích lại từ đầu."))
    return el

# ── Phần 7 — Áp dụng ─────────────────────────────────────────────────────────
def section7():
    el = [section_header("7", "Áp Dụng Vào Công Việc")]
    w = PAGE_W - 2*MARGIN - 4*mm

    el.append(sub_header("7.1 Viết lách & Soạn thảo"))
    rows = [
        ["Viết email",            "Viết email [mục đích] gửi [ai], giọng [chuyên nghiệp/thân thiện], dưới [X] từ"],
        ["Soạn thông báo nội bộ", "Soạn thông báo cho toàn team về [nội dung], format ngắn gọn dưới 200 từ"],
        ["Viết JD tuyển dụng",    "Viết JD cho vị trí [tên vị trí], yêu cầu [kỹ năng chính], tại [công ty/ngành]"],
        ["Tóm tắt tài liệu",      "Upload file PDF/Word + 'Tóm tắt tài liệu này thành 5 điểm chính'"],
    ]
    el.append(make_table(["Tác vụ", "Prompt mẫu"], rows, col_widths=[45*mm, w-45*mm]))

    el.append(sub_header("7.2 Phân tích & Báo cáo"))
    rows = [
        ["Phân tích số liệu",   "Upload Excel + 'Phân tích xu hướng, chỉ ra top 3 insight quan trọng nhất'"],
        ["Root cause analysis", "Dữ liệu: [chỉ số] giảm [X%] trong [khoảng thời gian]. Đề xuất 5 nguyên nhân tiềm ẩn"],
        ["Tóm tắt cuộc họp",    "Paste nội dung meeting + 'Tóm tắt: Quyết định / Action item / Vấn đề còn mở'"],
        ["Chuẩn bị slide",      "Tạo outline slide về [chủ đề], 10 slides, đối tượng là [ai]"],
    ]
    el.append(make_table(["Tác vụ", "Prompt mẫu"], rows, col_widths=[45*mm, w-45*mm]))

    el.append(sub_header("7.3 Nghiên cứu & Học tập"))
    rows = [
        ["Giải thích khái niệm",    "Giải thích [khái niệm] đơn giản như tôi chưa biết gì về lĩnh vực này"],
        ["So sánh lựa chọn",        "So sánh [option A] vs [option B] theo tiêu chí: chi phí, thời gian, rủi ro"],
        ["Brainstorm ý tưởng",      "Brainstorm 10 cách để [mục tiêu]. Sáng tạo, không giới hạn"],
        ["Chuẩn bị câu hỏi PV",     "Tạo 20 câu hỏi phỏng vấn cho vị trí [tên], tập trung vào [kỹ năng X]"],
    ]
    el.append(make_table(["Tác vụ", "Prompt mẫu"], rows, col_widths=[45*mm, w-45*mm]))

    el.append(sub_header("7.4 Use Cases cho Team Driver Management"))
    rows = [
        ["Soạn thông báo chính sách mới cho tài xế",
         "Viết thông báo chính sách [X] bằng ngôn ngữ đơn giản, tài xế dễ hiểu, dưới 150 chữ"],
        ["Phân tích báo cáo AR/FR tuần",
         "Upload báo cáo + 'Tóm tắt và chỉ ra khu vực nào cần ưu tiên can thiệp'"],
        ["Chuẩn bị nội dung họp team weekly",
         "Tạo agenda họp team ops tuần, dựa trên các vấn đề sau: [list vấn đề]"],
        ["Viết script training tài xế mới",
         "Viết script giải thích quy trình [X] cho tài xế mới, dùng ngôn ngữ đơn giản, có ví dụ"],
        ["Phân tích feedback tài xế",
         "Paste feedback + 'Phân loại theo chủ đề, chỉ ra top 3 vấn đề được đề cập nhiều nhất'"],
    ]
    el.append(make_table(["Tình huống", "Cách dùng Claude"], rows,
                         col_widths=[55*mm, w-55*mm]))
    return el

# ── Phần 8 — Giới hạn ────────────────────────────────────────────────────────
def section8():
    el = [section_header("8", "Những Điều Claude KHÔNG Làm Được")]
    el.append(sub_header("Claude có thể nói sai — và bạn cần biết điều này"))
    el.append(p('Claude đôi khi <b>"hallucinate"</b> (bịa ra thông tin nghe có vẻ đúng nhưng sai). Đặc biệt với:'))
    el += bullets([
        "Số liệu cụ thể, thống kê (luôn verify)",
        "Tên người, ngày tháng, sự kiện lịch sử cụ thể",
        "Thông tin pháp lý, y tế (không dùng thay cho chuyên gia)",
        "Thông tin mới sau ngày Claude được training (knowledge cutoff)",
    ])
    el.append(callout("<b>Nguyên tắc vàng:</b> Claude là <b>assistant thông minh</b>, không phải <b>nguồn sự thật</b>. Luôn verify thông tin quan trọng."))
    el.append(sub_header("Nên vs Không nên dùng Claude"))
    w = PAGE_W - 2*MARGIN - 4*mm
    rows_ok  = ["Draft văn bản, email, báo cáo", "Brainstorm ý tưởng",
                "Tóm tắt tài liệu dài", "Giải thích khái niệm", "Viết code, công thức"]
    rows_no  = ["Quyết định chiến lược quan trọng (không verify)",
                "Số liệu tài chính chính xác (phải kiểm tra)",
                "Tư vấn pháp lý, y tế",
                "Thay thế judgement của con người",
                "Thông tin real-time (giá cổ phiếu, tin tức hôm nay)"]
    data = [[Paragraph("NÊN dùng Claude", ST["th"]),
             Paragraph("KHÔNG dùng Claude thay thế", ST["th"])]]
    for ok, no in zip(rows_ok, rows_no):
        data.append([
            Paragraph(f"✓  {ok}",
                      ParagraphStyle("ok", fontName="ArialUni", fontSize=9,
                                     leading=13, textColor=SUCCESS)),
            Paragraph(f"✗  {no}",
                      ParagraphStyle("no", fontName="ArialUni", fontSize=9,
                                     leading=13, textColor=DANGER)),
        ])
    tbl = Table(data, colWidths=[w/2, w/2])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), BLUE),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, BG_GRAY]),
        ("GRID",          (0,0), (-1,-1), 0.4, BORDER),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
    el += [tbl, sp(3)]
    return el

# ── Phần 9 — Bảo mật ─────────────────────────────────────────────────────────
def section9():
    el = [section_header("9", "Bảo Mật & Lưu Ý Quan Trọng")]
    warn_tbl = Table(
        [[Paragraph("TUYỆT ĐỐI KHÔNG chia sẻ với Claude:",
                    ParagraphStyle("wt", fontName="ArialUni", fontSize=10,
                                   textColor=colors.HexColor("#7C2D12")))]],
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
    el += bullets([
        "<b>Mật khẩu, tài khoản ngân hàng</b>",
        "<b>Thông tin cá nhân nhạy cảm của tài xế/khách hàng</b> (CMND, SĐT, địa chỉ nhà)",
        "<b>Dữ liệu kinh doanh mật</b> (doanh thu nội bộ, chiến lược chưa công bố)",
        "<b>Hợp đồng, thỏa thuận bảo mật</b>",
    ])
    el.append(sub_header("Tại sao?"))
    el.append(p("Khi bạn gõ nội dung vào claude.ai, dữ liệu đó được gửi lên server của Anthropic. Mặc dù Anthropic có chính sách bảo mật tốt, nhưng <b>best practice</b> là không đưa thông tin nhạy cảm lên bất kỳ nền tảng AI cloud nào."))
    el.append(sub_header("Tips an toàn khi dùng cho công việc"))
    el.append(code_block(
        "SAI: 'Phân tích dữ liệu tài xế của Ahamove:\n"
        "       Nguyễn Văn A - SĐT 0901234567 - AR 45%...'\n\n"
        "ĐÚNG: 'Phân tích dữ liệu tài xế ẩn danh:\n"
        "        Tài xế X - AR 45%, tài xế Y - AR 62%...\n"
        "        Chỉ ra pattern và đề xuất cải thiện.'"
    ))
    el.append(callout("<b>Anonymize (ẩn danh hóa) trước khi hỏi</b> — thay tên thật bằng Tài xế A, B, C hoặc dùng ID giả."))
    return el

# ── Phần 10 — Từ điển ────────────────────────────────────────────────────────
def section10():
    el = [section_header("10", "Từ Điển Thuật Ngữ")]
    terms = [
        ("AI (Artificial Intelligence)",    "Trí tuệ nhân tạo — phần mềm có khả năng xử lý ngôn ngữ và lý luận"),
        ("LLM (Large Language Model)",      "'Mô hình ngôn ngữ lớn' — loại AI được train trên lượng văn bản khổng lồ. Claude và ChatGPT đều là LLM"),
        ("Prompt",                          "Câu lệnh/câu hỏi bạn gửi cho Claude"),
        ("Context Window",                  "'Bộ nhớ làm việc' — lượng text Claude xử lý được trong 1 hội thoại"),
        ("Hallucination",                   "Khi AI tự bịa ra thông tin sai nhưng trình bày tự tin như thật"),
        ("Training / Training Data",        "Quá trình 'học' của AI — đọc hàng tỷ tài liệu để hiểu ngôn ngữ"),
        ("Knowledge Cutoff",                "Ngày Claude ngừng được cập nhật kiến thức mới (sau đó không biết tin tức mới)"),
        ("Model",                           "Phiên bản AI cụ thể. Claude có: Haiku (nhanh/nhẹ), Sonnet (cân bằng), Opus (mạnh nhất)"),
        ("Token",                           "Đơn vị đo văn bản của AI. Giới hạn context window tính bằng token"),
        ("Agent",                           "Claude được trang bị thêm tools (tìm kiếm web, đọc file, chạy code) để tự thực hiện tác vụ phức tạp"),
        ("API",                             "Cách kết nối Claude vào phần mềm/app khác (dành cho developer)"),
        ("Claude Code",                     "Phiên bản Claude chạy trong terminal/IDE, có thể đọc/ghi file thật trên máy tính"),
        ("Claude Desktop",                  "App cài đặt trên máy Mac/Windows, giao diện như claude.ai nhưng hỗ trợ kết nối MCP"),
        ("Pulu-workspace",                          "Môi trường làm việc đầy đủ xây trên Claude Code — có Memory, Skills, kết nối Gmail/Calendar/Drive"),
        ("Projects (Workspace)",            "Không gian làm việc trong claude.ai — lưu system prompt và tài liệu nền để dùng lại nhiều lần"),
        ("MCP (Model Context Protocol)",    "Chuẩn kết nối cho phép Claude 'với tay' sang app khác: Google Workspace, Notion, Slack..."),
        ("Skills",                          "Lệnh tắt chuyên dụng trong Pulu-workspace — gõ /tên-skill để Claude thực hiện task phức tạp theo quy trình định sẵn"),
        ("Memory",                          "Hệ thống lưu trữ thông tin qua nhiều session trong Pulu-workspace — Claude nhớ bạn là ai, sở thích, dự án đang chạy"),
        ("Anthropic",                       "Công ty tạo ra Claude, thành lập 2021 tại Mỹ, tập trung vào AI an toàn"),
        ("System Prompt",                   "Lệnh nền được cài sẵn để định hình cách Claude phản hồi (bạn thường không thấy)"),
    ]
    w = PAGE_W - 2*MARGIN - 4*mm
    el.append(make_table(["Thuật ngữ", "Giải thích đơn giản"],
                         [[t, d] for t, d in terms],
                         col_widths=[58*mm, w-58*mm]))
    return el

# ── Trang kết ─────────────────────────────────────────────────────────────────
def closing_page():
    el = [sp(10)]
    tbl = Table(
        [[Paragraph("Bắt Đầu Ngay Hôm Nay!", ParagraphStyle("ct2",
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

    cl_items = [
        "Tạo tài khoản tại claude.ai",
        "Gửi 1 câu hỏi bất kỳ để làm quen giao diện",
        "Thử upload 1 file PDF/Word và hỏi Claude tóm tắt",
        "Thử viết 1 email theo công thức COAT",
        "Hỏi Claude 1 điều bạn đang thắc mắc trong công việc",
    ]
    cl_data = [[Paragraph("CHECKLIST 15 PHÚT ĐẦU TIÊN",
                          ParagraphStyle("clh", fontName="ArialUni", fontSize=11,
                                         textColor=BLUE))]]
    for item in cl_items:
        cl_data.append([Paragraph(f"[ ]  {item}",
                                  ParagraphStyle("cli", fontName="ArialUni",
                                                 fontSize=10, leading=18,
                                                 textColor=TEXT_DARK, leftIndent=8))])
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
    el.append(callout(
        "Câu hỏi có đáp án rõ ràng, không nhạy cảm → Hỏi Claude trước\n"
        "Câu hỏi cần judgement, context nội bộ → Hỏi đồng nghiệp/quản lý\n"
        "Câu hỏi quan trọng → Claude draft trước, đồng nghiệp review sau"
    ))
    el += [sp(6), hr(ORANGE, 1.5), sp(3)]
    el.append(p("Tài liệu được soạn bởi Driver Management Team — Ahamove  |  2026-05-04", "footer"))
    el.append(p("Câu hỏi hoặc góp ý: liên hệ Khanh — khanhlp@ahamove.com", "footer"))
    return el

# ── Build ─────────────────────────────────────────────────────────────────────
def build():
    out_path = os.path.join(os.path.dirname(__file__),
                            "2026-05-claude-guide-for-team.pdf")
    doc = SimpleDocTemplate(
        out_path, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=14*mm, bottomMargin=14*mm,
        title="Claude AI — Hướng Dẫn Toàn Diện Cho Team",
        author="Ahamove Driver Management Team",
        subject="Claude AI Guide",
    )
    story = []
    story += cover_page()
    story += toc()
    story += section1();  story += [PageBreak()]
    story += section2();  story += [PageBreak()]
    story += section3();  story += [PageBreak()]
    story += section4();  story += [PageBreak()]
    story += section5()
    story += section6();  story += [PageBreak()]
    story += section7();  story += [PageBreak()]
    story += section8()
    story += section9();  story += [PageBreak()]
    story += section10(); story += [PageBreak()]
    story += closing_page()

    doc.build(story, onFirstPage=lambda c, d: None, onLaterPages=page_template)
    print(f"✓ PDF saved: {out_path}")

if __name__ == "__main__":
    build()
