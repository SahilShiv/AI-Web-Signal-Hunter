"""End-to-end integration test of the complete research pipeline."""

from core.content_cleaner import ContentCleaner
from core.deduplicator import Deduplicator
from core.ai_analyzer import AIAnalyzer
from core.signal_extractor import SignalExtractor
from core.opportunity_grouper import OpportunityGrouper
from core.opportunity_brief import OpportunityBriefGenerator
from models.page import CrawledPage
from utils.helpers import compute_sha256
from datetime import datetime, timezone


def test_end_to_end_pipeline():
    # 1. Simulate Crawled Pages
    sample_text_1 = """
    # Managing WhatsApp Messaging Costs
    Meta charges per conversation. Many small retailers face unpredictable monthly conversation charges
    that damage their margins. We recommend closely monitoring daily marketing broadcast limits.
    """
    sample_text_2 = """
    # Why WhatsApp Numbers Get Banned
    Sudden account bans occur when customer quality scores plummet. When low quality ratings trigger automated Meta flags,
    business operations halt completely.
    """
    sample_text_3 = """
    # CRM Integration with WhatsApp Web
    Sales teams complain that lack of native CRM integration forces hours of manual data entry.
    Merchants demand seamless two-way CRM sync between WhatsApp chats and HubSpot records.
    """

    cleaner = ContentCleaner()
    dedup = Deduplicator()

    pages = [
        CrawledPage(
            url="https://getwati.com/costs",
            domain="getwati.com",
            title="Managing WhatsApp Costs",
            cleaned_text=sample_text_1,
            word_count=50,
            content_hash=compute_sha256(sample_text_1),
            crawl_date=datetime.now(timezone.utc)
        ),
        CrawledPage(
            url="https://twilio.com/bans",
            domain="twilio.com",
            title="Why WhatsApp Accounts Get Banned",
            cleaned_text=sample_text_2,
            word_count=50,
            content_hash=compute_sha256(sample_text_2),
            crawl_date=datetime.now(timezone.utc)
        ),
        CrawledPage(
            url="https://sleekflow.io/crm-integration",
            domain="sleekflow.io",
            title="CRM Integration with WhatsApp",
            cleaned_text=sample_text_3,
            word_count=50,
            content_hash=compute_sha256(sample_text_3),
            crawl_date=datetime.now(timezone.utc)
        )
    ]

    # 2. Extract Signals using AIAnalyzer (offline rule-assisted heuristic mode)
    analyzer = AIAnalyzer()
    extractor = SignalExtractor(analyzer=analyzer, min_relevance=60.0)

    signals = extractor.extract_from_pages(
        topic="WhatsApp automation problems",
        pages=pages
    )
    assert len(signals) >= 3

    # Verify evidence existence in text
    for sig in signals:
        assert sig.evidence_verified is True
        assert len(sig.evidence.split()) <= 30

    # 3. Group Opportunities & Score
    grouper = OpportunityGrouper()
    opportunities = grouper.group_signals("WhatsApp automation problems", signals)
    assert len(opportunities) >= 2

    # 4. Generate Top Briefs
    brief_gen = OpportunityBriefGenerator()
    opportunities = brief_gen.generate_briefs(opportunities, top_n=5)

    top_brief = opportunities[0].brief
    assert top_brief is not None
    assert top_brief.title == opportunities[0].title
    assert len(top_brief.problem_description) > 10
    assert len(top_brief.target_audience) > 5
    assert len(top_brief.validation_strategy) > 10
