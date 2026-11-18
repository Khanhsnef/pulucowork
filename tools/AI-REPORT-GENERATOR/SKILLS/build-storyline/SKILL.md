---
name: build-storyline
description: Structures an executive narrative storyline using the Pyramid Principle and Situation-Complication-Resolution (S-C-R) framework.
---

# Build Storyline Skill

## Purpose
Transforms extracted insights into a cohesive executive storyline tailored to the target report slide count.

## Input
- `InsightCollection` (JSON)
- `target_slide_count` (e.g., 15 slides)

## Narrative Structure (Pyramid Principle)
1. **Executive Summary & Hero KPIs** (Chapter 1)
2. **Operational Health & SLA Metrics** (Chapter 2)
3. **Regional & Service Deep-Dives** (Chapter 3)
4. **Diagnostic Root-Causes & Bottlenecks** (Chapter 4)
5. **Capacity Planning & Action Plan** (Chapter 5)

## Output
- `Storyline` (JSON)
