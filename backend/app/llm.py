import os
import time
import re
from typing import List, Dict, Any

class LLMService:
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "groq")
        
        if self.provider == "groq":
            from groq import Groq
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY not set")
            self.client = Groq(api_key=api_key)
            self.model = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")
        else:
            from openai import OpenAI
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not set")
            self.client = OpenAI(api_key=api_key)
            self.model = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
    
    def generate_answer(
        self,
        query: str,
        context_chunks: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate answer with citations."""
        context_text = "\n\n".join([
            f"[{i+1}] {chunk['text']}"
            for i, chunk in enumerate(context_chunks)
        ])
        
        prompt = f"""You are a helpful assistant that answers questions based on the provided context. 
Always cite your sources using [1], [2], etc. when referencing information from the context.

Context:
{context_text}

Question: {query}

Answer the question based on the context above. Include inline citations like [1], [2] when referencing specific information. 
If the context doesn't contain enough information to answer, say "I don't have enough information to answer this question based on the provided context."

Answer:"""
        
        start_time = time.time()
        
        try:
            if self.provider == "groq":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that provides accurate answers with citations."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.1
                )
            else:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that provides accurate answers with citations."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.1
                )
            
            answer = response.choices[0].message.content
            if not answer:
                answer = "No answer generated."
            elapsed = time.time() - start_time
            
            # Extract citations from answer
            citation_ids = [int(x) for x in re.findall(r'\[(\d+)\]', answer) if x.isdigit()]
            citations = [
                {
                    "id": cid,
                    "text": context_chunks[cid-1]["text"][:200] + "...",
                    "source": context_chunks[cid-1]["source"],
                    "title": context_chunks[cid-1].get("title", ""),
                    "section": context_chunks[cid-1].get("section", "")
                }
                for cid in set(citation_ids) if 1 <= cid <= len(context_chunks)
            ]
            
            # Estimate tokens (rough)
            input_tokens = len(prompt.split()) * 1.3  # rough estimate
            output_tokens = len(answer.split()) * 1.3
            
            return {
                "answer": answer,
                "citations": citations,
                "timing": {"llm_generation": elapsed},
                "token_estimate": {
                    "input": int(input_tokens),
                    "output": int(output_tokens),
                    "total": int(input_tokens + output_tokens)
                },
                "cost_estimate": self._estimate_cost(input_tokens, output_tokens)
            }
        except Exception as e:
            return {
                "answer": f"Error generating answer: {str(e)}",
                "citations": [],
                "timing": {"llm_generation": 0},
                "token_estimate": {"input": 0, "output": 0, "total": 0},
                "cost_estimate": 0.0
            }
    
    def _estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Rough cost estimate."""
        if self.provider == "groq":
            # Groq is free tier, so $0
            return 0.0
        else:
            # OpenAI GPT-4 Turbo pricing (rough)
            return (input_tokens / 1000 * 0.01) + (output_tokens / 1000 * 0.03)

