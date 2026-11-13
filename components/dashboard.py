"""Executive Overview Dashboard component."""

import streamlit as st
import pandas as pd
from typing import Optional
from models.opportunity import ResearchSession
from config.constants import CATEGORY_COLORS
from components.charts import (
    create_category_distribution_chart,
    create_opportunity_ranking_chart,
    create_signal_scatter_chart
)
from services.export_service import ExportService


def render_dashboard(session: Optional[ResearchSession]):
    """Renders main executive intelligence dashboard."""
    if not session:
        st.warning("No active research session loaded. Please start a research session or select one from Research History.")
        return

    # A. Header
    st.markdown(
        f"""
        <div style="background: #111827; border: 1px solid #1F2937; border-radius: 10px; padding: 20px 24px; margin-bottom: 24px;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                <span style="background: #1E293B; color: #38BDF8; font-size: 11px; font-weight: 700; padding: 3px 8px; border-radius: 4px; text-transform: uppercase; letter-spacing: 0.05em;">
                    {session.ai_provider} Engine
                </span>
                <span style="color: #94A3B8; font-size: 13px;">
                    Analyzed {session.created_at.strftime('%B %d, %Y')}
                </span>
            </div>
            <h1 style="font-size: 26px; font-weight: 700; color: #F8FAFC; margin: 0 0 8px 0; letter-spacing: -0.02em; line-height: 1.3;">
                {session.topic}
            </h1>
            <p style="color: #94A3B8; font-size: 14px; margin: 0; line-height: 1.5;">
                Live web intelligence distilled from verified public discussions, product reviews, and industry articles across independent domains.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Top CTA Bar: Export buttons
    col_cta1, col_cta2, col_cta3 = st.columns([2, 1, 1])
    with col_cta1:
        if st.button("🔍 Run New Research Query", key="dash_new_search", type="primary"):
            st.session_state["current_page"] = "New Research"
            st.rerun()
    with col_cta2:
        csv_data = ExportService.export_csv(session)
        st.download_button(
            label="📥 Export CSV",
            data=csv_data,
            file_name=f"signals_{session.id}.csv",
            mime="text/csv",
            use_container_width=True
        )
    with col_cta3:
        json_data = ExportService.export_json(session)
        st.download_button(
            label="📦 Export JSON",
            data=json_data,
            file_name=f"signals_{session.id}.json",
            mime="application/json",
            use_container_width=True
        )

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # B. Overview Metrics (4 meaningful metrics)
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.markdown(
            f"""
            <div style="background: #111827; border: 1px solid #1F2937; border-radius: 10px; padding: 18px 20px;">
                <div style="font-size: 12px; font-weight: 600; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em;">Pages Crawled</div>
                <div style="font-size: 32px; font-weight: 800; color: #F8FAFC; margin-top: 4px;">{session.pages_crawled_count}</div>
                <div style="font-size: 11px; color: #10B981; margin-top: 4px;">✓ Deduplicated & verified</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with m2:
        st.markdown(
            f"""
            <div style="background: #111827; border: 1px solid #1F2937; border-radius: 10px; padding: 18px 20px;">
                <div style="font-size: 12px; font-weight: 600; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em;">Useful Signals Found</div>
                <div style="font-size: 32px; font-weight: 800; color: #3B82F6; margin-top: 4px;">{len(session.signals)}</div>
                <div style="font-size: 11px; color: #94A3B8; margin-top: 4px;">Score ≥ {session.min_relevance_threshold:.0f} relevance</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with m3:
        st.markdown(
            f"""
            <div style="background: #111827; border: 1px solid #1F2937; border-radius: 10px; padding: 18px 20px;">
                <div style="font-size: 12px; font-weight: 600; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em;">Opportunities Discovered</div>
                <div style="font-size: 32px; font-weight: 800; color: #10B981; margin-top: 4px;">{len(session.opportunities)}</div>
                <div style="font-size: 11px; color: #94A3B8; margin-top: 4px;">Ranked by multi-factor formula</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with m4:
        st.markdown(
            f"""
            <div style="background: #111827; border: 1px solid #1F2937; border-radius: 10px; padding: 18px 20px;">
                <div style="font-size: 12px; font-weight: 600; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em;">Domains Analyzed</div>
                <div style="font-size: 32px; font-weight: 800; color: #F59E0B; margin-top: 4px;">{session.unique_domains_count}</div>
                <div style="font-size: 11px; color: #94A3B8; margin-top: 4px;">Cross-domain validation</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # C. Charts Section: Category Distribution & Opportunity Ranking
    c_left, c_right = st.columns([1, 1])

    with c_left:
        st.markdown("<h3 style='font-size: 16px; font-weight: 600; color: #F1F5F9; margin-bottom: 8px;'>Signal Category Distribution</h3>", unsafe_allow_html=True)
        dist_fig = create_category_distribution_chart(session.signals)
        st.plotly_chart(dist_fig, use_container_width=True, config={"displayModeBar": False})

    with c_right:
        st.markdown("<h3 style='font-size: 16px; font-weight: 600; color: #F1F5F9; margin-bottom: 8px;'>Opportunity Rankings (Score /100)</h3>", unsafe_allow_html=True)
        rank_fig = create_opportunity_ranking_chart(session.opportunities)
        st.plotly_chart(rank_fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # D. Top Opportunity Summary Cards
    st.markdown(
        """
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <h3 style="font-size: 18px; font-weight: 600; color: #F1F5F9; margin: 0;">Top Business Opportunities</h3>
            <span style="font-size: 12px; color: #64748B;">Click 'Opportunities' in sidebar for full briefs</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    for idx, opp in enumerate(session.opportunities[:3]):
        st.markdown(
            f"""
            <div style="background: #111827; border: 1px solid #1F2937; border-radius: 8px; padding: 16px; margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="background: #1E293B; color: #38BDF8; font-weight: 700; font-size: 12px; width: 22px; height: 22px; border-radius: 4px; display: inline-flex; align-items: center; justify-content: center;">
                            #{idx+1}
                        </span>
                        <span style="font-size: 15px; font-weight: 600; color: #F8FAFC;">{opp.title}</span>
                    </div>
                    <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); color: #10B981; font-weight: 700; padding: 4px 10px; border-radius: 6px; font-size: 13px;">
                        Score: {opp.opportunity_score:.1f}
                    </div>
                </div>
                <div style="color: #94A3B8; font-size: 13px; margin: 8px 0 10px 0; line-height: 1.5;">
                    {opp.problem_description}
                </div>
                <div style="display: flex; gap: 16px; font-size: 12px; color: #64748B;">
                    <span>⚡ <b>{opp.supporting_signal_count}</b> Supporting Signals</span>
                    <span>🌐 <b>{opp.unique_domains_count}</b> Independent Domains</span>
                    <span>🎯 Relevance: <b>{opp.relevance_score:.1f}</b></span>
                    <span>🔥 Urgency: <b>{opp.urgency_score:.1f}</b></span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # E. Recent Findings Table
    st.markdown("<h3 style='font-size: 18px; font-weight: 600; color: #F1F5F9; margin-bottom: 12px;'>Recent Verified Findings</h3>", unsafe_allow_html=True)

    table_data = []
    for s in session.signals[:10]:
        table_data.append({
            "Category": s.signal_category,
            "Summary": s.summary,
            "Relevance": f"{s.relevance_score:.0f}",
            "Urgency": f"{s.urgency_score:.0f}",
            "Confidence": f"{s.confidence_score:.0f}",
            "Source Domain": s.source_domain,
            "Link": s.source_url,
        })

    if table_data:
        df_table = pd.DataFrame(table_data)
        st.dataframe(
            df_table,
            column_config={
                "Link": st.column_config.LinkColumn("Source Link", display_text="Visit Source"),
                "Relevance": st.column_config.ProgressColumn("Relevance", min_value=0, max_value=100, format="%d"),
                "Urgency": st.column_config.ProgressColumn("Urgency", min_value=0, max_value=100, format="%d"),
                "Confidence": st.column_config.ProgressColumn("Confidence", min_value=0, max_value=100, format="%d"),
            },
            use_container_width=True,
            hide_index=True
        )

