---
name: visual-qa
description: Evaluates rendered HTML slides for text overflow, card overcrowding, contrast compliance, and data traceability.
---

# Visual QA Skill

## Purpose
Validates rendered slides against `SPEC/QA_RULES.md`. Triggers auto-fix loop if status != `PASS` (Max 3 iterations).

## Checks
1. Data Hallucination / Source Traceability Check.
2. Text Overflow / Boundary Bounding Box Check.
3. Card Density Check ($\le 4$ cards per slide).
4. Contrast Ratio Check ($\ge 4.5:1$).

## Output
- `QAReport` (JSON)
