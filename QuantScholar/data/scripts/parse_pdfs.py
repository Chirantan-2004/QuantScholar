"""
QuantumScholar - PDF and Document Parser
Extracts structured text, equations, and sections from PDF papers and docs.
"""

import os
import re
import json
from pathlib import Path
from typing import Optional, Dict, Any, List

def clean_extracted_text(text: str) -> str:
    """Normalizes whitespace, fixes hyphenation, and standardizes LaTeX notation."""
    # Fix hyphenated words at line breaks
    text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)
    # Remove multiple linebreaks
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Standardize spaces
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

def parse_metadata_file(json_path: Path) -> Optional[Dict[str, Any]]:
    """Loads paper metadata from JSON sidecar."""
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[!] Error reading {json_path}: {e}")
        return None

def parse_raw_corpus(raw_dir: str = "data/raw") -> List[Dict[str, Any]]:
    """Walks the raw papers, books, and docs directory and extracts structured documents."""
    base_path = Path(raw_dir)
    documents = []

    # 1. Process arXiv papers metadata & text
    arxiv_dir = base_path / "arxiv_papers"
    if arxiv_dir.exists():
        for meta_file in arxiv_dir.glob("*.json"):
            meta = parse_metadata_file(meta_file)
            if meta:
                content = meta.get("abstract", "")
                documents.append({
                    "id": f"arxiv_{meta.get('arxiv_id', meta_file.stem)}",
                    "title": meta.get("title", ""),
                    "authors": meta.get("authors", []),
                    "year": meta.get("year", 2024),
                    "venue": meta.get("venue", "arXiv"),
                    "url": meta.get("url", ""),
                    "doc_type": "paper",
                    "content": content
                })

    # 2. Process Books & Docs (JSON or Markdown)
    for doc_type in ["books", "docs"]:
        target_dir = base_path / doc_type
        if target_dir.exists():
            for doc_file in target_dir.glob("*.*"):
                if doc_file.suffix in [".json", ".jsonl"]:
                    meta = parse_metadata_file(doc_file)
                    if meta:
                        documents.append(meta)
                elif doc_file.suffix in [".md", ".txt"]:
                    content = doc_file.read_text(encoding="utf-8")
                    documents.append({
                        "id": f"{doc_type}_{doc_file.stem}",
                        "title": doc_file.stem.replace("_", " ").title(),
                        "authors": ["Quantum Community"],
                        "year": 2024,
                        "venue": f"Official {doc_type.title()} Documentation",
                        "url": f"https://docs.antigravity.quantum/{doc_file.stem}",
                        "doc_type": doc_type[:-1] if doc_type.endswith("s") else doc_type,
                        "content": content
                    })

    print(f"[+] Loaded {len(documents)} raw documents from {raw_dir}")
    return documents

if __name__ == "__main__":
    docs = parse_raw_corpus()
    print(f"Total parsed documents: {len(docs)}")
