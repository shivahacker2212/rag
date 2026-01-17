from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class DocumentChunk(BaseModel):
    text: str
    source: str
    title: Optional[str] = None
    section: Optional[str] = None
    position: int
    metadata: Dict[str, Any] = {}

class UploadRequest(BaseModel):
    text: str
    title: Optional[str] = "Untitled Document"
    source: Optional[str] = "user_input"

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5
    rerank_top_k: int = 3

class RetrievedChunk(BaseModel):
    text: str
    source: str
    title: Optional[str]
    section: Optional[str]
    position: int
    score: float
    metadata: Dict[str, Any] = {}

class Citation(BaseModel):
    id: int
    text: str
    source: str
    title: Optional[str]
    section: Optional[str]

class AnswerResponse(BaseModel):
    answer: str
    citations: List[Citation]
    retrieved_chunks: List[RetrievedChunk]
    timing: Dict[str, float]
    token_estimate: Dict[str, int]
    cost_estimate: Optional[float] = None

