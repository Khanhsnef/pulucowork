import sys
import pptx
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_SHAPE_TYPE

# Theme Palette: Executive Light Mode
BG_LIGHT = RGBColor(248, 250, 252)         # #F8FAFC Modern Off-White Canvas
CARD_WHITE = RGBColor(255, 255, 255)       # Pure White Card Fill
CARD_BORDER = RGBColor(203, 213, 225)      # #CBD5E1 Clean Border Stroke
CARD_BORDER_SOFT = RGBColor(226, 232, 240) # #E2E8F0 Soft Border

TEXT_DARK = RGBColor(15, 23, 42)           # #0F172A Deep Slate Heading Text
TEXT_BODY = RGBColor(51, 65, 85)           # #334155 High-readability Charcoal Body
TEXT_MUTED = RGBColor(100, 116, 139)       # #64748B Subdued Silver/Slate
TEXT_WHITE = RGBColor(255, 255, 255)

ORANGE_BRAND = RGBColor(255, 102, 0)       # #FF6600 Ahamove Vivid Orange
NAVY_HEADER = RGBColor(15, 23, 42)         # #0F172A Deep Navy Header
TAB_INACTIVE = RGBColor(226, 232, 240)      # #E2E8F0 Light Slate Inactive Tab

RED_ACCENT = RGBColor(220, 38, 38)         # #DC2626 Red Accent Text
RED_PILL = RGBColor(254, 226, 226)         # #FEE2E2 Light Red Fill

AMBER_ACCENT = RGBColor(217, 119, 6)       # #D97706 Amber Accent Text
AMBER_PILL = RGBColor(254, 243, 199)       # #FEF3C7 Light Amber Fill

GREEN_ACCENT = RGBColor(5, 150, 105)       # #059669 Green Accent Text
GREEN_PILL = RGBColor(209, 250, 229)       # #D1FAE5 Light Green Fill

FONT_NAME = "Helvetica Neue"

prs = pptx.Presentation('/Users/ts-1148/Desktop/Pulu-workspace/Data sources/BaoCao_ThangDM_T7_Core_v7_1.pptx')

def apply_font_family(shape, font_family=FONT_NAME):
    if not shape.has_text_frame:
        return
    for p in shape.text_frame.paragraphs:
        p.font.name = font_family
        for r in p.runs:
            r.font.name = font_family

def style_card(shape, fill_rgb, border_rgb=CARD_BORDER, line_width=1, make_rounded=True):
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_rgb
    if border_rgb:
        shape.line.color.rgb = border_rgb
        shape.line.width = Pt(line_width)
    else:
        shape.line.fill.background()
        
    if make_rounded and shape.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE:
        spPr = shape.element.spPr
        prstGeom = spPr.find('{http://schemas.openxmlformats.org/drawingml/2006/main}prstGeom')
        if prstGeom is not None and prstGeom.get('prst') == 'rect':
            prstGeom.set('prst', 'roundRect')

for slide_idx, slide in enumerate(prs.slides):
    # Set light canvas background
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = BG_LIGHT
    
    for shape in slide.shapes:
        apply_font_family(shape, FONT_NAME)
        
        # 1. Shape Styling
        if shape.shape_type in [MSO_SHAPE_TYPE.AUTO_SHAPE, MSO_SHAPE_TYPE.FREEFORM]:
            # Convert rectangles to rounded rectangles
            spPr = shape.element.spPr
            prstGeom = spPr.find('{http://schemas.openxmlformats.org/drawingml/2006/main}prstGeom')
            if prstGeom is not None and prstGeom.get('prst') == 'rect':
                prstGeom.set('prst', 'roundRect')

            if shape.fill.type == pptx.enum.dml.MSO_COLOR_TYPE.RGB:
                rgb = shape.fill.fore_color.rgb
                
                # Check for top nav tabs (Slides 4-7)
                if slide_idx in [3, 4, 5, 6] and shape.top and shape.top.inches < 1.0 and shape.height and shape.height.inches < 0.6 and shape.width and shape.width.inches > 1.5:
                    if rgb[0] > 200 or rgb[0] < 50: # active vs inactive tabs
                        if shape.left.inches < 3.0: # active tab
                            style_card(shape, ORANGE_BRAND, ORANGE_BRAND, 1)
                        else:
                            style_card(shape, TAB_INACTIVE, CARD_BORDER, 1)
                    continue

                # Main background cards / containers -> White with soft border
                if (rgb[0] > 200 and rgb[1] > 200 and rgb[2] > 200) or (rgb[0] < 50 and rgb[1] < 60 and rgb[2] < 140):
                    style_card(shape, CARD_WHITE, CARD_BORDER, 1)
                # Orange accent shapes
                elif rgb[0] > 220 and rgb[1] > 90 and rgb[2] < 50:
                    style_card(shape, ORANGE_BRAND, None, 0)
                # Red accent shapes
                elif rgb[0] > 200 and rgb[1] < 80 and rgb[2] < 80:
                    style_card(shape, RED_ACCENT, None, 0)
                # Green accent shapes
                elif rgb[0] < 50 and rgb[1] > 150 and rgb[2] < 100:
                    style_card(shape, GREEN_ACCENT, None, 0)

        # 2. Text Content Styling
        if shape.has_text_frame:
            txt = shape.text_frame.text.strip()
            
            # Default text color for body text in light mode
            for p in shape.text_frame.paragraphs:
                p.font.name = FONT_NAME
                for r in p.runs:
                    r.font.name = FONT_NAME
                    # Adjust text colors
                    if r.font.color and r.font.color.type == pptx.enum.dml.MSO_COLOR_TYPE.RGB:
                        c_rgb = r.font.color.rgb
                        # Light text converted to dark text for light cards
                        if c_rgb[0] > 180 and c_rgb[1] > 180 and c_rgb[2] > 180:
                            # Exception: Active Tab or Red/Orange badge fills
                            if slide_idx in [3, 4, 5, 6] and shape.top and shape.top.inches < 1.0 and shape.left and shape.left.inches < 3.0:
                                r.font.color.rgb = TEXT_WHITE
                            else:
                                r.font.color.rgb = TEXT_BODY
                        elif c_rgb[0] < 80 and c_rgb[1] < 80 and c_rgb[2] < 80:
                            r.font.color.rgb = TEXT_BODY
                    else:
                        r.font.color.rgb = TEXT_BODY
                        
            # Slide Header Title
            if shape.top and shape.top.inches < 1.0 and shape.height and shape.height.inches > 0.4:
                for p in shape.text_frame.paragraphs:
                    p.font.name = FONT_NAME
                    p.font.bold = True
                    for r in p.runs:
                        r.font.name = FONT_NAME
                        r.font.color.rgb = TEXT_DARK
                        
            # Category Kicker (top-left)
            if shape.top and shape.top.inches < 0.35 and shape.left and shape.left.inches < 1.0:
                for p in shape.text_frame.paragraphs:
                    p.font.name = FONT_NAME
                    p.font.bold = True
                    for r in p.runs:
                        r.font.name = FONT_NAME
                        r.font.color.rgb = ORANGE_BRAND
                        
            # Subtitle / Presenter info (top-right)
            if shape.top and shape.top.inches < 0.35 and shape.left and shape.left.inches > 7.0:
                for p in shape.text_frame.paragraphs:
                    p.font.name = FONT_NAME
                    for r in p.runs:
                        r.font.name = FONT_NAME
                        r.font.color.rgb = TEXT_MUTED

            # Inactive Tab Text (Slides 4-7)
            if slide_idx in [3, 4, 5, 6] and shape.top and shape.top.inches < 1.0 and shape.left and shape.left.inches > 2.8 and shape.width and shape.width.inches < 3.0:
                for p in shape.text_frame.paragraphs:
                    p.font.name = FONT_NAME
                    for r in p.runs:
                        r.font.name = FONT_NAME
                        r.font.color.rgb = TEXT_MUTED

            # Key Takeaway keyword accent
            if "Key Takeaway" in txt:
                for p in shape.text_frame.paragraphs:
                    for r in p.runs:
                        r.font.name = FONT_NAME
                        if "Key Takeaway" in r.text:
                            r.font.color.rgb = ORANGE_BRAND
                            r.font.bold = True
                        else:
                            r.font.color.rgb = TEXT_BODY

            # Highlights / Lowlights titles
            if txt in ["HIGHLIGHTS", "LOWLIGHTS", "ĐÃ LÀM GÌ (T7)", "TÁC ĐỘNG", "BƯỚC TIẾP THEO", "CẦN SUPPORT TỪ"]:
                for p in shape.text_frame.paragraphs:
                    p.font.name = FONT_NAME
                    p.font.bold = True
                    for r in p.runs:
                        r.font.name = FONT_NAME
                        if txt == "HIGHLIGHTS":
                            r.font.color.rgb = GREEN_ACCENT
                        elif txt in ["LOWLIGHTS", "TÁC ĐỘNG"]:
                            r.font.color.rgb = RED_ACCENT
                        else:
                            r.font.color.rgb = TEXT_DARK

            # Numbers / Stat Callouts in Card 1 (Slides 4-7)
            if slide_idx in [3, 4, 5, 6] and txt in ["~2x", "68.2%", "-10%", "2/9"]:
                for p in shape.text_frame.paragraphs:
                    p.font.name = FONT_NAME
                    p.font.size = Pt(38)
                    p.font.bold = True
                    for r in p.runs:
                        r.font.name = FONT_NAME
                        r.font.color.rgb = TEXT_DARK

        # 3. Tables (Slide 3 & Slide 9)
        if shape.has_table:
            table = shape.table
            for row_idx, row in enumerate(table.rows):
                for cell_idx, cell in enumerate(row.cells):
                    cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                    if row_idx == 0:
                        cell.fill.solid()
                        cell.fill.fore_color.rgb = NAVY_HEADER
                        for p in cell.text_frame.paragraphs:
                            p.alignment = PP_ALIGN.LEFT
                            p.font.name = FONT_NAME
                            p.font.bold = True
                            for r in p.runs:
                                r.font.name = FONT_NAME
                                r.font.color.rgb = TEXT_WHITE
                    else:
                        cell.fill.solid()
                        cell.fill.fore_color.rgb = CARD_WHITE if row_idx % 2 == 1 else BG_LIGHT
                        for p in cell.text_frame.paragraphs:
                            p.alignment = PP_ALIGN.LEFT
                            p.font.name = FONT_NAME
                            for r in p.runs:
                                r.font.name = FONT_NAME
                                txt_c = r.text.strip()
                                if "ĐỎ" in txt_c:
                                    r.font.color.rgb = RED_ACCENT
                                    r.font.bold = True
                                elif "VÀNG" in txt_c:
                                    r.font.color.rgb = AMBER_ACCENT
                                    r.font.bold = True
                                elif "XANH" in txt_c:
                                    r.font.color.rgb = GREEN_ACCENT
                                    r.font.bold = True
                                else:
                                    r.font.color.rgb = TEXT_BODY

output_file = '/Users/ts-1148/Desktop/Pulu-workspace/Data sources/BaoCao_ThangDM_T7_Core_v7_1.pptx'
prs.save(output_file)
print("Executive Light theme deck saved successfully:", output_file)
