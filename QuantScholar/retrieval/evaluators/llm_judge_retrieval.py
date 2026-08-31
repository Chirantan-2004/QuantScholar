"""
QuantumScholar - LLM Judge for Retrieval Relevance
Scores retrieved context chunks against queries for relevance and topical coverage.
"""

from typing import List, Dict, Any

class LLMJudgeRetrieval:
    """Evaluates whether retrieved quantum chunks contain necessary information."""
    
    def evaluate(self, query: str, retrieved_chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Judges retrieval relevance score (0.0 to 1.0) and identifies missing subtopics."""
        if not retrieved_chunks:
            return {
                "relevance_score": 0.0,
                "coverage_sufficient": False,
                "missing_topics": ["No chunks retrieved"]
            }

        q_lower = query.lower()
        chunk_texts = " ".join([f"{c.get('title', '')} {c.get('content', '')}".lower() for c in retrieved_chunks])
        
        # Check topic presence
        keywords = [w for w in q_lower.split() if len(w) > 3]
        matches = [kw for kw in keywords if kw in chunk_texts]
        coverage_ratio = len(matches) / max(len(keywords), 1)

        relevance_score = min(round(coverage_ratio * 0.9 + 0.1, 2), 1.0)
        sufficient = relevance_score >= 0.70

        missing = []
        if not sufficient:
            missing = [kw for kw in keywords if kw not in chunk_texts]

        return {
            "relevance_score": relevance_score,
            "coverage_sufficient": sufficient,
            "missing_topics": missing
        }
