"""Sidebar navigation component for AI Web Signal Hunter."""

import streamlit as st
from config.settings import settings
from config.constants import SUPPORTED_PROVIDERS, PROVIDER_GROQ, PROVIDER_GEMINI


def render_sidebar() -> str:
    """Renders sleek enterprise navigation sidebar and returns selected menu item."""
    with st.sidebar:
        # Brand Header
        st.markdown(
            """
            <div style="padding: 10px 0 20px 0;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="width: 32px; height: 32px; background: linear-gradient(135deg, #3B82F6, #6366F1); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: bold; color: white; font-size: 16px;">
                        W
                    </div>
                    <div>
                        <div style="font-weight: 700; font-size: 17px; letter-spacing: -0.02em; color: #F8FAFC;">Signal Hunter</div>
                        <div style="font-size: 11px; color: #64748B; font-weight: 500;">WEB MARKET INTELLIGENCE</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<div style='height: 1px; background: #1E293B; margin-bottom: 20px;'></div>", unsafe_allow_html=True)

        # Navigation Menu
        menu_items = [
            ("📊 Dashboard", "Dashboard"),
            ("🔍 New Research", "New Research"),
            ("💡 Opportunities", "Opportunities"),
            ("🔎 Findings Explorer", "Findings Explorer"),
            ("📜 Research History", "Research History"),
            ("⚙️ Settings", "Settings"),
        ]

        if "current_page" not in st.session_state:
            st.session_state["current_page"] = "Dashboard"

        selected_page = st.session_state["current_page"]

        for label, page_key in menu_items:
            is_active = (selected_page == page_key)
            btn_style = "primary" if is_active else "secondary"
            if st.button(label, key=f"nav_{page_key}", use_container_width=True, type=btn_style):
                st.session_state["current_page"] = page_key
                st.rerun()

        st.markdown("<div style='height: 1px; background: #1E293B; margin: 25px 0 15px 0;'></div>", unsafe_allow_html=True)

        # AI Provider Status Card
        st.markdown("<div style='font-size: 11px; font-weight: 600; color: #64748B; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.05em;'>AI ENGINE STATUS</div>", unsafe_allow_html=True)

        groq_status = "Connected" if settings.is_groq_available() else "Ready (Fallback)"
        gemini_status = "Connected" if settings.is_gemini_available() else "Ready (Fallback)"

        groq_badge = "#10B981" if settings.is_groq_available() else "#64748B"
        gemini_badge = "#10B981" if settings.is_gemini_available() else "#64748B"

        st.markdown(
            f"""
            <div style="background: #111827; border: 1px solid #1F2937; border-radius: 8px; padding: 10px 12px; margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; font-size: 12px;">
                    <span style="color: #94A3B8;">Groq Llama-3.3</span>
                    <span style="display: flex; align-items: center; gap: 5px; color: {groq_badge}; font-weight: 600; font-size: 11px;">
                        <span style="width: 6px; height: 6px; border-radius: 50%; background: {groq_badge}; display: inline-block;"></span>
                        {groq_status}
                    </span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; font-size: 12px;">
                    <span style="color: #94A3B8;">Gemini 2.5 Flash</span>
                    <span style="display: flex; align-items: center; gap: 5px; color: {gemini_badge}; font-weight: 600; font-size: 11px;">
                        <span style="width: 6px; height: 6px; border-radius: 50%; background: {gemini_badge}; display: inline-block;"></span>
                        {gemini_status}
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Active Session topic indicator
        current_session = st.session_state.get("active_session")
        if current_session:
            st.markdown(
                f"""
                <div style="background: #0F172A; border-left: 3px solid #3B82F6; padding: 8px 10px; border-radius: 0 6px 6px 0;">
                    <div style="font-size: 10px; color: #64748B; font-weight: 600;">ACTIVE TOPIC</div>
                    <div style="font-size: 12px; color: #E2E8F0; font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                        {current_session.topic}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        return st.session_state["current_page"]

