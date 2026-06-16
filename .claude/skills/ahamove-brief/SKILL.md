---
name: Ahamove Ops Brief
description: Creates a standard one-pager Ops brief using the Pyramid Principle, suitable for Ahamove CPO or management meetings.
---

# Ahamove Ops Brief Generator

## Goal
Transform raw operational data, metrics, or scattered notes into a structured, executive-ready One-Pager Ops Brief.

## Core Principles
1. **Pyramid Principle:** Start with the Executive Summary (The Answer/Insight), followed by supporting arguments, and end with raw data/metrics.
2. **Ahamove Standard:** Use standard terminology (e.g., SLA, FR, AR, CPO, Active Drivers, Peak-hour). Avoid fluff and marketing language. Lead with evidence.
3. **Action-Oriented:** Every brief must end with clear Next Steps or Trade-off decisions.

## Structure of the Brief
Create the brief using the following Markdown structure:

```markdown
# [Title: Action-oriented and descriptive]

## 1. Executive Summary (Insight)
- One sentence summarizing the core finding or decision.
- Key impact (e.g., "Expected to reduce CPO by 5% while maintaining SLA").

## 2. Context & Problem Statement (Situation & Complication)
- Current baseline metrics vs Target.
- The bottleneck or gap identified.

## 3. Analysis & Evidence (Resolution)
- **Descriptive:** What is happening right now?
- **Diagnostic:** Why is it happening? (Root causes).
- **Predictive:** What will happen if we take action X?
- **Prescriptive:** What is the recommended strategy?

## 4. Key Metrics (KPIs)
| Metric | Current | Projected | Change |
|--------|---------|-----------|--------|
| ...    | ...     | ...       | ...    |

## 5. Next Steps / Trade-offs
- Action items.
- Known risks and how to mitigate them.
```

## Instructions for Agent
1. Read the user's input data carefully.
2. Extract the core insight. If data is missing, make reasonable assumptions based on standard Ahamove context, but highlight them.
3. Generate the brief in Vietnamese (with English terms for metrics).
4. Output as a clean Markdown format or offer to export as Docx/HTML if requested.
