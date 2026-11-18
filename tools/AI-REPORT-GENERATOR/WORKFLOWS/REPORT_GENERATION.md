# REPORT GENERATION WORKFLOW — 10-PHASE PIPELINE

This document defines the exact step-by-step pipeline executed when generating an executive report.

---

## 📋 WORKFLOW OVERVIEW & INPUT ARGUMENTS

### Input Parameters:
- `source_path`: Path to input deck (.pptx, .pdf) or raw operational data markdown.
- `slide_range`: e.g. `1-30` or `all`.
- `target_slide_count`: Target number of report slides (e.g., `15`).
- `domain_profile`: e.g., `PROFILES/dm-monthly-report.md`.
- `visual_style`: e.g., `STYLES/operations.json`.
- `output_dir`: Path to output folder (default `OUTPUT/<report_name>/`).

---

## ⚙️ 10-PHASE PIPELINE EXECUTION STEPS

### PHASE 1 — INGEST
- **Skill**: `SKILLS/ingest-presentation/SKILL.md`
- **Tool**: `TOOLS/pptx-parser/parse_pptx.py` or PDF parser.
- **Input**: `source_path`, `slide_range`.
- **Output**: `NormalizedSourceDeck` (JSON schema in `SPEC/DATA_SCHEMA.md`).

### PHASE 2 — ANALYZE
- **Skill**: `SKILLS/analyze-slides/SKILL.md`
- **Process**: Group slides by topic clusters, classify slide categories (Diagnostic, Strategic, Operational), assign strategic weights.
- **Output**: `AnalyzedSlides`.

### PHASE 3 — INSIGHT
- **Skill**: `SKILLS/extract-insights/SKILL.md`
- **Profile Context**: Load `domain_profile` (e.g. `dm-monthly-report.md`).
- **Process**: Detect KPI target gaps, root causes, business impact, and strategic recommendations.
- **Output**: `InsightCollection`.

### PHASE 4 — STORYLINE
- **Skill**: `SKILLS/build-storyline/SKILL.md`
- **Process**: Build narrative arc following Pyramid Principle (Executive Summary $\rightarrow$ KPI Overview $\rightarrow$ Regional Breakdowns $\rightarrow$ Root Causes $\rightarrow$ Capacity & Action Plan).
- **Output**: `Storyline`.

### PHASE 5 — PLAN
- **Skill**: `SKILLS/plan-slides/SKILL.md`
- **Process**: Map storyline chapters into `target_slide_count` specific slide units, assigning each slide to 1 of 7 Master Templates in `TEMPLATES/`.
- **Output**: `ReportPlan`.

### PHASE 6 — DESIGN
- **Skill**: `SKILLS/design-slides/SKILL.md`
- **Style Theme**: Load `visual_style` (`STYLES/operations.json`).
- **Process**: Generate rich layout JSON containing takeaways, hero KPIs, floating glass cards, icon badges, and data tables.
- **Output**: `SlideJSON`.

### PHASE 7 — RENDER
- **Skill**: `SKILLS/render-slides/SKILL.md`
- **Tool**: `TOOLS/renderer/render_html.py`
- **Process**: Compile `SlideJSON` into interactive HTML 16:9 presentation (`report.html`).
- **Output**: HTML file + PNG/PDF snapshots.

### PHASE 8 — QA & VALIDATION
- **Skill**: `SKILLS/visual-qa/SKILL.md`
- **Rules**: Execute `SPEC/QA_RULES.md` against rendered HTML & data contracts.
- **Output**: `QAReport` (STATUS = PASS or FAIL).

### PHASE 9 — AUTO-FIX LOOP
- **Logic**:
  ```python
  if qa_report.overall_status != "PASS" and iteration_count < 3:
      apply_auto_fixes(qa_report.recommended_fixes)
      re_render_slides()
      run_qa_check()
  ```
- **Output**: Validated `SlideJSON` & re-rendered HTML.

### PHASE 10 — EXPORT
- **Skill**: `SKILLS/export-report/SKILL.md`
- **Tools**: `TOOLS/pptx-exporter/export_pptx.py`, `TOOLS/chatgpt-exporter/export_chatgpt_prompt.py`
- **Output**:
  - `OUTPUT/<report_name>/report.html` (Interactive Live Edit Mode)
  - `OUTPUT/<report_name>/report-editable.pptx` (Native 16:9 Editable PPTX)
  - `OUTPUT/<report_name>/report.pdf` (High-res PDF)
  - `OUTPUT/<report_name>/CHATGPT_CANVAS_PROMPT.md` (ChatGPT Canvas Prompt)

