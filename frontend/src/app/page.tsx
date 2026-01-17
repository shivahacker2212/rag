'use client';

import { useState } from 'react';
import TextUpload from '@/components/TextUpload';
import QueryBox from '@/components/QueryBox';
import AnswerPanel from '@/components/AnswerPanel';
import { AnswerResponse } from '@/lib/api';

export default function Home() {
  const [answer, setAnswer] = useState<AnswerResponse | null>(null);

  return (
    <main className="min-h-screen bg-gray-100 py-8">
      <div className="container mx-auto px-4 max-w-6xl">
        <h1 className="text-3xl font-bold text-center mb-8">
          RAG Application
        </h1>
        
        <div className="space-y-6">
          <TextUpload onUpload={() => setAnswer(null)} />
          <QueryBox onAnswer={setAnswer} />
          <AnswerPanel response={answer} />
        </div>
      </div>
    </main>
  );
}

