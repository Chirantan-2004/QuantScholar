"""
QuantumScholar - Ralph Loop: Quality Agent
Evaluates live/benchmark answers using LLM-as-a-Judge for groundedness, clarity, and pedagogy.
"""

from typing import List, Dict, Any
from llm.evaluators.groundedness_eval import GroundednessEvaluator
from llm.evaluators.pedagogy_eval import PedagogyEvaluator

class QualityAgent:
    """Agent responsible for measuring response quality and identifying degradation or hallucinations."""

    def __init__(self):
        self.groundedness_evaluator = GroundednessEvaluator()
        self.pedagogy_evaluator = PedagogyEvaluator()

    def audit_response(self, query: str, answer: str, retrieved_chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Runs quality audit on a single response."""
        g_res = self.groundedness_evaluator.evaluate(answer, retrieved_chunks)
        p_res = self.pedagogy_evaluator.evaluate(answer)

        is_passed = (
            g_res["groundedness_score"] >= 0.90 and
            p_res["clarity_score"] >= 0.85 and
            p_res["pedagogy_score"] >= 0.85
        )

        return {
            "query": query,
            "passed": is_passed,
            "groundedness_score": g_res["groundedness_score"],
            "clarity_score": p_res["clarity_score"],
            "pedagogy_score": p_res["pedagogy_score"],
            "unsupported_claims": g_res.get("unsupported_claims", []),
            "citation_count": g_res.get("citation_count", 0),
            "has_sources": g_res.get("has_sources_section", False)
        }

    def evaluate_batch(self, pairs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Evaluates a batch of queries, answers, and context chunks."""
        audits = []
        for item in pairs:
            audit = self.audit_response(
                query=item["query"],
                answer=item["answer"],
                retrieved_chunks=item.get("chunks", [])
            )
            audits.append(audit)

        avg_groundedness = sum(a["groundedness_score"] for a in audits) / max(len(audits), 1)
        avg_clarity = sum(a["clarity_score"] for a in audits) / max(len(audits), 1)
        avg_pedagogy = sum(a["pedagogy_score"] for a in audits) / max(len(audits), 1)
        pass_rate = sum(1 for a in audits if a["passed"]) / max(len(audits), 1)

        return {
            "mean_groundedness": round(avg_groundedness, 4),
            "mean_clarity": round(avg_clarity, 4),
            "mean_pedagogy": round(avg_pedagogy, 4),
            "pass_rate": round(pass_rate, 4),
            "audits": audits
        }
