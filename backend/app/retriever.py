from app.vector_db import VectorDB
from app.embeddings import EmbeddingService
from typing import List, Dict, Any
import time

class Retriever:
    def __init__(self):
        self.vector_db = VectorDB()
        self.embedding_service = EmbeddingService()
    
    def retrieve(
        self,
        query: str,
        top_k: int = 5
    ) -> tuple[List[Dict[str, Any]], Dict[str, float]]:
        """Retrieve relevant chunks for a query."""
        start_time = time.time()
        
        # Embed query
        query_embedding = self.embedding_service.embed_text(query)
        embedding_time = time.time() - start_time
        
        # Search vector DB
        search_start = time.time()
        chunks = self.vector_db.search(query_embedding, top_k=top_k)
        search_time = time.time() - search_start
        
        timing = {
            "embedding": embedding_time,
            "retrieval": search_time,
            "total_retrieval": time.time() - start_time
        }
        
        return chunks, timing

