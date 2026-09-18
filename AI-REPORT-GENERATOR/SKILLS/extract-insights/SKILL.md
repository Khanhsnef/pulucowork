---
name: extract-insights
description: Extracts business insights, KPI target gaps, root causes, business impact, and recommended action initiatives.
---

# Extract Insights Skill

## Purpose
Synthesizes business insights from analyzed slides, matching operational metrics against domain rules defined in `PROFILES/` (e.g. `PROFILES/dm-monthly-report.md`).

## Input
- `AnalyzedSlides` (JSON)
- `PROFILES/dm-monthly-report.md` (Domain Context)

## Execution Rules
- **Never invent data**: Every metric MUST cite its source slide ID.
- **Business Implication over Description**: State the operational impact, not just raw trend descriptions.
- Detect KPI gaps (Ontime, Occupancy, Non-offload, Driver Grade, CPO).
- Detect root causes (Peak-hour supply shortage, Mini-hub bottlenecks, Promo burn).

## Output
- `InsightCollection` (JSON)
