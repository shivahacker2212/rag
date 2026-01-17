'use client';

import { AnswerResponse } from '@/lib/api';

interface AnswerPanelProps {
  response: AnswerResponse | null;
}

export default function AnswerPanel({ response }: AnswerPanelProps) {
  if (!response) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <p className="text-gray-500">Enter a query to get an answer...</p>
      </div>
    );
  }

  const formatTime = (ms: number) => {
    return ms < 1 ? `${(ms * 1000).toFixed(0)}ms` : `${ms.toFixed(2)}s`;
  };

  return (
    <div className="space-y-6">
      {/* Answer */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-bold mb-4">Answer</h2>
        <div className="prose max-w-none">
          <p className="whitespace-pre-wrap">{response.answer}</p>
        </div>
      </div>

      {/* Citations */}
      {response.citations.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-bold mb-4">Citations</h3>
          <div className="space-y-3">
            {response.citations.map((citation) => (
              <div key={citation.id} className="border-l-4 border-blue-500 pl-4">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-bold text-blue-600">[{citation.id}]</span>
                  <span className="text-sm text-gray-600">
                    {citation.title || citation.source}
                    {citation.section && ` - ${citation.section}`}
                  </span>
                </div>
                <p className="text-sm text-gray-700">{citation.text}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Retrieved Chunks */}
      {response.retrieved_chunks.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-bold mb-4">Retrieved Chunks</h3>
          <div className="space-y-4">
            {response.retrieved_chunks.map((chunk, idx) => (
              <div key={idx} className="border rounded p-3">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm font-medium text-gray-600">
                    {chunk.title || chunk.source}
                    {chunk.section && ` - ${chunk.section}`}
                  </span>
                  <span className="text-xs text-gray-500">
                    Score: {chunk.score.toFixed(3)}
                  </span>
                </div>
                <p className="text-sm text-gray-700">{chunk.text}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Timing & Stats */}
      <div className="bg-gray-50 rounded-lg p-6">
        <h3 className="text-lg font-bold mb-4">Performance Metrics</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div>
            <p className="text-sm text-gray-600">Total Time</p>
            <p className="text-lg font-bold">
              {formatTime(response.timing.total || 0)}
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Retrieval</p>
            <p className="text-lg font-bold">
              {formatTime(response.timing.total_retrieval || 0)}
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-600">LLM Generation</p>
            <p className="text-lg font-bold">
              {formatTime(response.timing.llm_generation || 0)}
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Tokens</p>
            <p className="text-lg font-bold">
              {response.token_estimate.total.toLocaleString()}
            </p>
          </div>
        </div>
        {response.cost_estimate !== undefined && response.cost_estimate > 0 && (
          <div className="mt-4">
            <p className="text-sm text-gray-600">Estimated Cost</p>
            <p className="text-lg font-bold">${response.cost_estimate.toFixed(4)}</p>
          </div>
        )}
      </div>
    </div>
  );
}

