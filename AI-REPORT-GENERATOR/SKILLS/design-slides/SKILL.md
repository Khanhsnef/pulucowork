---
name: design-slides
description: Generates rich visual design JSON (SlideJSON), enforcing tokens, typography, colors, icon badges, and giant number callouts.
---

# Design Slides Skill

## Purpose
Applies `SPEC/DESIGN_SYSTEM.md`, `SPEC/LAYOUT_RULES.md`, and theme config from `STYLES/*.json` to populate detailed `SlideJSON` slide content.

## Input
- `ReportPlan` (JSON)
- `STYLES/operations.json` (Theme tokens)

## Layout Rules
- **Takeaway Header**: Max 20 words, action-oriented, bold key metrics.
- **Hero KPIs**: Giant text callouts (`48px`), badges (`+18%`, `-5.2%`).
- **Icon Badges**: 🎯 Target, ⚡ Impact, 💡 Insight, 🔴 Critical, 📋 Action.
- **Max Cards**: $\le 4$ floating glass cards per slide.

## Output
- `SlideJSON` (JSON)
