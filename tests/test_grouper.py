"""Unit tests for opportunity grouper."""

from core.opportunity_grouper import OpportunityGrouper
from models.signal import Signal


def test_opportunity_grouping():
    grouper = OpportunityGrouper()

    signals = [
        Signal(
            source_url="https://getwati.com/pricing",
            source_domain="getwati.com",
            signal_category="Pricing Concern",
            summary="Meta conversation pricing is too expensive for small shops",
            evidence="pricing is too expensive",
            relevance_score=85.0,
            urgency_score=75.0,
            confidence_score=90.0,
            reasoning="Cost friction"
        ),
        Signal(
            source_url="https://twilio.com/bans",
            source_domain="twilio.com",
            signal_category="Pain Point",
            summary="Accounts get banned without notice when spam rating drops",
            evidence="accounts get banned without notice",
            relevance_score=92.0,
            urgency_score=90.0,
            confidence_score=95.0,
            reasoning="Account ban risk"
        ),
        Signal(
            source_url="https://sleekflow.io/crm",
            source_domain="sleekflow.io",
            signal_category="Feature Request",
            summary="Need native integration with HubSpot and Zoho CRM",
            evidence="need native integration with hubspot",
            relevance_score=88.0,
            urgency_score=70.0,
            confidence_score=89.0,
            reasoning="CRM synchronization request"
        )
    ]

    opportunities = grouper.group_signals("WhatsApp automation problems", signals)

    assert len(opportunities) >= 3
    # Ensure descending sort by opportunity score
    scores = [o.opportunity_score for o in opportunities]
    assert scores == sorted(scores, reverse=True)

