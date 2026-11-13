"""AI Web Signal Hunter - Enterprise AI Web Intelligence Platform.

Main Streamlit Application.
"""

import os
import time
import streamlit as st
from config.settings import settings
from config.constants import (
    SUPPORTED_PROVIDERS,
    PROVIDER_GROQ,
    PROVIDER_GEMINI,
    DEFAULT_CRAWL_LIMIT,
    MIN_CRAWL_LIMIT,
    MAX_CRAWL_LIMIT,
    DEFAULT_MIN_RELEVANCE
)
from database.database import DatabaseManager
from services.database_service import DatabaseService
from services.export_service import ExportService
from core.search_engine import SearchEngine
from core.crawler import WebCrawler
from core.ai_analyzer import AIAnalyzer
from core.signal_extractor import SignalExtractor
from core.opportunity_grouper import OpportunityGrouper
from core.opportunity_brief import OpportunityBriefGenerator
from models.opportunity import ResearchSession
from utils.validators import clean_keywords
from data.sample_data import build_sample_session

from components.sidebar import render_sidebar
from components.dashboard import render_dashboard
from components.findings_table import render_findings_explorer
from components.opportunity_details import render_opportunity_details


# Configure Streamlit page settings
st.set_page_config(
    page_title="AI Web Signal Hunter | Market Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Enterprise SaaS CSS
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Force dark background and light text across whole app */
    .stApp {
        background-color: #0B0F19 !important;
        color: #F8FAFC !important;
    }

    header[data-testid="stHeader"] {
        background-color: #0B0F19 !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid #1E293B !important;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2.5rem;
        max-width: 1280px;
    }

    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        color: #F8FAFC !important;
    }

    /* Paragraphs and labels */
    p, span, label, div {
        color: inherit;
    }

    /* Sleek scrollbars */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #0B0F19;
    }
    ::-webkit-scrollbar-thumb {
        background: #1E293B;
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #334155;
    }

    /* Metric card styling */
    div[data-testid="stMetricValue"] {
        font-weight: 800 !important;
        color: #F8FAFC !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #94A3B8 !important;
    }

    /* Buttons */
    button[kind="primary"] {
        background: linear-gradient(135deg, #2563EB, #1D4ED8) !important;
        border: 1px solid #3B82F6 !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        border-radius: 6px !important;
        transition: all 0.2s ease;
    }
    button[kind="primary"]:hover {
        background: #1D4ED8 !important;
        border-color: #60A5FA !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
    }
    button[kind="secondary"] {
        background: #111827 !important;
        border: 1px solid #1F2937 !important;
        color: #E2E8F0 !important;
        border-radius: 6px !important;
    }
    button[kind="secondary"]:hover {
        background: #1E293B !important;
        border-color: #374151 !important;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #111827 !important;
        border: 1px solid #1F2937 !important;
        border-radius: 6px !important;
        color: #F1F5F9 !important;
        font-weight: 600 !important;
    }

    /* Input textboxes */
    input[type="text"], input[type="password"], textarea {
        background-color: #111827 !important;
        border: 1px solid #1F2937 !important;
        color: #F8FAFC !important;
        border-radius: 6px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def initialize_app_state():
    """Initializes database and seeds genuine sample run on first launch."""
    if "db_service" not in st.session_state:
        db_mgr = DatabaseManager()
        st.session_state["db_service"] = DatabaseService(db_mgr)

    db_service: DatabaseService = st.session_state["db_service"]

    # Pre-seed benchmark research if empty
    sessions = db_service.list_sessions()
    if not sessions:
        sample_session, sample_pages = build_sample_session()
        db_service.save_session(sample_session, pages=sample_pages)
        st.session_state["active_session"] = sample_session
    elif "active_session" not in st.session_state:
        # Load most recent session
        latest_id = sessions[0]["id"]
        st.session_state["active_session"] = db_service.get_session(latest_id)


def execute_research_pipeline(
    topic: str,
    raw_keywords: str,
    crawl_limit: int,
    ai_provider: str,
    min_relevance: float,
    status_container
):
    """Executes the end-to-end intelligence collection pipeline."""
    keywords = clean_keywords(raw_keywords)

    with status_container:
        st.markdown("### 🔄 Research Pipeline Active")
        progress_bar = st.progress(0)
        status_text = st.empty()
        log_box = st.empty()

        def update_progress(pct: int, msg: str):
            progress_bar.progress(pct)
            status_text.markdown(f"**Step Progress:** {msg}")

        # Phase 1: Web Discovery
        update_progress(5, "Discovering candidate public pages across independent domains...")
        searcher = SearchEngine()
        discovered_urls = searcher.discover_urls(topic, keywords=keywords, max_urls=crawl_limit + 10)

        if not discovered_urls:
            st.error("No candidate URLs discovered for this query. Please check your keywords or topic.")
            return None

        update_progress(15, f"Discovered {len(discovered_urls)} candidate URLs. Beginning respectful crawl...")

        # Phase 2: Crawling & Cleaning
        crawler = WebCrawler(
            request_timeout=settings.request_timeout,
            request_delay=settings.request_delay
        )

        def crawler_progress(data: dict):
            pct = 15 + int(data.get("percent", 0) * 0.40)
            update_progress(
                pct,
                f"Crawled {data.get('crawled')}/{crawl_limit} pages (Domain: {data.get('current_domain')})"
            )
            log_box.caption(f"Status: {data.get('status_text')}")

        crawled_pages = crawler.crawl_urls(
            discovered_urls,
            max_pages=crawl_limit,
            progress_callback=crawler_progress
        )

        if not crawled_pages:
            st.error("Failed to collect web pages. Sources may be temporarily unreachable.")
            return None

        update_progress(55, f"Successfully collected {len(crawled_pages)} verified pages. Starting AI Signal Extraction...")

        # Phase 3: AI Signal Extraction
        analyzer = AIAnalyzer(provider=ai_provider)
        extractor = SignalExtractor(analyzer=analyzer, min_relevance=min_relevance)

        def extraction_progress(data: dict):
            pct = 55 + int(data.get("percent", 0) * 0.25)
            update_progress(
                pct,
                f"Extracting signals from {data.get('domain')} ({data.get('current_index')}/{data.get('total_pages')})"
            )
            log_box.caption(f"Found {data.get('signals_found_so_far')} business signals so far...")

        signals = extractor.extract_from_pages(
            topic=topic,
            pages=crawled_pages,
            progress_callback=extraction_progress
        )

        update_progress(80, f"Extracted {len(signals)} signals. Clustering into opportunity themes...")

        # Phase 4: Opportunity Grouping & Scoring
        grouper = OpportunityGrouper()
        opportunities = grouper.group_signals(topic=topic, signals=signals)

        update_progress(90, "Synthesizing executive briefs for top opportunities...")

        # Phase 5: Opportunity Brief Generation
        brief_gen = OpportunityBriefGenerator()
        opportunities = brief_gen.generate_briefs(opportunities, top_n=5)

        unique_domains = list({p.domain for p in crawled_pages})

        session = ResearchSession(
            topic=topic,
            keywords=keywords,
            ai_provider=ai_provider,
            crawl_limit=crawl_limit,
            min_relevance_threshold=min_relevance,
            pages_discovered=len(discovered_urls),
            pages_crawled_count=len(crawled_pages),
            pages_skipped_count=len(discovered_urls) - len(crawled_pages),
            signals_count=len(signals),
            opportunities_count=len(opportunities),
            unique_domains_count=len(unique_domains),
            signals=signals,
            opportunities=opportunities
        )

        # Phase 6: Persistence in SQLite
        update_progress(98, "Persisting findings to local database...")
        db_service: DatabaseService = st.session_state["db_service"]
        db_service.save_session(session, pages=crawled_pages)

        update_progress(100, "Research completed successfully!")
        st.success(f"✓ Research finished: {len(crawled_pages)} pages crawled, {len(signals)} signals found, {len(opportunities)} opportunities synthesized.")
        return session


def render_new_research_page():
    """Renders research input section and triggers live crawl pipeline."""
    st.markdown(
        """
        <div style="margin-bottom: 24px;">
            <h1 style="font-size: 26px; font-weight: 700; color: #F8FAFC; margin-bottom: 4px;">
                🔍 Launch New Web Intelligence Research
            </h1>
            <p style="color: #94A3B8; font-size: 14px; margin: 0;">
                Enter a business question, industry, or software domain to automatically crawl live public web pages, extract customer signals, and rank opportunities.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.container():
        # Example queries expander
        with st.expander("💡 Recommended Research Prompts (Click to explore)", expanded=False):
            st.markdown(
                """
                - **What problems do small businesses face with WhatsApp automation tools?**
                - **What features are customers requesting from AI meeting assistants?**
                - **What complaints and opportunities exist in EV charging services?**
                - **What are the common problems faced by users of project management software?**
                - **What are customers saying about AI-powered resume builders?**
                """
            )

        col1, col2 = st.columns([3, 1])

        with col1:
            topic_input = st.text_input(
                "Primary Research Topic / Business Question *",
                value="What problems do small businesses face with WhatsApp automation tools?",
                placeholder="e.g. What are the common complaints with project management tools?"
            )

        with col2:
            provider_choice = st.selectbox(
                "Preferred AI Provider",
                SUPPORTED_PROVIDERS,
                index=0
            )

        keywords_input = st.text_input(
            "Optional Focus Keywords (comma-separated)",
            value="pricing, bans, CRM, integration, onboarding",
            placeholder="e.g. pricing, latency, bugs, support"
        )

        col_s1, col_s2 = st.columns(2)
        with col_s1:
            crawl_limit = st.slider(
                "Target Pages to Crawl (Minimum 5, Default 25)",
                min_value=MIN_CRAWL_LIMIT,
                max_value=MAX_CRAWL_LIMIT,
                value=DEFAULT_CRAWL_LIMIT,
                step=5
            )
        with col_s2:
            min_relevance = st.slider(
                "Minimum Relevance Score Filter (0-100)",
                min_value=0,
                max_value=100,
                value=DEFAULT_MIN_RELEVANCE,
                step=5
            )

        status_container = st.container()

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        if st.button("🚀 Start Intelligence Pipeline", type="primary", use_container_width=True):
            if not topic_input or len(topic_input.strip()) < 5:
                st.error("Please enter a valid research topic or business question (at least 5 characters).")
            else:
                new_session = execute_research_pipeline(
                    topic=topic_input.strip(),
                    raw_keywords=keywords_input,
                    crawl_limit=crawl_limit,
                    ai_provider=provider_choice,
                    min_relevance=float(min_relevance),
                    status_container=status_container
                )
                if new_session:
                    st.session_state["active_session"] = new_session
                    time.sleep(1.5)
                    st.session_state["current_page"] = "Dashboard"
                    st.rerun()


def render_research_history_page():
    """Renders list of saved research runs with option to reload or delete."""
    st.markdown(
        """
        <div style="margin-bottom: 24px;">
            <h1 style="font-size: 24px; font-weight: 700; color: #F8FAFC; margin-bottom: 4px;">
                📜 Research History
            </h1>
            <p style="color: #94A3B8; font-size: 14px; margin: 0;">
                All completed research sessions are persistently stored in your local SQLite database.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    db_service: DatabaseService = st.session_state["db_service"]
    sessions = db_service.list_sessions()

    if not sessions:
        st.info("No saved research sessions yet.")
        return

    active_id = st.session_state.get("active_session").id if st.session_state.get("active_session") else ""

    for s in sessions:
        is_current = (s["id"] == active_id)
        border_color = "#3B82F6" if is_current else "#1F2937"

        st.markdown(
            f"""
            <div style="background: #111827; border: 1px solid {border_color}; border-radius: 8px; padding: 16px; margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="font-size: 16px; font-weight: 700; color: #F8FAFC;">
                        {s['topic']}
                        {' <span style="background: #1D4ED8; color: #BFDBFE; font-size: 10px; padding: 2px 6px; border-radius: 4px; margin-left: 8px;">ACTIVE</span>' if is_current else ''}
                    </div>
                    <div style="font-size: 12px; color: #64748B;">
                        {s['created_at'][:10]}
                    </div>
                </div>
                <div style="display: flex; gap: 20px; font-size: 12px; color: #94A3B8; margin-top: 8px;">
                    <span>🤖 Provider: <b>{s['ai_provider']}</b></span>
                    <span>📄 Pages: <b>{s['pages_crawled_count']}</b></span>
                    <span>⚡ Signals: <b>{s['signals_count']}</b></span>
                    <span>💡 Opportunities: <b>{s['opportunities_count']}</b></span>
                    <span>🌐 Domains: <b>{s['unique_domains_count']}</b></span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        col_b1, col_b2, _ = st.columns([1, 1, 4])
        with col_b1:
            if not is_current:
                if st.button("Load Session", key=f"load_{s['id']}"):
                    loaded = db_service.get_session(s['id'])
                    if loaded:
                        st.session_state["active_session"] = loaded
                        st.session_state["current_page"] = "Dashboard"
                        st.rerun()
        with col_b2:
            if st.button("🗑️ Delete", key=f"del_{s['id']}"):
                db_service.delete_session(s['id'])
                if is_current:
                    st.session_state["active_session"] = None
                st.rerun()


def render_settings_page():
    """Renders settings, API key status, crawler rate limits, and formula explanation."""
    st.markdown(
        """
        <div style="margin-bottom: 24px;">
            <h1 style="font-size: 24px; font-weight: 700; color: #F8FAFC; margin-bottom: 4px;">
                ⚙️ Platform Configuration & Settings
            </h1>
            <p style="color: #94A3B8; font-size: 14px; margin: 0;">
                Configure AI API credentials, crawling throttles, and review the transparent scoring architecture.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h3 style='font-size: 16px; font-weight: 600; color: #F1F5F9;'>AI Credentials</h3>", unsafe_allow_html=True)
        st.info("API keys can be supplied via .env file or entered below for this session.")

        groq_key_input = st.text_input(
            "Groq API Key",
            value=settings.get_masked_key("Groq") if settings.is_groq_available() else "",
            type="password",
            placeholder="gsk_..."
        )

        gemini_key_input = st.text_input(
            "Google Gemini API Key",
            value=settings.get_masked_key("Gemini") if settings.is_gemini_available() else "",
            type="password",
            placeholder="AIzaSy..."
        )

        if st.button("Save Key Overrides", key="save_keys"):
            if groq_key_input and "••••" not in groq_key_input:
                settings.groq_api_key = groq_key_input.strip()
            if gemini_key_input and "••••" not in gemini_key_input:
                settings.gemini_api_key = gemini_key_input.strip()
            st.success("API Key settings updated.")

    with col2:
        st.markdown("<h3 style='font-size: 16px; font-weight: 600; color: #F1F5F9;'>Crawler & Politeness Settings</h3>", unsafe_allow_html=True)
        req_delay = st.number_input("Request Delay between requests to same domain (seconds)", value=settings.request_delay, min_value=0.2, max_value=5.0, step=0.1)
        req_timeout = st.number_input("Request Timeout (seconds)", value=settings.request_timeout, min_value=5, max_value=30, step=1)
        user_agent_str = st.text_input("Crawler User-Agent Header", value=settings.user_agent)

        if st.button("Save Crawler Settings"):
            settings.request_delay = req_delay
            settings.request_timeout = int(req_timeout)
            settings.user_agent = user_agent_str
            st.success("Crawler settings saved.")

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # Transparent Scoring Formula Display (Section 9 requirement)
    st.markdown(
        """
        <div style="background: #111827; border: 1px solid #1F2937; border-radius: 8px; padding: 20px;">
            <h3 style="font-size: 16px; font-weight: 700; color: #F8FAFC; margin-bottom: 8px;">
                📐 Transparent Opportunity Ranking Formula
            </h3>
            <p style="font-size: 13px; color: #94A3B8; margin-bottom: 12px;">
                Every opportunity score is an explainable analytical index calculated using the following audited formula:
            </p>
            <div style="background: #0B0F19; border: 1px solid #1E293B; border-radius: 6px; padding: 12px; font-family: monospace; font-size: 13px; color: #38BDF8; margin-bottom: 12px;">
                Opportunity Score = (Frequency × 0.30) + (Relevance × 0.25) + (Urgency × 0.20) + (Confidence × 0.15) + (Recency × 0.10)
            </div>
            <ul style="font-size: 12px; color: #94A3B8; line-height: 1.6; margin: 0; padding-left: 20px;">
                <li><b>Frequency Score (30%):</b> Measures independent supporting domains (weighted 70%) and total signal volume (30%) to prevent single-source spam.</li>
                <li><b>Relevance Score (25%):</b> Average relevance of extracted signals to the primary research question.</li>
                <li><b>Urgency Score (20%):</b> Severity of user pain point or active operational friction.</li>
                <li><b>Confidence Score (15%):</b> AI extraction certainty and quote verification against the source document.</li>
                <li><b>Recency Score (10%):</b> Publication date freshness when available from article metadata.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )


def main():
    initialize_app_state()
    selected_page = render_sidebar()
    active_session = st.session_state.get("active_session")

    if selected_page == "Dashboard":
        render_dashboard(active_session)
    elif selected_page == "New Research":
        render_new_research_page()
    elif selected_page == "Opportunities":
        if active_session:
            render_opportunity_details(active_session.opportunities)
        else:
            st.warning("No active research session loaded.")
    elif selected_page == "Findings Explorer":
        if active_session:
            render_findings_explorer(active_session.signals)
        else:
            st.warning("No active research session loaded.")
    elif selected_page == "Research History":
        render_research_history_page()
    elif selected_page == "Settings":
        render_settings_page()


if __name__ == "__main__":
    main()

