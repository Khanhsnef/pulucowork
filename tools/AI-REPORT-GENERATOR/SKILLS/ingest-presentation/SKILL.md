---
name: ingest-presentation
description: Ingests raw input presentation decks (PPTX, PDF, Google Slides) or data markdown and normalizes them into structured JSON format.
---

# Ingest Presentation Skill

## Purpose
Parses source files and extracts raw text, titles, structured tables, and key metric candidates into a standardized `NormalizedSourceDeck` schema.

## Input
- `source_path`: Path to file (.pptx, .pdf, .md)
- `slide_range`: Specified range (e.g. 1–30)

## Execution Protocol
1. Call `TOOLS/pptx-parser/parse_pptx.py` for `.pptx` files.
2. Read text, paragraph blocks, table headers & rows per slide.
3. Extract candidates for KPI metrics (values with `%`, `VND`, `k`, `x` units).
4. Assign slide numbers and validate total slide count.

## Output
- `NormalizedSourceDeck` (JSON)
