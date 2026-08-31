"""
QuantumScholar - Groundedness Evaluator
Evaluates whether every factual claim in an answer is supported by retrieved context chunks.
"""

import re
from typing import List, Dict, Any

class GroundednessEvaluator:
    """Evaluates strict factual grounding and citation compliance."""

    def evaluate(self, answer: str, retrieved_chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculates:
        - groundedness_score (0.0 - 1.0)
        - citation_count
        - has_sources_section (bool)
        - unsupported_claims (list of str)
        """
        if not answer:
            return {"groundedness_score": 0.0, "citation_count": 0, "has_sources_section": False, "unsupported_claims": ["Empty answer"]}

        # 1. Check Citation Tags [Paper:...], [Book:...], [Doc:...]
        citation_tags = re.findall(r'\[(?:Paper|Book|Doc):\s*[^\]]+\]', answer)
        citation_count = len(citation_tags)

        # 2. Check Sources Section
        has_sources = "## 3. Sources" in answer or "## Sources" in answer or "### Sources" in answer

        # 3. Compile context tokens from all retrieved chunks
        context_text = " ".join([
            f"{c.get('title', '')} {c.get('content', '')} {' '.join(c.get('authors', []))}"
            for c in retrieved_chunks
        ]).lower()
        context_tokens = set(re.findall(r'[a-zA-Z0-9_\-\^]+', context_text))

        # Split into claim sentences
        raw_lines = answer.split("\n")
        sentences = []
        for line in raw_lines:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("\\[") or line.startswith("\\]") or line.startswith("- **Confidence") or line.startswith("- **Gap"):
                continue
            if "sources" in line.lower() or "direct link" in line.lower():
                continue
            for s in re.split(r'(?<=[.!?])\s+', line):
                if len(s.strip()) > 15:
                    sentences.append(s.strip())

        unsupported = []
        supported_count = 0

        for sent in sentences:
            # Extract content words (> 3 chars)
            tokens = [t.lower() for t in re.findall(r'[a-zA-Z]{3,}', sent)]
            # Filter common stop words
            stopwords = {"the", "and", "for", "with", "this", "that", "from", "are", "key", "all", "its", "each", "into", "over", "can", "based"}
            content_tokens = [t for t in tokens if t not in stopwords]
            
            if not content_tokens:
                supported_count += 1
                continue

            matches = sum(1 for t in content_tokens if t in context_tokens)
            support_ratio = matches / len(content_tokens)

            # Grounded threshold for a sentence
            if support_ratio >= 0.35:
                supported_count += 1
            else:
                unsupported.append(sent)

        total_evaluated_sentences = max(len(sentences), 1)
        groundedness_score = round(min(supported_count / total_evaluated_sentences, 1.0), 4)

        if citation_count == 0:
            groundedness_score = round(groundedness_score * 0.5, 4)
        if not has_sources:
            groundedness_score = round(groundedness_score * 0.8, 4)

        return {
            "groundedness_score": max(groundedness_score, 0.0),
            "citation_count": citation_count,
            "has_sources_section": has_sources,
            "unsupported_claims": unsupported,
            "is_grounded": groundedness_score >= 0.85
        }
