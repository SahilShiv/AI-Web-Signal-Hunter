"""Export service generating compliant CSV and JSON intelligence datasets."""

import io
import json
import pandas as pd
from typing import List, Optional
from models.opportunity import ResearchSession, Opportunity
from models.page import CrawledPage
from utils.logger import logger


class ExportService:
    """Handles CSV and JSON report exports."""

    @staticmethod
    def export_csv(
        session: ResearchSession,
        opportunities: Optional[List[Opportunity]] = None
    ) -> str:
        """
        Exports research findings as CSV with required columns:
        - Opportunity name
        - Signal category
        - Summary
        - Evidence
        - Relevance score
        - Urgency score
        - Confidence score
        - Opportunity score
        - Source domain
        - Source URL
        """
        opps = opportunities or session.opportunities
        rows = []

        # Map signals to opportunities
        for opp in opps:
            opp_name = opp.title
            opp_score = opp.opportunity_score

            for sig in opp.signals:
                rows.append({
                    "Opportunity Name": opp_name,
                    "Signal Category": sig.signal_category,
                    "Summary": sig.summary,
                    "Evidence": sig.evidence,
                    "Relevance Score": sig.relevance_score,
                    "Urgency Score": sig.urgency_score,
                    "Confidence Score": sig.confidence_score,
                    "Opportunity Score": opp_score,
                    "Source Domain": sig.source_domain,
                    "Source URL": sig.source_url,
                })

        # If some signals were unassigned to an opportunity
        all_signals = session.signals
        assigned_sig_ids = {s.id for o in opps for s in o.signals}
        for sig in all_signals:
            if sig.id not in assigned_sig_ids:
                rows.append({
                    "Opportunity Name": "Uncategorized Signals",
                    "Signal Category": sig.signal_category,
                    "Summary": sig.summary,
                    "Evidence": sig.evidence,
                    "Relevance Score": sig.relevance_score,
                    "Urgency Score": sig.urgency_score,
                    "Confidence Score": sig.confidence_score,
                    "Opportunity Score": 0.0,
                    "Source Domain": sig.source_domain,
                    "Source URL": sig.source_url,
                })

        df = pd.DataFrame(rows)
        if df.empty:
            df = pd.DataFrame(columns=[
                "Opportunity Name", "Signal Category", "Summary", "Evidence",
                "Relevance Score", "Urgency Score", "Confidence Score",
                "Opportunity Score", "Source Domain", "Source URL"
            ])

        return df.to_csv(index=False)

    @staticmethod
    def export_json(
        session: ResearchSession,
        crawled_pages: Optional[List[CrawledPage]] = None
    ) -> str:
        """
        Exports complete research findings into structured hierarchical JSON.
        Includes metadata, crawled pages, extracted signals, grouped opportunities,
        ranking calculations, and top 5 opportunity briefs.
        """
        data = {
            "research_metadata": {
                "session_id": session.id,
                "topic": session.topic,
                "keywords": session.keywords,
                "ai_provider": session.ai_provider,
                "ai_model": session.ai_model,
                "crawl_limit": session.crawl_limit,
                "min_relevance_threshold": session.min_relevance_threshold,
                "created_at": session.created_at.isoformat(),
                "pages_discovered": session.pages_discovered,
                "pages_crawled_count": session.pages_crawled_count,
                "unique_domains_count": session.unique_domains_count,
                "signals_count": len(session.signals),
                "opportunities_count": len(session.opportunities)
            },
            "crawled_pages": [
                {
                    "url": p.url,
                    "domain": p.domain,
                    "title": p.title,
                    "word_count": p.word_count,
                    "crawl_date": p.crawl_date.isoformat(),
                    "published_date": p.published_date,
                    "status_code": p.status_code
                }
                for p in (crawled_pages or [])
            ],
            "extracted_signals": [
                {
                    "id": s.id,
                    "source_url": s.source_url,
                    "source_domain": s.source_domain,
                    "page_title": s.page_title,
                    "signal_category": s.signal_category,
                    "summary": s.summary,
                    "evidence": s.evidence,
                    "evidence_verified": s.evidence_verified,
                    "relevance_score": s.relevance_score,
                    "urgency_score": s.urgency_score,
                    "confidence_score": s.confidence_score,
                    "reasoning": s.reasoning,
                    "published_date": s.published_date
                }
                for s in session.signals
            ],
            "grouped_opportunities": [
                {
                    "id": opp.id,
                    "title": opp.title,
                    "problem_description": opp.problem_description,
                    "target_audience": opp.target_audience,
                    "why_it_matters": opp.why_it_matters,
                    "possible_solution": opp.possible_solution,
                    "validation_strategy": opp.validation_strategy,
                    "supporting_signal_count": opp.supporting_signal_count,
                    "unique_domains_count": opp.unique_domains_count,
                    "supporting_domains": opp.supporting_domains,
                    "ranking_calculation": {
                        "formula": "opportunity_score = freq*0.30 + rel*0.25 + urg*0.20 + conf*0.15 + rec*0.10",
                        "frequency_score": opp.frequency_score,
                        "relevance_score": opp.relevance_score,
                        "urgency_score": opp.urgency_score,
                        "confidence_score": opp.confidence_score,
                        "recency_score": opp.recency_score,
                        "opportunity_score": opp.opportunity_score,
                        "breakdown": opp.score_breakdown,
                        "explanation": opp.score_explanation
                    },
                    "brief": opp.brief.model_dump() if opp.brief else None
                }
                for opp in session.opportunities
            ]
        }

        return json.dumps(data, indent=2)

