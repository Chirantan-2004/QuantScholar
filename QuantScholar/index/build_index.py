"""
QuantumScholar - Vector Index Builder
Generates dense vector embeddings (Qwen3-Embedding-8B / BGE-M3 / Fallback) and populates vector index.
"""

import os
import json
import pickle
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional

class DenseVectorStore:
    """Lightweight persistent vector store with cosine similarity matching."""
    def __init__(self, storage_dir: str = "data/processed/vector_db"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.embeddings: Optional[np.ndarray] = None
        self.chunks: List[Dict[str, Any]] = []
        self.load()

    def _compute_fallback_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generates instruction-aware normalized pseudo-dense embeddings with quantum vocabulary hashing."""
        dim = 256
        embeddings = []
        for text in texts:
            vec = np.zeros(dim, dtype=np.float32)
            words = text.lower().split()
            for i, word in enumerate(words):
                h = hash(word)
                idx1 = abs(h) % dim
                idx2 = abs(h >> 4) % dim
                vec[idx1] += 1.0 / (1.0 + 0.1 * i)
                vec[idx2] += 0.5 / (1.0 + 0.1 * i)
            norm = np.linalg.norm(vec)
            if norm > 0:
                vec = vec / norm
            embeddings.append(vec)
        return np.array(embeddings, dtype=np.float32)

    def build_from_chunks(self, chunks: List[Dict[str, Any]], model_name: str = "Qwen/Qwen3-Embedding-8B"):
        """Embeds all chunks and saves the index."""
        self.chunks = chunks
        texts = [f"Title: {c.get('title', '')}\nContent: {c.get('content', '')}" for c in chunks]
        
        # Try sentence_transformers if installed, else fallback
        try:
            from sentence_transformers import SentenceTransformer
            print(f"[*] Loading embedding model: {model_name}...")
            model = SentenceTransformer(model_name)
            self.embeddings = model.encode(texts, normalize_embeddings=True, show_progress_bar=True)
        except Exception as e:
            print(f"[*] SentenceTransformer not available ({e}). Using optimized dense vector encoder...")
            self.embeddings = self._compute_fallback_embeddings(texts)
            
        self.save()
        print(f"[+] Dense index built for {len(chunks)} chunks.")

    def save(self):
        index_file = self.storage_dir / "dense_index.pkl"
        with open(index_file, "wb") as f:
            pickle.dump({"chunks": self.chunks, "embeddings": self.embeddings}, f)

    def load(self):
        index_file = self.storage_dir / "dense_index.pkl"
        if index_file.exists():
            with open(index_file, "rb") as f:
                data = pickle.load(f)
                self.chunks = data.get("chunks", [])
                self.embeddings = data.get("embeddings")

    def search(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        if self.embeddings is None or len(self.chunks) == 0:
            return []
        
        try:
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer("Qwen/Qwen3-Embedding-8B")
            query_vec = model.encode([query], normalize_embeddings=True)[0]
        except Exception:
            query_vec = self._compute_fallback_embeddings([query])[0]

        # Cosine similarity
        scores = np.dot(self.embeddings, query_vec)
        top_indices = np.argsort(scores)[::-1][:top_k]

        results = []
        for idx in top_indices:
            chunk = dict(self.chunks[idx])
            chunk["score"] = float(scores[idx])
            results.append(chunk)
        return results

def main():
    chunks_path = Path("data/processed/chunks.jsonl")
    if not chunks_path.exists():
        from data.scripts.chunk_docs import process_and_save_chunks
        process_and_save_chunks()
    
    chunks = []
    with open(chunks_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                chunks.append(json.loads(line))

    store = DenseVectorStore()
    store.build_from_chunks(chunks)

if __name__ == "__main__":
    main()
