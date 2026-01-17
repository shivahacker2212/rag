from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import time
from dotenv import load_dotenv

from app.models import (
    UploadRequest, QueryRequest, AnswerResponse, RetrievedChunk, Citation
)
from app.chunking import TextChunker
from app.embeddings import EmbeddingService
from app.vector_db import VectorDB
from app.retriever import Retriever
from app.reranker import Reranker
from app.llm import LLMService

# Load environment variables
load_dotenv()

app = FastAPI(title="RAG API", version="1.0.0")

# CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services (lazy loading to handle missing env vars gracefully)
chunker = None
embedding_service = None
vector_db = None
retriever = None
reranker = None
llm_service = None

def get_services():
    """Lazy initialization of services."""
    global chunker, embedding_service, vector_db, retriever, reranker, llm_service
    
    if chunker is None:
        chunker = TextChunker(chunk_size=1000, chunk_overlap=150)
    if embedding_service is None:
        embedding_service = EmbeddingService()
    if vector_db is None:
        vector_db = VectorDB()
    if retriever is None:
        retriever = Retriever()
    if reranker is None:
        reranker = Reranker()
    if llm_service is None:
        llm_service = LLMService()
    
    return chunker, embedding_service, vector_db, retriever, reranker, llm_service

@app.get("/")
def root():
    return {"message": "RAG API is running"}

@app.post("/api/upload")
async def upload_document(request: UploadRequest):
    """Upload and process a document."""
    try:
        chunker, embedding_service, vector_db, _, _, _ = get_services()
        
        start_time = time.time()
        
        # Chunk text
        chunks = chunker.chunk_text(
            text=request.text,
            source=request.source or "user_input",
            title=request.title or "Untitled Document"
        )
        
        # Generate embeddings
        texts = [chunk.text for chunk in chunks]
        embeddings = embedding_service.embed_batch(texts)
        
        # Prepare chunks for vector DB
        chunk_dicts = [chunk.dict() for chunk in chunks]
        
        # Upsert to vector DB
        vector_db.upsert_chunks(chunk_dicts, embeddings)
        
        elapsed = time.time() - start_time
        
        return {
            "message": "Document uploaded successfully",
            "chunks_created": len(chunks),
            "processing_time": elapsed
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/query", response_model=AnswerResponse)
async def query(request: QueryRequest):
    """Query the RAG system."""
    try:
        _, _, _, retriever, reranker, llm_service = get_services()
        
        total_start = time.time()
        
        # Retrieve chunks
        retrieved_chunks, retrieval_timing = retriever.retrieve(
            query=request.query,
            top_k=request.top_k
        )
        
        if not retrieved_chunks:
            return AnswerResponse(
                answer="No relevant documents found in the knowledge base.",
                citations=[],
                retrieved_chunks=[],
                timing={"total": time.time() - total_start},
                token_estimate={"input": 0, "output": 0, "total": 0}
            )
        
        # Rerank
        rerank_start = time.time()
        reranked_chunks = reranker.rerank(
            query=request.query,
            documents=retrieved_chunks,
            top_n=request.rerank_top_k
        )
        rerank_time = time.time() - rerank_start
        
        # Generate answer
        llm_result = llm_service.generate_answer(
            query=request.query,
            context_chunks=reranked_chunks
        )
        
        # Format retrieved chunks for response
        formatted_chunks = [
            RetrievedChunk(
                text=chunk["text"],
                source=chunk["source"],
                title=chunk.get("title"),
                section=chunk.get("section"),
                position=chunk.get("position", 0),
                score=chunk.get("rerank_score", chunk.get("score", 0.0)),
                metadata=chunk.get("metadata", {})
            )
            for chunk in reranked_chunks
        ]
        
        # Format citations
        citations = [
            Citation(**citation)
            for citation in llm_result["citations"]
        ]
        
        total_time = time.time() - total_start
        
        timing = {
            **retrieval_timing,
            "reranking": rerank_time,
            **llm_result["timing"],
            "total": total_time
        }
        
        return AnswerResponse(
            answer=llm_result["answer"],
            citations=citations,
            retrieved_chunks=formatted_chunks,
            timing=timing,
            token_estimate=llm_result["token_estimate"],
            cost_estimate=llm_result.get("cost_estimate")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

