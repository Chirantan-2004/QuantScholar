"""
QuantumScholar - Ralph Loop: Retrieval Agent
Diagnoses retrieval failures, identifies missing coverage, and tunes retrieval hyperparameters.
"""

from typing import List, Dict, Any

class RetrievalAgent:
    """Agent responsible for analyzing retrieval performance and tuning retrieval parameters."""

    def __init__(self):
        self.current_params = {
            "top_k": 5,
            "fusion_strategy": "reciprocal_rank_fusion",
            "dense_weight": 0.65,
            "sparse_weight": 0.35,
            "enable_reranking": True,
            "reranker_threshold": 0.30
        }

    def diagnose_gaps(self, audits: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Identifies patterns in low-scoring queries (e.g. low recall, missing keywords)."""
        failed_queries = [a for a in audits if not a.get("passed", False)]
        unsupported_count = sum(len(a.get("unsupported_claims", [])) for a in failed_queries)

        recommendations = []
        if len(failed_queries) > 0:
            if unsupported_count > 2:
                recommendations.append("Increase top_k retrieval depth from 5 to 7 to provide broader context.")
                recommendations.append("Increase BM25 sparse weight to capture specific mathematical and acronym tokens.")
            else:
                recommendations.append("Tune cross-encoder reranker threshold to filter out marginal chunks.")

        return {
            "failed_count": len(failed_queries),
            "unsupported_claims_total": unsupported_count,
            "diagnoses": recommendations,
            "healthy": len(failed_queries) == 0
        }

    def propose_hyperparameters(self, diagnosis: Dict[str, Any]) -> Dict[str, Any]:
        """Proposes parameter adjustments based on diagnosis."""
        new_params = dict(self.current_params)
        if not diagnosis.get("healthy", False):
            # Self-healing parameter adjustment
            new_params["top_k"] = min(self.current_params["top_k"] + 2, 10)
            new_params["sparse_weight"] = min(self.current_params["sparse_weight"] + 0.05, 0.50)
            new_params["dense_weight"] = round(1.0 - new_params["sparse_weight"], 2)

        return {
            "previous_params": self.current_params,
            "proposed_params": new_params,
            "changed": new_params != self.current_params
        }

    def apply_parameters(self, params: Dict[str, Any]):
        """Updates active retrieval hyperparameters."""
        self.current_params.update(params)
