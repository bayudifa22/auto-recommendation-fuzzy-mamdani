import React from 'react';
import { AlertCircle, RefreshCw } from 'lucide-react';

export default function ErrorMessage({ message, onRetry }) {
  return (
    <div className="bg-rose-50 border border-rose-200 rounded-xl p-6 text-rose-900 shadow-sm my-6 max-w-2xl mx-auto">
      <div className="flex items-start gap-4">
        <div className="p-2 bg-rose-100 rounded-lg text-rose-600 flex-shrink-0">
          <AlertCircle className="w-6 h-6" />
        </div>
        <div className="flex-1">
          <h3 className="font-bold text-lg text-rose-950">Terjadi Kendala</h3>
          <p className="mt-1 text-sm text-rose-800 leading-relaxed">
            {message || 'Server backend tidak dapat dihubungi. Pastikan server FastAPI aktif di http://localhost:8000.'}
          </p>
          {onRetry && (
            <button
              onClick={onRetry}
              className="mt-4 inline-flex items-center gap-2 px-4 py-2 bg-rose-600 hover:bg-rose-700 text-white rounded-lg text-sm font-semibold transition-colors shadow-sm"
            >
              <RefreshCw className="w-4 h-4" />
              Coba Lagi
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
