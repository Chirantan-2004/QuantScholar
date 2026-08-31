"""
QuantumScholar - Ralph Loop: Prompt Agent
Generates, mutates, and tests prompt variants to optimize groundedness and pedagogical quality.
"""

from typing import Dict, Any, List

class PromptAgent:
    """Agent that evolves system prompt variants to maximize factual accuracy and clarity."""

    def __init__(self, master_prompt_path: str = "llm/prompts/system_quantumscholar.md"):
        self.master_prompt_path = master_prompt_path
        self.variants = []

    def propose_prompt_mutation(self, diagnosis: Dict[str, Any]) -> Dict[str, Any]:
        """Proposes a prompt mutation if groundedness or formatting issues are detected."""
        mutations = []
        if diagnosis.get("unsupported_claims_total", 0) > 0:
            mutations.append("Reinforce negative constraint: 'Under no circumstances extrapolate or synthesize unretrieved claims.'")
            mutations.append("Mandate strict inline citation tag format: '[Paper: AuthorYear]' immediately after each claim.")
        else:
            mutations.append("Enhance pedagogical scaffolding: Include explicit Dirac notation representations for all state operations.")

        return {
            "version": "v1.1-scaffolded",
            "proposed_mutations": mutations,
            "rationale": "Improve mathematical clarity and eliminate boundary hallucination."
        }
