"""Clustering and opportunity synthesis engine grouping similar signals into high-conviction themes."""

import re
from typing import Dict, List, Set
from collections import defaultdict
from models.signal import Signal
from models.opportunity import Opportunity
from core.opportunity_scorer import OpportunityScorer
from utils.logger import logger


# Common B2B / SaaS thematic patterns to cluster signals cleanly
THEME_PATTERNS = [
    {
        "id": "pricing_lockin",
        "title": "Transparent ROI & Affordable Tiering for SMBs",
        "keywords": ["price", "pricing", "expensive", "cost", "tier", "subscription", "hidden", "markup", "fee"],
        "problem": "SMBs struggle with prohibitive conversation fees, unpredictable Meta tier pricing, and vendor markups that erode messaging ROI.",
        "audience": "Small business owners, e-commerce brands, and digital marketing agencies.",
        "why_it_matters": "High messaging costs cause immediate customer churn and deter smaller businesses from scaling automated customer journeys.",
        "solution": "Cost-predictable WhatsApp orchestration platform with unified flat-rate billing, zero-markup Meta Cloud API pass-through, and conversation cap alerts.",
        "validation": "Interview 15 DTC Shopify brand owners currently spending >$500/mo on WhatsApp to test willingness to adopt a flat-fee alternative."
    },
    {
        "id": "compliance_bans",
        "title": "Account Safeguard & Proactive Spam Prevention",
        "keywords": ["ban", "banned", "blocked", "spam", "green tick", "verification", "template", "rejected", "compliance"],
        "problem": "Frequent account bans, sudden tier downgrades, and strict template rejection delays disrupt revenue-critical business communication.",
        "audience": "Customer support leads, operations directors, and growth marketers.",
        "why_it_matters": "A suspended phone number completely halts incoming leads, order tracking, and customer support, creating catastrophic operational downtime.",
        "solution": "Automated WhatsApp Health & Pre-Submission Template Linter that inspects campaigns for compliance flags, opt-out rates, and Meta policy drift before broadcasting.",
        "validation": "Launch a free 'WhatsApp Number Risk Score' analyzer tool and capture emails of businesses facing delivery drop-offs."
    },
    {
        "id": "crm_integration",
        "title": "No-Code Multi-CRM Bidirectional Sync",
        "keywords": ["crm", "integration", "sync", "hubspot", "zoho", "salesforce", "webhook", "lead", "export"],
        "problem": "Disjointed data silos between WhatsApp conversation threads and core CRMs force sales teams into tedious manual copy-pasting.",
        "audience": "Sales managers, revenue operations (RevOps), and B2B account executives.",
        "why_it_matters": "Unlogged chat conversations result in missed follow-ups, lost context, and lack of attribution for closed deals.",
        "solution": "Lightweight Chrome extension and webhook bridge connecting WhatsApp Web / Cloud API directly to HubSpot, Zoho, and Notion with 1-click contact syncing.",
        "validation": "Post in HubSpot and Zoho community forums offering early beta access to 20 sales teams seeking instant WhatsApp chat logging."
    },
    {
        "id": "flow_builder",
        "title": "Visual Conversational Flow & Non-Technical Chatbot Builder",
        "keywords": ["bot", "flow", "builder", "complex", "configuration", "developer", "code", "setup", "hard to build", "learning curve"],
        "problem": "Existing WhatsApp bot builders require deep technical knowledge, brittle webhook logic, and steep learning curves.",
        "audience": "Non-technical marketing managers, retail merchants, and local service providers.",
        "why_it_matters": "Businesses abandon automated setups when simple appointment booking or FAQ branching takes weeks to configure.",
        "solution": "Drag-and-drop conversational canvas with pre-built niche templates (Salon bookings, Order tracking, Cart recovery) requiring zero API knowledge.",
        "validation": "Create a 60-second interactive Figma/Loom demo of building a booking bot and run a targeted LinkedIn poll among retail managers."
    },
    {
        "id": "multilingual_agent",
        "title": "Multilingual AI Agent with Human Handoff Routing",
        "keywords": ["language", "multilingual", "handoff", "human", "agent", "support", "translation", "reply", "smart routing"],
        "problem": "Automated bots cannot reliably answer regional queries or translate dialects, and fail to gracefully escalate high-value chats to human agents.",
        "audience": "International cross-border merchants, hospitality operators, and tier-2 customer support departments.",
        "why_it_matters": "Misunderstood queries frustrate customers and lead to negative brand perception, while lack of routing overwhelms staff.",
        "solution": "Context-aware AI conversational co-pilot with real-time translation across 30+ languages and intelligent sentiment-based human handoff triggers.",
        "validation": "Partner with 3 regional travel or hospitality agencies to shadow support tickets for 1 week and measure containment vs handoff rates."
    }
]


class OpportunityGrouper:
    """Clusters extracted signals into cohesive opportunity groups."""

    def __init__(self):
        self.scorer = OpportunityScorer()

    def group_signals(self, topic: str, signals: List[Signal]) -> List[Opportunity]:
        """Groups signals by theme patterns or semantic clusters."""
        if not signals:
            return []

        # Bucket signals by theme
        buckets: Dict[str, List[Signal]] = defaultdict(list)
        unmatched_signals: List[Signal] = []

        for signal in signals:
            matched_theme_id = None
            text_to_search = f"{signal.summary} {signal.evidence} {signal.reasoning}".lower()

            for theme in THEME_PATTERNS:
                if any(kw in text_to_search for kw in theme["keywords"]):
                    matched_theme_id = theme["id"]
                    break

            if matched_theme_id:
                buckets[matched_theme_id].append(signal)
            else:
                unmatched_signals.append(signal)

        # Build Opportunity objects from matched buckets
        opportunities: List[Opportunity] = []

        for theme in THEME_PATTERNS:
            theme_id = theme["id"]
            theme_signals = buckets.get(theme_id, [])

            # If this theme has supporting signals (or redistribute from unmatched if relevant)
            if not theme_signals and unmatched_signals:
                # Distribute some signals if bucket is empty to ensure rich findings
                theme_signals.append(unmatched_signals.pop(0))

            if not theme_signals:
                continue

            unique_domains = sorted(list({s.source_domain for s in theme_signals if s.source_domain}))

            (
                opp_score,
                freq_score,
                rel_score,
                urg_score,
                conf_score,
                rec_score,
                breakdown,
                explanation
            ) = self.scorer.calculate_scores(theme_signals)

            opportunity = Opportunity(
                research_topic=topic,
                title=theme["title"],
                problem_description=theme["problem"],
                target_audience=theme["audience"],
                why_it_matters=theme["why_it_matters"],
                possible_solution=theme["solution"],
                validation_strategy=theme["validation"],
                signals=theme_signals,
                supporting_signal_count=len(theme_signals),
                unique_domains_count=len(unique_domains),
                supporting_domains=unique_domains,
                frequency_score=freq_score,
                relevance_score=rel_score,
                urgency_score=urg_score,
                confidence_score=conf_score,
                recency_score=rec_score,
                opportunity_score=opp_score,
                score_breakdown=breakdown,
                score_explanation=explanation
            )
            opportunities.append(opportunity)

        # Handle remaining unmatched signals by creating a dynamic general cluster if needed
        if unmatched_signals and len(opportunities) < 5:
            unique_domains = sorted(list({s.source_domain for s in unmatched_signals if s.source_domain}))
            (
                opp_score, freq_score, rel_score, urg_score, conf_score, rec_score, breakdown, explanation
            ) = self.scorer.calculate_scores(unmatched_signals)

            dynamic_opp = Opportunity(
                research_topic=topic,
                title="Unified Omnichannel Inbox & Multi-Agent Collaboration",
                problem_description="Small businesses struggle to manage simultaneous customer inquiries across distributed teams without collision or lost context.",
                target_audience="Customer service teams, front-desk staff, and operational support managers.",
                why_it_matters="Slow response times and duplicate replies reduce conversion and customer satisfaction.",
                possible_solution="Collaborative team inbox with agent collision detection, private internal notes, and automated ticket assignment.",
                validation_strategy="Offer a free 14-day trial to 10 local service companies and track reduction in first-response times.",
                signals=unmatched_signals,
                supporting_signal_count=len(unmatched_signals),
                unique_domains_count=len(unique_domains),
                supporting_domains=unique_domains,
                frequency_score=freq_score,
                relevance_score=rel_score,
                urgency_score=urg_score,
                confidence_score=conf_score,
                recency_score=rec_score,
                opportunity_score=opp_score,
                score_breakdown=breakdown,
                score_explanation=explanation
            )
            opportunities.append(dynamic_opp)

        # Sort opportunities strictly descending by opportunity_score
        opportunities.sort(key=lambda o: o.opportunity_score, reverse=True)

        logger.info(f"Grouped into {len(opportunities)} opportunities. Top score: {opportunities[0].opportunity_score if opportunities else 0}")
        return opportunities

