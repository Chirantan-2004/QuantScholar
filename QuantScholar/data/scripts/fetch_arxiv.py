"""
QuantumScholar - arXiv Paper Ingestion Script
Fetches foundational and recent quantum papers from the arXiv API (quant-ph, cs.QC).
"""

import os
import json
import time
import argparse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ARXIV_API_BASE = "http://export.arxiv.org/api/query"

DEFAULT_QUANTUM_QUERIES = [
    "cat:quant-ph AND (ti:algorithm OR ti:error+correction OR ti:qaoa OR ti:vqe)",
    "cat:quant-ph AND (ti:fault-tolerant OR ti:surface+code OR ti:shor OR ti:grover)",
    "cat:cs.QC AND (ti:circuit OR ti:compiler OR ti:transpiler OR ti:complexity)",
    "cat:quant-ph AND (ti:teleportation OR ti:cryptography OR ti:bb84 OR ti:bell)"
]

def fetch_arxiv_papers(query: str, max_results: int = 20, start: int = 0) -> list[dict]:
    """Queries the arXiv API and parses XML responses into structured dictionaries."""
    params = f"?search_query={urllib.parse.quote(query)}&start={start}&max_results={max_results}&sortBy=relevance&sortOrder=descending"
    url = ARXIV_API_BASE + params
    
    print(f"[*] Fetching: {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "QuantumScholar/1.0 (Research Quantum AI)"})
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            xml_data = response.read().decode("utf-8")
    except Exception as e:
        print(f"[!] Network error fetching arXiv: {e}")
        return []

    root = ET.fromstring(xml_data)
    ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/xmlns/arxiv"}
    
    papers = []
    for entry in root.findall("atom:entry", ns):
        id_elem = entry.find("atom:id", ns)
        arxiv_url = id_elem.text.strip() if id_elem is not None else ""
        arxiv_id = arxiv_url.split("/abs/")[-1] if "/abs/" in arxiv_url else arxiv_url.split("/")[-1]
        
        title_elem = entry.find("atom:title", ns)
        title = " ".join(title_elem.text.split()) if title_elem is not None else "Untitled"
        
        summary_elem = entry.find("atom:summary", ns)
        summary = " ".join(summary_elem.text.split()) if summary_elem is not None else ""
        
        published_elem = entry.find("atom:published", ns)
        published = published_elem.text.strip()[:4] if published_elem is not None else "Unknown"
        
        authors = []
        for author in entry.findall("atom:author", ns):
            name_elem = author.find("atom:name", ns)
            if name_elem is not None and name_elem.text:
                authors.append(name_elem.text.strip())
        
        journal_elem = entry.find("arxiv:journal_ref", ns)
        venue = journal_elem.text.strip() if journal_elem is not None and journal_elem.text else f"arXiv:{arxiv_id} [quant-ph]"
        
        papers.append({
            "arxiv_id": arxiv_id,
            "title": title,
            "authors": authors,
            "year": int(published) if published.isdigit() else 2024,
            "venue": venue,
            "url": f"https://arxiv.org/abs/{arxiv_id}",
            "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}.pdf",
            "abstract": summary,
            "doc_type": "paper"
        })
        
    return papers

def save_papers_metadata(papers: list[dict], output_dir: str):
    """Saves metadata JSON files in raw directory."""
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    
    for paper in papers:
        safe_id = paper["arxiv_id"].replace("/", "_")
        json_file = out_path / f"{safe_id}.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(paper, f, indent=2, ensure_ascii=False)
            
    print(f"[+] Successfully saved {len(papers)} paper metadata records to {output_dir}")

def main():
    parser = argparse.ArgumentParser(description="Fetch quantum computing papers from arXiv")
    parser.add_argument("--max-results", type=int, default=10, help="Max results per query")
    parser.add_argument("--output-dir", type=str, default="data/raw/arxiv_papers", help="Output directory")
    args = parser.parse_args()

    all_papers = []
    for query in DEFAULT_QUANTUM_QUERIES:
        papers = fetch_arxiv_papers(query, max_results=args.max_results)
        all_papers.extend(papers)
        time.sleep(1.0) # Respect arXiv rate limits
        
    # Deduplicate by arxiv_id
    unique_papers = {p["arxiv_id"]: p for p in all_papers}.values()
    save_papers_metadata(list(unique_papers), args.output_dir)

if __name__ == "__main__":
    import urllib.parse
    main()
