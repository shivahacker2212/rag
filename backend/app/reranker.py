import cohere
import os
from typing import List, Dict, Any

class Reranker:
    def __init__(self):
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            raise ValueError("COHERE_API_KEY not set")
        self.client = cohere.Client(api_key=api_key)
    
    def rerank(
        self,
        query: str,
        documents: List[Dict[str, Any]],
        top_n: int = 3
    ) -> List[Dict[str, Any]]:
        """Rerank documents using Cohere Rerank API."""
        if not documents:
            return []
        
        doc_texts = [doc["text"] for doc in documents]
        
        try:
            results = self.client.rerank(
                model="rerank-english-v3.0",
                query=query,
                documents=doc_texts,
                top_n=min(top_n, len(documents))
            )
            
            reranked = []
            for result in results.results:
                original_doc = documents[result.index]
                reranked.append({
                    **original_doc,
                    "rerank_score": result.relevance_score,
                    "original_score": original_doc.get("score", 0.0)
                })
            
            return reranked
        except Exception as e:
            print(f"Reranking error: {e}")
            # Fallback: return original order
            return documents[:top_n]

