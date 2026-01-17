'use client';

import { useState } from 'react';
import { uploadDocument } from '@/lib/api';

export default function TextUpload({ onUpload }: { onUpload: () => void }) {
  const [text, setText] = useState('');
  const [title, setTitle] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!text.trim()) {
      setMessage('Please enter some text');
      return;
    }

    setLoading(true);
    setMessage('');

    try {
      await uploadDocument({
        text,
        title: title || 'Untitled Document',
        source: 'user_input'
      });
      setMessage('Document uploaded successfully!');
      setText('');
      setTitle('');
      onUpload();
    } catch (error: any) {
      setMessage(`Error: ${error.response?.data?.detail || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <h2 className="text-xl font-bold mb-4">Upload Document</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-sm font-medium mb-2">Title (optional)</label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md"
            placeholder="Document title"
          />
        </div>
        <div className="mb-4">
          <label className="block text-sm font-medium mb-2">Text Content</label>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            rows={8}
            className="w-full px-3 py-2 border border-gray-300 rounded-md"
            placeholder="Paste or type your document text here..."
            required
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Uploading...' : 'Upload Document'}
        </button>
        {message && (
          <p className={`mt-2 text-sm ${message.includes('Error') ? 'text-red-600' : 'text-green-600'}`}>
            {message}
          </p>
        )}
      </form>
    </div>
  );
}

