---
name: analyze-slides
description: Performs semantic analysis on normalized input slides, grouping content into topic clusters and classifying slide categories.
---

# Analyze Slides Skill

## Purpose
Analyzes the semantic content of `NormalizedSourceDeck`, identifies topic clusters (e.g. SLA, CPO, Driver Tiering, Regional performance), and classifies slide intent.

## Input
- `NormalizedSourceDeck` (JSON)

## Execution Protocol
1. Group slides into logical topic clusters.
2. Classify each input slide category: `EXEC_SUMMARY`, `KPI_HEALTH`, `DIAGNOSTIC`, `STRATEGIC`, `PROCESS`, `ACTION_PLAN`.
3. Score the strategic weight of each slide based on metric urgency and target gaps.

## Output
- `AnalyzedSlides` (JSON)
