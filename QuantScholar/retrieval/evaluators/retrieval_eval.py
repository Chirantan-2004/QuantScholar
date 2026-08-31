"""
QuantumScholar - Information Retrieval Metrics Evaluator
Calculates Recall@k, Precision@k, MRR, and nDCG@k over quantum QA benchmarks.
"""

import numpy as np
from typing import List, Dict, Any, Set

def compute_recall_at_k(retrieved_ids: List[str], ground_truth_ids: Set[str], k: int = 5) -> float:
    """Calculates Recall@k."""
    if not ground_truth_ids:
        return 1.0
    top_k_ids = set(retrieved_ids[:k])
    relevant_retrieved = top_k_ids.intersection(ground_truth_ids)
    return len(relevant_retrieved) / len(ground_truth_ids)

def compute_precision_at_k(retrieved_ids: List[str], ground_truth_ids: Set[str], k: int = 5) -> float:
    """Calculates Precision@k."""
    if k == 0:
        return 0.0
    top_k_ids = set(retrieved_ids[:k])
    relevant_retrieved = top_k_ids.intersection(ground_truth_ids)
    return len(relevant_retrieved) / k

def compute_mrr(retrieved_ids: List[str], ground_truth_ids: Set[str]) -> float:
    """Calculates Mean Reciprocal Rank (MRR)."""
    for rank, doc_id in enumerate(retrieved_ids, 1):
        if doc_id in ground_truth_ids:
            return 1.0 / rank
    return 0.0

def compute_ndcg_at_k(retrieved_ids: List[str], ground_truth_ids: Set[str], k: int = 5) -> float:
    """Calculates Normalized Discounted Cumulative Gain (nDCG@k) with binary relevance."""
    dcg = 0.0
    for rank, doc_id in enumerate(retrieved_ids[:k], 1):
        rel = 1.0 if doc_id in ground_truth_ids else 0.0
        dcg += rel / np.log2(rank + 1)

    # Ideal DCG
    ideal_rels = [1.0] * min(len(ground_truth_ids), k)
    idcg = sum(rel / np.log2(rank + 1) for rank, rel in enumerate(ideal_rels, 1))

    if idcg == 0.0:
        return 0.0
    return float(dcg / idcg)

def evaluate_retrieval_benchmark(retriever, golden_dataset: List[Dict[str, Any]], k: int = 5) -> Dict[str, float]:
    """Evaluates a retriever over an entire golden dataset."""
    recalls = []
    precisions = []
    mrrs = []
    ndcgs = []

    for sample in golden_dataset:
        query = sample["query"]
        expected_ids = set(sample.get("expected_chunk_ids", []))
        
        results = retriever.retrieve(query, top_k=k)
        retrieved_ids = [r["chunk_id"] for r in results]

        recalls.append(compute_recall_at_k(retrieved_ids, expected_ids, k=k))
        precisions.append(compute_precision_at_k(retrieved_ids, expected_ids, k=k))
        mrrs.append(compute_mrr(retrieved_ids, expected_ids))
        ndcgs.append(compute_ndcg_at_k(retrieved_ids, expected_ids, k=k))

    return {
        f"recall@{k}": float(np.mean(recalls)),
        f"precision@{k}": float(np.mean(precisions)),
        "mrr": float(np.mean(mrrs)),
        f"ndcg@{k}": float(np.mean(ndcgs))
    }
