import React from 'react';

/**
 * Komponen ScoreBadge untuk menampilkan skor rekomendasi (0-100) dan label kategorinya
 * dengan variasi warna yang intuitif.
 */
export default function ScoreBadge({ score, label, size = 'md' }) {
  const numScore = typeof score === 'number' ? score : parseFloat(score) || 0;

  // Penentuan skema warna berdasarkan skor
  let colorClasses = 'bg-emerald-50 text-emerald-700 border-emerald-200';
  let badgeClasses = 'bg-emerald-600 text-white';

  if (numScore >= 80) {
    colorClasses = 'bg-emerald-50 text-emerald-800 border-emerald-300';
    badgeClasses = 'bg-emerald-600 text-white';
  } else if (numScore >= 60) {
    colorClasses = 'bg-indigo-50 text-indigo-800 border-indigo-300';
    badgeClasses = 'bg-indigo-600 text-white';
  } else if (numScore >= 40) {
    colorClasses = 'bg-amber-50 text-amber-800 border-amber-300';
    badgeClasses = 'bg-amber-600 text-white';
  } else {
    colorClasses = 'bg-rose-50 text-rose-800 border-rose-300';
    badgeClasses = 'bg-rose-600 text-white';
  }

  const isSmall = size === 'sm';
  const isLarge = size === 'lg';

  return (
    <div className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-full border ${colorClasses}`}>
      <span
        className={`font-black rounded-full flex items-center justify-center font-mono ${
          isSmall
            ? 'text-xs w-6 h-6'
            : isLarge
            ? 'text-base w-10 h-10'
            : 'text-sm w-8 h-8'
        } ${badgeClasses}`}
      >
        {numScore.toFixed(1)}
      </span>
      <span className={`font-semibold ${isSmall ? 'text-xs' : isLarge ? 'text-base' : 'text-sm'}`}>
        {label || (numScore >= 80 ? 'Sangat direkomendasikan' : numScore >= 60 ? 'Direkomendasikan' : numScore >= 40 ? 'Cukup direkomendasikan' : 'Kurang direkomendasikan')}
      </span>
    </div>
  );
}
