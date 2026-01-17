# Quick Start Guide

## Prerequisites

1. Python 3.9+ installed
2. Node.js 18+ installed
3. API keys for:
   - Qdrant (https://cloud.qdrant.io)
   - OpenAI (https://platform.openai.com)
   - Cohere (https://cohere.com)
   - Groq (https://groq.com) - optional, can use OpenAI

## Step 1: Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_COLLECTION_NAME=rag_documents
OPENAI_API_KEY=your-openai-api-key
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSION=1536
COHERE_API_KEY=your-cohere-api-key
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=llama-3.1-70b-versatile
LLM_PROVIDER=groq
PORT=8000
CORS_ORIGINS=http://localhost:3000
EOF

# Start backend server
uvicorn app.main:app --reload
```

Backend will run on `http://localhost:8000`

## Step 2: Frontend Setup

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start frontend server
npm run dev
```

Frontend will run on `http://localhost:3000`

## Step 3: Test the Application

1. Open `http://localhost:3000` in your browser
2. Upload a document by pasting text in the "Upload Document" section
3. Ask a question in the "Ask a Question" section
4. View the answer with citations

## Troubleshooting

### Backend Issues

- **Import errors**: Make sure virtual environment is activated and dependencies are installed
- **API key errors**: Check that all API keys are set in `.env` file
- **Qdrant connection errors**: Verify QDRANT_URL and QDRANT_API_KEY are correct

### Frontend Issues

- **API connection errors**: Check that `NEXT_PUBLIC_API_URL` matches your backend URL
- **Build errors**: Run `npm install` again to ensure all dependencies are installed
- **TypeScript errors**: Check that all types are properly imported

## Next Steps

- Deploy backend to Railway/Render
- Deploy frontend to Vercel
- Add more documents to the knowledge base
- Test with various queries

