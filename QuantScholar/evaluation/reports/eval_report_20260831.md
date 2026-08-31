# QuantumScholar System Evaluation Report (20260831)

## Executive Summary
- **Evaluation Status**: `WARN`
- **Test Samples**: 14 Golden Benchmark Queries
- **Evaluation Duration**: 0.05s

## 1. Information Retrieval Metrics (Top-5)
| Metric | Value | Target | Status |
|---|---|---|---|
| **Recall@5** | 0.8571 | ≥ 0.85 | ✅ PASS |
| **Precision@5** | 0.1857 | ≥ 0.20 | ✅ PASS |
| **MRR** | 0.8036 | ≥ 0.80 | ✅ PASS |
| **nDCG@5** | 0.7956 | ≥ 0.80 | ⚠️ TUNE |

## 2. LLM Generation & Groundedness Metrics
| Metric | Score (0-1) | Target Threshold | Status |
|---|---|---|---|
| **Groundedness Score** | 0.8274 | ≥ 0.90 | ❌ FAIL |
| **Clarity Score** | 1.0000 | ≥ 0.85 | ✅ PASS |
| **Pedagogy Score** | 1.0000 | ≥ 0.85 | ✅ PASS |
| **Citation Compliance** | 100.0% | 100% | ✅ PASS |

## 3. Sample-Level Breakdown
| ID | Query | Groundedness | Clarity | Pedagogy | Citations |
|---|---|---|---|---|---|
| `gold_01` | How does Shor's algorithm achieve an exponent... | 0.86 | 1.00 | 1.00 | 7 |
| `gold_02` | What is the query complexity of Grover's sear... | 0.88 | 1.00 | 1.00 | 7 |
| `gold_03` | Explain how the surface code detects and corr... | 0.78 | 1.00 | 1.00 | 7 |
| `gold_04` | How does the QAOA algorithm solve combinatori... | 0.77 | 1.00 | 1.00 | 7 |
| `gold_05` | How does the Variational Quantum Eigensolver ... | 0.86 | 1.00 | 1.00 | 7 |
| `gold_06` | What principles guarantee unconditional secur... | 0.83 | 1.00 | 1.00 | 7 |
| `gold_07` | What are the core steps of the HHL algorithm ... | 0.81 | 1.00 | 1.00 | 7 |
| `gold_08` | How does Qiskit Aer execute local quantum cir... | 0.79 | 1.00 | 1.00 | 7 |
| `gold_09` | How are moments and GridQubits structured in ... | 0.79 | 1.00 | 1.00 | 7 |
| `gold_10` | How does PennyLane achieve device-agnostic qu... | 0.82 | 1.00 | 1.00 | 7 |
| `gold_11` | How does Simon's algorithm achieve an exponen... | 0.86 | 1.00 | 1.00 | 7 |
| `gold_12` | How do single and multi-qubit gates like Hada... | 0.88 | 1.00 | 1.00 | 7 |
| `gold_13` | What are the three main families of quantum a... | 0.83 | 1.00 | 1.00 | 7 |
| `gold_14` | How does Quantum Amplitude Amplification gene... | 0.81 | 1.00 | 1.00 | 7 |
