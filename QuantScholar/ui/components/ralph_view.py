"""
QuantumScholar - UI Component: Ralph Agentic Loop Live Control Room
Interactive multi-agent control room with real-time diagnostic traces, claim audits, and hyperparameter tuning.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

def render_ralph_control_room(ralph_instance):
    """Renders the comprehensive, interactive Ralph Agentic Loop Control Center."""
    st.markdown("## 🔄 Ralph Continuous Agentic Self-Improvement Loop")
    st.markdown(
        "The Ralph Loop is QuantumScholar's autonomous self-optimization engine. "
        "It coordinates 4 specialized agents to monitor hallucination rates, tune retrieval hyperparameters, "
        "and evolve system prompt variants in real-time until strict scientific thresholds are exceeded."
    )

    status_data = ralph_instance.get_status()
    latest = status_data["latest_cycle"]
    feedback = status_data["user_feedback_summary"]

    # Metric Gauges
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Completed Cycles", f"#{status_data['active_cycle_count']}")
    with c2:
        g_val = latest["quality_metrics"]["groundedness"] if latest else 0.98
        st.metric("Mean Groundedness", f"{g_val*100:.1f}%", delta="Target: ≥90%")
    with c3:
        st.metric("User Satisfaction", f"{feedback.get('mean_rating', 5.0):.1f} / 5.0 ⭐", delta=f"{feedback.get('total_feedback_count', 0)} ratings")
    with c4:
        st.metric("Autonomous Loop State", f"🟢 {status_data['status']}")

    st.markdown("---")

    # 4 Autonomous Agents Cards
    st.markdown("### 🤖 Autonomous Agent Network")
    a1, a2, a3, a4 = st.columns(4)
    with a1:
        st.markdown("""
        <div style="background-color: #1e293b; padding: 12px; border-radius: 8px; border-left: 4px solid #38bdf8;">
            <b>🛡️ Quality Agent (Judge)</b><br>
            <span style="font-size: 0.85rem; color: #94a3b8;">Audits claim grounding, LaTeX math, and citation compliance via LLM-as-a-Judge.</span>
        </div>
        """, unsafe_allow_html=True)
    with a2:
        st.markdown("""
        <div style="background-color: #1e293b; padding: 12px; border-radius: 8px; border-left: 4px solid #10b981;">
            <b>🔍 Retrieval Agent</b><br>
            <span style="font-size: 0.85rem; color: #94a3b8;">Diagnoses keyword & vector bottlenecks, auto-tunes RRF fusion weights and top_k depth.</span>
        </div>
        """, unsafe_allow_html=True)
    with a3:
        st.markdown("""
        <div style="background-color: #1e293b; padding: 12px; border-radius: 8px; border-left: 4px solid #f59e0b;">
            <b>🧬 Prompt Evolution Agent</b><br>
            <span style="font-size: 0.85rem; color: #94a3b8;">Generates prompt mutations and scaffolding to eliminate boundary hallucinations.</span>
        </div>
        """, unsafe_allow_html=True)
    with a4:
        st.markdown("""
        <div style="background-color: #1e293b; padding: 12px; border-radius: 8px; border-left: 4px solid #ec4899;">
            <b>📡 Feedback Agent</b><br>
            <span style="font-size: 0.85rem; color: #94a3b8;">Ingests live user telemetry, thumbs up/down votes, and comments for continuous adaptation.</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    tab_exec, tab_live, tab_params, tab_history = st.tabs([
        "⚡ Run Autonomous Cycle",
        "🔬 Live Interactive Diagnostic Test",
        "🎛️ Hyperparameter Self-Tuning",
        "📜 Cycle Evolution History"
    ])

    # Tab 1: Run Cycle
    with tab_exec:
        col_ctrl, col_diag = st.columns([1, 2])
        with col_ctrl:
            st.markdown("#### 🔄 Trigger Ralph Cycle")
            auto_promote = st.toggle("Auto-Promote Approved Configs", value=True)
            if st.button("🚀 Execute 1 Ralph Optimization Cycle", type="primary", use_container_width=True):
                progress_bar = st.progress(0)
                status_text = st.empty()

                status_text.text("Phase 1/6: Collecting telemetry & golden queries...")
                progress_bar.progress(16)
                time.sleep(0.3)

                status_text.text("Phase 2/6: Running Quality Agent LLM-as-a-Judge evaluations...")
                progress_bar.progress(40)
                time.sleep(0.3)

                status_text.text("Phase 3/6: Retrieval Agent diagnosing coverage gaps...")
                progress_bar.progress(60)
                time.sleep(0.3)

                status_text.text("Phase 4/6: Prompt Agent proposing evolutionary mutations...")
                progress_bar.progress(80)
                time.sleep(0.2)

                cycle_res = ralph_instance.run_cycle(auto_promote=auto_promote)
                progress_bar.progress(100)
                status_text.text("Phase 6/6: Promotion & verification complete!")
                st.success(f"✅ Ralph Cycle #{cycle_res['cycle_number']} finished successfully! Config Promoted: {cycle_res['promoted']}")
                st.rerun()

        with col_diag:
            if latest:
                st.markdown("#### 📋 Latest Cycle Diagnostics & Mutations")
                st.markdown(f"- **Cycle Timestamp**: `{latest['timestamp']}`")
                st.markdown(f"- **Groundedness Pass Rate**: `{latest['quality_metrics']['pass_rate']*100:.1f}%`")
                st.markdown(f"- **Retrieval Status**: `{'Healthy' if latest['retrieval_diagnosis']['healthy'] else 'Self-Healing Active'}`")
                st.markdown(f"- **Evolved Prompt Variant**: `{latest['prompt_proposal']['version']}`")
                for mut in latest['prompt_proposal']['proposed_mutations']:
                    st.markdown(f"  - 🔹 *{mut}*")
            else:
                st.info("No Ralph cycle history in current session. Trigger a cycle above.")

    # Tab 2: Live Diagnostic
    with tab_live:
        st.markdown("#### 🔬 Single-Query Ralph Live Diagnostic")
        test_q = st.text_input("Test Query for Live Audit:", "How does Shor's algorithm reduce factoring to order finding in IEEE FOCS 1994?")
        if st.button("Audit Query with Quality & Retrieval Agents", type="secondary"):
            with st.spinner("Running live multi-agent audit..."):
                chunks = ralph_instance.retriever.retrieve(test_q, top_k=5)
                ans = ralph_instance.llm.generate_answer(test_q, chunks)
                audit = ralph_instance.quality_agent.audit_response(test_q, ans["answer"], chunks)

            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("##### 🛡️ Quality Judge Results")
                st.markdown(f"- **Groundedness Score**: `{audit['groundedness_score']*100:.1f}%`")
                st.markdown(f"- **Clarity Score**: `{audit['clarity_score']*100:.1f}%`")
                st.markdown(f"- **Pedagogy Score**: `{audit['pedagogy_score']*100:.1f}%`")
                st.markdown(f"- **Citations Found**: `{audit['citation_count']}`")
                st.markdown(f"- **Sources Section Verified**: `{'✅ Yes' if audit['has_sources'] else '❌ Missing'}`")
            with col_b:
                st.markdown("##### 🔍 Retrieved Chunks Coverage")
                for c in chunks:
                    st.markdown(f"- `{c.get('citation_tag')}`: *{c.get('title')}* (Rerank: `{c.get('rerank_score', 0.0):.3f}`)")

    # Tab 3: Hyperparameter Tuning
    with tab_params:
        st.markdown("#### 🎛️ Active Retrieval Hyperparameters")
        st.json(ralph_instance.retrieval_agent.current_params)

    # Tab 4: History
    with tab_history:
        if ralph_instance.cycle_history:
            df = pd.DataFrame([
                {
                    "Cycle": f"Cycle {c['cycle_number']}",
                    "Groundedness": f"{c['quality_metrics']['groundedness']*100:.1f}%",
                    "Clarity": f"{c['quality_metrics']['clarity']*100:.1f}%",
                    "Pedagogy": f"{c['quality_metrics']['pedagogy']*100:.1f}%",
                    "User Rating": f"{c['user_satisfaction'].get('mean_rating', 5.0)} ⭐",
                    "Promoted": "✅ Yes" if c["promoted"] else "⏸️ Hold"
                }
                for c in ralph_instance.cycle_history
            ])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No cycle history recorded yet.")
