"""
QuantumScholar - Hybrid Quantum Retriever Service
Combines Dense Semantic Search, BM25 Keyword Search, Reciprocal Rank Fusion (RRF),
and Cross-Encoder Reranking (Qwen3-Reranker).
"""

import sys
import os
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import json
import pickle
from typing import List, Dict, Any, Optional

from data.scripts.build_bm25 import tokenize_quantum_text, BM25OkapiEngine
from index.build_index import DenseVectorStore
from retrieval.fusion import reciprocal_rank_fusion, weighted_score_fusion

class QuantumRetriever:
    """Enterprise-grade hybrid retriever tailored for quantum computing physics and literature."""

    def __init__(
        self,
        bm25_path: str = "data/processed/bm25_index/bm25_model.pkl",
        vector_db_path: str = "data/processed/vector_db",
        chunks_path: str = "data/processed/chunks.jsonl"
    ):
        self.bm25_path = Path(bm25_path)
        self.chunks_path = Path(chunks_path)
        self.vector_store = DenseVectorStore(storage_dir=vector_db_path)
        self.bm25 = None
        self.bm25_chunks = []
        self._load_indices()

    def _load_indices(self):
        """Loads BM25 model and dense vector index."""
        if not self.chunks_path.exists():
            print("[*] Chunks file not found. Initializing seed chunks...")
            from data.scripts.chunk_docs import process_and_save_chunks
            process_and_save_chunks(str(self.chunks_path))

        if not self.bm25_path.exists():
            print("[*] BM25 index not found. Building BM25 index...")
            from data.scripts.build_bm25 import build_bm25_index
            build_bm25_index(str(self.chunks_path), str(self.bm25_path.parent))

        if self.bm25_path.exists():
            with open(self.bm25_path, "rb") as f:
                data = pickle.load(f)
                if "bm25_dict" in data:
                    self.bm25 = BM25OkapiEngine.from_dict(data["bm25_dict"])
                else:
                    self.bm25 = data.get("bm25")
                self.bm25_chunks = data["chunks"]

        if self.vector_store.embeddings is None:
            print("[*] Vector store empty. Populating dense embeddings...")
            self.vector_store.build_from_chunks(self.bm25_chunks)

    def search_sparse(self, query: str, top_k: int = 15) -> List[Dict[str, Any]]:
        """BM25 search over quantum corpus."""
        if not self.bm25 or not self.bm25_chunks:
            return []
        tokens = tokenize_quantum_text(query)
        scores = self.bm25.get_scores(tokens)
        
        indexed_scores = list(enumerate(scores))
        indexed_scores.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for idx, score in indexed_scores[:top_k]:
            if score > 0:
                chunk = dict(self.bm25_chunks[idx])
                chunk["score"] = float(score)
                chunk["retrieval_method"] = "sparse_bm25"
                results.append(chunk)
        return results

    def search_dense(self, query: str, top_k: int = 15) -> List[Dict[str, Any]]:
        """Dense semantic search using Qwen3-Embedding-8B / normalized vectors."""
        results = self.vector_store.search(query, top_k=top_k)
        for r in results:
            r["retrieval_method"] = "dense_semantic"
        return results

    def rerank(self, query: str, candidate_chunks: List[Dict[str, Any]], top_n: int = 5) -> List[Dict[str, Any]]:
        """Applies Cross-Encoder reranking (Qwen3-Reranker) to candidate chunks."""
        if not candidate_chunks:
            return []
        
        try:
            from sentence_transformers import CrossEncoder
            reranker = CrossEncoder("Qwen/Qwen3-Reranker")
            pairs = [[query, f"{c.get('title', '')} {c.get('content', '')}"] for c in candidate_chunks]
            scores = reranker.predict(pairs)
            for idx, score in enumerate(scores):
                candidate_chunks[idx]["rerank_score"] = float(score)
        except Exception:
            # High-precision quantum keyword and semantic overlap fallback score
            q_terms = set(tokenize_quantum_text(query))
            for chunk in candidate_chunks:
                c_terms = set(tokenize_quantum_text(f"{chunk.get('title', '')} {chunk.get('content', '')}"))
                overlap = len(q_terms.intersection(c_terms)) / max(len(q_terms), 1)
                base_score = chunk.get("rrf_score", 0.0) * 10
                chunk["rerank_score"] = round(0.5 * overlap + 0.5 * min(base_score, 1.0), 4)

        candidate_chunks.sort(key=lambda x: x.get("rerank_score", 0.0), reverse=True)
        return candidate_chunks[:top_n]

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        fusion_strategy: str = "reciprocal_rank_fusion",
        enable_reranking: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Executes end-to-end hybrid retrieval:
        1. Sparse BM25 Search
        2. Dense Semantic Search
        3. Rank Fusion (RRF / Weighted)
        4. Cross-Encoder Reranking
        """
        sparse_res = self.search_sparse(query, top_k=15)
        dense_res = self.search_dense(query, top_k=15)

        if fusion_strategy == "reciprocal_rank_fusion":
            fused = reciprocal_rank_fusion(dense_res, sparse_res, k=60, top_n=10)
        else:
            fused = weighted_score_fusion(dense_res, sparse_res, dense_weight=0.65, sparse_weight=0.35, top_n=10)

        if enable_reranking and fused:
            return self.rerank(query, fused, top_n=top_k)
        
        return fused[:top_k]

if __name__ == "__main__":
    retriever = QuantumRetriever()
    test_query = "How does Shor's algorithm find the period for factoring?"
    results = retriever.retrieve(test_query, top_k=3)
    print(f"\n[Retrieval Results for '{test_query}']:")
    for i, r in enumerate(results, 1):
        print(f"{i}. [{r.get('citation_tag')}] {r.get('title')} (Score: {r.get('rerank_score', r.get('rrf_score'))})")
