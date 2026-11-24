import React from 'react';

export default function LoadingSpinner({ text = 'Sedang memproses perhitungan Fuzzy Mamdani...' }) {
  return (
    <div className="flex flex-col items-center justify-center py-12 px-4 text-center">
      <div className="relative w-16 h-16">
        <div className="w-16 h-16 rounded-full border-4 border-indigo-200 border-t-indigo-600 animate-spin"></div>
        <div className="absolute inset-0 flex items-center justify-center font-mono text-xs font-bold text-indigo-600">
          μ(z)
        </div>
      </div>
      <p className="mt-4 text-base font-medium text-slate-700">{text}</p>
      <p className="mt-1 text-xs text-slate-500">Mengevaluasi keanggotaan fuzzy, aturan implikasi, dan titik centroid...</p>
    </div>
  );
}
