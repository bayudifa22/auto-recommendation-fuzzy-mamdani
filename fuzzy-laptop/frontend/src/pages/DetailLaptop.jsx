import React, { useEffect, useState } from 'react';
import { useParams, useLocation, Link, useNavigate } from 'react-router-dom';
import {
  ArrowLeft,
  Cpu,
  HardDrive,
  MemoryStick,
  Battery,
  Monitor,
  Scale,
  Calendar,
  Database,
  Tag,
  ShieldCheck,
} from 'lucide-react';
import { api } from '../services/api';
import { formatRupiah } from '../components/LaptopCard';
import ScoreBadge from '../components/ScoreBadge';
import FuzzyDetailPanel from '../components/FuzzyDetailPanel';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';

export default function DetailLaptop() {
  const { id } = useParams();
  const location = useLocation();
  const navigate = useNavigate();

  const stateLaptop = location.state?.laptopData;

  const [laptop, setLaptop] = useState(stateLaptop || null);
  const [loading, setLoading] = useState(!stateLaptop);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Selalu sinkronkan dengan endpoint laptop untuk menjamin data mutakhir
    api.getLaptopById(id)
      .then((data) => {
        // Gabungkan data dasar dari backend dengan detail fuzzy dari alur rekomendasi jika ada
        setLaptop((prev) => ({
          ...data,
          ...(prev?.detail_fuzzy ? { detail_fuzzy: prev.detail_fuzzy } : {}),
          ...(prev?.skor_rekomendasi !== undefined ? { skor_rekomendasi: prev.skor_rekomendasi } : {}),
          ...(prev?.label ? { label: prev.label } : {}),
          ...(prev?.alasan ? { alasan: prev.alasan } : {}),
        }));
      })
      .catch((err) => {
        if (!stateLaptop) {
          setError(err.message || 'Laptop tidak ditemukan.');
        }
      })
      .finally(() => {
        setLoading(false);
      });
  }, [id, stateLaptop]);

  if (loading) {
    return <LoadingSpinner text="Memuat spesifikasi laptop..." />;
  }

  if (error || !laptop) {
    return <ErrorMessage message={error || 'Data laptop tidak ditemukan.'} onRetry={() => navigate(-1)} />;
  }

  const storageStr =
    laptop.penyimpanan_gb >= 1000
      ? `${laptop.penyimpanan_gb / 1000} TB`
      : `${laptop.penyimpanan_gb} GB`;

  return (
    <div className="max-w-4xl mx-auto py-8 space-y-8">
      {/* Tombol Kembali */}
      <button
        onClick={() => navigate(-1)}
        className="inline-flex items-center gap-2 text-xs font-bold text-slate-600 hover:text-indigo-600 transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        Kembali ke Halaman Sebelumnya
      </button>

      {/* Header Detail Laptop */}
      <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-10 shadow-sm space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
          <div>
            <span className="px-3 py-1 rounded-md bg-indigo-50 text-indigo-700 text-xs font-bold uppercase tracking-wider">
              {laptop.merek}
            </span>
            <h1 className="mt-2 text-2xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
              {laptop.nama_laptop}
            </h1>
            <p className="mt-2 text-2xl sm:text-3xl font-black text-indigo-700">
              {formatRupiah(laptop.harga)}
            </p>
          </div>

          {laptop.skor_rekomendasi !== undefined && (
            <div className="flex flex-col items-start sm:items-end gap-1">
              <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                Hasil Inferensi Fuzzy
              </span>
              <ScoreBadge score={laptop.skor_rekomendasi} label={laptop.label} size="lg" />
            </div>
          )}
        </div>

        {/* Alasan Rekomendasi jika ada */}
        {laptop.alasan && (
          <div className="p-4 rounded-2xl bg-indigo-50 border border-indigo-100 flex items-start gap-3">
            <ShieldCheck className="w-5 h-5 text-indigo-600 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="font-bold text-indigo-950 text-xs uppercase tracking-wider mb-0.5">
                Alasan Rekomendasi Sistem
              </h4>
              <p className="text-xs sm:text-sm text-indigo-900 leading-relaxed">
                {laptop.alasan}
              </p>
            </div>
          </div>
        )}

        {/* Grid Spesifikasi Teknis Lengkap */}
        <div className="pt-4 border-t border-slate-100">
          <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider mb-4">
            Spesifikasi Teknis
          </h3>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 text-xs">
            <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200">
              <span className="text-slate-500 flex items-center gap-1.5 mb-1">
                <MemoryStick className="w-4 h-4 text-indigo-600" />
                Kapasitas RAM
              </span>
              <span className="font-bold text-slate-900 text-sm">{laptop.ram_gb} GB</span>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200">
              <span className="text-slate-500 flex items-center gap-1.5 mb-1">
                <HardDrive className="w-4 h-4 text-indigo-600" />
                Penyimpanan
              </span>
              <span className="font-bold text-slate-900 text-sm">{storageStr} {laptop.tipe_penyimpanan}</span>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200">
              <span className="text-slate-500 flex items-center gap-1.5 mb-1">
                <Cpu className="w-4 h-4 text-indigo-600" />
                Skor Prosesor
              </span>
              <span className="font-bold text-slate-900 text-sm">{laptop.skor_prosesor} / 10</span>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200">
              <span className="text-slate-500 flex items-center gap-1.5 mb-1">
                <Monitor className="w-4 h-4 text-indigo-600" />
                GPU / Kartu Grafis
              </span>
              <span className="font-bold text-slate-900 text-sm">{laptop.gpu || '-'}</span>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200">
              <span className="text-slate-500 flex items-center gap-1.5 mb-1">
                <Monitor className="w-4 h-4 text-indigo-600" />
                Ukuran Layar
              </span>
              <span className="font-bold text-slate-900 text-sm">{laptop.ukuran_layar} Inci</span>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200">
              <span className="text-slate-500 flex items-center gap-1.5 mb-1">
                <Scale className="w-4 h-4 text-indigo-600" />
                Bobot Laptop
              </span>
              <span className="font-bold text-slate-900 text-sm">{laptop.berat_kg} kg</span>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200">
              <span className="text-slate-500 flex items-center gap-1.5 mb-1">
                <Battery className="w-4 h-4 text-indigo-600" />
                Daya Tahan Baterai
              </span>
              <span className="font-bold text-slate-900 text-sm">~{laptop.baterai_jam} Jam</span>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200">
              <span className="text-slate-500 flex items-center gap-1.5 mb-1">
                <Tag className="w-4 h-4 text-indigo-600" />
                Kategori Ideal
              </span>
              <span className="font-bold text-slate-900 text-sm capitalize">
                {laptop.kategori_penggunaan?.replace('_', ' ')}
              </span>
            </div>
          </div>
        </div>

        {/* Keterangan Sumber & Tanggal Data */}
        <div className="pt-4 border-t border-slate-100 flex flex-wrap items-center justify-between gap-4 text-xs text-slate-500">
          {/* <div className="flex items-center gap-2">
            <Database className="w-4 h-4 text-slate-400" />
            <span>Sumber: <strong>{laptop.sumber}</strong></span>
          </div> */}
          <div className="flex items-center gap-2">
            <Calendar className="w-4 h-4 text-slate-400" />
            <span>Tanggal Data: <strong>{laptop.tanggal_data}</strong></span>
          </div>
        </div>
      </div>

      {/* Panel Perhitungan Fuzzy Mamdani (Collapsible) */}
      {/* <FuzzyDetailPanel
        detailFuzzy={laptop.detail_fuzzy}
        skorRekomendasi={laptop.skor_rekomendasi}
        label={laptop.label}
      /> */}
    </div>
  );
}
