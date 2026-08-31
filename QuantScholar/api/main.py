"""
QuantumScholar - FastAPI Application
Exposes endpoints for citation-grounded quantum Q&A, retrieval search, multi-backend circuit simulation, feedback, and Ralph loop control.
"""

import sys
import os
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List

from api.schemas import (
    AskRequest, AskResponse, SourceChunk, GroundednessAudit,
    SearchRequest, SearchResponse,
    CircuitExecutionRequest, CircuitExecutionResponse,
    FeedbackRequest, FeedbackResponse,
    RalphStatusResponse
)
from api.middleware.logging import RequestLoggingMiddleware, logger
from retrieval.service import QuantumRetriever
from llm.service import QuantumLLM
from llm.evaluators.groundedness_eval import GroundednessEvaluator
from llm.evaluators.pedagogy_eval import PedagogyEvaluator
from integrations.qiskit.circuit_runner import QiskitCircuitRunner
from integrations.cirq.cirq_runner import CirqRunner
from integrations.pennylane.pennylane_devices import PennyLaneDeviceManager
from agents.ralph_loop import RalphLoop

app = FastAPI(
    title="QuantumScholar API",
    version="0.1.0",
    description="Citation-grounded, quantum-only AI platform API with multi-backend simulation and Ralph agentic loop."
)

# Add Middleware
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Services Singletons
retriever = QuantumRetriever()
llm = QuantumLLM()
groundedness_evaluator = GroundednessEvaluator()
pedagogy_evaluator = PedagogyEvaluator()
qiskit_runner = QiskitCircuitRunner()
cirq_runner = CirqRunner()
pennylane_manager = PennyLaneDeviceManager()
ralph_loop = RalphLoop()

@app.get("/health", tags=["System"])
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "QuantumScholar",
        "version": "0.1.0",
        "verified_corpus_loaded": len(retriever.bm25_chunks) > 0
    }

@app.post("/ask", response_model=AskResponse, tags=["Quantum Q&A"])
def ask_quantum_scholar(request: AskRequest):
    """
    Main endpoint: Retrieves peer-reviewed quantum chunks and synthesizes a citation-grounded response.
    """
    # 1. Hybrid Retrieval
    chunks = retriever.retrieve(
        query=request.query,
        top_k=request.top_k,
        fusion_strategy=request.fusion_strategy,
        enable_reranking=request.enable_reranking
    )

    # 2. LLM Generation
    gen_result = llm.generate_answer(query=request.query, chunks=chunks)
    answer = gen_result["answer"]

    # 3. Groundedness & Quality Audit
    g_eval = groundedness_evaluator.evaluate(answer, chunks)
    p_eval = pedagogy_evaluator.evaluate(answer)

    audit = GroundednessAudit(
        groundedness_score=g_eval["groundedness_score"],
        clarity_score=p_eval["clarity_score"],
        pedagogy_score=p_eval["pedagogy_score"],
        citation_count=g_eval["citation_count"],
        has_sources_section=g_eval["has_sources_section"],
        is_grounded=g_eval["is_grounded"],
        unsupported_claims=g_eval.get("unsupported_claims", [])
    )

    source_chunks = [SourceChunk(**c) for c in chunks]

    return AskResponse(
        query=request.query,
        answer=answer,
        sources=source_chunks,
        model=gen_result["model"],
        audit=audit
    )

@app.post("/search", response_model=SearchResponse, tags=["Retrieval"])
def search_corpus(request: SearchRequest):
    """Searches quantum papers, books, and docs directly."""
    chunks = retriever.retrieve(
        query=request.query,
        top_k=request.top_k,
        fusion_strategy=request.fusion_strategy
    )
    return SearchResponse(
        query=request.query,
        total_retrieved=len(chunks),
        results=[SourceChunk(**c) for c in chunks]
    )

@app.post("/execute_circuit", response_model=CircuitExecutionResponse, tags=["Quantum Simulator"])
def execute_quantum_circuit(request: CircuitExecutionRequest):
    """Runs circuits across Qiskit Aer, Cirq, or PennyLane."""
    framework = request.framework.lower()
    
    if framework == "qiskit":
        res = qiskit_runner.simulator.simulate_circuit(request.circuit_type, num_qubits=request.num_qubits, shots=request.shots)
        return CircuitExecutionResponse(
            framework="Qiskit Aer",
            circuit_type=request.circuit_type,
            shots=request.shots,
            counts=res["counts"],
            qasm_or_diagram=res.get("qasm", ""),
            success=res.get("success", True)
        )
    elif framework == "cirq":
        if request.circuit_type == "qaoa":
            res = cirq_runner.run_qaoa_cirq(repetitions=request.shots)
        else:
            res = cirq_runner.run_bell_circuit(repetitions=request.shots)
        return CircuitExecutionResponse(
            framework="Google Cirq",
            circuit_type=request.circuit_type,
            shots=request.shots,
            counts=res["counts"],
            qasm_or_diagram=res.get("circuit_diagram", ""),
            success=res.get("success", True)
        )
    elif framework == "pennylane":
        res = pennylane_manager.execute_cross_platform_qnode(circuit_type=request.circuit_type, shots=request.shots)
        return CircuitExecutionResponse(
            framework="PennyLane Multi-Device",
            circuit_type=request.circuit_type,
            shots=request.shots,
            counts=res["qiskit_backend"]["counts"],
            qasm_or_diagram=res["cirq_backend"].get("diagram", ""),
            success=True,
            details=res
        )
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported framework: {request.framework}")

@app.post("/feedback", response_model=FeedbackResponse, tags=["Ralph Feedback"])
def submit_feedback(request: FeedbackRequest):
    """Submits user rating and commentary for the Ralph loop."""
    ralph_loop.feedback_agent.log_feedback(
        query_id=request.query_id,
        query=request.query,
        rating=request.rating,
        feedback_type=request.feedback_type,
        comment=request.user_comment
    )
    return FeedbackResponse(
        status="success",
        message="Feedback recorded. Telemetry ingested by Ralph Feedback Agent."
    )

@app.get("/ralph/status", response_model=RalphStatusResponse, tags=["Ralph Loop"])
def get_ralph_status():
    """Gets current status, metrics, and parameters of the Ralph improvement loop."""
    status_data = ralph_loop.get_status()
    return RalphStatusResponse(**status_data)

@app.post("/ralph/run_cycle", tags=["Ralph Loop"])
def run_ralph_cycle(auto_promote: bool = True):
    """Triggers an autonomous optimization cycle (Collect -> Evaluate -> Diagnose -> Propose -> Experiment -> Promote)."""
    cycle_result = ralph_loop.run_cycle(auto_promote=auto_promote)
    return cycle_result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
