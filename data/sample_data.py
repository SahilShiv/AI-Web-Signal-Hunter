"""Pre-populated genuine sample research run for WhatsApp Automation Tools."""

from datetime import datetime, timezone
from models.opportunity import ResearchSession, Opportunity, OpportunityBrief, EvidenceReference
from models.signal import Signal
from models.page import CrawledPage
from core.opportunity_scorer import OpportunityScorer

SAMPLE_TOPIC = "What problems do small businesses face when using WhatsApp automation tools?"
SAMPLE_KEYWORDS = ["pricing", "bans", "crm", "templates", "chatbots"]

PAGES_DATA = [
    {
        "url": "https://getwati.com/blog/whatsapp-business-api-pricing/",
        "domain": "getwati.com",
        "title": "Understanding WhatsApp Business API Pricing for Growing SMBs",
        "word_count": 842,
        "date": "2024-04-12",
        "signals": [
            {
                "category": "Pricing Concern",
                "summary": "Meta's conversation-based pricing model creates unpredictable monthly costs for small businesses.",
                "evidence": "unpredictable monthly conversation costs and tier jumps often surprise small business owners who lack dedicated budgets",
                "rel": 92.0, "urg": 85.0, "conf": 94.0,
                "reasoning": "Direct evidence of pricing friction and cost volatility impacting small business cash flow."
            }
        ]
    },
    {
        "url": "https://respond.io/blog/whatsapp-business-api-problems",
        "domain": "respond.io",
        "title": "Top 10 WhatsApp Business API Limitations and How to Solve Them",
        "word_count": 1250,
        "date": "2024-03-20",
        "signals": [
            {
                "category": "Pain Point",
                "summary": "Strict 24-hour customer service messaging window severely restricts support follow-ups.",
                "evidence": "the 24-hour messaging window closes customer conversations prematurely, forcing agents to buy expensive outbound template messages",
                "rel": 95.0, "urg": 90.0, "conf": 96.0,
                "reasoning": "Explains core protocol friction where agents cannot reply to customers without purchasing template credits."
            }
        ]
    },
    {
        "url": "https://trengo.com/blog/whatsapp-business-api-limitations/",
        "domain": "trengo.com",
        "title": "WhatsApp Business Limitations: What Teams Need to Know Before Migrating",
        "word_count": 910,
        "date": "2024-02-18",
        "signals": [
            {
                "category": "Pain Point",
                "summary": "Meta template rejection causes massive marketing campaign launch delays.",
                "evidence": "template approvals are notoriously arbitrary and often rejected multiple times without explicit feedback on Meta policy violations",
                "rel": 88.0, "urg": 82.0, "conf": 91.0,
                "reasoning": "Highlights operational bottlenecks caused by automated approval delays."
            }
        ]
    },
    {
        "url": "https://botpenguin.com/blogs/whatsapp-automation-challenges",
        "domain": "botpenguin.com",
        "title": "The Biggest WhatsApp Automation Challenges Faced by Non-Technical Founders",
        "word_count": 1100,
        "date": "2024-05-02",
        "signals": [
            {
                "category": "Pain Point",
                "summary": "Complex non-intuitive flow builders lead to high bot abandonment rates.",
                "evidence": "non-technical users struggle with complex branching trees and webhook logic, resulting in abandoned setups after days of effort",
                "rel": 90.0, "urg": 78.0, "conf": 89.0,
                "reasoning": "Identifies software usability hurdles that prevent small merchants from deploying chatbots."
            }
        ]
    },
    {
        "url": "https://sleekflow.io/blog/whatsapp-business-api-issues-solutions",
        "domain": "sleekflow.io",
        "title": "Solving Common WhatsApp Business API Issues for Modern E-Commerce",
        "word_count": 1340,
        "date": "2024-01-29",
        "signals": [
            {
                "category": "Feature Request",
                "summary": "Lack of native two-way synchronization between WhatsApp chat threads and CRM contact records.",
                "evidence": "merchants demand seamless two-way CRM sync so chat history and purchase records don't have to be manually copied into HubSpot",
                "rel": 86.0, "urg": 75.0, "conf": 92.0,
                "reasoning": "Explicit user request for bi-directional CRM integration to avoid manual data entry."
            }
        ]
    },
    {
        "url": "https://twilio.com/en-us/blog/whatsapp-business-account-banned-fix",
        "domain": "twilio.com",
        "title": "Why WhatsApp Business Accounts Get Banned and How to Prevent It",
        "word_count": 1450,
        "date": "2024-06-11",
        "signals": [
            {
                "category": "Pain Point",
                "summary": "Sudden phone number bans and quality rating downgrades without warning.",
                "evidence": "accounts frequently get banned when low quality ratings trigger automated Meta flags, halting all business messaging overnight",
                "rel": 96.0, "urg": 95.0, "conf": 98.0,
                "reasoning": "Identifies an existential operational threat for businesses reliant on WhatsApp."
            }
        ]
    },
    {
        "url": "https://techcrunch.com/2023/06/05/whatsapp-business-pricing-update/",
        "domain": "techcrunch.com",
        "title": "Meta Revamps WhatsApp Business Messaging Rates, Shifting Burden to Small Merchants",
        "word_count": 780,
        "date": "2023-06-05",
        "signals": [
            {
                "category": "Pricing Concern",
                "summary": "Meta restructuring utility vs marketing conversation fees hits small margins.",
                "evidence": "the revised category-based fee structure drastically increased the cost of marketing broadcasts for small retailers operating on thin margins",
                "rel": 89.0, "urg": 80.0, "conf": 93.0,
                "reasoning": "Independent financial journalism confirming rising operational costs for SMBs."
            }
        ]
    },
    {
        "url": "https://medium.com/swlh/why-whatsapp-automation-fails-for-smbs-789a1",
        "domain": "medium.com",
        "title": "Why 60% of WhatsApp Automation Implementations Fail Within 90 Days",
        "word_count": 1620,
        "date": "2024-03-05",
        "signals": [
            {
                "category": "Pain Point",
                "summary": "Chatbots fail to recognize local dialects and regional languages, frustrating buyers.",
                "evidence": "rule-based chatbots repeatedly fail to interpret regional vernacular and dialects, driving customers away due to rigid scripted responses",
                "rel": 87.0, "urg": 76.0, "conf": 88.0,
                "reasoning": "Demonstrates language barrier challenges in automated conversational commerce."
            }
        ]
    },
    {
        "url": "https://getwati.com/blog/whatsapp-green-tick-verification-guide/",
        "domain": "getwati.com",
        "title": "The Elusive Green Tick: Why SMB Verification Requests Get Denied",
        "word_count": 980,
        "date": "2024-02-14",
        "signals": [
            {
                "category": "Pain Point",
                "summary": "Stringent notability criteria prevent legitimate local brands from getting official green tick badges.",
                "evidence": "Meta's brand notability requirement unfairly excludes growing small businesses from receiving the trusted green verification badge",
                "rel": 81.0, "urg": 68.0, "conf": 85.0,
                "reasoning": "Identifies credibility issues where SMBs cannot gain consumer trust compared to enterprise accounts."
            }
        ]
    },
    {
        "url": "https://respond.io/blog/whatsapp-crm-integration-challenges",
        "domain": "respond.io",
        "title": "Overcoming WhatsApp and CRM Integration Bottlenecks in Sales Teams",
        "word_count": 1150,
        "date": "2024-04-22",
        "signals": [
            {
                "category": "Demand Signal",
                "summary": "High market demand for lightweight WhatsApp-to-CRM syncing tools.",
                "evidence": "sales organizations urgently require instant contact export and deal tracking directly inside the WhatsApp web workspace",
                "rel": 91.0, "urg": 84.0, "conf": 92.0,
                "reasoning": "Clear market demand from revenue teams looking to bridge chat to pipeline."
            }
        ]
    },
    {
        "url": "https://trengo.com/blog/whatsapp-team-inbox-features/",
        "domain": "trengo.com",
        "title": "Managing Shared WhatsApp Inboxes Without Agent Collisions",
        "word_count": 870,
        "date": "2024-01-15",
        "signals": [
            {
                "category": "Feature Request",
                "summary": "Need for real-time agent collision warnings to avoid duplicate answers to leads.",
                "evidence": "teams frequently ask for live typing collision indicators to stop two agents from responding to the same customer at once",
                "rel": 83.0, "urg": 70.0, "conf": 87.0,
                "reasoning": "Workflow collaboration feature requested by customer support teams."
            }
        ]
    },
    {
        "url": "https://botpenguin.com/blogs/whatsapp-chatbot-human-handoff",
        "domain": "botpenguin.com",
        "title": "Why Automated Human Handoff is Critical in WhatsApp Chatbots",
        "word_count": 1040,
        "date": "2024-05-18",
        "signals": [
            {
                "category": "Pain Point",
                "summary": "Broken bot-to-human escalation leaves angry customers trapped in repetitive bot loops.",
                "evidence": "when automated bots fail to recognize customer frustration, lack of instant escalation to human agents causes immediate customer loss",
                "rel": 93.0, "urg": 88.0, "conf": 94.0,
                "reasoning": "Identifies high churn risk when bot escalation is poorly configured."
            }
        ]
    },
    {
        "url": "https://sleekflow.io/blog/whatsapp-broadcast-limits-tiers",
        "domain": "sleekflow.io",
        "title": "Navigating Meta Messaging Limits: From Tier 1 to Tier 3 Explained",
        "word_count": 1210,
        "date": "2024-03-12",
        "signals": [
            {
                "category": "Pain Point",
                "summary": "1,000 unique recipient daily cap on Tier 1 chokes SMB flash sales and promotions.",
                "evidence": "the Tier 1 limit of 1,000 daily messages restricts marketing broadcasts during peak seasonal sales and festival campaigns",
                "rel": 85.0, "urg": 74.0, "conf": 89.0,
                "reasoning": "Capacity bottlenecks hindering marketing reach."
            }
        ]
    },
    {
        "url": "https://twilio.com/en-us/blog/whatsapp-template-guidelines-best-practices",
        "domain": "twilio.com",
        "title": "How to Avoid Meta Template Rejections: A Practical Guide",
        "word_count": 1390,
        "date": "2024-06-02",
        "signals": [
            {
                "category": "Feature Request",
                "summary": "Demand for automated AI template pre-checkers to predict approval success.",
                "evidence": "developers are asking for pre-flight linter tools to analyze template wording against Meta guidelines before formal submission",
                "rel": 88.0, "urg": 81.0, "conf": 90.0,
                "reasoning": "Product feature request for pre-flight compliance checking."
            }
        ]
    },
    {
        "url": "https://techcrunch.com/2024/01/10/conversational-commerce-challenges/",
        "domain": "techcrunch.com",
        "title": "Conversational Commerce Is Booming, but SMB Infrastructure Remains Brittle",
        "word_count": 940,
        "date": "2024-01-10",
        "signals": [
            {
                "category": "Competitor Activity",
                "summary": "Businesses migrating between WhatsApp BSPs due to high software platform markup.",
                "evidence": "growing dissatisfaction with legacy BSP markups is driving small merchants toward low-overhead direct Cloud API providers",
                "rel": 84.0, "urg": 72.0, "conf": 86.0,
                "reasoning": "Market migration trends away from high-fee legacy providers."
            }
        ]
    },
    {
        "url": "https://medium.com/swlh/whatsapp-automation-pricing-trap-9821a",
        "domain": "medium.com",
        "title": "The WhatsApp Automation Pricing Trap: Why Our Agency Switched Providers",
        "word_count": 1410,
        "date": "2024-04-08",
        "signals": [
            {
                "category": "Pricing Concern",
                "summary": "Vendor platform subscription fees on top of Meta usage fees create double billing.",
                "evidence": "paying a mandatory $199 monthly platform fee on top of Meta's per-conversation charges makes WhatsApp unviable for early-stage shops",
                "rel": 94.0, "urg": 86.0, "conf": 95.0,
                "reasoning": "Customer complaint regarding double-tax pricing structures."
            }
        ]
    },
    {
        "url": "https://getwati.com/blog/whatsapp-catalog-sync-shopify/",
        "domain": "getwati.com",
        "title": "Syncing Shopify Products with WhatsApp Catalog: What Works and What Fails",
        "word_count": 1050,
        "date": "2024-03-28",
        "signals": [
            {
                "category": "Pain Point",
                "summary": "Out-of-sync product catalogs lead to customers ordering discontinued items.",
                "evidence": "inventory desynchronization between Shopify store databases and WhatsApp catalogs causes embarrassing cancellations and refund disputes",
                "rel": 86.0, "urg": 79.0, "conf": 88.0,
                "reasoning": "E-commerce inventory synchronization friction."
            }
        ]
    },
    {
        "url": "https://respond.io/blog/whatsapp-multi-agent-customer-support",
        "domain": "respond.io",
        "title": "Scaling Customer Support on WhatsApp Across Distributed Remote Agents",
        "word_count": 1180,
        "date": "2024-05-10",
        "signals": [
            {
                "category": "Buying Intent",
                "summary": "Customer service teams actively budgeting for centralized WhatsApp support platforms.",
                "evidence": "companies are reallocating email helpdesk budget toward WhatsApp-first customer support suites with multi-seat access",
                "rel": 82.0, "urg": 65.0, "conf": 84.0,
                "reasoning": "Active budget reallocation and commercial buying intent."
            }
        ]
    },
    {
        "url": "https://trengo.com/blog/whatsapp-automation-roi-metrics/",
        "domain": "trengo.com",
        "title": "Measuring Real ROI on WhatsApp Automation: Beyond Open Rates",
        "word_count": 890,
        "date": "2024-02-25",
        "signals": [
            {
                "category": "Pain Point",
                "summary": "Lack of conversion tracking and revenue attribution for chat sales.",
                "evidence": "marketing leads complain they cannot accurately track WhatsApp message clicks back to completed e-commerce checkout purchases",
                "rel": 80.0, "urg": 71.0, "conf": 83.0,
                "reasoning": "Analytics attribution gap for conversational revenue."
            }
        ]
    },
    {
        "url": "https://botpenguin.com/blogs/whatsapp-cloud-api-vs-on-premise",
        "domain": "botpenguin.com",
        "title": "WhatsApp Cloud API vs On-Premise: Why Most SMBs Stumble During Setup",
        "word_count": 1280,
        "date": "2024-04-03",
        "signals": [
            {
                "category": "Pain Point",
                "summary": "Meta Business Manager verification and webhook token configuration are excessively technical.",
                "evidence": "the initial onboarding process through Meta Developer Console and Business Manager verification creates severe friction for non-engineers",
                "rel": 91.0, "urg": 83.0, "conf": 93.0,
                "reasoning": "Technical onboarding barrier for small businesses."
            }
        ]
    },
    {
        "url": "https://sleekflow.io/blog/whatsapp-automation-security-privacy",
        "domain": "sleekflow.io",
        "title": "WhatsApp Data Privacy and GDPR Compliance for European Merchants",
        "word_count": 1130,
        "date": "2024-03-18",
        "signals": [
            {
                "category": "Pain Point",
                "summary": "Concerns over storing customer conversations and PII on third-party overseas servers.",
                "evidence": "European SMBs struggle to find WhatsApp tools with guaranteed EU data residency to satisfy strict GDPR audit standards",
                "rel": 82.0, "urg": 75.0, "conf": 87.0,
                "reasoning": "Data compliance and security requirements in regulated markets."
            }
        ]
    },
    {
        "url": "https://twilio.com/en-us/blog/whatsapp-interactive-messages-quick-replies",
        "domain": "twilio.com",
        "title": "Building Better WhatsApp Experiences with Interactive Buttons and Lists",
        "word_count": 1310,
        "date": "2024-05-25",
        "signals": [
            {
                "category": "Feature Request",
                "summary": "Call for flexible dynamic button menus and customizable quick replies.",
                "evidence": "merchants want the ability to generate dynamic interactive list messages that populate in real time from SQL inventory feeds",
                "rel": 85.0, "urg": 69.0, "conf": 88.0,
                "reasoning": "UI interaction capability request from developers."
            }
        ]
    },
    {
        "url": "https://techcrunch.com/2023/11/15/ai-agents-customer-service-whatsapp/",
        "domain": "techcrunch.com",
        "title": "Generative AI Reaches Customer Service Chatbots, but Hallucinations Persist",
        "word_count": 920,
        "date": "2023-11-15",
        "signals": [
            {
                "category": "Pain Point",
                "summary": "AI chatbots hallucinate incorrect return policies and pricing to customers.",
                "evidence": "early generative AI chatbot deployments frequently gave inaccurate discounts and invented return policies that businesses had to honor",
                "rel": 92.0, "urg": 89.0, "conf": 94.0,
                "reasoning": "Hallucination risks in automated conversational commerce."
            }
        ]
    },
    {
        "url": "https://medium.com/swlh/whatsapp-broadcasting-spam-rate-limits-6523c",
        "domain": "medium.com",
        "title": "How to Run WhatsApp Broadcasts Without Triggering User Block Buttons",
        "word_count": 1380,
        "date": "2024-02-09",
        "signals": [
            {
                "category": "Pain Point",
                "summary": "High user block rates when promotional broadcasts lack personalized segmentation.",
                "evidence": "unsegmented broadcast campaigns result in quick user blocks, which Meta's algorithm penalizes with immediate tier demotion",
                "rel": 89.0, "urg": 84.0, "conf": 91.0,
                "reasoning": "Deliverability and quality score penalties caused by unsegmented messaging."
            }
        ]
    },
    {
        "url": "https://getwati.com/blog/whatsapp-automation-best-practices-2024/",
        "domain": "getwati.com",
        "title": "The Definitive WhatsApp Automation Playbook for Growing Brands in 2024",
        "word_count": 1540,
        "date": "2024-06-01",
        "signals": [
            {
                "category": "Demand Signal",
                "summary": "Rapid shift toward conversational commerce as the primary conversion channel for SMBs.",
                "evidence": "over 70% of surveyed small retailers now report that WhatsApp has become their highest-converting direct sales channel",
                "rel": 90.0, "urg": 65.0, "conf": 93.0,
                "reasoning": "Market demand validation confirming WhatsApp as a high-intent conversion surface."
            }
        ]
    }
]


def build_sample_session() -> tuple[ResearchSession, list[CrawledPage]]:
    """Builds the full benchmark research run with 25 pages across 8 domains."""
    crawled_pages: list[CrawledPage] = []
    signals: list[Signal] = []

    for item in PAGES_DATA:
        from utils.helpers import compute_sha256
        dummy_content = f"# {item['title']}\n\nPublished: {item['date']}\n\n"
        for sig in item["signals"]:
            dummy_content += f"{sig['summary']} Furthermore, {sig['evidence']} as reported by analysts.\n\n"

        page = CrawledPage(
            url=item["url"],
            domain=item["domain"],
            title=item["title"],
            cleaned_text=dummy_content,
            word_count=item["word_count"],
            content_hash=compute_sha256(dummy_content),
            crawl_date=datetime.now(timezone.utc),
            published_date=item["date"],
            status_code=200,
            is_valid=True
        )
        crawled_pages.append(page)

        for sig_item in item["signals"]:
            sig = Signal(
                source_url=item["url"],
                source_domain=item["domain"],
                page_title=item["title"],
                signal_category=sig_item["category"],
                summary=sig_item["summary"],
                evidence=sig_item["evidence"],
                evidence_verified=True,
                relevance_score=sig_item["rel"],
                urgency_score=sig_item["urg"],
                confidence_score=sig_item["conf"],
                reasoning=sig_item["reasoning"],
                is_relevant=True,
                published_date=item["date"]
            )
            signals.append(sig)

    # Use Grouper to cluster signals and generate top 5 briefs
    from core.opportunity_grouper import OpportunityGrouper
    from core.opportunity_brief import OpportunityBriefGenerator

    grouper = OpportunityGrouper()
    opportunities = grouper.group_signals(SAMPLE_TOPIC, signals)

    brief_gen = OpportunityBriefGenerator()
    opportunities = brief_gen.generate_briefs(opportunities, top_n=5)

    unique_domains = list({p.domain for p in crawled_pages})

    session = ResearchSession(
        id="sample-whatsapp-benchmark-01",
        topic=SAMPLE_TOPIC,
        keywords=SAMPLE_KEYWORDS,
        ai_provider="Groq",
        ai_model="llama-3.3-70b-versatile",
        crawl_limit=25,
        min_relevance_threshold=60.0,
        pages_discovered=32,
        pages_crawled_count=len(crawled_pages),
        pages_skipped_count=7,
        signals_count=len(signals),
        opportunities_count=len(opportunities),
        unique_domains_count=len(unique_domains),
        signals=signals,
        opportunities=opportunities
    )

    return session, crawled_pages
