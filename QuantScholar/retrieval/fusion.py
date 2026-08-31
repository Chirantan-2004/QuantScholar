"""
QuantumScholar - Retrieval Fusion Module
Implements Reciprocal Rank Fusion (RRF) and Weighted Score Fusion for hybrid retrieval.
"""

from typing import List, Dict, Any

def reciprocal_rank_fusion(
    dense_results: List[Dict[str, Any]],
    sparse_results: List[Dict[str, Any]],
    k: int = 60,
    top_n: int = 10
) -> List[Dict[str, Any]]:
    """
    Combines dense and sparse ranked lists using Reciprocal Rank Fusion (RRF):
    RRF_score(d) = sum_{m in models} 1 / (k + rank_m(d))
    """
    scores: Dict[str, float] = {}
    chunk_map: Dict[str, Dict[str, Any]] = {}

    # Process Dense Results
    for rank, doc in enumerate(dense_results, 1):
        doc_id = doc["chunk_id"]
        chunk_map[doc_id] = doc
        scores[doc_id] = scores.get(doc_id, 0.0) + (1.0 / (k + rank))

    # Process Sparse (BM25) Results
    for rank, doc in enumerate(sparse_results, 1):
        doc_id = doc["chunk_id"]
        if doc_id not in chunk_map:
            chunk_map[doc_id] = doc
        scores[doc_id] = scores.get(doc_id, 0.0) + (1.0 / (k + rank))

    # Sort combined results by RRF score
    sorted_doc_ids = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)

    fused_results = []
    for doc_id in sorted_doc_ids[:top_n]:
        item = dict(chunk_map[doc_id])
        item["rrf_score"] = scores[doc_id]
        fused_results.append(item)

    return fused_results

def weighted_score_fusion(
    dense_results: List[Dict[str, Any]],
    sparse_results: List[Dict[str, Any]],
    dense_weight: float = 0.65,
    sparse_weight: float = 0.35,
    top_n: int = 10
) -> List[Dict[str, Any]]:
    """Combines normalized dense and sparse scores with linear weighting."""
    def min_max_normalize(results):
        if not results:
            return {}
        scores = [r.get("score", 0.0) for r in results]
        min_s, max_s = min(scores), max(scores)
        denom = (max_s - min_s) if (max_s - min_s) > 0 else 1.0
        return {r["chunk_id"]: (r.get("score", 0.0) - min_s) / denom for r in results}

    dense_norm = min_max_normalize(dense_results)
    sparse_norm = min_max_normalize(sparse_results)

    all_ids = set(dense_norm.keys()) | set(sparse_norm.keys())
    chunk_map = {r["chunk_id"]: r for r in (dense_results + sparse_results)}

    combined = []
    for doc_id in all_ids:
        d_score = dense_norm.get(doc_id, 0.0)
        s_score = sparse_norm.get(doc_id, 0.0)
        final_score = (dense_weight * d_score) + (sparse_weight * s_score)
        
        item = dict(chunk_map[doc_id])
        item["weighted_score"] = final_score
        combined.append(item)

    combined.sort(key=lambda x: x["weighted_score"], reverse=True)
    return combined[:top_n]
