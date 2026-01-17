from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from typing import List, Dict, Any
import os
import uuid

class VectorDB:
    def __init__(self):
        url = os.getenv("QDRANT_URL")
        api_key = os.getenv("QDRANT_API_KEY")
        
        if not url or not api_key:
            raise ValueError("QDRANT_URL and QDRANT_API_KEY must be set")
        
        self.client = QdrantClient(url=url, api_key=api_key)
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME", "rag_documents")
        self.dimension = int(os.getenv("EMBEDDING_DIMENSION", "1536"))
        self._ensure_collection()
    
    def _ensure_collection(self):
        """Create collection if it doesn't exist."""
        try:
            collections = self.client.get_collections().collections
            collection_names = [c.name for c in collections]
            
            if self.collection_name not in collection_names:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.dimension,
                        distance=Distance.COSINE
                    )
                )
        except Exception as e:
            print(f"Error ensuring collection: {e}")
            raise
    
    def upsert_chunks(
        self,
        chunks: List[Dict[str, Any]],
        embeddings: List[List[float]]
    ):
        """Upsert document chunks with embeddings."""
        if not chunks or not embeddings:
            return
        
        points = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            point_id = str(uuid.uuid4())
            point = PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    "text": chunk["text"],
                    "source": chunk["source"],
                    "title": chunk.get("title", ""),
                    "section": chunk.get("section", ""),
                    "position": chunk["position"],
                    "metadata": chunk.get("metadata", {})
                }
            )
            points.append(point)
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
    
    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        score_threshold: float = 0.0
    ) -> List[Dict[str, Any]]:
        """Search for similar chunks using MMR-like diversity."""
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=top_k * 2,  # Get more for diversity
            score_threshold=score_threshold
        )
        
        # Simple MMR: select diverse results
        selected = []
        used_sources = set()
        
        for result in results:
            source = result.payload.get("source", "")
            if len(selected) < top_k:
                if source not in used_sources or len(used_sources) < top_k // 2:
                    selected.append({
                        "text": result.payload["text"],
                        "source": result.payload.get("source", ""),
                        "title": result.payload.get("title", ""),
                        "section": result.payload.get("section", ""),
                        "position": result.payload.get("position", 0),
                        "score": result.score,
                        "metadata": result.payload.get("metadata", {})
                    })
                    used_sources.add(source)
        
        return selected[:top_k]

