"""
QuantumScholar - UI Component: Chat & Citation Renderer
Renders grounded markdown, math equations, and feedback telemetry triggers.
"""

import streamlit as st
from typing import Dict, Any, List

def render_audit_badge(audit: Dict[str, Any]):
    """Renders visual verification badges for groundedness and quality."""
    g_score = audit.get("groundedness_score", 1.0)
    c_score = audit.get("clarity_score", 1.0)
    citations = audit.get("citation_count", 0)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        color = "green" if g_score >= 0.90 else "orange"
        st.metric(label="🛡️ Groundedness", value=f"{g_score*100:.1f}%")
    with col2:
        st.metric(label="✨ Clarity", value=f"{c_score*100:.1f}%")
    with col3:
        st.metric(label="🔖 Citations Found", value=f"{citations}")
    with col4:
        status_label = "✅ Verified Grounded" if g_score >= 0.85 else "⚠️ Low Confidence"
        st.markdown(f"**Verification**\n\n`{status_label}`")

def render_feedback_buttons(query_id: str, query: str, on_feedback_callback):
    """Renders thumbs up / thumbs down and rating widgets."""
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        if st.button("👍 Grounded", key=f"up_{query_id}"):
            on_feedback_callback(query_id, query, 5, "thumbs_up", "Accurate citation")
            st.toast("Feedback recorded! Ingested by Ralph loop.")
    with col2:
        if st.button("👎 Issue", key=f"down_{query_id}"):
            on_feedback_callback(query_id, query, 1, "thumbs_down", "User flagged issue")
            st.toast("Feedback recorded. Ralph loop will diagnose.")
