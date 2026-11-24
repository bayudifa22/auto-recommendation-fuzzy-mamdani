import React, { useState } from 'react';
import { ChevronDown, ChevronUp, Calculator, CheckCircle2, Info } from 'lucide-react';

export default function FuzzyDetailPanel({ detailFuzzy, skorRekomendasi, label }) {
  const [isOpen, setIsOpen] = useState(true);

  if (!detailFuzzy) {
    return (
      <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 text-xs text-slate-500">
        Rincian perhitungan fuzzy tidak tersedia atau tidak diaktifkan pada pencarian ini.
      </div>
    );
  }

  const { inputs_ternormalisasi, derajat_keanggotaan, aturan_aktif } = detailFuzzy;

  return (
    <div className="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm">
      {/* Header Panel Toggle */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full px-6 py-4 flex items-center justify-between bg-slate-50 hover:bg-slate-100 transition-colors text-left"
      >
        <div className="flex items-center gap-3">
          <div className="p-2 bg-indigo-100 rounded-lg text-indigo-700">
            <Calculator className="w-5 h-5" />
          </div>
          <div>
            <h4 className="font-bold text-slate-900 text-sm md:text-base">
              Rincian Perhitungan Fuzzy Mamdani
            </h4>
            <p className="text-xs text-slate-500">
              Transparansi langkah perhitungan untuk verifikasi dosen/penguji
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2 text-slate-600 text-xs font-semibold">
          <span>{isOpen ? 'Tutup Rincian' : 'Buka Rincian'}</span>
          {isOpen ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </div>
      </button>

      {/* Konten Rincian */}
      {isOpen && (
        <div className="p-6 space-y-6 text-xs md:text-sm text-slate-700 border-t border-slate-100">
          {/* 1. Nilai Masukan */}
          <div>
            <h5 className="font-bold text-slate-900 uppercase tracking-wider text-xs mb-3 flex items-center gap-2">
              <span className="w-5 h-5 rounded-full bg-indigo-600 text-white flex items-center justify-center font-mono text-[10px]">1</span>
              Nilai Input & Rasio
            </h5>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              {inputs_ternormalisasi && Object.entries(inputs_ternormalisasi).map(([key, val]) => (
                <div key={key} className="bg-slate-50 p-3 rounded-xl border border-slate-200">
                  <div className="text-[11px] text-slate-500 font-mono uppercase">{key}</div>
                  <div className="text-base font-bold text-slate-900 font-mono mt-0.5">{val}</div>
                </div>
              ))}
            </div>
          </div>

          {/* 2. Derajat Keanggotaan (Fuzzifikasi) */}
          <div>
            <h5 className="font-bold text-slate-900 uppercase tracking-wider text-xs mb-3 flex items-center gap-2">
              <span className="w-5 h-5 rounded-full bg-indigo-600 text-white flex items-center justify-center font-mono text-[10px]">2</span>
              Derajat Keanggotaan Tiap Himpunan (Fuzzifikasi)
            </h5>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {derajat_keanggotaan && Object.entries(derajat_keanggotaan).map(([varName, sets]) => (
                <div key={varName} className="bg-slate-50/70 p-4 rounded-xl border border-slate-200">
                  <div className="font-semibold text-slate-900 mb-2 font-mono text-xs">
                    Variabel: {varName}
                  </div>
                  <div className="space-y-2">
                    {Object.entries(sets).map(([setName, mu]) => (
                      <div key={setName} className="flex items-center justify-between text-xs">
                        <span className="text-slate-600">{setName}:</span>
                        <div className="flex items-center gap-2 w-36">
                          <div className="flex-1 bg-slate-200 rounded-full h-2 overflow-hidden">
                            <div
                              className="bg-indigo-600 h-full rounded-full transition-all duration-300"
                              style={{ width: `${Math.min(mu * 100, 100)}%` }}
                            ></div>
                          </div>
                          <span className="font-mono font-bold w-12 text-right">{mu.toFixed(4)}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* 3. Aturan Fuzzy Aktif (Inferensi AND) */}
          <div>
            <h5 className="font-bold text-slate-900 uppercase tracking-wider text-xs mb-3 flex items-center gap-2">
              <span className="w-5 h-5 rounded-full bg-indigo-600 text-white flex items-center justify-center font-mono text-[10px]">3</span>
              Aturan Fuzzy yang Aktif (Alpha-Predikat &gt; 0)
            </h5>
            {aturan_aktif && aturan_aktif.length > 0 ? (
              <div className="overflow-x-auto rounded-xl border border-slate-200">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-100 text-slate-700 font-semibold uppercase tracking-wider text-[10px]">
                    <tr>
                      <th className="p-3">ID Aturan</th>
                      <th className="p-3">Pernyataan Aturan</th>
                      <th className="p-3 text-center">Output</th>
                      <th className="p-3 text-right">Nilai α-Predikat (min)</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-200 bg-white">
                    {aturan_aktif.map((rule) => (
                      <tr key={rule.id} className="hover:bg-slate-50 transition-colors">
                        <td className="p-3 font-mono font-bold text-indigo-700">{rule.id}</td>
                        <td className="p-3 text-slate-800">{rule.nama}</td>
                        <td className="p-3 text-center">
                          <span className={`px-2 py-0.5 rounded-full font-bold text-[10px] ${
                            rule.output === 'Tinggi'
                              ? 'bg-emerald-100 text-emerald-800'
                              : rule.output === 'Sedang'
                              ? 'bg-indigo-100 text-indigo-800'
                              : 'bg-rose-100 text-rose-800'
                          }`}>
                            {rule.output}
                          </span>
                        </td>
                        <td className="p-3 text-right font-mono font-bold text-slate-900">
                          {rule.alpha.toFixed(4)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p className="text-xs text-slate-500 italic">Tidak ada aturan yang aktif dengan alpha &gt; 0.</p>
            )}
          </div>

          {/* 4. Agregasi & Defuzzifikasi Centroid */}
          <div className="bg-indigo-50/70 p-4 rounded-xl border border-indigo-200">
            <h5 className="font-bold text-indigo-950 uppercase tracking-wider text-xs mb-2 flex items-center gap-2">
              <span className="w-5 h-5 rounded-full bg-indigo-700 text-white flex items-center justify-center font-mono text-[10px]">4</span>
              Agregasi Max & Defuzzifikasi Centroid
            </h5>
            <p className="text-xs text-indigo-900 leading-relaxed">
              Output tiap aturan aktif dipotong (clipping) setinggi derajat α-predikatnya, kemudian digabungkan dengan fungsi maksimum (MAX).
              Skor akhir dihitung menggunakan titik berat pusat massa (Center of Gravity):
            </p>
            <div className="my-3 p-3 bg-white rounded-lg border border-indigo-100 font-mono text-center text-xs md:text-sm font-bold text-indigo-900">
              z* = Σ ( μ(z) · z ) / Σ μ(z) = <span className="text-indigo-600 text-base">{skorRekomendasi?.toFixed(1)}</span> (0 - 100)
            </div>
            <div className="flex items-center gap-2 text-xs font-semibold text-indigo-950">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span>Label Kategori: <strong>{label}</strong></span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
