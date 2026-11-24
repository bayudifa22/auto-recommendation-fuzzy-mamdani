import React, { useEffect, useState } from 'react';
import { useLocation, Link, useNavigate } from 'react-router-dom';
import { ArrowLeft, AlertTriangle, Sparkles, Filter, RefreshCw } from 'lucide-react';
import LaptopCard from '../components/LaptopCard';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import { api } from '../services/api';

export default function Hasil() {
  const location = useLocation();
  const navigate = useNavigate();

  const stateData = location.state?.rekomendasiData;
  const inputQuery = location.state?.inputQuery;

  const [data, setData] = useState(stateData || null);
  const [loading, setLoading] = useState(!stateData);
  const [error, setError] = useState(null);

  // Jika pengguna langsung membuka URL /hasil tanpa submit form sebelumnya,
  // jalankan rekomendasi default agar halaman tetap interaktif dan tidak kosong
  useEffect(() => {
    if (!data) {
      setLoading(true);
      api.getRecommendations({
        anggaran_maks: 10000000,
        kebutuhan: 'kuliah_umum',
        include_detail: true,
      })
        .then((res) => {
          setData(res);
        })
        .catch((err) => {
          setError(err.message || 'Gagal memuat rekomendasi.');
        })
        .finally(() => {
          setLoading(false);
        });
    }
  }, [data]);

  if (loading) {
    return <LoadingSpinner text="Menghitung skor rekomendasi Fuzzy Mamdani..." />;
  }

  if (error) {
    return <ErrorMessage message={error} onRetry={() => navigate('/rekomendasi')} />;
  }

  const hasilList = data?.hasil || [];
  const pesanFallback = data?.pesan;

  return (
    <div className="space-y-8 py-6">
      {/* Header Halaman Hasil */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-slate-200">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-indigo-600 mb-1">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Hasil Penilaian Fuzzy Mamdani</span>
          </div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-slate-900 tracking-tight">
            Rekomendasi Laptop Terbaik
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            Ditemukan {hasilList.length} laptop terbaik yang diurutkan dari skor rekomendasi tertinggi.
          </p>
        </div>

        <Link
          to="/rekomendasi"
          className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl border border-slate-300 bg-white hover:bg-slate-50 text-slate-700 text-xs font-bold shadow-sm transition-colors self-start md:self-auto"
        >
          <ArrowLeft className="w-4 h-4" />
          Ubah Preferensi & Anggaran
        </Link>
      </div>

      {/* Ringkasan Parameter Pencarian */}
      {inputQuery && (
        <div className="bg-white p-4 rounded-2xl border border-slate-200 flex flex-wrap items-center gap-3 text-xs text-slate-600 shadow-sm">
          <span className="font-bold text-slate-900 flex items-center gap-1">
            <Filter className="w-3.5 h-3.5 text-indigo-600" />
            Filter Terpilih:
          </span>
          <span className="px-2.5 py-1 rounded-md bg-slate-100 font-medium">
            Anggaran: <strong className="text-indigo-700">{inputQuery.anggaranFormatted}</strong>
          </span>
          <span className="px-2.5 py-1 rounded-md bg-slate-100 font-medium">
            Kebutuhan: <strong className="text-slate-800 capitalize">{inputQuery.kebutuhan.replace('_', ' ')}</strong>
          </span>
          {inputQuery.ram_min_gb && (
            <span className="px-2.5 py-1 rounded-md bg-slate-100 font-medium">
              RAM min: <strong>{inputQuery.ram_min_gb} GB</strong>
            </span>
          )}
          {inputQuery.penyimpanan_min_gb && (
            <span className="px-2.5 py-1 rounded-md bg-slate-100 font-medium">
              SSD min: <strong>{inputQuery.penyimpanan_min_gb} GB</strong>
            </span>
          )}
        </div>
      )}

      {/* Pesan Peringatan Fallback jika ada */}
      {pesanFallback && (
        <div className="bg-amber-50 border border-amber-200 rounded-2xl p-5 text-amber-900 text-xs md:text-sm flex items-start gap-3 shadow-sm">
          <AlertTriangle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
          <div>
            <h4 className="font-bold text-amber-950 mb-1">Pemberitahuan Preferensi Ketat</h4>
            <p className="leading-relaxed text-amber-900">{pesanFallback}</p>
          </div>
        </div>
      )}

      {/* Grid Kartu Laptop */}
      {hasilList.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {hasilList.map((laptop, index) => (
            <LaptopCard
              key={laptop.id}
              laptop={laptop}
              ranking={index + 1}
              showScore={true}
            />
          ))}
        </div>
      ) : (
        <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center max-w-lg mx-auto">
          <p className="text-slate-600 text-sm mb-4">Tidak ada data laptop yang dapat ditampilkan.</p>
          <Link
            to="/rekomendasi"
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-indigo-600 text-white text-xs font-bold"
          >
            Kembali ke Form
          </Link>
        </div>
      )}
    </div>
  );
}
