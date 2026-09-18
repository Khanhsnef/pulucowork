# QA & VALIDATION RULES — AI REPORT GENERATOR

This specification details the Content QA and Visual QA protocols, threshold conditions, and automated correction loops required before slide export.

---

## 1. CONTENT QA RULES (Kiểm Thử Nội Dung & Dữ Liệu)

### Rule C-01: Zero Data Hallucination
- **Check**: Every metric (`value`, `percentage`, `currency`, `count`) present in generated `SlideJSON` MUST exist in `NormalizedSourceDeck` or input logs.
- **Severity**: BLOCKER (Fail build).
- **Auto-Fix**: Remove untraceable metric or flag for manual verification.

### Rule C-02: Source Metric Traceability
- **Check**: `source_slides` field in `SlideJSON` MUST contain valid integer slide numbers from the input deck.
- **Severity**: HIGH.
- **Auto-Fix**: Auto-populate source slide mappings from Phase 2 topic cluster metadata.

### Rule C-03: Single Dominant Message
- **Check**: Slide `takeaway_header` MUST be an action-oriented executive sentence ($> 5$ words, $< 20$ words), expressing a business impact or decision point.
- **Severity**: MEDIUM.
- **Auto-Fix**: Rewrite generic headers (e.g. *"Ontime Summary"*) into executive takeaways (e.g. *"Ontime Rate Rebounds to 96% Following Mini-Hub Incentive Rollout"*).

---

## 2. VISUAL QA RULES (Kiểm Thử Thị Giác & Layout)

### Rule V-01: Text Overflow & Container Clipping
- **Check**: Calculated bounding boxes for text blocks inside HTML cards MUST NOT exceed card height/width boundaries.
- **Severity**: BLOCKER.
- **Auto-Fix**:
  1. Reduce font size by 10-15% (e.g., `14px` $\rightarrow$ `12.5px`).
  2. Truncate bullet points to top 3 key takeaways.
  3. Split card into 2 separate cards if density is high.

### Rule V-02: Card Density Threshold
- **Check**: Maximum cards per slide $\le 4$. Maximum table rows $\le 6$.
- **Severity**: HIGH.
- **Auto-Fix**: Consolidate minor cards or split content into a 2-slide series.

### Rule V-03: Color Contrast Ratio
- **Check**: Text color vs background color MUST achieve minimum contrast ratio of `4.5:1` (WCAG AA standard).
- **Severity**: HIGH.
- **Auto-Fix**: Force dark text (`#0F172A`) on light card backgrounds (`#FFFFFF`).

---

## 3. AUTO-FIX LOOP PROTOCOL (Vòng Lặp Tự Sửa Lỗi)

```
[Phase 7: Render] ──► Output HTML/PNG
                         │
                         ▼
                 [Phase 8: QA Check]
                         │
        ┌────────────────┴────────────────┐
        ▼                                 ▼
   STATUS == PASS                   STATUS == FAIL
        │                                 │
        ▼                                 ▼
 [Phase 10: Export]             Iteration Count < 3?
                                 ├── YES ──► Apply Auto-Fix Rules ──► Re-Render
                                 └── NO  ──► Log Warning & Export with QA Flags
```
