import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface UploadRequest {
  text: string;
  title?: string;
  source?: string;
}

export interface QueryRequest {
  query: string;
  top_k?: number;
  rerank_top_k?: number;
}

export interface Citation {
  id: number;
  text: string;
  source: string;
  title?: string;
  section?: string;
}

export interface RetrievedChunk {
  text: string;
  source: string;
  title?: string;
  section?: string;
  position: number;
  score: number;
  metadata: Record<string, any>;
}

export interface AnswerResponse {
  answer: string;
  citations: Citation[];
  retrieved_chunks: RetrievedChunk[];
  timing: Record<string, number>;
  token_estimate: {
    input: number;
    output: number;
    total: number;
  };
  cost_estimate?: number;
}

export const uploadDocument = async (data: UploadRequest) => {
  const response = await axios.post(`${API_URL}/api/upload`, data);
  return response.data;
};

export const queryRAG = async (data: QueryRequest): Promise<AnswerResponse> => {
  const response = await axios.post(`${API_URL}/api/query`, data);
  return response.data;
};

