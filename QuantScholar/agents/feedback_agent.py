"""
QuantumScholar - Ralph Loop: Feedback Agent
Ingests live user feedback, logs ratings, and computes user satisfaction metrics.
"""

import json
from pathlib import Path
from typing import List, Dict, Any

class FeedbackAgent:
    """Agent that monitors user feedback telemetry to guide Ralph loop cycles."""

    def __init__(self, feedback_log_path: str = "evaluation/datasets/user_feedback_logs.jsonl"):
        self.feedback_log_path = Path(feedback_log_path)

    def log_feedback(self, query_id: str, query: str, rating: int, feedback_type: str, comment: str = ""):
        """Appends user feedback record to the log."""
        self.feedback_log_path.parent.mkdir(parents=True, exist_ok=True)
        record = {
            "query_id": query_id,
            "query": query,
            "rating": rating,
            "feedback_type": feedback_type,
            "user_comment": comment
        }
        with open(self.feedback_log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def get_satisfaction_metrics(self) -> Dict[str, Any]:
        """Calculates mean rating, positive ratio, and feedback volume."""
        if not self.feedback_log_path.exists():
            return {"mean_rating": 5.0, "total_feedback_count": 0, "positive_ratio": 1.0}

        records = []
        with open(self.feedback_log_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        records.append(json.loads(line))
                    except Exception:
                        pass

        if not records:
            return {"mean_rating": 5.0, "total_feedback_count": 0, "positive_ratio": 1.0}

        ratings = [r.get("rating", 5) for r in records]
        thumbs_up = sum(1 for r in records if r.get("feedback_type") == "thumbs_up" or r.get("rating", 0) >= 4)

        return {
            "mean_rating": round(float(sum(ratings) / len(ratings)), 2),
            "total_feedback_count": len(records),
            "positive_ratio": round(float(thumbs_up / len(records)), 2),
            "recent_feedback": records[-5:]
        }
