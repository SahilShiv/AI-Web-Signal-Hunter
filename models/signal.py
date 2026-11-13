"""Data models for extracted business signals."""

import uuid
from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from config.constants import SIGNAL_CATEGORIES, CATEGORY_IRRELEVANT, MAX_EVIDENCE_WORDS


class RawSignalExtraction(BaseModel):
    """Raw signal schema produced by LLM JSON output."""

    source_url: str = Field(..., description="Original URL from which this signal was extracted")
    signal_category: str = Field(..., description="Category: Pain Point, Demand Signal, Feature Request, etc.")
    summary: str = Field(..., description="Concise 1-2 sentence business signal summary")
    evidence: str = Field(..., description="Exact supporting excerpt from original page (max 30 words)")
    relevance_score: float = Field(..., ge=0, le=100, description="Relevance to research topic (0-100)")
    urgency_score: float = Field(..., ge=0, le=100, description="Urgency / severity of problem (0-100)")
    confidence_score: float = Field(..., ge=0, le=100, description="AI extraction confidence (0-100)")
    reasoning: str = Field(..., description="Analytical justification for classification and score")
    is_relevant: bool = Field(default=True, description="Whether signal meets relevance criteria")

    @field_validator("signal_category")
    @classmethod
    def validate_category(cls, v: str) -> str:
        for cat in SIGNAL_CATEGORIES:
            if v.strip().lower() == cat.lower():
                return cat
        return CATEGORY_IRRELEVANT

    @field_validator("evidence")
    @classmethod
    def validate_evidence_length(cls, v: str) -> str:
        words = v.strip().split()
        if len(words) > MAX_EVIDENCE_WORDS:
            return " ".join(words[:MAX_EVIDENCE_WORDS]) + "..."
        return v.strip()

    @field_validator("relevance_score", "urgency_score", "confidence_score")
    @classmethod
    def clamp_score(cls, v: float) -> float:
        return max(0.0, min(100.0, float(v)))


class ExtractedSignalList(BaseModel):
    """Container for batch LLM signal extraction response."""
    signals: List[RawSignalExtraction] = Field(default_factory=list)


class Signal(BaseModel):
    """Full application signal model with tracking IDs, metadata, and verification flags."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: Optional[str] = Field(default=None, description="Associated research session ID")
    source_url: str = Field(..., description="Original source link")
    source_domain: str = Field(..., description="Domain of source")
    page_title: str = Field(default="Source Page", description="Title of crawled page")
    signal_category: str = Field(..., description="Category of the business signal")
    summary: str = Field(..., description="Concise summary of the signal")
    evidence: str = Field(..., description="Verifiable quotation from source content")
    evidence_verified: bool = Field(default=True, description="True if evidence was found in page body")
    relevance_score: float = Field(default=0.0, ge=0, le=100)
    urgency_score: float = Field(default=0.0, ge=0, le=100)
    confidence_score: float = Field(default=0.0, ge=0, le=100)
    reasoning: str = Field(default="")
    is_relevant: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    published_date: Optional[str] = Field(default=None)
