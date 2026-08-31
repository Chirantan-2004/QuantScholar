"""
QuantumScholar - UI Component: Sources Inspector
Renders verified quantum paper metadata cards with direct links and citation tags.
"""

import streamlit as st
from typing import List, Dict, Any

def render_sources_list(sources: List[Dict[str, Any]]):
    """Renders formatted cards for retrieved source chunks."""
    if not sources:
        st.info("No sources retrieved.")
        return

    st.markdown("### 📚 Verified Quantum Sources")
    for i, src in enumerate(sources, 1):
        citation_tag = src.get("citation_tag", "Source")
        title = src.get("title", "Untitled")
        authors = ", ".join(src.get("authors", []))
        year = src.get("year", "N/A")
        venue = src.get("venue", "arXiv")
        url = src.get("url", "#")
        content = src.get("content", "")
        doc_type = src.get("doc_type", "paper").upper()

        with st.expander(f"**[{i}] {citation_tag}** — {title} ({year})", expanded=(i == 1)):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**Authors**: {authors}")
                st.markdown(f"**Venue**: *{venue}*")
            with col2:
                st.markdown(f"**Type**: `{doc_type}`")
                if url and url != "#":
                    st.markdown(f"[🔗 Direct Link]({url})")

            st.markdown("---")
            st.markdown(f"**Excerpt / Abstract**:")
            st.markdown(f"> *{content}*")
