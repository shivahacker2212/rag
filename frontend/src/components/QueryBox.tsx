'use client';

import { useState } from 'react';
import { queryRAG, AnswerResponse } from '@/lib/api';

interface QueryBoxProps {
  onAnswer: (response: AnswerResponse) => void;
}

export default function QueryBox({ onAnswer }: QueryBoxProps) {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    try {
      const response = await queryRAG({
        query,
        top_k: 5,
        rerank_top_k: 3
      });
      onAnswer(response);
    } catch (error: any) {
      console.error('Query error:', error);
      alert(`Error: ${error.response?.data?.detail || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <h2 className="text-xl font-bold mb-4">Ask a Question</h2>
      <form onSubmit={handleSubmit}>
        <div className="flex gap-2">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="flex-1 px-4 py-2 border border-gray-300 rounded-md"
            placeholder="Enter your question..."
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading || !query.trim()}
            className="bg-green-600 text-white px-6 py-2 rounded-md hover:bg-green-700 disabled:opacity-50"
          >
            {loading ? 'Searching...' : 'Ask'}
          </button>
        </div>
      </form>
    </div>
  );
}

