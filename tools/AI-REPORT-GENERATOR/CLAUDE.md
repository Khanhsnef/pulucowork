# 🤖 AHAMOVE AI REPORT GENERATOR — SYSTEM DIRECTIVES

This directory contains the full implementation of the **AI Report Generator System** designed specifically for Ahamove Driver Management (DM) operation reports led by Lê Phương Khanh.

## 📜 Official Design & Governance Rulebook
All report generation, slide layouts, content density calculations, and insight engines MUST strictly follow:
👉 [`SPEC/REPORT_DESIGN_RULEBOOK_v1.0.md`](file:///Users/ts-1148/Desktop/Pulu-workspace-v2/AI-REPORT-GENERATOR/SPEC/REPORT_DESIGN_RULEBOOK_v1.0.md) (30 Sections, 98 Rules, 10 Supreme Laws).

## ⚠️ SYSTEM MANDATES (STRICT RULES FOR AI ASSISTANTS)

When executing any report generation request (e.g., *"Generate a 15-slide executive report from slides 1–30"*):

1. **NEVER BYPASS SPECIFICATIONS**: All execution MUST follow:
   - `SPEC/MASTER_SPEC.md`
   - `WORKFLOWS/REPORT_GENERATION.md`
   - Relevant `SKILLS/*`
   - Relevant `SPEC/DESIGN_SYSTEM.md` & `SPEC/LAYOUT_RULES.md`
   - `SPEC/QA_RULES.md`

2. **ZERO DATA HALLUCINATION**:
   - Do NOT invent metrics, data points, dates, or cause-effect relationships.
   - Every metric MUST have a traceable `source_slide` ID or data reference.

3. **SINGLE DOMINANT MESSAGE PER SLIDE**:
   - Every generated slide MUST express exactly ONE core strategic message.
   - Secondary details belong in cards or tables, not mixed into header clutter.

4. **16:9 CANVAS & VISUAL BALANCE**:
   - Default aspect ratio is strictly 16:9 (1920 × 1080 px).
   - Enforce 40/60 Asymmetric Dual-Pane balance (40% visual anchors / 60% structured content).
   - Max card density: 4 cards per slide. Max table rows: 6 rows.

5. **EXPORT DELIVERABLES**:
   - Deliverables focus strictly on:
     1. Interactive 16:9 HTML Presentation (`report.html` with Live Edit Mode).
     2. Native Editable PowerPoint (`report-editable.pptx`).
     3. High-resolution PDF document (`report.pdf`).
     4. ChatGPT Canvas Prompt (`CHATGPT_CANVAS_PROMPT.md`).
   - No Google Slides cloud upload workflow required.

6. **QA & AUTO-FIX LOOP**:
   - All generated slides MUST pass Content QA (metric accuracy) and Visual QA (no text overflow, contrast, spacing).
   - If QA fails, run auto-fix loop (Max 3 iterations) before final export.

---

## 🔄 STANDARD REPORT GENERATION EXECUTION PIPELINE

When a user initiates a report generation command:
1. Load `SPEC/MASTER_SPEC.md` & `WORKFLOWS/REPORT_GENERATION.md`.
2. Determine active domain profile (e.g., `PROFILES/dm-monthly-report.md`) & visual style (e.g., `STYLES/operations.json`).
3. Execute Phase 1 through Phase 10 sequentially using specialized skills (`SKILLS/*`).
4. Invoke render engines & QA validator scripts.
5. Export final assets into `OUTPUT/` (HTML, PPTX, PDF, PNG).

---

**AI Report Generator System v2.0 | Ahamove Operations Architecture**
