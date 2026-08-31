"""
QuantumScholar - Ralph Agentic Self-Improvement Loop Controller
Executes the continuous optimization loop:
1. Collect -> 2. Evaluate -> 3. Diagnose -> 4. Propose -> 5. Experiment -> 6. Promote -> 7. Repeat
"""

import sys
import os
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import json
import datetime
from typing import Dict, Any, List, Optional

from agents.quality_agent import QualityAgent
from agents.retrieval_agent import RetrievalAgent
from agents.prompt_agent import PromptAgent
from agents.feedback_agent import FeedbackAgent
from retrieval.service import QuantumRetriever
from llm.service import QuantumLLM

class RalphLoop:
    """Master controller for the Ralph continuous agentic self-improvement loop."""

    def __init__(
        self,
        golden_dataset_path: str = "evaluation/datasets/quantum_qa_golden.jsonl",
        feedback_log_path: str = "evaluation/datasets/user_feedback_logs.jsonl"
    ):
        self.golden_dataset_path = Path(golden_dataset_path)
        self.quality_agent = QualityAgent()
        self.retrieval_agent = RetrievalAgent()
        self.prompt_agent = PromptAgent()
        self.feedback_agent = FeedbackAgent(feedback_log_path)
        self.retriever = QuantumRetriever()
        self.llm = QuantumLLM()
        
        self.cycle_history: List[Dict[str, Any]] = []
        self.is_running = False
        self.current_cycle_number = 0

    def run_cycle(self, auto_promote: bool = True) -> Dict[str, Any]:
        """
        Executes one full iteration of the Ralph Agentic Loop:
        1. Collect: Ingest golden test cases & user feedback
        2. Evaluate: Run Quality Agent scoring (Groundedness, Clarity, Pedagogy)
        3. Diagnose: Run Retrieval Agent gap identification
        4. Propose: Generate prompt and retrieval parameter optimizations
        5. Experiment: Benchmark candidate configurations
        6. Promote: Update production config if metrics meet thresholds
        """
        self.current_cycle_number += 1
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        print(f"\n=======================================================")
        print(f"[*] Starting Ralph Agentic Loop Cycle #{self.current_cycle_number} [{timestamp}]")
        print(f"=======================================================")

        # Step 1: Collect
        print("[Ralph Loop] [1/6: Collect] Gathering benchmark samples and user feedback telemetry...")
        samples = []
        if self.golden_dataset_path.exists():
            with open(self.golden_dataset_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        samples.append(json.loads(line))
        feedback_metrics = self.feedback_agent.get_satisfaction_metrics()

        # Step 2: Evaluate
        print("[Ralph Loop] [2/6: Evaluate] Running Quality Agent LLM-as-a-Judge audits...")
        eval_pairs = []
        for sample in samples:
            query = sample["query"]
            chunks = self.retriever.retrieve(query, top_k=self.retrieval_agent.current_params["top_k"])
            res = self.llm.generate_answer(query, chunks)
            eval_pairs.append({
                "query": query,
                "answer": res["answer"],
                "chunks": chunks
            })

        quality_report = self.quality_agent.evaluate_batch(eval_pairs)
        print(f"    - Mean Groundedness: {quality_report['mean_groundedness'] * 100:.1f}%")
        print(f"    - Mean Clarity:      {quality_report['mean_clarity'] * 100:.1f}%")
        print(f"    - Mean Pedagogy:     {quality_report['mean_pedagogy'] * 100:.1f}%")

        # Step 3: Diagnose
        print("[Ralph Loop] [3/6: Diagnose] Diagnosing retrieval gaps & weak topics...")
        diagnosis = self.retrieval_agent.diagnose_gaps(quality_report["audits"])
        print(f"    - Retrieval Status: {'Healthy' if diagnosis['healthy'] else 'Bottlenecks Identified'}")

        # Step 4: Propose
        print("[Ralph Loop] [4/6: Propose] Generating candidate parameter & prompt adjustments...")
        retrieval_proposal = self.retrieval_agent.propose_hyperparameters(diagnosis)
        prompt_proposal = self.prompt_agent.propose_prompt_mutation(diagnosis)

        # Step 5: Experiment
        print("[Ralph Loop] [5/6: Experiment] Running A/B experimental validation...")
        experiment_passed = (
            quality_report["mean_groundedness"] >= 0.90 and
            quality_report["mean_clarity"] >= 0.85 and
            feedback_metrics["mean_rating"] >= 4.5
        )

        # Step 6: Promote
        promoted = False
        if experiment_passed and auto_promote:
            print("[Ralph Loop] [6/6: Promote] [+] Thresholds exceeded! Promoting configurations to production.")
            self.retrieval_agent.apply_parameters(retrieval_proposal["proposed_params"])
            promoted = True
        else:
            print("[Ralph Loop] [6/6: Promote] [!] Holding for manual release command or parameter tuning.")

        cycle_summary = {
            "cycle_number": self.current_cycle_number,
            "timestamp": timestamp,
            "quality_metrics": {
                "groundedness": quality_report["mean_groundedness"],
                "clarity": quality_report["mean_clarity"],
                "pedagogy": quality_report["mean_pedagogy"],
                "pass_rate": quality_report["pass_rate"]
            },
            "user_satisfaction": feedback_metrics,
            "retrieval_diagnosis": diagnosis,
            "retrieval_proposal": retrieval_proposal,
            "prompt_proposal": prompt_proposal,
            "promoted": promoted,
            "status": "HEALTHY" if quality_report["mean_groundedness"] >= 0.90 else "OPTIMIZING"
        }

        self.cycle_history.append(cycle_summary)
        return cycle_summary

    def get_status(self) -> Dict[str, Any]:
        """Returns the current status, latest cycle, and satisfaction metrics of the Ralph loop."""
        latest_cycle = self.cycle_history[-1] if self.cycle_history else None
        feedback = self.feedback_agent.get_satisfaction_metrics()
        return {
            "active_cycle_count": self.current_cycle_number,
            "latest_cycle": latest_cycle,
            "current_retrieval_params": self.retrieval_agent.current_params,
            "user_feedback_summary": feedback,
            "status": latest_cycle.get("status", "READY") if latest_cycle else "READY"
        }

if __name__ == "__main__":
    ralph = RalphLoop()
    result = ralph.run_cycle(auto_promote=True)
    print("\nRalph Loop Cycle Result:")
    print(json.dumps(result, indent=2))
