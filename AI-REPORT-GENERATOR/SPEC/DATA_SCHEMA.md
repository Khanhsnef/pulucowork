# DATA SCHEMA CONTRACTS — AI REPORT GENERATOR

This specification defines the JSON Schema contracts passed sequentially between phases in the Report Generation Workflow.

---

## 1. Phase 1 Output: `NormalizedSourceDeck`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "NormalizedSourceDeck",
  "type": "OBJECT",
  "properties": {
    "deck_id": { "type": "STRING" },
    "source_file": { "type": "STRING" },
    "total_slides": { "type": "INTEGER" },
    "slides": {
      "type": "ARRAY",
      "items": {
        "type": "OBJECT",
        "properties": {
          "slide_number": { "type": "INTEGER" },
          "raw_title": { "type": "STRING" },
          "paragraphs": { "type": "ARRAY", "items": { "type": "STRING" } },
          "tables": {
            "type": "ARRAY",
            "items": {
              "type": "OBJECT",
              "properties": {
                "headers": { "type": "ARRAY", "items": { "type": "STRING" } },
                "rows": { "type": "ARRAY", "items": { "type": "ARRAY", "items": { "type": "STRING" } } }
              }
            }
          },
          "key_metrics_extracted": {
            "type": "ARRAY",
            "items": {
              "type": "OBJECT",
              "properties": {
                "metric_name": { "type": "STRING" },
                "value": { "type": "STRING" },
                "unit": { "type": "STRING" },
                "context": { "type": "STRING" }
              }
            }
          }
        }
      }
    }
  }
}
```

---

## 2. Phase 2 Output: `AnalyzedSlides`

```json
{
  "title": "AnalyzedSlides",
  "type": "OBJECT",
  "properties": {
    "deck_summary": { "type": "STRING" },
    "topic_clusters": {
      "type": "ARRAY",
      "items": {
        "type": "OBJECT",
        "properties": {
          "topic_name": { "type": "STRING" },
          "source_slide_numbers": { "type": "ARRAY", "items": { "type": "INTEGER" } },
          "primary_kpi": { "type": "STRING" }
        }
      }
    },
    "classified_slides": {
      "type": "ARRAY",
      "items": {
        "type": "OBJECT",
        "properties": {
          "slide_number": { "type": "INTEGER" },
          "category": { "enum": ["EXEC_SUMMARY", "KPI_HEALTH", "DIAGNOSTIC", "STRATEGIC", "PROCESS", "ACTION_PLAN"] },
          "strategic_weight": { "type": "NUMBER" }
        }
      }
    }
  }
}
```

---

## 3. Phase 3 Output: `InsightCollection`

```json
{
  "title": "InsightCollection",
  "type": "OBJECT",
  "properties": {
    "insights": {
      "type": "ARRAY",
      "items": {
        "type": "OBJECT",
        "properties": {
          "insight_id": { "type": "STRING" },
          "source_slides": { "type": "ARRAY", "items": { "type": "INTEGER" } },
          "kpi_name": { "type": "STRING" },
          "current_value": { "type": "STRING" },
          "target_gap": { "type": "STRING" },
          "root_cause": { "type": "STRING" },
          "impact_assessment": { "type": "STRING" },
          "recommended_action": { "type": "STRING" },
          "priority_score": { "type": "NUMBER" }
        }
      }
    }
  }
}
```

---

## 4. Phase 4 Output: `Storyline`

```json
{
  "title": "Storyline",
  "type": "OBJECT",
  "properties": {
    "executive_narrative": { "type": "STRING" },
    "target_slide_count": { "type": "INTEGER" },
    "chapters": {
      "type": "ARRAY",
      "items": {
        "type": "OBJECT",
        "properties": {
          "chapter_title": { "type": "STRING" },
          "purpose": { "type": "STRING" },
          "slide_topics": { "type": "ARRAY", "items": { "type": "STRING" } }
        }
      }
    }
  }
}
```

---

## 5. Phase 6 Output: `SlideJSON` (Target Design Payload)

```json
{
  "title": "SlideJSON",
  "type": "OBJECT",
  "properties": {
    "deck_title": { "type": "STRING" },
    "style_theme": { "type": "STRING" },
    "slides": {
      "type": "ARRAY",
      "items": {
        "type": "OBJECT",
        "properties": {
          "slide_id": { "type": "INTEGER" },
          "layout_template": { "enum": ["executive-summary", "kpi-dashboard", "comparison", "trend", "cause-effect", "timeline", "action-plan"] },
          "takeaway_header": { "type": "STRING" },
          "hero_kpis": {
            "type": "ARRAY",
            "items": {
              "type": "OBJECT",
              "properties": {
                "label": { "type": "STRING" },
                "value": { "type": "STRING" },
                "delta": { "type": "STRING" },
                "badge_status": { "enum": ["positive", "negative", "neutral"] }
              }
            }
          },
          "cards": {
            "type": "ARRAY",
            "items": {
              "type": "OBJECT",
              "properties": {
                "card_id": { "type": "STRING" },
                "icon_badge": { "type": "STRING" },
                "title": { "type": "STRING" },
                "bullets": { "type": "ARRAY", "items": { "type": "STRING" } }
              }
            }
          },
          "data_table": {
            "type": "OBJECT",
            "properties": {
              "headers": { "type": "ARRAY", "items": { "type": "STRING" } },
              "rows": { "type": "ARRAY", "items": { "type": "ARRAY", "items": { "type": "STRING" } } }
            }
          },
          "source_slides": { "type": "ARRAY", "items": { "type": "INTEGER" } }
        }
      }
    }
  }
}
```

---

## 6. Phase 8 Output: `QAReport`

```json
{
  "title": "QAReport",
  "type": "OBJECT",
  "properties": {
    "overall_status": { "enum": ["PASS", "FAIL"] },
    "content_qa": {
      "type": "OBJECT",
      "properties": {
        "hallucination_detected": { "type": "BOOLEAN" },
        "missing_source_traceability": { "type": "ARRAY", "items": { "type": "STRING" } }
      }
    },
    "visual_qa": {
      "type": "OBJECT",
      "properties": {
        "text_overflow_slides": { "type": "ARRAY", "items": { "type": "INTEGER" } },
        "low_contrast_elements": { "type": "ARRAY", "items": { "type": "STRING" } },
        "card_overcrowding": { "type": "ARRAY", "items": { "type": "INTEGER" } }
      }
    },
    "iteration_count": { "type": "INTEGER" },
    "recommended_fixes": { "type": "ARRAY", "items": { "type": "STRING" } }
  }
}
```
