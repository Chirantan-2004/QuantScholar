"""
QuantumScholar - Incremental Index Updater
Adds new research papers or SDK docs to both BM25 and Dense vector indices.
"""

import json
import argparse
from pathlib import Path
from typing import Dict, Any, List
from data.scripts.build_bm25 import build_bm25_index
from index.build_index import DenseVectorStore

def add_document_chunk(chunk: Dict[str, Any], chunks_path: str = "data/processed/chunks.jsonl"):
    """Appends a new chunk to chunks.jsonl and rebuilds indices."""
    chunks_file = Path(chunks_path)
    chunks_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(chunks_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
        
    print(f"[+] Added chunk {chunk.get('chunk_id')} to {chunks_path}")

def sync_indices(chunks_path: str = "data/processed/chunks.jsonl"):
    """Synchronizes both BM25 and Vector indices with chunks.jsonl."""
    print("[*] Synchronizing BM25 sparse index...")
    build_bm25_index(chunks_path)
    
    print("[*] Synchronizing Dense vector index...")
    chunks = []
    with open(chunks_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                chunks.append(json.loads(line))
                
    store = DenseVectorStore()
    store.build_from_chunks(chunks)
    print("[+] Indices successfully synchronized.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update and sync indices")
    parser.add_argument("--sync", action="store_true", help="Sync all indices")
    args = parser.parse_args()
    if args.sync:
        sync_indices()
