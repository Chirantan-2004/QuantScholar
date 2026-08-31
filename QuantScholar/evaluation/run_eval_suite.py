"""
QuantumScholar - Automated Benchmark & Evaluation Suite
Runs comprehensive evaluation over retrieval (Recall, nDCG, MRR) and generation (Groundedness, Pedagogy, Citations).
"""

import sys
import os
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import json
import time
import datetime
from typing import Dict, Any, List

from retrieval.service import QuantumRetriever
from retrieval.evaluators.retrieval_eval import evaluate_retrieval_benchmark
from llm.service import QuantumLLM
from llm.evaluators.groundedness_eval import GroundednessEvaluator
from llm.evaluators.pedagogy_eval import PedagogyEvaluator

def run_evaluation(
    golden_dataset_path: str = "evaluation/datasets/quantum_qa_golden.jsonl",
    output_report_dir: str = "evaluation/reports",
    top_k: int = 5
) -> Dict[str, Any]:
    """Runs complete end-to-end evaluation suite and generates Markdown report."""
    print("[*] Initializing QuantumScholar Evaluation Suite...")
    
    golden_file = Path(golden_dataset_path)
    if not golden_file.exists():
        raise FileNotFoundError(f"Golden dataset not found at {golden_dataset_path}")

    samples = []
    with open(golden_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                samples.append(json.loads(line))

    print(f"[*] Loaded {len(samples)} golden benchmark test cases.")

    retriever = QuantumRetriever()
    llm = QuantumLLM()
    groundedness_evaluator = GroundednessEvaluator()
    pedagogy_evaluator = PedagogyEvaluator()

    # 1. Evaluate Retrieval
    print("[*] Evaluating Hybrid Retrieval (Dense + BM25 + RRF + Reranker)...")
    retrieval_metrics = evaluate_retrieval_benchmark(retriever, samples, k=top_k)

    # 2. Evaluate Generation & Groundedness
    print("[*] Evaluating LLM Generation Groundedness & Pedagogy...")
    groundedness_scores = []
    clarity_scores = []
    pedagogy_scores = []
    citation_compliance_list = []
    detailed_results = []

    start_time = time.time()
    for sample in samples:
        query = sample["query"]
        chunks = retriever.retrieve(query, top_k=top_k)
        gen_res = llm.generate_answer(query, chunks)
        answer = gen_res["answer"]

        g_eval = groundedness_evaluator.evaluate(answer, chunks)
        p_eval = pedagogy_evaluator.evaluate(answer)

        groundedness_scores.append(g_eval["groundedness_score"])
        clarity_scores.append(p_eval["clarity_score"])
        pedagogy_scores.append(p_eval["pedagogy_score"])
        citation_compliance_list.append(g_eval["has_sources_section"] and g_eval["citation_count"] > 0)

        detailed_results.append({
            "id": sample["id"],
            "query": query,
            "groundedness": g_eval["groundedness_score"],
            "clarity": p_eval["clarity_score"],
            "pedagogy": p_eval["pedagogy_score"],
            "citations_found": g_eval["citation_count"],
            "has_sources_section": g_eval["has_sources_section"]
        })

    eval_duration = round(time.time() - start_time, 2)
    avg_groundedness = round(float(sum(groundedness_scores) / len(groundedness_scores)), 4)
    avg_clarity = round(float(sum(clarity_scores) / len(clarity_scores)), 4)
    avg_pedagogy = round(float(sum(pedagogy_scores) / len(pedagogy_scores)), 4)
    citation_compliance_rate = round(float(sum(citation_compliance_list) / len(citation_compliance_list)), 4)

    summary = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "sample_count": len(samples),
        "eval_duration_sec": eval_duration,
        "retrieval": retrieval_metrics,
        "generation": {
            "mean_groundedness": avg_groundedness,
            "mean_clarity": avg_clarity,
            "mean_pedagogy": avg_pedagogy,
            "citation_compliance_rate": citation_compliance_rate
        },
        "system_status": "PASS" if avg_groundedness >= 0.90 and avg_clarity >= 0.85 else "WARN"
    }

    # Generate Markdown report
    out_dir = Path(output_report_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    today_str = datetime.date.today().strftime("%Y%m%d")
    report_file = out_dir / f"eval_report_{today_str}.md"

    report_md = f"""# QuantumScholar System Evaluation Report ({today_str})

## Executive Summary
- **Evaluation Status**: `{summary['system_status']}`
- **Test Samples**: {summary['sample_count']} Golden Benchmark Queries
- **Evaluation Duration**: {eval_duration}s

## 1. Information Retrieval Metrics (Top-{top_k})
| Metric | Value | Target | Status |
|---|---|---|---|
| **Recall@{top_k}** | {retrieval_metrics.get(f'recall@{top_k}', 0.0):.4f} | ≥ 0.85 | {'✅ PASS' if retrieval_metrics.get(f'recall@{top_k}', 0.0) >= 0.85 else '⚠️ TUNE'} |
| **Precision@{top_k}** | {retrieval_metrics.get(f'precision@{top_k}', 0.0):.4f} | ≥ 0.20 | ✅ PASS |
| **MRR** | {retrieval_metrics.get('mrr', 0.0):.4f} | ≥ 0.80 | {'✅ PASS' if retrieval_metrics.get('mrr', 0.0) >= 0.80 else '⚠️ TUNE'} |
| **nDCG@{top_k}** | {retrieval_metrics.get(f'ndcg@{top_k}', 0.0):.4f} | ≥ 0.80 | {'✅ PASS' if retrieval_metrics.get(f'ndcg@{top_k}', 0.0) >= 0.80 else '⚠️ TUNE'} |

## 2. LLM Generation & Groundedness Metrics
| Metric | Score (0-1) | Target Threshold | Status |
|---|---|---|---|
| **Groundedness Score** | {avg_groundedness:.4f} | ≥ 0.90 | {'✅ PASS' if avg_groundedness >= 0.90 else '❌ FAIL'} |
| **Clarity Score** | {avg_clarity:.4f} | ≥ 0.85 | {'✅ PASS' if avg_clarity >= 0.85 else '❌ FAIL'} |
| **Pedagogy Score** | {avg_pedagogy:.4f} | ≥ 0.85 | {'✅ PASS' if avg_pedagogy >= 0.85 else '❌ FAIL'} |
| **Citation Compliance** | {citation_compliance_rate * 100:.1f}% | 100% | {'✅ PASS' if citation_compliance_rate >= 0.99 else '⚠️ AUDIT'} |

## 3. Sample-Level Breakdown
| ID | Query | Groundedness | Clarity | Pedagogy | Citations |
|---|---|---|---|---|---|
"""
    for r in detailed_results:
        report_md += f"| `{r['id']}` | {r['query'][:45]}... | {r['groundedness']:.2f} | {r['clarity']:.2f} | {r['pedagogy']:.2f} | {r['citations_found']} |\n"

    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report_md)

    print(f"[+] Evaluation complete. Report saved to {report_file}")
    return summary

if __name__ == "__main__":
    summary = run_evaluation()
    print("\nEvaluation Summary:")
    print(json.dumps(summary, indent=2))
