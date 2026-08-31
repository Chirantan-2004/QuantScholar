"""
QuantumScholar - BM25 Sparse Index Builder
Creates and serializes BM25 inverted index for quantum terminology and lexical search.
"""

import os
import re
import math
import json
import pickle
from pathlib import Path
from typing import List, Dict, Any

class BM25OkapiEngine:
    """Pure-Python Okapi BM25 implementation for quantum documents with dictionary serialization."""
    def __init__(self, corpus: List[List[str]] = None, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.corpus_size = len(corpus) if corpus else 0
        self.avgdl = (sum(len(doc) for doc in corpus) / max(self.corpus_size, 1)) if corpus else 0.0
        self.doc_freqs: List[Dict[str, int]] = []
        self.idf: Dict[str, float] = {}
        self.doc_len: List[int] = []

        if corpus:
            self._fit(corpus)

    def _fit(self, corpus: List[List[str]]):
        df: Dict[str, int] = {}
        for doc in corpus:
            self.doc_len.append(len(doc))
            frequencies: Dict[str, int] = {}
            for word in doc:
                frequencies[word] = frequencies.get(word, 0) + 1
            self.doc_freqs.append(frequencies)

            for word in frequencies:
                df[word] = df.get(word, 0) + 1

        for word, freq in df.items():
            self.idf[word] = math.log((self.corpus_size - freq + 0.5) / (freq + 0.5) + 1)

    def get_scores(self, query: List[str]) -> List[float]:
        score = [0.0] * self.corpus_size
        for q in query:
            q_idf = self.idf.get(q, 0.0)
            if q_idf == 0.0:
                continue
            for idx, doc_freq in enumerate(self.doc_freqs):
                freq = doc_freq.get(q, 0)
                if freq > 0:
                    numerator = freq * (self.k1 + 1)
                    denominator = freq + self.k1 * (1 - self.b + self.b * (self.doc_len[idx] / self.avgdl))
                    score[idx] += q_idf * (numerator / denominator)
        return score

    def to_dict(self) -> Dict[str, Any]:
        return {
            "k1": self.k1,
            "b": self.b,
            "corpus_size": self.corpus_size,
            "avgdl": self.avgdl,
            "doc_freqs": self.doc_freqs,
            "idf": self.idf,
            "doc_len": self.doc_len
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BM25OkapiEngine":
        engine = cls()
        engine.k1 = data["k1"]
        engine.b = data["b"]
        engine.corpus_size = data["corpus_size"]
        engine.avgdl = data["avgdl"]
        engine.doc_freqs = data["doc_freqs"]
        engine.idf = data["idf"]
        engine.doc_len = data["doc_len"]
        return engine

def tokenize_quantum_text(text: str) -> List[str]:
    """Tokenizes text with preservation of math symbols, latex operators, and quantum keywords."""
    text = text.lower()
    tokens = re.findall(r'[a-zA-Z0-9_\-\^\+\/\\]+|\|[\d\w\+\-]+\>', text)
    return tokens

def build_bm25_index(
    chunks_path: str = "data/processed/chunks.jsonl",
    output_dir: str = "data/processed/bm25_index"
):
    """Builds and serializes a BM25 index from chunks.jsonl."""
    chunks_file = Path(chunks_path)
    if not chunks_file.exists():
        from data.scripts.chunk_docs import process_and_save_chunks
        process_and_save_chunks(chunks_path)

    corpus_chunks = []
    with open(chunks_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                corpus_chunks.append(json.loads(line))

    tokenized_corpus = []
    for chunk in corpus_chunks:
        full_text = f"{chunk.get('title', '')} {chunk.get('content', '')}"
        tokens = tokenize_quantum_text(full_text)
        tokenized_corpus.append(tokens)

    bm25 = BM25OkapiEngine(tokenized_corpus)

    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    index_data = {
        "bm25_dict": bm25.to_dict(),
        "chunks": corpus_chunks,
        "tokenized_corpus": tokenized_corpus
    }

    with open(out_path / "bm25_model.pkl", "wb") as f:
        pickle.dump(index_data, f)

    print(f"[+] BM25 index built and saved to {out_path / 'bm25_model.pkl'}")

if __name__ == "__main__":
    build_bm25_index()
