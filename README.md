# ⚛️ QuantumScholar (Antigravity Platform)

> **Citation-Grounded, Quantum-Only AI Platform powered by the 2026 Open-Source Stack and Ralph Agentic Self-Improvement Loop.**

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-FF4B4B)](https://streamlit.io)
[![Qiskit](https://img.shields.io/badge/Qiskit-1.0%2B-6929C4)](https://qiskit.org)
[![Cirq](https://img.shields.io/badge/Google_Cirq-1.3%2B-4285F4)](https://quantumai.google/cirq)
[![PennyLane](https://img.shields.io/badge/PennyLane-0.35%2B-FA5A2C)](https://pennylane.ai)

---

## 🎯 Mission
**QuantumScholar** answers quantum computing questions **only** using verified knowledge from peer-reviewed research papers (arXiv quant-ph, cs.QC, PRX Quantum, Nature), textbooks (Nielsen & Chuang, Mark Wilde), and official quantum SDK documentation (Qiskit, Cirq, PennyLane), with explicit mandatory inline citations and direct links. It incorporates a **Ralph-style agentic loop** to continuously self-improve until system metrics and user satisfaction thresholds are met.

---

## 🧠 2026 Open-Source Model Stack

| Component | Model Choice | Why? | License |
|---|---|---|---|
| **Generation LLM** | **Qwen3-30B-Instruct** | Top-tier reasoning, 256K context, state-of-the-art for RAG synthesis. | Apache 2.0 |
| **Embedding** | **Qwen3-Embedding-8B** | #1 on MTEB, 32K context, instruction-aware. | Apache 2.0 |
| **Reranker** | **Qwen3-Reranker** | Cross-encoder matching embedding model, high precision for quantum science. | Apache 2.0 |
| **Alternative LLM** | **Llama-3.1-70B-Instruct** | Maximum general reasoning performance. | Llama 3.1 |
| **Alternative Embed** | **BGE-M3** | Dense + sparse multi-lingual retrieval. | MIT |

---

## 📂 Complete Repository Architecture

```
antigravity/
├─ README.md                     # Project overview & architecture
├─ LICENSE                       # Apache 2.0 License
├─ .gitignore
├─ pyproject.toml
├─ requirements.txt
│
├─ configs/
│  ├─ default.yaml               # Global paths, model names, thresholds
│  ├─ models.yaml                # LLM, embed, reranker configs
│  └─ rag.yaml                   # Chunking, retrieval, fusion params
│
├─ data/
│  ├─ raw/
│  │  ├─ arxiv_papers/           # Downloaded PDFs + metadata JSONs
│  │  ├─ books/                  # Textbooks (PDF/HTML)
│  │  └─ docs/                   # SDK docs (Qiskit, Cirq, PennyLane)
│  ├─ processed/
│  │  ├─ chunks.jsonl            # Chunked documents with metadata
│  │  └─ bm25_index/             # BM25 index files
│  └─ scripts/
│     ├─ fetch_arxiv.py          # arXiv quant-ph API harvester
│     ├─ parse_pdfs.py           # Structured PDF parser
│     ├─ chunk_docs.py           # Citation-aware chunker
│     ├─ seed_corpus.py          # Foundational verified quantum seed data
│     └─ build_bm25.py           # Inverted sparse index generator
│
├─ index/
│  ├─ build_index.py             # Create dense vector index
│  └─ update_index.py            # Incremental updates and sync
│
├─ retrieval/
│  ├─ service.py                 # QuantumRetriever class (hybrid + rerank)
│  ├─ fusion.py                  # Reciprocal Rank & Weighted score fusion
│  └─ evaluators/
│     ├─ retrieval_eval.py       # nDCG, Recall@k, MRR
│     └─ llm_judge_retrieval.py  # LLM Judge relevance evaluation
│
├─ llm/
│  ├─ service.py                 # QuantumLLM class (citation grounded)
│  ├─ prompts/
│  │  ├─ system_quantumscholar.md # MASTER PROMPT
│  │  ├─ user_template.txt       # Context + question template
│  │  └─ judge_prompts.yaml      # LLM-as-a-judge prompts
│  └─ evaluators/
│     ├─ groundedness_eval.py    # Strict claim support & hallucination check
│     └─ pedagogy_eval.py        # Clarity & Dirac math evaluator
│
├─ api/
│  ├─ main.py                    # FastAPI app, /ask, /search, /execute_circuit
│  ├─ schemas.py                 # Pydantic data contracts
│  └─ middleware/
│     └─ logging.py              # Request/response logging
│
├─ ui/
│  ├─ streamlit_app.py           # Streamlit Web Application
│  ├─ components/
│  │  ├─ chat.py                 # Grounded chat with audit badges
│  │  └─ sources.py              # Verified paper card inspector
│  └─ assets/
│
├─ agents/
│  ├─ ralph_loop.py              # 🔄 Main agentic loop controller
│  ├─ quality_agent.py           # Checks groundedness, clarity, pedagogy
│  ├─ retrieval_agent.py         # Tunes retrieval params
│  ├─ prompt_agent.py            # Evolves prompt variants
│  └─ feedback_agent.py          # Ingests user feedback & metrics
│
├─ evaluation/
│  ├─ run_eval_suite.py          # Full eval (retrieval + generation)
│  ├─ datasets/
│  │  ├─ quantum_qa_golden.jsonl # Golden benchmark test suite
│  │  └─ user_feedback_logs.jsonl# Feedback telemetry
│  └─ reports/
│     └─ eval_report_YYYYMMDD.md # Generated evaluation reports
│
├─ integrations/
│  ├─ qiskit/
│  │  ├─ circuit_runner.py       # Qiskit circuit execution
│  │  └─ aer_simulator.py        # Aer statevector simulation
│  ├─ cirq/
│  │  └─ cirq_runner.py          # Google Cirq GridQubit simulation
│  └─ pennylane/
│     └─ pennylane_devices.py    # PennyLane multi-device layer
│
└─ notebooks/
   ├─ 01_corpus_exploration.ipynb
   ├─ 02_retrieval_experiments.ipynb
   ├─ 03_prompt_ablations.ipynb
   └─ 04_ralph_loop_demo.ipynb
```

---

## 🔄 Ralph Agentic Self-Improvement Loop

```
                       ┌────────────────────────┐
                       │  1. COLLECT Telemetry  │
                       │ (Queries, Docs, Votes) │
                       └───────────┬────────────┘
                                   │
                                   ▼
                       ┌────────────────────────┐
                       │   2. EVALUATE Quality  │
                       │ (Groundedness, Pedagogy)│
                       └───────────┬────────────┘
                                   │
                                   ▼
                       ┌────────────────────────┐
                       │   3. DIAGNOSE Gaps     │
                       │ (Retrieval Bottlenecks)│
                       └───────────┬────────────┘
                                   │
                                   ▼
                       ┌────────────────────────┐
                       │   4. PROPOSE Tweaks    │
                       │ (Prompts & Hyperparams)│
                       └───────────┬────────────┘
                                   │
                                   ▼
                       ┌────────────────────────┐
                       │  5. EXPERIMENT (A/B)   │
                       │ (Test Golden Dataset)  │
                       └───────────┬────────────┘
                                   │
                                   ▼
                       ┌────────────────────────┐
                       │   6. PROMOTE Config    │
                       │ (Update Prod Settings) │
                       └────────────────────────┘
```

---

## 🚀 Quick Start Guide

### 1. Installation
```bash
git clone <your-repo-url> antigravity
cd antigravity
pip install -r requirements.txt
```

### 2. Ingest Data & Build Hybrid Index
```bash
python data/scripts/chunk_docs.py
python data/scripts/build_bm25.py
python index/build_index.py
```

### 3. Run Automated Evaluation Suite
```bash
python evaluation/run_eval_suite.py
```

### 4. Run 1 Ralph Agentic Optimization Cycle
```bash
python agents/ralph_loop.py
```

### 5. Launch FastAPI Backend
```bash
python api/main.py
# API running at http://localhost:8000 (Swagger docs at http://localhost:8000/docs)
```

### 6. Launch Interactive Streamlit UI
```bash
streamlit run ui/streamlit_app.py
```

---

## 📄 License
Distributed under the **Apache 2.0 License**. See `LICENSE` for details.
