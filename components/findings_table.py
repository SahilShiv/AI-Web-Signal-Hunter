"""Interactive Findings Explorer component with filters, search, and evidence inspect modal/cards."""

import streamlit as st
import pandas as pd
from typing import List
from models.signal import Signal
from config.constants import CATEGORY_COLORS, SIGNAL_CATEGORIES


def render_findings_explorer(signals: List[Signal]):
    """Renders interactive findings explorer with granular search and evidence inspection."""
    st.markdown(
        """
        <div style="margin-bottom: 20px;">
            <h1 style="font-size: 24px; font-weight: 700; color: #F8FAFC; margin-bottom: 4px;">
                🔎 Findings Explorer
            </h1>
            <p style="color: #94A3B8; font-size: 14px; margin: 0;">
                Inspect individual business signals, filter by category or domain, and verify original source quotes.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if not signals:
        st.info("No signals found in current session.")
        return

    # Filter Controls
    f_col1, f_col2, f_col3 = st.columns([2, 1.5, 1.5])

    with f_col1:
        search_query = st.text_input("🔍 Search signals by keyword...", placeholder="e.g. pricing, bans, CRM, integration")

    with f_col2:
        all_categories = sorted(list({s.signal_category for s in signals}))
        selected_categories = st.multiselect("Filter by Category", all_categories, default=[])

    with f_col3:
        all_domains = sorted(list({s.source_domain for s in signals if s.source_domain}))
        selected_domains = st.multiselect("Filter by Domain", all_domains, default=[])

    # Slider and Sort
    s_col1, s_col2 = st.columns([2, 1])
    with s_col1:
        min_rel = st.slider("Minimum Relevance Threshold", min_value=0, max_value=100, value=50, step=5)
    with s_col2:
        sort_by = st.selectbox("Sort By", ["Relevance (Highest)", "Urgency (Highest)", "Confidence (Highest)"])

    # Apply Filters
    filtered_signals = signals

    if search_query:
        q = search_query.lower()
        filtered_signals = [
            s for s in filtered_signals
            if q in s.summary.lower() or q in s.evidence.lower() or q in s.reasoning.lower() or q in s.source_domain.lower()
        ]

    if selected_categories:
        filtered_signals = [s for s in filtered_signals if s.signal_category in selected_categories]

    if selected_domains:
        filtered_signals = [s for s in filtered_signals if s.source_domain in selected_domains]

    filtered_signals = [s for s in filtered_signals if s.relevance_score >= min_rel]

    # Sort
    if sort_by == "Relevance (Highest)":
        filtered_signals.sort(key=lambda s: s.relevance_score, reverse=True)
    elif sort_by == "Urgency (Highest)":
        filtered_signals.sort(key=lambda s: s.urgency_score, reverse=True)
    elif sort_by == "Confidence (Highest)":
        filtered_signals.sort(key=lambda s: s.confidence_score, reverse=True)

    st.markdown(
        f"<div style='font-size: 13px; color: #94A3B8; margin-bottom: 15px;'>Showing <b>{len(filtered_signals)}</b> of {len(signals)} signals</div>",
        unsafe_allow_html=True
    )

    # Detailed Signal Cards
    for s in filtered_signals:
        cat_color = CATEGORY_COLORS.get(s.signal_category, "#3B82F6")

        with st.expander(f"[{s.signal_category.upper()}]  {s.summary}  —  {s.source_domain}", expanded=False):
            st.markdown(
                f"""
                <div style="background: #0B0F19; border: 1px solid #1E293B; border-radius: 8px; padding: 14px; margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span style="background: {cat_color}22; color: {cat_color}; border: 1px solid {cat_color}44; font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 4px; text-transform: uppercase;">
                            {s.signal_category}
                        </span>
                        <span style="font-size: 12px; color: #94A3B8;">
                            Source: <a href="{s.source_url}" target="_blank" style="color: #38BDF8; text-decoration: none; font-weight: 600;">{s.source_domain} ↗</a>
                        </span>
                    </div>
                    <div style="font-size: 14px; font-weight: 600; color: #F1F5F9; margin-bottom: 10px;">
                        {s.summary}
                    </div>

                    <!-- Direct Evidence Excerpt -->
                    <div style="background: #161F30; border-left: 3px solid #3B82F6; padding: 10px 12px; border-radius: 0 6px 6px 0; margin-bottom: 12px;">
                        <div style="font-size: 11px; font-weight: 700; color: #38BDF8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">
                            📄 Exact Source Quotation (Evidence)
                        </div>
                        <div style="font-size: 13px; color: #E2E8F0; font-style: italic;">
                            "{s.evidence}"
                        </div>
                    </div>

                    <!-- AI Analytical Reasoning -->
                    <div style="font-size: 13px; color: #94A3B8; margin-bottom: 12px;">
                        <b style="color: #CBD5E1;">Analytical Reasoning:</b> {s.reasoning}
                    </div>

                    <!-- Scores -->
                    <div style="display: flex; gap: 20px; font-size: 12px; color: #64748B; border-top: 1px solid #1E293B; padding-top: 10px;">
                        <span>🎯 Relevance: <b style="color: #F8FAFC;">{s.relevance_score:.0f}/100</b></span>
                        <span>🔥 Urgency: <b style="color: #F8FAFC;">{s.urgency_score:.0f}/100</b></span>
                        <span>🛡️ Confidence: <b style="color: #F8FAFC;">{s.confidence_score:.0f}/100</b></span>
                        <span>🔗 <a href="{s.source_url}" target="_blank" style="color: #60A5FA;">Open Original Page</a></span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

