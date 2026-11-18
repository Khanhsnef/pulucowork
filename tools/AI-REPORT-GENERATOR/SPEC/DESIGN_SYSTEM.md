# DESIGN SYSTEM — AI REPORT GENERATOR (16:9 EXECUTIVE SUITE)

This document establishes the universal design tokens, color palettes, typography scale, spacing system, and micro-visual anchor guidelines for all generated 16:9 executive report slides.

---

## 1. CANVAS & GRID SPECIFICATIONS
- **Resolution**: `1920px × 1080px` (Widescreen 16:9).
- **Safety Margins**:
  - Top: `48px`
  - Bottom: `48px`
  - Left / Right: `64px`
- **Internal Card Padding**: `24px – 32px` (0.25 in). NEVER allow text to touch card borders.
- **Grid Layout**: Flexible 12-column CSS Grid / Flexbox container with `24px` gutter gap.

---

## 2. COLOR PALETTE & THEMING (AHAMOVE EXECUTIVE STANDARD)

### Core Operational Palette:
- **Brand Primary (Blue)**: `#0E4174` (Deep Corporate Navy)
- **Brand Accent (Orange)**: `#FF7F32` (Vibrant Ops Highlight)
- **Neutral Dark (Text)**: `#0F172A` (Slate 900)
- **Neutral Muted**: `#475569` (Slate 600)
- **Card Background**: `#FFFFFF` (Solid Card) / `rgba(255, 255, 255, 0.85)` (Glassmorphism)
- **Canvas Background**: `#F8FAFC` (Slate 50 Light Gray)

### Semantic KPI Colors:
- **Positive / Growth**: `#10B981` (Emerald 500) | BG: `#ECFDF5`
- **Danger / SLA Drop**: `#EF4444` (Red 500) | BG: `#FEF2F2`
- **Warning / Target Gap**: `#F59E0B` (Amber 500) | BG: `#FFFBEB`
- **Neutral Info**: `#3B82F6` (Blue 500) | BG: `#EFF6FF`

### Knaflic Storytelling Color & Decluttering Rules:
- **90% Gray Baseline**: Baseline series, gridlines (`#F1F5F9`), and non-focus bars MUST use neutral gray (`#94A3B8`).
- **Single Accent Highlight**: Only the single most critical series / outlier gets saturated Ahamove Orange (`#FF7F32`) or Blue (`#0E4174`).
- **Direct Labeling Mandate**: Never put charts in isolated containers with detached legends; place series labels directly at the line/bar end points.
- **Red Line Avoidance**: 🚫 No Pie/Donut charts, 🚫 No 3D depth, 🚫 No Dual Y-Axes.

---

## 3. TYPOGRAPHY SCALE (Google Fonts: Inter / Lexend)

| Element | Font Weight | Size | Line Height | Usage |
| :--- | :--- | :--- | :--- | :--- |
| **Takeaway Header** | Extra Bold (800) | `32px` | `1.2` | Slide top dominant takeaway |
| **Giant KPI Number** | Black (900) | `48px – 56px` | `1.0` | Hero KPI callouts |
| **Card Header (H2)** | Bold (700) | `20px` | `1.3` | Card top titles with Icon Badges |
| **Body Lead / Highlight**| SemiBold (600) | `16px` | `1.4` | First bullet point / Key bold text |
| **Body Regular** | Regular (400) | `14px` | `1.5` | Supporting bullet points / Table text |
| **Micro Caption / Source**| Medium (500) | `12px` | `1.4` | Footer metric source & slide trace |

---

## 4. CARD UI & GLASSMORPHISM
- **Border Radius**: `16px` (bo góc mềm mại).
- **Border Stroke**: `1px solid rgba(226, 232, 240, 0.8)` (Slate 200).
- **Shadow**: `0 10px 25px -5px rgba(14, 65, 116, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.03)` (Soft Floating Shadow).
- **Header Accent Bar**: `4px` vertical pill or left border accent for rapid scanning.

---

## 5. MICRO-VISUAL ANCHORS & ICON BADGES
Every card header MUST feature a relevant visual anchor icon badge:
- 🎯 **Target / Strategy**: Strategic objectives & SLA targets.
- ⚡ **Impact / Performance**: Metric gains, CPO savings, efficiency.
- 💡 **Insight**: Analytical takeaways & root-cause discoveries.
- 🔴 **Critical Issue**: SLA breaches, driver churn spikes, offload risk.
- 🏆 **Key Takeaway**: Executive Summary top highlights.
- 📋 **Action Plan**: Next step initiatives & operational SOPs.
- 📊 **Matrix / Table**: Comparative data & regional breakdowns.
