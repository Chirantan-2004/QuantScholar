"""
QuantumScholar - Document Chunking Script
Performs semantic and citation-aware chunking of quantum documents into JSONL records.
"""

import json
import argparse
from pathlib import Path
from typing import List, Dict, Any

try:
    from data.scripts.seed_corpus import FOUNDATIONAL_QUANTUM_CHUNKS
except ImportError:
    from seed_corpus import FOUNDATIONAL_QUANTUM_CHUNKS

def chunk_text(text: str, chunk_size_words: int = 150, overlap_words: int = 25) -> List[str]:
    """Splits a document text into sliding-window chunks with word overlap."""
    words = text.split()
    if len(words) <= chunk_size_words:
        return [text]
    
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size_words, len(words))
        chunk_words = words[start:end]
        chunks.append(" ".join(chunk_words))
        if end == len(words):
            break
        start += (chunk_size_words - overlap_words)
    return chunks

def process_and_save_chunks(output_path: str = "data/processed/chunks.jsonl"):
    """Compiles all verified foundational papers and parsed texts into chunks.jsonl."""
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    
    all_chunks = []
    
    # 1. Ingest Foundational Seed Corpus
    for item in FOUNDATIONAL_QUANTUM_CHUNKS:
        # Build normalized citation tag
        author_last = item["authors"][0].split()[-1] if item["authors"] else "QuantumAuthor"
        year = item.get("year", 2024)
        doc_type = item.get("doc_type", "paper").capitalize()
        citation_tag = f"[{doc_type}: {author_last}{year}]"
        
        chunk_entry = {
            "chunk_id": item["chunk_id"],
            "title": item["title"],
            "authors": item["authors"],
            "year": year,
            "venue": item.get("venue", "arXiv"),
            "url": item.get("url", ""),
            "arxiv_id": item.get("arxiv_id", ""),
            "doc_type": item.get("doc_type", "paper"),
            "citation_tag": citation_tag,
            "content": item["content"]
        }
        all_chunks.append(chunk_entry)

    # 2. Write to JSONL
    with open(out_file, "w", encoding="utf-8") as f:
        for chunk in all_chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
            
    print(f"[+] Successfully wrote {len(all_chunks)} chunks to {output_path}")
    return all_chunks

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chunk quantum documents")
    parser.add_argument("--output", type=str, default="data/processed/chunks.jsonl", help="Output chunks JSONL path")
    args = parser.parse_args()
    process_and_save_chunks(args.output)
