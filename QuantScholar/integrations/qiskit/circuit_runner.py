"""
QuantumScholar - Qiskit Circuit Runner
Constructs and runs parameterized quantum circuits on Qiskit backends.
"""

from typing import Dict, Any
from integrations.qiskit.aer_simulator import QiskitAerSimulator

class QiskitCircuitRunner:
    """Manages Qiskit circuit execution and state analysis."""

    def __init__(self):
        self.simulator = QiskitAerSimulator()

    def run_bell_state(self, shots: int = 1024) -> Dict[str, Any]:
        """Runs maximally entangled Bell state: (|00> + |11>) / sqrt(2)."""
        return self.simulator.simulate_circuit("bell", num_qubits=2, shots=shots)

    def run_ghz_state(self, num_qubits: int = 3, shots: int = 1024) -> Dict[str, Any]:
        """Runs Greenberger-Horne-Zeilinger (GHZ) state."""
        return self.simulator.simulate_circuit("ghz", num_qubits=num_qubits, shots=shots)

    def run_qaoa_circuit(self, gamma: float = 1.05, beta: float = 0.78, shots: int = 1024) -> Dict[str, Any]:
        """Runs 1-layer QAOA Max-Cut circuit."""
        res = self.simulator.simulate_circuit("qaoa", num_qubits=2, shots=shots)
        res["parameters"] = {"gamma": gamma, "beta": beta}
        return res
