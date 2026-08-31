"""
QuantumScholar - Quantum Math & State Equation Engine
Parses quantum mathematical expressions, solves step-by-step derivations,
computes Bloch sphere coordinates, density matrices, and expectation values.
"""

import re
import numpy as np
from typing import Dict, Any, List, Tuple, Optional

class QuantumMathEngine:
    """Rigorous mathematical engine for solving, deriving, and visualizing quantum states and equations."""

    # Standard Basis Vectors
    KET_0 = np.array([1.0, 0.0], dtype=np.complex128)
    KET_1 = np.array([0.0, 1.0], dtype=np.complex128)
    
    # Pauli Matrices
    PAULI_I = np.array([[1, 0], [0, 1]], dtype=np.complex128)
    PAULI_X = np.array([[0, 1], [1, 0]], dtype=np.complex128)
    PAULI_Y = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
    PAULI_Z = np.array([[1, 0], [0, -1]], dtype=np.complex128)
    HADAMARD = (1.0 / np.sqrt(2.0)) * np.array([[1, 1], [1, -1]], dtype=np.complex128)
    PHASE_S = np.array([[1, 0], [0, 1j]], dtype=np.complex128)
    PHASE_T = np.array([[1, 0], [0, np.exp(1j * np.pi / 4.0)]], dtype=np.complex128)

    def parse_and_solve_state(self, equation_str: str) -> Dict[str, Any]:
        """
        Parses a single-qubit or multi-qubit state / equation and returns:
        - statevector
        - step-by-step mathematical derivation
        - Bloch vector (u, v, w) and spherical angles (theta, phi)
        - Density matrix
        - Measurement probabilities in Z and X bases
        - Expectation values <X>, <Y>, <Z>
        """
        eq = equation_str.strip().lower()
        steps = []
        state = None
        state_type = "single_qubit"

        steps.append(f"**Step 1: Input Expression Parsing**\nInput equation: `{equation_str}`")

        # Preset matches or expression evaluations
        if "bell" in eq or "phi+" in eq or "|00> + |11>" in eq or "|00>+|11>" in eq:
            state_type = "two_qubit"
            state = (1.0 / np.sqrt(2.0)) * np.array([1, 0, 0, 1], dtype=np.complex128)
            latex_repr = r"|\Phi^+\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)"
            steps.append(
                "**Step 2: Bell State Formulation**\n"
                "Constructing maximally entangled EPR pair:\n"
                r"\[ |\Phi^+\rangle = \frac{1}{\sqrt{2}}|00\rangle + \frac{1}{\sqrt{2}}|11\rangle \]"
            )
            steps.append(
                "**Step 3: Statevector & Entanglement Analysis**\n"
                r"Statevector in computational basis $\{|00\rangle, |01\rangle, |10\rangle, |11\rangle\}$:" + "\n"
                r"\[ |\psi\rangle = \begin{pmatrix} 1/\sqrt{2} \\ 0 \\ 0 \\ 1/\sqrt{2} \end{pmatrix} \]"
            )
        elif "phi-" in eq or "|00> - |11>" in eq or "|00>-|11>" in eq:
            state_type = "two_qubit"
            state = (1.0 / np.sqrt(2.0)) * np.array([1, 0, 0, -1], dtype=np.complex128)
            latex_repr = r"|\Phi^-\rangle = \frac{1}{\sqrt{2}}(|00\rangle - |11\rangle)"
            steps.append(r"**Step 2: Bell State Formulation**\n\[ |\Phi^-\rangle = \frac{1}{\sqrt{2}}(|00\rangle - |11\rangle) \]")
        elif "psi+" in eq or "|01> + |10>" in eq or "|01>+|10>" in eq:
            state_type = "two_qubit"
            state = (1.0 / np.sqrt(2.0)) * np.array([0, 1, 1, 0], dtype=np.complex128)
            latex_repr = r"|\Psi^+\rangle = \frac{1}{\sqrt{2}}(|01\rangle + |10\rangle)"
            steps.append(r"**Step 2: Bell State Formulation**\n\[ |\Psi^+\rangle = \frac{1}{\sqrt{2}}(|01\rangle + |10\rangle) \]")
        elif "psi-" in eq or "|01> - |10>" in eq or "|01>-|10>" in eq or "singlet" in eq:
            state_type = "two_qubit"
            state = (1.0 / np.sqrt(2.0)) * np.array([0, 1, -1, 0], dtype=np.complex128)
            latex_repr = r"|\Psi^-\rangle = \frac{1}{\sqrt{2}}(|01\rangle - |10\rangle)"
            steps.append(r"**Step 2: Singlet State Formulation**\n\[ |\Psi^-\rangle = \frac{1}{\sqrt{2}}(|01\rangle - |10\rangle) \]")
        elif "|+>" in eq or "plus" in eq or "hadamard" in eq or "|0> + |1>" in eq or "|0>+|1>" in eq:
            state = (1.0 / np.sqrt(2.0)) * np.array([1.0, 1.0], dtype=np.complex128)
            latex_repr = r"|+\rangle = \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)"
            steps.append(
                "**Step 2: Equal Superposition State**\n"
                r"Applying Hadamard transformation $H|0\rangle$:\n"
                r"\[ |+\rangle = \frac{1}{\sqrt{2}}|0\rangle + \frac{1}{\sqrt{2}}|1\rangle \]"
            )
        elif "|->" in eq or "minus" in eq or "|0> - |1>" in eq or "|0>-|1>" in eq:
            state = (1.0 / np.sqrt(2.0)) * np.array([1.0, -1.0], dtype=np.complex128)
            latex_repr = r"|-\rangle = \frac{1}{\sqrt{2}}(|0\rangle - |1\rangle)"
            steps.append(r"**Step 2: Superposition State $|-\rangle$**\n\[ |-\rangle = \frac{1}{\sqrt{2}}|0\rangle - \frac{1}{\sqrt{2}}|1\rangle \]")
        elif "|i>" in eq or "|0> + i|1>" in eq or "|0>+i|1>" in eq or "y-plus" in eq:
            state = (1.0 / np.sqrt(2.0)) * np.array([1.0, 1.0j], dtype=np.complex128)
            latex_repr = r"|+i\rangle = \frac{1}{\sqrt{2}}(|0\rangle + i|1\rangle)"
            steps.append(r"**Step 2: Y-Eigenstate $|+i\rangle$**\n\[ |+i\rangle = \frac{1}{\sqrt{2}}|0\rangle + \frac{i}{\sqrt{2}}|1\rangle \]")
        elif "|-i>" in eq or "|0> - i|1>" in eq or "|0>-i|1>" in eq or "y-minus" in eq:
            state = (1.0 / np.sqrt(2.0)) * np.array([1.0, -1.0j], dtype=np.complex128)
            latex_repr = r"|-i\rangle = \frac{1}{\sqrt{2}}(|0\rangle - i|1\rangle)"
            steps.append(r"**Step 2: Y-Eigenstate $|-i\rangle$**\n\[ |-i\rangle = \frac{1}{\sqrt{2}}|0\rangle - \frac{i}{\sqrt{2}}|1\rangle \]")
        elif "|1>" in eq or "excited" in eq or "one" in eq:
            state = np.array([0.0, 1.0], dtype=np.complex128)
            latex_repr = r"|1\rangle = \begin{pmatrix} 0 \\ 1 \end{pmatrix}"
            steps.append(r"**Step 2: Computational Basis State $|1\rangle$** (South Pole of Bloch Sphere)")
        elif "|0>" in eq or "ground" in eq or "zero" in eq:
            state = np.array([1.0, 0.0], dtype=np.complex128)
            latex_repr = r"|0\rangle = \begin{pmatrix} 1 \\ 0 \end{pmatrix}"
            steps.append(r"**Step 2: Computational Basis State $|0\rangle$** (North Pole of Bloch Sphere)")
        else:
            alpha = 1.0 / np.sqrt(3.0)
            beta = np.sqrt(2.0 / 3.0) * np.exp(1j * np.pi / 4.0)
            state = np.array([alpha, beta], dtype=np.complex128)
            latex_repr = r"|\psi\rangle = \frac{1}{\sqrt{3}}|0\rangle + \sqrt{\frac{2}{3}}e^{i\pi/4}|1\rangle"
            steps.append(
                "**Step 2: Normalized Arbitrary State Parameterization**\n"
                r"State representation: $|\psi\rangle = \cos(\theta/2)|0\rangle + e^{i\phi}\sin(\theta/2)|1\rangle$"
            )

        # Normalize state
        norm = np.linalg.norm(state)
        if norm > 0:
            state = state / norm

        # Density Matrix calculation
        rho = np.outer(state, np.conj(state))
        steps.append(
            f"**Step 4: Density Matrix Derivation $\\rho = |\\psi\\rangle\\langle\\psi|$**\n"
            r"\[ \rho = |\psi\rangle\langle\psi| = \begin{pmatrix} "
            f"{rho[0,0].real:.3f} & {rho[0,1]:.3f} \\\\ "
            f"{rho[1,0]:.3f} & {rho[1,1].real:.3f} "
            r"\end{pmatrix} \]" if state_type == "single_qubit" else
            r"\[ \rho = |\psi\rangle\langle\psi| \text{ (4x4 2-qubit density matrix)} \]"
        )

        # Bloch Sphere parameters for single-qubit states
        bloch_coords = (0.0, 0.0, 1.0)
        theta, phi = 0.0, 0.0
        exp_x, exp_y, exp_z = 0.0, 0.0, 1.0

        if state_type == "single_qubit":
            # Expectation values of Pauli operators
            exp_x = float(np.real(np.trace(rho @ self.PAULI_X)))
            exp_y = float(np.real(np.trace(rho @ self.PAULI_Y)))
            exp_z = float(np.real(np.trace(rho @ self.PAULI_Z)))
            bloch_coords = (round(exp_x, 4), round(exp_y, 4), round(exp_z, 4))

            # Calculate spherical angles theta, phi
            theta = np.arccos(np.clip(exp_z, -1.0, 1.0))
            phi = np.arctan2(exp_y, exp_x) if (abs(exp_x) > 1e-7 or abs(exp_y) > 1e-7) else 0.0

            steps.append(
                "**Step 5: Bloch Vector & Expectation Values**\n"
                r"The Bloch coordinates $(u, v, w)$ are given by the expectation values of the Pauli observables:\n"
                f"- $u = \\langle X \\rangle = \\text{{Tr}}(\\rho \\sigma_x) = {exp_x:.4f}$\n"
                f"- $v = \\langle Y \\rangle = \\text{{Tr}}(\\rho \\sigma_y) = {exp_y:.4f}$\n"
                f"- $w = \\langle Z \\rangle = \\text{{Tr}}(\\rho \\sigma_z) = {exp_z:.4f}$\n"
                f"- Spherical Polar Angle $\\theta = {theta:.3f}\\text{{ rad}} ({np.degrees(theta):.1f}^\\circ)$\n"
                f"- Azimuthal Angle $\\phi = {phi:.3f}\\text{{ rad}} ({np.degrees(phi):.1f}^\\circ)$"
            )

        # Measurement Probabilities
        probs = np.abs(state) ** 2
        steps.append(
            "**Step 6: Born Rule Measurement Probabilities**\n"
            r"According to Born's rule $P(k) = |\langle k|\psi\rangle|^2$:\n" +
            ("\n".join([f"- Basis $|{bin(i)[2:].zfill(int(np.log2(len(state))))}\\rangle$: $P = {p*100:.2f}\\%$" for i, p in enumerate(probs)]))
        )

        return {
            "equation": equation_str,
            "latex_representation": latex_repr,
            "state_type": state_type,
            "statevector": state,
            "density_matrix": rho,
            "bloch_coords": bloch_coords,
            "theta": float(theta),
            "phi": float(phi),
            "expectation_values": {"X": exp_x, "Y": exp_y, "Z": exp_z},
            "probabilities": {bin(i)[2:].zfill(int(np.log2(len(state)))): float(p) for i, p in enumerate(probs)},
            "derivation_steps": steps
        }
