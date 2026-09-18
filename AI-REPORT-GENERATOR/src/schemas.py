"""
AI-REPORT-GENERATOR Data Schemas
Pydantic data models enforcing data contracts across all 10 phases.
"""

from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field


class SlideCategory(str, Enum):
    EXEC_SUMMARY = "EXEC_SUMMARY"
    KPI_HEALTH = "KPI_HEALTH"
    DIAGNOSTIC = "DIAGNOSTIC"
    STRATEGIC = "STRATEGIC"
    PROCESS = "PROCESS"
    ACTION_PLAN = "ACTION_PLAN"


class KeyMetric(BaseModel):
    metric_name: str
    value: str
    unit: Optional[str] = ""
    context: Optional[str] = ""


class ExtractedTable(BaseModel):
    headers: List[str]
    rows: List[List[str]]


class SourceSlide(BaseModel):
    slide_number: int
    raw_title: str
    paragraphs: List[str] = Field(default_factory=list)
    tables: List[ExtractedTable] = Field(default_factory=list)
    key_metrics_extracted: List[KeyMetric] = Field(default_factory=list)


class NormalizedSourceDeck(BaseModel):
    deck_id: str
    source_file: str
    total_slides: int
    slides: List[SourceSlide]


class ClassifiedSlide(BaseModel):
    slide_number: int
    category: SlideCategory
    strategic_weight: float = 1.0


class TopicCluster(BaseModel):
    topic_name: str
    source_slide_numbers: List[int]
    primary_kpi: Optional[str] = None


class AnalyzedSlides(BaseModel):
    deck_summary: str
    topic_clusters: List[TopicCluster]
    classified_slides: List[ClassifiedSlide]


class InsightItem(BaseModel):
    insight_id: str
    source_slides: List[int]
    kpi_name: str
    current_value: str
    target_gap: Optional[str] = None
    root_cause: Optional[str] = None
    impact_assessment: Optional[str] = None
    recommended_action: Optional[str] = None
    priority_score: float = 1.0


class InsightCollection(BaseModel):
    insights: List[InsightItem]


class StorylineChapter(BaseModel):
    chapter_title: str
    purpose: str
    slide_topics: List[str]


class Storyline(BaseModel):
    executive_narrative: str
    target_slide_count: int
    chapters: List[StorylineChapter]


class HeroKPI(BaseModel):
    label: str
    value: str
    delta: Optional[str] = None
    badge_status: str = "neutral"  # positive, negative, neutral


class SlideCard(BaseModel):
    card_id: str
    icon_badge: str = "💡"
    title: str
    bullets: List[str]


class SlideDesignItem(BaseModel):
    slide_id: int
    layout_template: str  # executive-summary, kpi-dashboard, comparison, trend, cause-effect, timeline, action-plan
    takeaway_header: str
    hero_kpis: List[HeroKPI] = Field(default_factory=list)
    cards: List[SlideCard] = Field(default_factory=list)
    data_table: Optional[ExtractedTable] = None
    executive_comment: Optional[str] = None
    source_slides: List[int] = Field(default_factory=list)



class SlideJSONPayload(BaseModel):
    deck_title: str
    style_theme: str = "operations"
    slides: List[SlideDesignItem]


class QAReport(BaseModel):
    overall_status: str  # PASS / FAIL
    content_qa_passed: bool
    visual_qa_passed: bool
    iteration_count: int = 1
    warnings: List[str] = Field(default_factory=list)
    recommended_fixes: List[str] = Field(default_factory=list)
