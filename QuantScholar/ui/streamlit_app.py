"""
QuantumScholar - Modern Streamlit Application
Open-Source Citation-Grounded Quantum-Only AI Platform
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import time

from retrieval.service import QuantumRetriever
from llm.service import QuantumLLM
from llm.evaluators.groundedness_eval import GroundednessEvaluator
from llm.evaluators.pedagogy_eval import PedagogyEvaluator
from integrations.qiskit.circuit_runner import QiskitCircuitRunner
from integrations.cirq.cirq_runner import CirqRunner
from integrations.pennylane.pennylane_devices import PennyLaneDeviceManager
from integrations.math_engine import QuantumMathEngine
from agents.ralph_loop import RalphLoop
from evaluation.run_eval_suite import run_evaluation
from ui.components.sources import render_sources_list
from ui.components.chat import render_audit_badge, render_feedback_buttons
from ui.components.math_solver import render_math_equation_solver_section
from ui.components.ralph_view import render_ralph_control_room

# Page Configuration
st.set_page_config(
    page_title="QuantumScholar | Quantum AI Platform",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Modern Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 50%, #7f00ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #94a3b8;
        margin-bottom: 1.5rem;
    }
    .glass-card {
        border-radius: 12px;
        padding: 20px;
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 1.2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
</style>
""", unsafe_allow_html=True)

# Cache services in session state
@st.cache_resource
def get_services():
    retriever = QuantumRetriever()
    llm = QuantumLLM()
    g_eval = GroundednessEvaluator()
    p_eval = PedagogyEvaluator()
    qiskit = QiskitCircuitRunner()
    cirq = CirqRunner()
    pennylane = PennyLaneDeviceManager()
    ralph = RalphLoop()
    math_eng = QuantumMathEngine()
    return retriever, llm, g_eval, p_eval, qiskit, cirq, pennylane, ralph, math_eng

retriever, llm, g_eval, p_eval, qiskit, cirq, pennylane, ralph, math_eng = get_services()

# Sidebar Navigation
st.sidebar.title("⚛️ QuantumScholar")
st.sidebar.caption("Citation-Grounded Quantum AI Platform")

mode = st.sidebar.radio(
    "Platform Navigation",
    [
        "💬 Quantum AI Tutor",
        "📐 Quantum Math & 3D/2D Visualizer",
        "⚡ Quantum Circuit Sandbox",
        "🔄 Ralph Agentic Loop Control Center",
        "📚 Verified Corpus & Benchmarks"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🧠 2026 Model Architecture")
st.sidebar.markdown("- **Generation LLM**: `Qwen3-30B-Instruct`")
st.sidebar.markdown("- **Dense Embeddings**: `Qwen3-Embedding-8B`")
st.sidebar.markdown("- **Cross-Encoder**: `Qwen3-Reranker`")
st.sidebar.markdown("- **Quantum Engines**: `Qiskit Aer`, `Google Cirq`, `PennyLane`")
st.sidebar.markdown("- **License**: `Apache 2.0`")

# ----------------------------------------------------
# TAB 1: QUANTUM AI TUTOR
# ----------------------------------------------------
if mode == "💬 Quantum AI Tutor":
    st.markdown('<div class="main-header">QuantumScholar AI Tutor</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Answers quantum computing questions strictly from peer-reviewed literature and SDK docs with mandatory citations and proofs.</div>', unsafe_allow_html=True)

    col_tutor_mode, col_depth = st.columns([2, 1])
    with col_tutor_mode:
        tutor_mode = st.segmented_control(
            "Pedagogical Mode:",
            ["🎓 Professor Mode", "💡 Intuitive & Visual Mode", "💻 Code & Circuit Builder Mode", "🔬 Research & Paper Deep-Dive"],
            default="🎓 Professor Mode"
        )
    with col_depth:
        top_k = st.slider("Retrieval Depth (top_k chunks)", min_value=1, max_value=8, value=4)

    # Preset query selector for instant exploration
    preset = st.selectbox(
        "💡 Quick Quantum Concepts & Research Topics:",
        [
            "Select an example or type below...",
            "What are the three main families of quantum algorithms according to Ashley Montanaro's Springer survey?",
            "How does Shor's algorithm reduce factoring to order finding in IEEE FOCS 1994?",
            "How do single and multi-qubit gates work in Qiskit according to Learn Quantum Computing with Qiskit?",
            "How does Simon's algorithm achieve an exponential speedup in the Open-Access curriculum?",
            "What is the query complexity and diffusion operator in Grover's algorithm (arXiv:quant-ph/9605043)?",
            "How does Quantum Amplitude Amplification generalize Grover search according to Brassard et al. 2002?",
            "Explain how the 2D surface code detects and corrects quantum errors (Fowler 2012)."
        ]
    )

    default_val = "" if preset == "Select an example or type below..." else preset
    user_query = st.text_area("Ask QuantumScholar:", value=default_val, height=90, placeholder="e.g. How does Shor's algorithm find the period for factoring?")

    col_btn, col_rerank = st.columns([2, 3])
    with col_btn:
        ask_btn = st.button("🚀 Ask QuantumScholar", type="primary", use_container_width=True)
    with col_rerank:
        enable_rerank = st.checkbox("Enable Qwen3-Reranker Cross-Encoder", value=True)

    if ask_btn and user_query.strip():
        with st.spinner("Retrieving verified peer-reviewed literature & synthesizing grounded answer..."):
            start_t = time.time()
            clean_mode = tutor_mode.split(" ", 1)[1] if " " in tutor_mode else tutor_mode
            chunks = retriever.retrieve(user_query, top_k=top_k, enable_reranking=enable_rerank)
            gen_res = llm.generate_answer(user_query, chunks, mode=clean_mode)
            elapsed = time.time() - start_t

            answer = gen_res["answer"]
            audit_g = g_eval.evaluate(answer, chunks)
            audit_p = p_eval.evaluate(answer)
            full_audit = {**audit_g, **audit_p}

        st.markdown("### 📝 Grounded Pedagogical Response")
        st.markdown(answer)

        st.markdown("---")
        st.markdown(f"⏱️ *Generated in {elapsed:.2f}s in `{clean_mode}` using {gen_res['model']} with strict citation enforcement.*")
        render_audit_badge(full_audit)

        # Telemetry feedback
        def handle_feedback(qid, q, rating, fb_type, comment):
            ralph.feedback_agent.log_feedback(qid, q, rating, fb_type, comment)

        st.markdown("##### 💬 Rate this answer (Feeds Ralph Loop Telemetry):")
        render_feedback_buttons(f"ui_{int(time.time())}", user_query, handle_feedback)

        st.markdown("---")
        render_sources_list(chunks)

# ----------------------------------------------------
# TAB 2: QUANTUM MATH EQUATION SOLVER & 3D/2D VISUALIZER
# ----------------------------------------------------
elif mode == "📐 Quantum Math & 3D/2D Visualizer":
    render_math_equation_solver_section()

# ----------------------------------------------------
# TAB 3: QUANTUM CIRCUIT SANDBOX
# ----------------------------------------------------
elif mode == "⚡ Quantum Circuit Sandbox":
    st.markdown('<div class="main-header">⚡ Multi-Backend Quantum Circuit Lab</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Live circuit execution across Qiskit Aer, Google Cirq, and PennyLane with cross-backend verification.</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        framework = st.selectbox("Quantum Backend:", ["PennyLane (Multi-Device)", "Qiskit Aer Simulator", "Google Cirq"])
    with c2:
        circuit_type = st.selectbox("Circuit Type:", ["Bell State (Entanglement)", "QAOA Step (p=1)", "GHZ State (3 Qubits)", "Superposition"])
    with c3:
        shots = st.number_input("Measurement Shots:", min_value=100, max_value=10000, value=1024, step=100)

    if st.button("▶️ Execute Quantum Circuit", type="primary"):
        with st.spinner("Compiling and sampling quantum backend..."):
            norm_type = "bell" if "Bell" in circuit_type else ("qaoa" if "QAOA" in circuit_type else ("ghz" if "GHZ" in circuit_type else "superposition"))
            
            if "PennyLane" in framework:
                res = pennylane.execute_cross_platform_qnode(circuit_type=norm_type, shots=shots)
                q_counts = res["qiskit_backend"]["counts"]
                c_counts = res["cirq_backend"]["counts"]

                st.success(f"✅ Executed on PennyLane across Qiskit Aer & Cirq Simulator (Fidelity Agreement: {res['fidelity_agreement']*100:.1f}%)")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("#### 🔵 Qiskit Aer Backend Counts")
                    df_q = pd.DataFrame(list(q_counts.items()), columns=["State", "Counts"])
                    fig_q = px.bar(df_q, x="State", y="Counts", title="Qiskit Aer Histogram", color="Counts", color_continuous_scale="Viridis")
                    st.plotly_chart(fig_q, use_container_width=True)
                    st.code(res["qiskit_backend"]["qasm"], language="qasm")

                with col_b:
                    st.markdown("#### 🔴 Google Cirq Backend Counts")
                    df_c = pd.DataFrame(list(c_counts.items()), columns=["State", "Counts"])
                    fig_c = px.bar(df_c, x="State", y="Counts", title="Cirq Simulator Histogram", color="Counts", color_continuous_scale="Magma")
                    st.plotly_chart(fig_c, use_container_width=True)
                    st.code(res["cirq_backend"]["diagram"], language="text")

            elif "Qiskit" in framework:
                res = qiskit.simulator.simulate_circuit(norm_type, shots=shots)
                st.success("✅ Simulated on Qiskit Aer")
                df = pd.DataFrame(list(res["counts"].items()), columns=["State", "Counts"])
                fig = px.bar(df, x="State", y="Counts", title=f"Qiskit Aer: {circuit_type} Counts", color="Counts")
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("##### QASM Circuit Representation:")
                st.code(res["qasm"], language="qasm")

            else: # Cirq
                res = cirq.run_qaoa_cirq(repetitions=shots) if norm_type == "qaoa" else cirq.run_bell_circuit(repetitions=shots)
                st.success("✅ Simulated on Google Cirq")
                df = pd.DataFrame(list(res["counts"].items()), columns=["State", "Counts"])
                fig = px.bar(df, x="State", y="Counts", title=f"Google Cirq: {circuit_type} Counts", color="Counts", color_continuous_scale="Inferno")
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("##### Cirq Circuit Diagram:")
                st.code(res["circuit_diagram"], language="text")

# ----------------------------------------------------
# TAB 4: RALPH AGENTIC LOOP CONTROL CENTER
# ----------------------------------------------------
elif mode == "🔄 Ralph Agentic Loop Control Center":
    render_ralph_control_room(ralph)

# ----------------------------------------------------
# TAB 5: VERIFIED CORPUS & BENCHMARKS
# ----------------------------------------------------
elif mode == "📚 Verified Corpus & Benchmarks":
    st.markdown('<div class="main-header">📚 Verified Corpus & Golden Benchmark Suite</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Browse all 18 indexed peer-reviewed publications and run automated benchmark evaluation suites.</div>', unsafe_allow_html=True)

    tab_corpus, tab_eval = st.tabs(["📚 Verified Corpus Explorer", "📊 Golden Evaluation Suite"])

    with tab_corpus:
        search_kw = st.text_input("Filter indexed documents by keyword, author, or theorem:", "")
        docs = retriever.bm25_chunks
        if search_kw:
            docs = [d for d in docs if search_kw.lower() in d.get("title", "").lower() or search_kw.lower() in d.get("content", "").lower()]
        st.markdown(f"**Indexed Knowledge Records ({len(docs)} found):**")
        render_sources_list(docs)

    with tab_eval:
        st.markdown("### 📊 Automated Benchmark Harness")
        if st.button("🚀 Run Full Golden Evaluation Suite (14 Tests)", type="primary"):
            with st.spinner("Running retrieval and generation evaluation across golden dataset..."):
                summary = run_evaluation()
                st.success("✅ Evaluation Benchmark Suite Completed!")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### 🎯 Information Retrieval Performance")
                    st.json(summary["retrieval"])
                with col2:
                    st.markdown("#### 📝 Generation & Groundedness Quality")
                    st.json(summary["generation"])
