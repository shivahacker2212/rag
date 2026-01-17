# RAG Application - Mini RAG

A Retrieval Augmented Generation (RAG) application that allows users to upload documents, query them, and get AI-generated answers with citations.

## Architecture

```
┌─────────────┐
│   Frontend  │ (Next.js)
│  (Vercel)   │
└──────┬──────┘
       │ HTTP
       ▼
┌─────────────┐
│   Backend   │ (FastAPI)
│  (Railway)  │
└──────┬──────┘
       │
       ├──► Qdrant (Vector DB)
       ├──► OpenAI (Embeddings)
       ├──► Cohere (Reranker)
       └──► Groq/OpenAI (LLM)
```

## Components

### 1. Vector Database (Qdrant)
- **Collection**: `rag_documents`
- **Dimension**: 1536 (OpenAI text-embedding-3-small)
- **Distance**: Cosine
- **Upsert Strategy**: Batch upsert with UUIDs

### 2. Embeddings & Chunking
- **Model**: OpenAI `text-embedding-3-small`
- **Chunk Size**: 1000 tokens
- **Overlap**: 150 tokens (15%)
- **Metadata**: source, title, section, position, token_count

### 3. Retriever + Reranker
- **Retrieval**: Top-k with MMR-like diversity (top 5)
- **Reranker**: Cohere Rerank v3.0
- **Rerank Top-k**: 3 chunks

### 4. LLM & Answering
- **Provider**: Groq (Llama 3.1 70B) or OpenAI
- **Citations**: Inline [1], [2] format
- **Fallback**: Graceful handling of no-answer cases

### 5. Frontend
- **Framework**: Next.js 14
- **Styling**: Tailwind CSS
- **Features**: Text upload, query box, answer with citations, timing/metrics

## Setup

### Prerequisites

- Python 3.9+
- Node.js 18+
- API keys for: Qdrant, OpenAI, Cohere, Groq (optional)

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your API keys:
# - QDRANT_URL and QDRANT_API_KEY
# - OPENAI_API_KEY
# - COHERE_API_KEY
# - GROQ_API_KEY (optional, can use OpenAI for LLM)
```

5. Run the server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
# Create .env.local file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

4. Run the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## API Keys Required

1. **Qdrant**: Sign up at https://cloud.qdrant.io (free tier available)
2. **OpenAI**: Get API key from https://platform.openai.com
3. **Cohere**: Sign up at https://cohere.com (free tier available)
4. **Groq**: Sign up at https://groq.com (optional, can use OpenAI for LLM)

## API Endpoints

### POST `/api/upload`
Upload a document to the vector database.

**Request Body:**
```json
{
  "text": "Your document text here...",
  "title": "Document Title (optional)",
  "source": "user_input (optional)"
}
```

### POST `/api/query`
Query the RAG system.

**Request Body:**
```json
{
  "query": "Your question here",
  "top_k": 5,
  "rerank_top_k": 3
}
```

**Response:**
```json
{
  "answer": "Generated answer with citations [1], [2]...",
  "citations": [...],
  "retrieved_chunks": [...],
  "timing": {...},
  "token_estimate": {...},
  "cost_estimate": 0.0
}
```

## Deployment

### Backend (Railway/Render)

1. Connect your GitHub repo to Railway/Render
2. Set environment variables in the platform dashboard
3. Deploy

**Environment Variables to Set:**
- All variables from `.env.example`

### Frontend (Vercel)

1. Import project from GitHub to Vercel
2. Set `NEXT_PUBLIC_API_URL` to your backend URL
3. Deploy

## Evaluation

### Sample Q/A Pairs

1. **Q**: "What is the main topic of the document?"
   **A**: [Answer with citations]

2. **Q**: "Summarize the key points."
   **A**: [Answer with citations]

3. **Q**: "What are the specific details mentioned?"
   **A**: [Answer with citations]

4. **Q**: "Explain the process described."
   **A**: [Answer with citations]

5. **Q**: "What conclusions are drawn?"
   **A**: [Answer with citations]

## Remarks

- **Provider Limits**: 
  - Groq has rate limits on free tier (30 requests/minute)
  - Cohere free tier: 100 requests/minute
  - Qdrant free tier: 1GB storage

- **Trade-offs**: 
  - Using smaller embedding model (`text-embedding-3-small`) for cost efficiency
  - Simple MMR implementation for diversity (could be improved)
  - Token estimation is rough (not exact)

- **Next Steps**: 
  - Add document persistence and management
  - Implement better MMR algorithm
  - Add user authentication
  - Support file uploads (PDF, DOCX)
  - Add evaluation metrics dashboard
  - Implement streaming responses
  - Add conversation history

## Project Structure

```
rag/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI application
│   │   ├── models.py        # Pydantic models
│   │   ├── chunking.py      # Text chunking logic
│   │   ├── embeddings.py    # Embedding service
│   │   ├── vector_db.py     # Qdrant integration
│   │   ├── retriever.py     # Retrieval logic
│   │   ├── reranker.py      # Cohere reranking
│   │   └── llm.py           # LLM service
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx
│   │   │   ├── layout.tsx
│   │   │   └── globals.css
│   │   ├── components/
│   │   │   ├── TextUpload.tsx
│   │   │   ├── QueryBox.tsx
│   │   │   └── AnswerPanel.tsx
│   │   └── lib/
│   │       └── api.ts
│   ├── package.json
│   └── next.config.js
└── README.md
```

## License

MIT

# rag
