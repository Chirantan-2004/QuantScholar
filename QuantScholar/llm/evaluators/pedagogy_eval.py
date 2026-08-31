"""
QuantumScholar - Pedagogy & Clarity Evaluator
Evaluates educational clarity, mathematical rigor (LaTeX/Dirac notation), and scaffolding.
"""

import re
from typing import Dict, Any

class PedagogyEvaluator:
    """Evaluates pedagogical quality of quantum computing responses."""

    def evaluate(self, answer: str) -> Dict[str, Any]:
        """
        Calculates:
        - clarity_score (0.0 to 1.0)
        - pedagogy_score (0.0 to 1.0)
        - has_latex_math (bool)
        - has_dirac_notation (bool)
        - has_structured_sections (bool)
        """
        if not answer:
            return {"clarity_score": 0.0, "pedagogy_score": 0.0, "has_latex_math": False, "has_dirac_notation": False}

        # 1. Structure Verification (4-part QuantumScholar structure)
        has_direct_ans = "1. Direct Answer" in answer or "Direct Answer" in answer
        has_explanation = "2. Explanation" in answer or "Explanation" in answer
        has_confidence = "4. Confidence" in answer or "Confidence" in answer
        has_structure = has_direct_ans and has_explanation

        # 2. LaTeX Math & Dirac Notation
        has_latex = bool(re.search(r'\\\[|\\\(|\$\$|\$|\\sum|\\prod|\\rangle|\\langle', answer))
        has_dirac = bool(re.search(r'\|[01\+\-\w\s]+\>|\\langle|\\rangle', answer))

        # 3. Readability & Scaffolding
        word_count = len(answer.split())
        adequate_length = 50 <= word_count <= 800

        # Compute Clarity
        clarity_components = [
            0.4 * (1.0 if has_structure else 0.4),
            0.3 * (1.0 if adequate_length else 0.5),
            0.3 * (1.0 if "##" in answer else 0.5)
        ]
        clarity_score = round(sum(clarity_components), 3)

        # Compute Pedagogy
        pedagogy_components = [
            0.35 * (1.0 if has_latex or has_dirac else 0.4),
            0.35 * (1.0 if has_explanation else 0.5),
            0.30 * (1.0 if has_confidence else 0.5)
        ]
        pedagogy_score = round(sum(pedagogy_components), 3)

        return {
            "clarity_score": clarity_score,
            "pedagogy_score": pedagogy_score,
            "has_latex_math": has_latex,
            "has_dirac_notation": has_dirac,
            "has_structured_sections": has_structure,
            "word_count": word_count
        }
