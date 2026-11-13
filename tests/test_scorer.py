"""Unit tests for transparent opportunity ranking formula."""

from core.opportunity_scorer import OpportunityScorer
from models.signal import Signal


def test_opportunity_scorer_formula():
    scorer = OpportunityScorer()

    signals = [
        Signal(
            source_url="https://getwati.com/pricing",
            source_domain="getwati.com",
            signal_category="Pricing Concern",
            summary="High costs",
            evidence="high costs hurt margins",
            relevance_score=80.0,
            urgency_score=70.0,
            confidence_score=90.0
        ),
        Signal(
            source_url="https://respond.io/issues",
            source_domain="respond.io",
            signal_category="Pricing Concern",
            summary="Double billing",
            evidence="double billing structure is unfair",
            relevance_score=90.0,
            urgency_score=80.0,
            confidence_score=90.0
        )
    ]

    (
        opp_score,
        freq_score,
        rel_score,
        urg_score,
        conf_score,
        rec_score,
        breakdown,
        explanation
    ) = scorer.calculate_scores(signals)

    # Check math:
    # rel = (80 + 90)/2 = 85.0
    # urg = (70 + 80)/2 = 75.0
    # conf = (90 + 90)/2 = 90.0
    assert rel_score == 85.0
    assert urg_score == 75.0
    assert conf_score == 90.0

    # Formula check: freq*0.30 + rel*0.25 + urg*0.20 + conf*0.15 + rec*0.10
    expected = round((freq_score * 0.30) + (rel_score * 0.25) + (urg_score * 0.20) + (conf_score * 0.15) + (rec_score * 0.10), 1)
    assert abs(opp_score - expected) <= 0.2
    assert "Frequency (30%)" in breakdown
    assert "Opportunity Score" in explanation

