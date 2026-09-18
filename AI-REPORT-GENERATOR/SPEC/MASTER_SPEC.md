# MASTER SPECIFICATION — AI REPORT GENERATOR SYSTEM

## 1. PRODUCT VISION & GOALS
The **AI Report Generator System** is an enterprise-grade, specification-driven framework designed to ingest raw presentation decks (PPTX, PDF, Google Slides) or operational data, perform deep semantic analysis, extract actionable insights, structure executive storylines, layout 16:9 slides, run automated content & visual QA, and export publication-ready assets (HTML Live Edit, Native PPTX, PDF, PNG).

Key Objectives:
- Eliminate redundant manual prompt specifications.
- Maintain 100% data integrity and metric traceability.
- Enforce executive 16:9 presentation aesthetics (Gemini/Canvas style: floating cards, giant callouts, clear visual flow).
- Provide automated quality assurance with iterative auto-fix capabilities.

---

## 2. SYSTEM ARCHITECTURE & LAYERS

The system follows a strict 10-layer architecture:

```
[Layer 1: Governance]    CLAUDE.md & SPEC/MASTER_SPEC.md
[Layer 2: Specifications] SPEC/ (DATA_SCHEMA, DESIGN_SYSTEM, LAYOUT_RULES, QA_RULES)
[Layer 3: Workflows]      WORKFLOWS/REPORT_GENERATION.md
[Layer 4: Profiles]       PROFILES/ (Domain context e.g. dm-monthly-report.md)
[Layer 5: Styles]         STYLES/ (*.json color/typography themes)
[Layer 6: Skills]         SKILLS/ (9 modular task instructions)
[Layer 7: Templates]      TEMPLATES/ (7 standard 16:9 executive layouts)
[Layer 8: Executables]    TOOLS/ & src/ (Python parsers, renderers, exporters)
[Layer 9: QA Engine]      Visual & Content Validation Scripts
[Layer 10: Outputs]       OUTPUT/ (.html, .pptx, .pdf, .png)
```

---

## 3. CORE PRINCIPLES & RULES

### 3.1 Data Integrity & Traceability
- **No Inventions**: Zero tolerance for hallucinated KPIs, dates, or causes.
- **Source Linkage**: Every metric in a synthesized slide must reference its `source_slide_id` or `data_row_id`.
- **Unit & Period Consistency**: Currency (VND), Percentages (%), time windows (WoW, DoD, MoM) must maintain precise formatting.

### 3.2 Executive Storytelling Architecture
- **Pyramid Principle**: Lead with the answer/insight (Executive Summary $\rightarrow$ Core KPIs $\rightarrow$ Diagnostic Root-Causes $\rightarrow$ Actionable Roadmap).
- **Situation-Complication-Resolution (S-C-R)** framework for operational issue slides.
- **Single Dominant Message**: Each slide header must contain a clear, action-oriented takeaway, not just a title (e.g., *"Ontime Rate Drops to 92% Due to Peak-Hour Driver Shortage in HCM North"*, not *"Ontime Report"*).

### 3.3 Visual Layout Standards
- **Aspect Ratio**: 16:9 widescreen (1920 × 1080 canvas size).
- **Asymmetric Focus**: 1 Primary Hero focal element (Giant KPI callout or main heatmap) 1.5x-2x larger than surrounding context cards.
- **Card-Based UI**: Content organized inside floating glass cards with 8-12px rounded corners and subtle 1px border strokes.
- **Breathability**: Minimum 0.25 inch (24px) padding inside cards and between grid items.

---

## 4. INPUT & OUTPUT CONTRACTS

### Input Types:
- Raw PPTX presentations (.pptx)
- Exported PDF decks (.pdf)
- Google Slides URL / Presentation ID
- Raw Markdown / Ops metric logs

### Output Deliverables:
- `OUTPUT/<report_name>/report.html` — Live In-Browser Editable HTML 16:9 Presentation.
- `OUTPUT/<report_name>/report-editable.pptx` — Native PowerPoint 16:9 Presentation with editable vector shapes, text boxes, and tables.
- `OUTPUT/<report_name>/report.pdf` — High-resolution PDF document.
- `OUTPUT/<report_name>/slides/` — Individual PNG slides (1920 × 1080).

---

## 5. ACCEPTANCE CRITERIA
1. **Traceability**: 100% of metrics in the final report map to ingested data.
2. **Visual Integrity**: 0 text overflows, 0 overlapping cards, minimum contrast ratio 4.5:1.
3. **Executive Clarity**: 100% of slides feature action-oriented takeaway titles.
4. **Editability**: `.pptx` file opens clean in Microsoft PowerPoint and Google Slides without formatting degradation.
