"""Data models for grouped business opportunities and research sessions."""

import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from models.signal import Signal


class EvidenceReference(BaseModel):
    """Reference excerpt with source link."""
    excerpt: str = Field(..., description="Quoted evidence text")
    url: str = Field(..., description="Original URL")
    domain: str = Field(..., description="Source domain")
    page_title: str = Field(default="Source", description="Title of article")


class OpportunityBrief(BaseModel):
    """Detailed business brief for top opportunities."""

    title: str = Field(..., description="A. Clear, meaningful opportunity title")
    problem_description: str = Field(..., description="B. What is happening? The core problem")
    target_audience: str = Field(..., description="C. Who experiences the problem?")
    why_it_matters: str = Field(..., description="D. Why this opportunity is valuable now")
    possible_solution: str = Field(..., description="E. Suggested product, SaaS, feature, or service")
    validation_strategy: str = Field(..., description="H. Practical real-user validation method")
    evidence_samples: List[EvidenceReference] = Field(
        default_factory=list, description="F. Supporting evidence excerpts"
    )
    source_links: List[str] = Field(default_factory=list, description="G. Clickable source links")
    solution_type: str = Field(default="SaaS Platform", description="Product, SaaS, Feature, Tool, or Service")


class Opportunity(BaseModel):
    """Clustered business opportunity with ranking score and supporting signals."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: Optional[str] = Field(default=None)
    research_topic: str = Field(default="")
    title: str = Field(..., description="Opportunity name/theme")
    problem_description: str = Field(default="")
    target_audience: str = Field(default="")
    why_it_matters: str = Field(default="")
    possible_solution: str = Field(default="")
    validation_strategy: str = Field(default="")

    # Supporting evidence & metrics
    signals: List[Signal] = Field(default_factory=list)
    supporting_signal_count: int = Field(default=0)
    unique_domains_count: int = Field(default=0)
    supporting_domains: List[str] = Field(default_factory=list)

    # Normalized component scores (0-100)
    frequency_score: float = Field(default=0.0)
    relevance_score: float = Field(default=0.0)
    urgency_score: float = Field(default=0.0)
    confidence_score: float = Field(default=0.0)
    recency_score: float = Field(default=0.0)

    # Final weighted Opportunity Score (0-100)
    opportunity_score: float = Field(default=0.0)
    score_breakdown: Dict[str, float] = Field(default_factory=dict)
    score_explanation: str = Field(default="")

    # Brief
    brief: Optional[OpportunityBrief] = Field(default=None)


class ResearchSession(BaseModel):
    """Complete container for a saved research run."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    topic: str = Field(..., description="Primary research question or topic")
    keywords: List[str] = Field(default_factory=list)
    ai_provider: str = Field(default="Groq")
    ai_model: str = Field(default="")
    crawl_limit: int = Field(default=25)
    min_relevance_threshold: int = Field(default=60)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Statistics
    pages_discovered: int = Field(default=0)
    pages_crawled_count: int = Field(default=0)
    pages_skipped_count: int = Field(default=0)
    signals_count: int = Field(default=0)
    opportunities_count: int = Field(default=0)
    unique_domains_count: int = Field(default=0)

    # Full objects
    signals: List[Signal] = Field(default_factory=list)
    opportunities: List[Opportunity] = Field(default_factory=list)
