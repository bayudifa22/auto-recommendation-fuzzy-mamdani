import React, { useEffect, useState } from 'react';
import { BookOpen, Layers, Calculator, ShieldAlert, CheckCircle2, HelpCircle } from 'lucide-react';
import { api } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';

export default function Tentang() {
  const [info, setInfo] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getMethodInfo()
      .then((data) => setInfo(data))
      .catch(() => {
        // Fallback info jika backend offline
        setInfo({
          metode: 'Fuzzy Logic Mamdani (Max-Min Inference)',
          tahapan: [
            '1. Fuzzifikasi: Menghitung derajat keanggotaan nilai numerik ke himpunan linguistik.',
            '2. Evaluasi Aturan: Logika AND (nilai minimum) untuk menentukan alpha-predikat.',
            '3. Agregasi Implikasi: Pemotongan level alpha dan penggabungan dengan fungsi maksimum.',
            '4. Defuzzifikasi Centroid: Perhitungan titik berat pusat massa (Center of Gravity).',
            '5. Klasifikasi Skor: Menetapkan label rekomendasi (0-100).',
          ],
          rumus_defuzzifikasi: 'z* = Σ ( μ(z) · z ) / Σ μ(z), domain z ∈ [0, 100]',
          disclaimer: 'Aplikasi ini dibangun untuk keperluan akademik (Project UAS Kecerdasan Buatan). Skor rekomendasi bukan keputusan mutlak dan tidak mencakup fluktuasi harga riil di pasar.',
        });
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <LoadingSpinner text="Memuat dokumentasi metodologi..." />;
  }

  return (
    <div className="max-w-4xl mx-auto py-8 space-y-10">
      {/* Header Halaman */}
      <div className="text-center space-y-3">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-50 border border-indigo-200 text-indigo-700 text-xs font-bold">
          <BookOpen className="w-3.5 h-3.5" />
          Dokumentasi Metode & Logika AI
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
          Penerapan Logika Fuzzy Mamdani
        </h1>
        <p className="text-sm text-slate-600 max-w-2xl mx-auto leading-relaxed">
          Penjelasan rinci bagaimana kecerdasan buatan Fuzzy Mamdani mengubah preferensi subjektif mahasiswa menjadi skor rekomendasi objektif (0–100).
        </p>
      </div>

      {/* 5 Tahapan Fuzzy Mamdani */}
      <section className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-10 shadow-sm space-y-6">
        <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2.5">
          <Calculator className="w-5 h-5 text-indigo-600" />
          5 Tahapan Alur Inferensi Mamdani
        </h2>
        <div className="space-y-4">
          {[
            {
              tahap: '1. Fuzzifikasi',
              desc: 'Mengubah nilai tegas (crisp input) seperti rasio harga, kapasitas RAM, skor prosesor, dan kapasitas penyimpanan menjadi derajat keanggotaan μ ∈ [0, 1] menggunakan fungsi keanggotaan segitiga dan trapesium.',
            },
            {
              tahap: '2. Pembentukan Basis Aturan & Evaluasi Logika AND',
              desc: 'Setiap aturan dievaluasi menggunakan operator minimum (min). Nilai terkecil dari kondisi anteseden menjadi nilai α-predikat (kekuatan aturan). Aturan dengan α = 0 diabaikan.',
            },
            {
              tahap: '3. Agregasi Implikasi (Metode Max-Min / Clipping)',
              desc: 'Fungsi keanggotaan himpunan konsekuensi (skor rekomendasi) dipotong setinggi α-predikat masing-masing aturan aktif, lalu digabungkan menjadi satu kurva fuzzy agregasi menggunakan operator maksimum (max).',
            },
            {
              tahap: '4. Defuzzifikasi Centroid (Center of Gravity / COG)',
              desc: 'Menghitung titik berat dari area kurva gabungan pada domain z dari 0 sampai 100 dengan resolusi diskrit 0.5 poin untuk menghasilkan nilai riil z*.',
            },
            {
              tahap: '5. Klasifikasi Kategori Rekomendasi',
              desc: 'Nilai defuzzifikasi dikonversi menjadi label: 80-100 (Sangat direkomendasikan), 60-79.9 (Direkomendasikan), 40-59.9 (Cukup direkomendasikan), dan 0-39.9 (Kurang direkomendasikan).',
            },
          ].map((item, idx) => (
            <div key={idx} className="p-4 rounded-2xl bg-slate-50 border border-slate-100 flex items-start gap-4">
              <span className="w-8 h-8 rounded-xl bg-indigo-600 text-white font-mono font-bold text-xs flex items-center justify-center flex-shrink-0">
                0{idx + 1}
              </span>
              <div>
                <h3 className="font-bold text-slate-900 text-sm">{item.tahap}</h3>
                <p className="mt-1 text-xs text-slate-600 leading-relaxed">{item.desc}</p>
              </div>
            </div>
          ))}
        </div>

        {/* Rumus Centroid */}
        <div className="mt-6 p-5 rounded-2xl bg-indigo-50 border border-indigo-100 text-center space-y-2">
          <span className="text-xs font-bold text-indigo-950 uppercase tracking-wider block">
            Rumus Defuzzifikasi Centroid (Center of Gravity)
          </span>
          <div className="font-mono text-base sm:text-lg font-black text-indigo-700 bg-white py-2 px-4 rounded-xl border border-indigo-200 inline-block shadow-sm">
            {info.rumus_defuzzifikasi}
          </div>
          <p className="text-[11px] text-indigo-900">
            z: domain nilai keluaran (0 - 100) • μ(z): derajat keanggotaan gabungan pada nilai z
          </p>
        </div>
      </section>

      {/* Variabel Fuzzy & Himpunan */}
      <section className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-10 shadow-sm space-y-6">
        <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2.5">
          <Layers className="w-5 h-5 text-indigo-600" />
          Variabel dan Himpunan Keanggotaan
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-2">
            <h3 className="font-bold text-slate-900 text-sm">1. Rasio Harga (harga / anggaran)</h3>
            <ul className="space-y-1 text-slate-600">
              <li>• <strong>Hemat</strong>: Trapesium (0, 0, 0.6, 0.85)</li>
              <li>• <strong>Sesuai</strong>: Segitiga (0.7, 0.9, 1.1)</li>
              <li>• <strong>Melebihi</strong>: Trapesium (0.95, 1.15, 2.0, 2.0)</li>
            </ul>
          </div>

          <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-2">
            <h3 className="font-bold text-slate-900 text-sm">2. Kapasitas RAM (GB)</h3>
            <ul className="space-y-1 text-slate-600">
              <li>• <strong>Kecil</strong>: Trapesium (0, 0, 4, 8)</li>
              <li>• <strong>Sedang</strong>: Segitiga (6, 10, 16)</li>
              <li>• <strong>Besar</strong>: Trapesium (12, 16, 64, 64)</li>
            </ul>
          </div>

          <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-2">
            <h3 className="font-bold text-slate-900 text-sm">3. Skor Prosesor (Skala 1 - 10)</h3>
            <ul className="space-y-1 text-slate-600">
              <li>• <strong>Rendah</strong>: Trapesium (0, 0, 2, 4)</li>
              <li>• <strong>Sedang</strong>: Segitiga (3, 5, 7)</li>
              <li>• <strong>Tinggi</strong>: Trapesium (6, 8, 10, 10)</li>
            </ul>
          </div>

          <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-2">
            <h3 className="font-bold text-slate-900 text-sm">4. Kapasitas Penyimpanan (GB)</h3>
            <ul className="space-y-1 text-slate-600">
              <li>• <strong>Kecil</strong>: Trapesium (0, 0, 128, 256)</li>
              <li>• <strong>Sedang</strong>: Segitiga (200, 384, 512)</li>
              <li>• <strong>Besar</strong>: Trapesium (400, 768, 4000, 4000)</li>
            </ul>
          </div>

          <div className="p-4 rounded-2xl bg-indigo-50/70 border border-indigo-200 md:col-span-2 space-y-2">
            <h3 className="font-bold text-indigo-950 text-sm">5. Skor Rekomendasi (Output 0 - 100)</h3>
            <ul className="space-y-1 text-indigo-900">
              <li>• <strong>Rendah</strong>: Trapesium (0, 0, 20, 40)</li>
              <li>• <strong>Sedang</strong>: Segitiga (30, 50, 70)</li>
              <li>• <strong>Tinggi</strong>: Trapesium (60, 80, 100, 100)</li>
            </ul>
          </div>
        </div>
      </section>

      {/* Informasi Dataset & Disclaimer Akademik */}
      <section className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-10 shadow-sm space-y-4">
        <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2.5">
          <ShieldAlert className="w-5 h-5 text-indigo-600" />
          Keterangan Dataset & Batasan Produk
        </h2>
        <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 text-xs text-slate-700 leading-relaxed space-y-2">
          <p>
            <strong>Sumber Dataset:</strong> Seluruh 40 data laptop di dalam aplikasi ini berstatus <span className="underline decoration-indigo-500 font-semibold">DATA CONTOH (Placeholder)</span> yang realistis untuk simulasi pengujian UAS. Pengguna dapat mengganti data dengan data katalog resmi di <code className="bg-slate-200 px-1 py-0.5 rounded text-indigo-700">backend/app/data/dataset_laptop.csv</code>.
          </p>
          <p>
            <strong>Tanggal Data:</strong> 24 November 2026.
          </p>
        </div>

        <div className="p-4 rounded-2xl bg-amber-50 border border-amber-200 text-xs text-amber-950 leading-relaxed">
          <h4 className="font-bold mb-1">Disclaimer Akademik:</h4>
          <p>{info.disclaimer}</p>
        </div>
      </section>
    </div>
  );
}
