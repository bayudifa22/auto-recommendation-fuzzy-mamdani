import React from 'react';
import { Link } from 'react-router-dom';
import { Cpu, HardDrive, MemoryStick, Battery, Monitor, ShieldCheck, ArrowRight } from 'lucide-react';
import ScoreBadge from './ScoreBadge';

/** Format angka integer ke format mata uang Rupiah */
export function formatRupiah(nominal) {
  if (nominal === undefined || nominal === null) return 'Rp 0';
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    maximumFractionDigits: 0,
  }).format(nominal);
}

export default function LaptopCard({ laptop, ranking, showScore = true }) {
  const {
    id,
    nama_laptop,
    merek,
    harga,
    ram_gb,
    penyimpanan_gb,
    tipe_penyimpanan,
    skor_prosesor,
    gpu,
    ukuran_layar,
    baterai_jam,
    skor_rekomendasi,
    label,
    alasan,
  } = laptop;

  const storageStr = penyimpanan_gb >= 1000 ? `${penyimpanan_gb / 1000} TB` : `${penyimpanan_gb} GB`;

  return (
    <div
      data-testid="laptop-card"
      className="bg-white rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition-all duration-200 overflow-hidden flex flex-col justify-between"
    >
      {/* Header Kartu */}
      <div className="p-5 border-b border-slate-100">
        <div className="flex items-start justify-between gap-3 mb-2">
          <div className="flex items-center gap-2">
            {ranking && (
              <span className="w-7 h-7 rounded-full bg-slate-900 text-white font-mono text-xs font-bold flex items-center justify-center flex-shrink-0">
                #{ranking}
              </span>
            )}
            <span className="px-2.5 py-0.5 rounded-md bg-slate-100 text-slate-700 font-semibold text-xs uppercase tracking-wider">
              {merek}
            </span>
          </div>
          {showScore && skor_rekomendasi !== undefined && (
            <ScoreBadge score={skor_rekomendasi} label={label} size="sm" />
          )}
        </div>

        <h3 className="font-bold text-lg text-slate-900 line-clamp-1 hover:text-indigo-600 transition-colors">
          <Link to={`/laptop/${id}`} state={{ laptopData: laptop }}>
            {nama_laptop}
          </Link>
        </h3>
        <p className="mt-1 text-xl font-extrabold text-indigo-700">
          {formatRupiah(harga)}
        </p>
      </div>

      {/* Grid Spesifikasi Utama */}
      <div className="p-5 grid grid-cols-2 gap-3 bg-slate-50/50 text-xs text-slate-600 border-b border-slate-100">
        <div className="flex items-center gap-2">
          <MemoryStick className="w-4 h-4 text-indigo-500 flex-shrink-0" />
          <span>RAM: <strong className="text-slate-900">{ram_gb} GB</strong></span>
        </div>
        <div className="flex items-center gap-2">
          <HardDrive className="w-4 h-4 text-indigo-500 flex-shrink-0" />
          <span>Penyimpanan: <strong className="text-slate-900">{storageStr} {tipe_penyimpanan}</strong></span>
        </div>
        <div className="flex items-center gap-2">
          <Cpu className="w-4 h-4 text-indigo-500 flex-shrink-0" />
          <span>Prosesor: <strong className="text-slate-900">{skor_prosesor}/10</strong></span>
        </div>
        <div className="flex items-center gap-2">
          <Battery className="w-4 h-4 text-indigo-500 flex-shrink-0" />
          <span>Baterai: <strong className="text-slate-900">~{baterai_jam} Jam</strong></span>
        </div>
        {gpu && (
          <div className="col-span-2 flex items-center gap-2 text-slate-500">
            <Monitor className="w-4 h-4 text-slate-400 flex-shrink-0" />
            <span className="truncate">GPU: {gpu} • Layar {ukuran_layar}"</span>
          </div>
        )}
      </div>

      {/* Alasan & Footer Kartu */}
      <div className="p-5 flex-1 flex flex-col justify-between">
        {alasan ? (
          <div className="mb-4 text-xs text-slate-700 bg-indigo-50/60 border border-indigo-100 rounded-lg p-3 leading-relaxed flex items-start gap-2">
            <ShieldCheck className="w-4 h-4 text-indigo-600 flex-shrink-0 mt-0.5" />
            <span>{alasan}</span>
          </div>
        ) : (
          <div className="mb-4 text-xs text-slate-500">
            Klik detail untuk melihat spesifikasi menyeluruh.
          </div>
        )}

        <Link
          to={`/laptop/${id}`}
          state={{ laptopData: laptop }}
          className="inline-flex items-center justify-center gap-2 w-full py-2.5 px-4 rounded-xl bg-slate-900 hover:bg-indigo-600 text-white text-xs font-semibold transition-colors duration-150"
        >
          Lihat Detail & Perhitungan
          <ArrowRight className="w-3.5 h-3.5" />
        </Link>
      </div>
    </div>
  );
}
