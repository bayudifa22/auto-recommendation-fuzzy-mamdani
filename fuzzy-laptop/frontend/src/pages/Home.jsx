import React from 'react';
import { Link } from 'react-router-dom';
import { Sparkles, BookOpen, Layers, Award, CheckCircle, Cpu, ShieldCheck } from 'lucide-react';

export default function Home() {
  const keunggulan = [
    {
      icon: Cpu,
      title: 'Fuzzy Mamdani Murni',
      desc: 'Perhitungan inferensi manual dengan NumPy (Max-Min dan Centroid COG) yang transparan dan dapat diverifikasi.',
    },
    {
      icon: ShieldCheck,
      title: 'Transparan & Terdokumentasi',
      desc: 'Setiap rekomendasi dilengkapi rincian nilai derajat keanggotaan dan daftar aturan fuzzy yang aktif.',
    },
    {
      icon: Award,
      title: 'Profil Kebutuhan Mahasiswa',
      desc: 'Disesuaikan dengan tugas kuliah umum, pemrograman (coding), desain grafis, editing video, dan mobilitas tinggi.',
    },
  ];

  return (
    <div className="space-y-16 py-8">
      {/* Hero Section */}
      <section className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-indigo-900 via-indigo-800 to-slate-900 text-white p-8 md:p-16 shadow-xl">
        <div className="relative z-10 max-w-3xl space-y-6">
          {/* <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/30 border border-indigo-400/30 text-indigo-200 text-xs font-semibold">
            <Sparkles className="w-3.5 h-3.5" />
            Project UAS Kecerdasan Buatan
          </div> */}

          <h1 className="text-3xl md:text-5xl font-black tracking-tight leading-tight">
            Sistem Rekomendasi Laptop Mahasiswa
          </h1>

          <p className="text-base md:text-lg text-indigo-100 leading-relaxed max-w-2xl">
            Temukan laptop yang paling tepat sesuai batas anggaran dan kebutuhan kuliah yang objektif dan transparan.
          </p>

          <div className="flex flex-wrap items-center gap-4 pt-4">
            <Link
              to="/rekomendasi"
              className="inline-flex items-center gap-2.5 px-6 py-3.5 rounded-xl bg-indigo-500 hover:bg-indigo-400 text-white font-bold text-sm shadow-lg shadow-indigo-500/30 transition-all hover:-translate-y-0.5"
            >
              <Sparkles className="w-4 h-4" />
              Mulai Rekomendasi
            </Link>

            {/* <Link
              to="/tentang"
              className="inline-flex items-center gap-2 px-5 py-3.5 rounded-xl bg-white/10 hover:bg-white/20 text-white font-semibold text-sm backdrop-blur-sm border border-white/10 transition-colors"
            >
              <BookOpen className="w-4 h-4" />
              Tentang Metode
            </Link> */}

            <Link
              to="/katalog"
              className="inline-flex items-center gap-2 px-5 py-3.5 rounded-xl bg-white/10 hover:bg-white/20 text-white font-semibold text-sm backdrop-blur-sm border border-white/10 transition-colors"
            >
              <Layers className="w-4 h-4" />
              Katalog Laptop
            </Link>
          </div>
        </div>

        {/* Ornamen Latar Belakang */}
        <div className="absolute -right-10 -bottom-10 w-96 h-96 bg-indigo-500/20 rounded-full blur-3xl pointer-events-none"></div>
      </section>

      {/* Statistik Cepat */}
      <section className="grid grid-cols-4 md:grid-cols-3 gap-4">
        {[
        ].map((stat, i) => (
          <div key={i} className="bg-white p-5 rounded-2xl border border-slate-200 text-center shadow-sm">
            <div className="text-2xl font-black text-indigo-700 font-mono">{stat.val}</div>
            <div className="text-xs text-slate-500 mt-1 font-medium">{stat.label}</div>
          </div>
        ))}
      </section>

      {/* Keunggulan Sistem */}
      <section className="space-y-6">
        <div className="text-center max-w-2xl mx-auto">
          <h2 className="text-2xl font-bold text-slate-900 tracking-tight">
            Mengapa Menggunakan Logika Fuzzy Mamdani?
          </h2>
          <p className="mt-2 text-sm text-slate-600">
            Berbeda dengan filter kaku (crisp), metode fuzzy mengevaluasi derajat kesesuaian harga dan spesifikasi secara bertingkat dan manusiawi.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {keunggulan.map((item, idx) => {
            const Icon = item.icon;
            return (
              <div
                key={idx}
                className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow space-y-3"
              >
                <div className="w-10 h-10 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center">
                  <Icon className="w-5 h-5" />
                </div>
                <h3 className="font-bold text-base text-slate-900">{item.title}</h3>
                <p className="text-xs text-slate-600 leading-relaxed">{item.desc}</p>
              </div>
            );
          })}
        </div>
      </section>
    </div>
  );
}
