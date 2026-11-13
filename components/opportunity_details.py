"""Detailed Opportunity Briefs and Transparent Scoring Breakdown component."""

import streamlit as st
from typing import List
from models.opportunity import Opportunity


def render_opportunity_details(opportunities: List[Opportunity]):
    """Renders comprehensive briefs for top-ranked business opportunities."""
    st.markdown(
        """
        <div style="margin-bottom: 24px;">
            <h1 style="font-size: 24px; font-weight: 700; color: #F8FAFC; margin-bottom: 4px;">
                💡 Top Business Opportunity Briefs
            </h1>
            <p style="color: #94A3B8; font-size: 14px; margin: 0;">
                Evidence-backed strategic briefs with concrete problem definitions, solution archetypes, and real-user validation strategies.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if not opportunities:
        st.info("No opportunity briefs generated yet.")
        return

    # Tabs for top opportunities
    tab_names = [f"#{idx+1} {opp.title[:24]}..." for idx, opp in enumerate(opportunities[:5])]
    tabs = st.tabs(tab_names)

    for idx, (tab, opp) in enumerate(zip(tabs, opportunities[:5])):
        with tab:
            # Header card with rank and total score
            st.markdown(
                f"""
                <div style="background: #111827; border: 1px solid #1F2937; border-radius: 10px; padding: 20px; margin-bottom: 20px;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                        <div>
                            <span style="background: #1E293B; color: #38BDF8; font-size: 12px; font-weight: 700; padding: 3px 8px; border-radius: 4px; text-transform: uppercase;">
                                Opportunity #{idx+1}
                            </span>
                            <h2 style="font-size: 22px; font-weight: 700; color: #F8FAFC; margin: 8px 0 4px 0;">
                                {opp.title}
                            </h2>
                        </div>
                        <div style="text-align: right;">
                            <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); color: #10B981; font-weight: 800; font-size: 22px; padding: 6px 14px; border-radius: 8px;">
                                {opp.opportunity_score:.1f} <span style="font-size: 13px; font-weight: 500; color: #94A3B8;">/100</span>
                            </div>
                            <div style="font-size: 11px; color: #64748B; margin-top: 4px;">OPPORTUNITY SCORE</div>
                        </div>
                    </div>

                    <!-- Score Breakdown Pills -->
                    <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 14px; border-top: 1px solid #1E293B; padding-top: 14px;">
                        <span style="background: #0B0F19; border: 1px solid #1E293B; border-radius: 6px; padding: 4px 10px; font-size: 12px; color: #94A3B8;">
                            Frequency (30%): <b style="color: #F8FAFC;">{opp.frequency_score:.1f}</b>
                        </span>
                        <span style="background: #0B0F19; border: 1px solid #1E293B; border-radius: 6px; padding: 4px 10px; font-size: 12px; color: #94A3B8;">
                            Relevance (25%): <b style="color: #F8FAFC;">{opp.relevance_score:.1f}</b>
                        </span>
                        <span style="background: #0B0F19; border: 1px solid #1E293B; border-radius: 6px; padding: 4px 10px; font-size: 12px; color: #94A3B8;">
                            Urgency (20%): <b style="color: #F8FAFC;">{opp.urgency_score:.1f}</b>
                        </span>
                        <span style="background: #0B0F19; border: 1px solid #1E293B; border-radius: 6px; padding: 4px 10px; font-size: 12px; color: #94A3B8;">
                            Confidence (15%): <b style="color: #F8FAFC;">{opp.confidence_score:.1f}</b>
                        </span>
                        <span style="background: #0B0F19; border: 1px solid #1E293B; border-radius: 6px; padding: 4px 10px; font-size: 12px; color: #94A3B8;">
                            Recency (10%): <b style="color: #F8FAFC;">{opp.recency_score:.1f}</b>
                        </span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Executive Brief Sections (A through H)
            col1, col2 = st.columns([1, 1])

            with col1:
                # B. Problem Description
                st.markdown(
                    f"""
                    <div style="background: #111827; border: 1px solid #1F2937; border-radius: 8px; padding: 16px; margin-bottom: 16px;">
                        <div style="font-size: 11px; font-weight: 700; color: #EF4444; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">
                            B. Core Problem Definition
                        </div>
                        <div style="color: #E2E8F0; font-size: 14px; line-height: 1.5;">
                            {opp.problem_description}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # C. Target Audience
                st.markdown(
                    f"""
                    <div style="background: #111827; border: 1px solid #1F2937; border-radius: 8px; padding: 16px; margin-bottom: 16px;">
                        <div style="font-size: 11px; font-weight: 700; color: #3B82F6; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">
                            C. Target Audience
                        </div>
                        <div style="color: #E2E8F0; font-size: 14px; line-height: 1.5;">
                            {opp.target_audience}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # D. Why It Matters
                st.markdown(
                    f"""
                    <div style="background: #111827; border: 1px solid #1F2937; border-radius: 8px; padding: 16px; margin-bottom: 16px;">
                        <div style="font-size: 11px; font-weight: 700; color: #F59E0B; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">
                            D. Strategic Urgency (Why Now?)
                        </div>
                        <div style="color: #E2E8F0; font-size: 14px; line-height: 1.5;">
                            {opp.why_it_matters}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col2:
                # E. Possible Business Solution
                solution_type = opp.brief.solution_type if opp.brief else "SaaS Platform"
                st.markdown(
                    f"""
                    <div style="background: #111827; border: 1px solid #1F2937; border-radius: 8px; padding: 16px; margin-bottom: 16px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                            <div style="font-size: 11px; font-weight: 700; color: #10B981; text-transform: uppercase; letter-spacing: 0.05em;">
                                E. Proposed Business Solution
                            </div>
                            <span style="background: #1E293B; color: #A7F3D0; font-size: 10px; font-weight: 600; padding: 2px 6px; border-radius: 4px;">
                                {solution_type}
                            </span>
                        </div>
                        <div style="color: #E2E8F0; font-size: 14px; line-height: 1.5;">
                            {opp.possible_solution}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # H. Validation Strategy
                st.markdown(
                    f"""
                    <div style="background: #111827; border: 1px solid #1F2937; border-radius: 8px; padding: 16px; margin-bottom: 16px;">
                        <div style="font-size: 11px; font-weight: 700; color: #8B5CF6; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">
                            H. User Validation Strategy
                        </div>
                        <div style="color: #E2E8F0; font-size: 14px; line-height: 1.5;">
                            {opp.validation_strategy}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Scoring explanation card
                st.markdown(
                    f"""
                    <div style="background: #0B0F19; border: 1px solid #1E293B; border-radius: 8px; padding: 12px 16px; margin-bottom: 16px;">
                        <div style="font-size: 11px; font-weight: 600; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">
                            Scoring Methodology & Reasoning
                        </div>
                        <div style="color: #94A3B8; font-size: 12px; line-height: 1.4;">
                            {opp.score_explanation}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # F & G: Real Supporting Evidence Excerpts and Source References
            st.markdown("<h4 style='font-size: 16px; font-weight: 600; color: #F1F5F9; margin: 16px 0 8px 0;'>F & G. Grounded Evidence Quotes & Clickable Sources</h4>", unsafe_allow_html=True)

            if opp.brief and opp.brief.evidence_samples:
                for ev in opp.brief.evidence_samples:
                    st.markdown(
                        f"""
                        <div style="background: #111827; border-left: 3px solid #38BDF8; border-radius: 0 6px 6px 0; padding: 12px 14px; margin-bottom: 8px;">
                            <div style="font-size: 13px; color: #F1F5F9; font-style: italic; margin-bottom: 6px;">
                                "{ev.excerpt}"
                            </div>
                            <div style="display: flex; justify-content: space-between; font-size: 11px; color: #64748B;">
                                <span>Domain: <b style="color: #94A3B8;">{ev.domain}</b></span>
                                <span>Original Link: <a href="{ev.url}" target="_blank" style="color: #38BDF8; text-decoration: none;">{ev.url} ↗</a></span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                for sig in opp.signals[:3]:
                    st.markdown(
                        f"""
                        <div style="background: #111827; border-left: 3px solid #38BDF8; border-radius: 0 6px 6px 0; padding: 12px 14px; margin-bottom: 8px;">
                            <div style="font-size: 13px; color: #F1F5F9; font-style: italic; margin-bottom: 6px;">
                                "{sig.evidence}"
                            </div>
                            <div style="display: flex; justify-content: space-between; font-size: 11px; color: #64748B;">
                                <span>Domain: <b style="color: #94A3B8;">{sig.source_domain}</b></span>
                                <span>Original Link: <a href="{sig.source_url}" target="_blank" style="color: #38BDF8; text-decoration: none;">{sig.source_url} ↗</a></span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

