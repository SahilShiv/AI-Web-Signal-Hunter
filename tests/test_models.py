"""Unit tests for Pydantic models and structured JSON validation."""

import pytest
from pydantic import ValidationError
from models.signal import RawSignalExtraction, Signal, ExtractedSignalList
from models.page import CrawledPage


def test_raw_signal_validation():
    valid_data = {
        "source_url": "https://getwati.com/pricing",
        "signal_category": "Pricing Concern",
        "summary": "Small business users complain about unexpected Meta conversation markups.",
        "evidence": "unexpected Meta conversation markups surprise early-stage founders",
        "relevance_score": 88.5,
        "urgency_score": 75.0,
        "confidence_score": 92.0,
        "reasoning": "Identifies recurring cost friction.",
        "is_relevant": True
    }

    raw = RawSignalExtraction.model_validate(valid_data)
    assert raw.signal_category == "Pricing Concern"
    assert raw.relevance_score == 88.5
    assert len(raw.evidence.split()) <= 30


def test_evidence_word_limit_clamping():
    long_evidence = "word " * 50
    data = {
        "source_url": "https://getwati.com/pricing",
        "signal_category": "Pain Point",
        "summary": "A problem occurred",
        "evidence": long_evidence,
        "relevance_score": 80.0,
        "urgency_score": 70.0,
        "confidence_score": 85.0,
        "reasoning": "Reason",
        "is_relevant": True
    }
    raw = RawSignalExtraction.model_validate(data)
    words = raw.evidence.split()
    assert len(words) <= 31  # 30 words + ellipsis


def test_invalid_category_fallback():
    data = {
        "source_url": "https://getwati.com/pricing",
        "signal_category": "Completely Unknown Category",
        "summary": "Summary",
        "evidence": "Evidence quote",
        "relevance_score": 50.0,
        "urgency_score": 50.0,
        "confidence_score": 50.0,
        "reasoning": "Reason",
        "is_relevant": True
    }
    raw = RawSignalExtraction.model_validate(data)
    assert raw.signal_category == "Irrelevant Content"

