"""Application constants and configuration presets for AI Web Signal Hunter."""

from typing import Dict, List

# Signal Categories
CATEGORY_PAIN_POINT = "Pain Point"
CATEGORY_DEMAND_SIGNAL = "Demand Signal"
CATEGORY_FEATURE_REQUEST = "Feature Request"
CATEGORY_PRICING_CONCERN = "Pricing Concern"
CATEGORY_BUYING_INTENT = "Buying Intent"
CATEGORY_COMPETITOR_ACTIVITY = "Competitor Activity"
CATEGORY_IRRELEVANT = "Irrelevant Content"

SIGNAL_CATEGORIES: List[str] = [
    CATEGORY_PAIN_POINT,
    CATEGORY_DEMAND_SIGNAL,
    CATEGORY_FEATURE_REQUEST,
    CATEGORY_PRICING_CONCERN,
    CATEGORY_BUYING_INTENT,
    CATEGORY_COMPETITOR_ACTIVITY,
    CATEGORY_IRRELEVANT,
]

RELEVANT_CATEGORIES: List[str] = [
    CATEGORY_PAIN_POINT,
    CATEGORY_DEMAND_SIGNAL,
    CATEGORY_FEATURE_REQUEST,
    CATEGORY_PRICING_CONCERN,
    CATEGORY_BUYING_INTENT,
    CATEGORY_COMPETITOR_ACTIVITY,
]

# UI Category Color Map (SaaS Slate / Indigo aesthetic)
CATEGORY_COLORS: Dict[str, str] = {
    CATEGORY_PAIN_POINT: "#EF4444",        # Red
    CATEGORY_DEMAND_SIGNAL: "#10B981",      # Emerald
    CATEGORY_FEATURE_REQUEST: "#3B82F6",    # Blue
    CATEGORY_PRICING_CONCERN: "#F59E0B",    # Amber
    CATEGORY_BUYING_INTENT: "#8B5CF6",      # Purple
    CATEGORY_COMPETITOR_ACTIVITY: "#06B6D4",# Cyan
    CATEGORY_IRRELEVANT: "#64748B",         # Slate
}

CATEGORY_DESCRIPTIONS: Dict[str, str] = {
    CATEGORY_PAIN_POINT: "Problems, bottlenecks, and frustrations experienced by users.",
    CATEGORY_DEMAND_SIGNAL: "Expressed market need, interest, or active search for a capability.",
    CATEGORY_FEATURE_REQUEST: "Explicit enhancements or new capabilities requested by customers.",
    CATEGORY_PRICING_CONCERN: "Complaints or friction regarding pricing tiers, ROI, or hidden costs.",
    CATEGORY_BUYING_INTENT: "Indications that customers are evaluating or actively purchasing tools.",
    CATEGORY_COMPETITOR_ACTIVITY: "Shifts, migrations, or comparisons regarding rival platforms.",
    CATEGORY_IRRELEVANT: "Fluff, marketing boilerplate, or non-actionable content.",
}

# Opportunity Scoring Weights (Must sum to 1.0)
WEIGHT_FREQUENCY = 0.30
WEIGHT_RELEVANCE = 0.25
WEIGHT_URGENCY = 0.20
WEIGHT_CONFIDENCE = 0.15
WEIGHT_RECENCY = 0.10

# AI Provider Names
PROVIDER_GROQ = "Groq"
PROVIDER_GEMINI = "Gemini"
SUPPORTED_PROVIDERS: List[str] = [PROVIDER_GROQ, PROVIDER_GEMINI]

# Default AI Models
DEFAULT_GROQ_MODEL = "llama-3.3-70b-versatile"
DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"

# Default Crawler Settings
DEFAULT_CRAWL_LIMIT = 25
MIN_CRAWL_LIMIT = 5
MAX_CRAWL_LIMIT = 50
DEFAULT_MIN_RELEVANCE = 60
DEFAULT_REQUEST_TIMEOUT = 12
DEFAULT_REQUEST_DELAY = 0.8
DEFAULT_USER_AGENT = "AI-Web-Signal-Hunter/1.0 (+https://github.com/internship/ai-web-signal-hunter; polite bot)"
MAX_EVIDENCE_WORDS = 30

