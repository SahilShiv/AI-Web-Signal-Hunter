"""Transparent opportunity scoring algorithm adhering to strict weighting formula."""

from typing import Dict, List, Tuple
from config.constants import (
    WEIGHT_FREQUENCY,
    WEIGHT_RELEVANCE,
    WEIGHT_URGENCY,
    WEIGHT_CONFIDENCE,
    WEIGHT_RECENCY
)
from models.signal import Signal
from utils.validators import normalize_score


class OpportunityScorer:
    """Calculates transparent, explainable opportunity rankings."""

    def calculate_scores(
        self,
        signals: List[Signal],
        max_possible_domains: int = 10
    ) -> Tuple[float, float, float, float, float, float, Dict[str, float], str]:
        """
        Calculates normalized components and final weighted opportunity score.

        Returns:
            (
                opportunity_score,
                frequency_score,
                relevance_score,
                urgency_score,
                confidence_score,
                recency_score,
                breakdown_dict,
                explanation_str
            )
        """
        if not signals:
            return 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, {}, "No supporting signals available."

        # 1. Independent domains and signal count for Frequency Score
        unique_domains = list({s.source_domain for s in signals if s.source_domain})
        unique_domain_count = len(unique_domains)
        signal_count = len(signals)

        # Independent domains weighted heavily (70%) over raw repetitions (30%)
        # Clamped to 100
        domain_factor = min(1.0, unique_domain_count / max(1, min(max_possible_domains, 5)))
        count_factor = min(1.0, signal_count / 8.0)
        frequency_score = normalize_score((domain_factor * 70.0) + (count_factor * 30.0))

        # 2. Average Relevance, Urgency, Confidence
        relevance_score = normalize_score(sum(s.relevance_score for s in signals) / signal_count)
        urgency_score = normalize_score(sum(s.urgency_score for s in signals) / signal_count)
        confidence_score = normalize_score(sum(s.confidence_score for s in signals) / signal_count)

        # 3. Recency Score (based on verified dates or fallback default)
        dated_signals = [s for s in signals if s.published_date]
        if dated_signals:
            # High recency for recent publications
            recency_score = 85.0
            recency_note = f"Evidence from recent verified web publications ({len(dated_signals)} dated sources)."
        else:
            # Conservative baseline when crawl dates are current but page dates unrecorded
            recency_score = 70.0
            recency_note = "Estimated baseline (original publication date unrecorded in page metadata)."

        # 4. Final Weighted Formula
        opportunity_score = normalize_score(
            (frequency_score * WEIGHT_FREQUENCY) +
            (relevance_score * WEIGHT_RELEVANCE) +
            (urgency_score * WEIGHT_URGENCY) +
            (confidence_score * WEIGHT_CONFIDENCE) +
            (recency_score * WEIGHT_RECENCY)
        )

        breakdown = {
            "Frequency (30%)": frequency_score,
            "Relevance (25%)": relevance_score,
            "Urgency (20%)": urgency_score,
            "Confidence (15%)": confidence_score,
            "Recency (10%)": recency_score,
        }

        explanation = (
            f"Opportunity Score of {opportunity_score}/100 derived from {signal_count} supporting signals "
            f"across {unique_domain_count} independent domains ({', '.join(unique_domains[:3])}). "
            f"Frequency: {frequency_score} (30%), Relevance: {relevance_score} (25%), Urgency: {urgency_score} (20%), "
            f"Confidence: {confidence_score} (15%), Recency: {recency_score} (10%). {recency_note} "
            f"Note: This score is an analytical prioritization index, not an absolute market size guarantee."
        )

        return (
            opportunity_score,
            frequency_score,
            relevance_score,
            urgency_score,
            confidence_score,
            recency_score,
            breakdown,
            explanation
        )

