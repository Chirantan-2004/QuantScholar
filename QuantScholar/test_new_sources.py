import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from retrieval.service import QuantumRetriever
from llm.service import QuantumLLM

r = QuantumRetriever()
l = QuantumLLM()

queries = [
    "What are the three main families of quantum algorithms according to Ashley Montanaro's Springer survey?",
    "How does Shor's algorithm reduce factoring to order finding in IEEE FOCS 1994?",
    "How do single and multi-qubit gates work in Qiskit according to Learn Quantum Computing with Qiskit?",
    "How does Simon's algorithm achieve an exponential speedup in the Open-Access curriculum?"
]

for q in queries:
    print("\n" + "="*70)
    print(f"QUERY: {q}")
    chunks = r.retrieve(q, top_k=2)
    print(f"Retrieved Chunks: {[c['citation_tag'] for c in chunks]}")
    ans = l.generate_answer(q, chunks)
    print("ANSWER:\n" + ans["answer"])
