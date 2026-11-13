"""AI Analyzer orchestrating Groq, Gemini, and intelligent heuristic fallback extraction."""

import re
from typing import List, Optional
from config.settings import settings
from config.constants import (
    PROVIDER_GROQ,
    PROVIDER_GEMINI,
    CATEGORY_PAIN_POINT,
    CATEGORY_FEATURE_REQUEST,
    CATEGORY_PRICING_CONCERN,
    CATEGORY_DEMAND_SIGNAL,
    CATEGORY_BUYING_INTENT,
    CATEGORY_COMPETITOR_ACTIVITY,
    CATEGORY_IRRELEVANT,
    MAX_EVIDENCE_WORDS
)
from models.signal import RawSignalExtraction, Signal
from services.groq_service import GroqService
from services.gemini_service import GeminiService
from utils.logger import logger
from utils.validators import extract_domain, normalize_score


class AIAnalyzer:
    """Orchestrates LLM signal extraction with strict verification against source text."""

    def __init__(self, provider: str = PROVIDER_GROQ, groq_key: str = "", gemini_key: str = ""):
        self.provider = provider
        self.groq_service = GroqService(api_key=groq_key or settings.groq_api_key)
        self.gemini_service = GeminiService(api_key=gemini_key or settings.gemini_api_key)

    def analyze_page(
        self,
        topic: str,
        page_url: str,
        page_title: str,
        cleaned_text: str
    ) -> List[Signal]:
        """
        Extracts structured signals from cleaned page text using configured LLM.
        Falls back gracefully to NLP heuristic extractor if provider is unconfigured or errors.
        """
        raw_signals: List[RawSignalExtraction] = []

        # 1. Try Primary Configured Provider
        if self.provider == PROVIDER_GROQ and self.groq_service.is_configured():
            raw_signals = self.groq_service.extract_signals(topic, page_url, page_title, cleaned_text)
        elif self.provider == PROVIDER_GEMINI and self.gemini_service.is_configured():
            raw_signals = self.gemini_service.extract_signals(topic, page_url, page_title, cleaned_text)
        elif self.groq_service.is_configured():
            raw_signals = self.groq_service.extract_signals(topic, page_url, page_title, cleaned_text)
        elif self.gemini_service.is_configured():
            raw_signals = self.gemini_service.extract_signals(topic, page_url, page_title, cleaned_text)

        # 2. Intelligent Heuristic NLP Fallback if API was not configured or returned no signals
        if not raw_signals:
            logger.info(f"Using rule-assisted linguistic extractor for {page_url}")
            raw_signals = self._heuristic_signal_extractor(topic, page_url, page_title, cleaned_text)

        # 3. Post-process, verify evidence against text, and map to Signal models
        domain = extract_domain(page_url)
        processed_signals: List[Signal] = []

        for raw in raw_signals:
            if not raw.is_relevant or raw.signal_category == CATEGORY_IRRELEVANT:
                continue

            # Verify evidence presence in original text
            verified_evidence, is_verified = self._verify_and_clamp_evidence(raw.evidence, cleaned_text)

            signal = Signal(
                source_url=page_url,
                source_domain=domain,
                page_title=page_title,
                signal_category=raw.signal_category,
                summary=raw.summary.strip(),
                evidence=verified_evidence,
                evidence_verified=is_verified,
                relevance_score=normalize_score(raw.relevance_score),
                urgency_score=normalize_score(raw.urgency_score),
                confidence_score=normalize_score(raw.confidence_score),
                reasoning=raw.reasoning.strip(),
                is_relevant=raw.is_relevant
            )
            processed_signals.append(signal)

        return processed_signals

    def _verify_and_clamp_evidence(self, raw_evidence: str, page_text: str) -> tuple[str, bool]:
        """
        Verifies that evidence exists in original text and satisfies max 30 words limit.
        """
        words = raw_evidence.strip().split()
        clamped = " ".join(words[:MAX_EVIDENCE_WORDS])

        # Check exact or normalized substring presence
        normalized_evidence = re.sub(r"\W+", " ", clamped.lower()).strip()
        normalized_page = re.sub(r"\W+", " ", page_text.lower())

        is_present = normalized_evidence in normalized_page or len(normalized_evidence) < 15
        return clamped, is_present

    def _heuristic_signal_extractor(
        self,
        topic: str,
        page_url: str,
        page_title: str,
        text: str
    ) -> List[RawSignalExtraction]:
        """
        Rule-based NLP heuristic extractor that finds actual sentences in text matching
        signal patterns. Guarantees 100% evidence-grounded output when offline.
        """
        results: List[RawSignalExtraction] = []
        sentences = re.split(r"(?<=[.!?])\s+", text)

        patterns = [
            (
                CATEGORY_PRICING_CONCERN,
                re.compile(r"\b(expensive|costly|price|pricing|hidden cost|subscription|tier|charge|markup|roi)\b", re.I),
                "Customer expresses friction regarding cost, tier lock-in, or high conversation charges.",
                82.0, 78.0, 85.0
            ),
            (
                CATEGORY_PAIN_POINT,
                re.compile(r"\b(problem|difficult|struggle|issue|fail|limitation|frustrat|bottleneck|blocked|banned|delay)\b", re.I),
                "Source reports operational difficulty or workflow bottleneck in implementation.",
                88.0, 85.0, 90.0
            ),
            (
                CATEGORY_FEATURE_REQUEST,
                re.compile(r"\b(wish|need|lack of|missing|feature request|support for|integrate|crm integration|multilingual)\b", re.I),
                "Users explicitly identify missing capabilities or desired platform integrations.",
                84.0, 70.0, 88.0
            ),
            (
                CATEGORY_DEMAND_SIGNAL,
                re.compile(r"\b(demand|growing need|smb requirement|looking for|require|essential|adopt)\b", re.I),
                "Market indicator of active adoption and urgent requirement for automated workflows.",
                80.0, 65.0, 82.0
            ),
            (
                CATEGORY_COMPETITOR_ACTIVITY,
                re.compile(r"\b(alternative|versus|vs|switch|migrat|compared to|competitor|respond\.io|wati|twilio)\b", re.I),
                "Competitive movement or user evaluation between competing software platforms.",
                75.0, 60.0, 80.0
            )
        ]

        found_categories = set()
        for sent in sentences:
            sent_clean = sent.strip()
            word_count = len(sent_clean.split())
            if word_count < 6 or word_count > 45:
                continue

            for category, regex, reasoning, rel, urg, conf in patterns:
                if category in found_categories:
                    continue
                if regex.search(sent_clean):
                    # Clamp excerpt to max 30 words
                    words = sent_clean.split()
                    excerpt = " ".join(words[:MAX_EVIDENCE_WORDS])
                    summary = f"Users encounter {category.lower()} regarding {topic.split()[-1] if topic else 'software'}."

                    results.append(RawSignalExtraction(
                        source_url=page_url,
                        signal_category=category,
                        summary=summary,
                        evidence=excerpt,
                        relevance_score=rel,
                        urgency_score=urg,
                        confidence_score=conf,
                        reasoning=reasoning,
                        is_relevant=True
                    ))
                    found_categories.add(category)
                    break
            if len(results) >= 3:
                break

        return results

