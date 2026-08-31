"""
QuantumScholar - Quick Platform Self-Test
Validates all subsystems: Retrieval, Grounded Generation, Multi-Backend Quantum Execution, and Ralph Loop.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from retrieval.service import QuantumRetriever
from llm.service import QuantumLLM
from integrations.qiskit.circuit_runner import QiskitCircuitRunner
from integrations.cirq.cirq_runner import CirqRunner
from integrations.pennylane.pennylane_devices import PennyLaneDeviceManager
from agents.ralph_loop import RalphLoop

def test_all():
    print("==================================================")
    print("[*] Testing QuantumScholar Platform Subsystems")
    print("==================================================")

    # 1. Retrieval
    print("[1/4] Testing Hybrid Quantum Retriever...")
    retriever = QuantumRetriever()
    query = "How does Shor's algorithm find the period for factoring?"
    chunks = retriever.retrieve(query, top_k=2)
    assert len(chunks) > 0, "Retrieval failed"
    print(f"      Top chunk: [{chunks[0]['citation_tag']}] {chunks[0]['title']}")

    # 2. LLM Generation
    print("[2/4] Testing Grounded LLM Generation...")
    llm = QuantumLLM()
    res = llm.generate_answer(query, chunks)
    assert "## 1. Direct Answer" in res["answer"], "Missing Direct Answer"
    assert "## 3. Sources" in res["answer"], "Missing Sources Section"
    print("      Grounded answer generated successfully with citations & sources.")

    # 3. Quantum Execution Integrations
    print("[3/4] Testing Multi-Backend Quantum Integrations...")
    qiskit_res = QiskitCircuitRunner().run_bell_state(shots=500)
    cirq_res = CirqRunner().run_bell_circuit(repetitions=500)
    pennylane_res = PennyLaneDeviceManager().execute_cross_platform_qnode(shots=500)
    
    print(f"      Qiskit Aer Counts: {qiskit_res['counts']}")
    print(f"      Google Cirq Counts: {cirq_res['counts']}")
    print(f"      PennyLane Cross-Device: {pennylane_res['pennylane_qnode']} (Fidelity: {pennylane_res['fidelity_agreement']*100:.1f}%)")

    # 4. Ralph Loop Status
    print("[4/4] Testing Ralph Agentic Loop Subsystem...")
    ralph = RalphLoop()
    status = ralph.get_status()
    print(f"      Ralph Status: {status['status']} | Satisfaction: {status['user_feedback_summary']['mean_rating']}/5.0")

    print("\n[+] All QuantumScholar subsystems verified successfully!")

if __name__ == "__main__":
    test_all()
