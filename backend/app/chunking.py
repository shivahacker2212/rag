import tiktoken
from typing import List
from app.models import DocumentChunk

class TextChunker:
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 150,
        encoding_name: str = "cl100k_base"
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.encoding = tiktoken.get_encoding(encoding_name)
    
    def chunk_text(
        self,
        text: str,
        source: str = "user_input",
        title: str = "Untitled",
        section: str = None
    ) -> List[DocumentChunk]:
        """Split text into chunks with overlap and metadata."""
        if not text or not text.strip():
            return []
        
        tokens = self.encoding.encode(text)
        if not tokens:
            return []
        
        chunks = []
        
        i = 0
        position = 0
        while i < len(tokens):
            chunk_tokens = tokens[i:i + self.chunk_size]
            chunk_text = self.encoding.decode(chunk_tokens)
            
            chunk = DocumentChunk(
                text=chunk_text,
                source=source,
                title=title,
                section=section,
                position=position,
                metadata={
                    "token_count": len(chunk_tokens),
                    "chunk_index": position
                }
            )
            chunks.append(chunk)
            
            i += self.chunk_size - self.chunk_overlap
            position += 1
        
        return chunks

