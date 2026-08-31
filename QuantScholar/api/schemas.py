"""
QuantumScholar - Pydantic API Schemas
Defines request and response data models for all endpoints.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class AskRequest(BaseModel):
    query: str = Field(..., description="Quantum computing question", example="How does Shor's algorithm find prime factors?")
    top_k: int = Field(5, ge=1, le=20, description="Number of source chunks to retrieve")
    enable_reranking: bool = Field(True, description="Whether to apply cross-encoder reranking")
    fusion_strategy: str = Field("reciprocal_rank_fusion", description="Fusion strategy: reciprocal_rank_fusion or weighted_score_fusion")

class SourceChunk(BaseModel):
    chunk_id: str
    title: str
    authors: List[str]
    year: int
    venue: str
    url: str
    doc_type: str
    citation_tag: str
    content: str
    score: Optional[float] = None
    rerank_score: Optional[float] = None

class GroundednessAudit(BaseModel):
    groundedness_score: float
    clarity_score: float
    pedagogy_score: float
    citation_count: int
    has_sources_section: bool
    is_grounded: bool
    unsupported_claims: List[str] = []

class AskResponse(BaseModel):
    query: str
    answer: str
    sources: List[SourceChunk]
    model: str
    audit: GroundednessAudit

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    fusion_strategy: str = "reciprocal_rank_fusion"

class SearchResponse(BaseModel):
    query: str
    total_retrieved: int
    results: List[SourceChunk]

class CircuitExecutionRequest(BaseModel):
    framework: str = Field("qiskit", description="qiskit, cirq, or pennylane")
    circuit_type: str = Field("bell", description="bell, ghz, qaoa, or superposition")
    shots: int = Field(1000, ge=1, le=10000)
    num_qubits: int = Field(2, ge=1, le=10)

class CircuitExecutionResponse(BaseModel):
    framework: str
    circuit_type: str
    shots: int
    counts: Dict[str, int]
    qasm_or_diagram: Optional[str] = None
    success: bool
    details: Optional[Dict[str, Any]] = None

class FeedbackRequest(BaseModel):
    query_id: str
    query: str
    rating: int = Field(..., ge=1, le=5)
    feedback_type: str = Field("thumbs_up", description="thumbs_up or thumbs_down")
    user_comment: str = ""

class FeedbackResponse(BaseModel):
    status: str
    message: str

class RalphStatusResponse(BaseModel):
    active_cycle_count: int
    latest_cycle: Optional[Dict[str, Any]] = None
    current_retrieval_params: Dict[str, Any]
    user_feedback_summary: Dict[str, Any]
    status: str
