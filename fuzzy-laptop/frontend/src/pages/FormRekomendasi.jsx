import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sparkles, DollarSign, Cpu, HardDrive, MemoryStick, Battery, CheckCircle2, AlertCircle } from 'lucide-react';
import { api } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';

export default function FormRekomendasi() {
  const navigate = useNavigate();

  // State Formulir
  const [anggaranInput, setAnggaranInput] = useState('10000000');
  const [kebutuhan, setKebutuhan] = useState('programming');
  const [ramMin, setRamMin] = useState('');
  const [penyimpananMin, setPenyimpananMin] = useState('');
  const [prosesorMin, setProsesorMin] = useState('');
  const [prioritasBaterai, setPrioritasBaterai] = useState(false);
  const [includeDetail, setIncludeDetail] = useState(true);

  // State UI
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});
  const [serverError, setServerError] = useState(null);

  // Format rupiah tampilan langsung
  const parseNominal = (val) => {
    const cleaned = val.replace(/\D/g, '');
    return cleaned ? parseInt(cleaned, 10) : 0;
  };

  const handleAnggaranChange = (e) => {
    const raw = e.target.value;
    const num = parseNominal(raw);
    setAnggaranInput(num > 0 ? num.toString() : '');
    if (errors.anggaran) {
      setErrors((prev) => ({ ...prev, anggaran: null }));
    }
  };

  const nominalAnggaran = parseNominal(anggaranInput);
  const tampilanRupiah = nominalAnggaran > 0
    ? new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 }).format(nominalAnggaran)
    : 'Rp 0';

  const opsiKebutuhan = [
    {
      id: 'kuliah_umum',
      label: 'Kuliah Umum / Office',
      desc: 'Tugas dokumen, browsing materi, webinar, dan pengetikan laporan',
      recom: 'RAM min 4 GB • SSD 256 GB',
    },
    {
      id: 'programming',
      label: 'Pemrograman / Coding',
      desc: 'Kompilasi kode, menjalankan IDE, virtualisasi ringan, multitasking',
      recom: 'RAM min 8 GB • SSD 512 GB',
    },
    {
      id: 'desain_grafis',
      label: 'Desain Grafis / Ilustrasi',
      desc: 'Manipulasi vektor, editing Photoshop/Illustrator, visual rendering',
      recom: 'RAM min 16 GB • SSD 512 GB',
    },
    {
      id: 'editing_video',
      label: 'Editing Video / Multimedia',
      desc: 'Timeline editing multi-track, Premiere Pro/DaVinci, rendering berat',
      recom: 'RAM min 16 GB • SSD 512 GB',
    },
    {
      id: 'mobilitas_tinggi',
      label: 'Mobilitas Tinggi',
      desc: 'Ringan dibawa bepergian seharian di kampus dengan baterai awet',
      recom: 'RAM min 8 GB • Baterai Tahan Lama',
    },
  ];

  const validate = () => {
    const newErrors = {};
    if (!nominalAnggaran || nominalAnggaran <= 0) {
      newErrors.anggaran = 'Anggaran maksimum wajib diisi dan harus lebih besar dari Rp 0.';
    } else if (nominalAnggaran < 1000000) {
      newErrors.anggaran = 'Anggaran minimal adalah Rp 1.000.000 agar rekomendasi laptop realistis.';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setServerError(null);

    if (!validate()) return;

    setLoading(true);
    try {
      const payload = {
        anggaran_maks: nominalAnggaran,
        kebutuhan,
        ram_min_gb: ramMin ? parseInt(ramMin, 10) : null,
        penyimpanan_min_gb: penyimpananMin ? parseInt(penyimpananMin, 10) : null,
        performa_prosesor: prosesorMin || null,
        prioritas_baterai: prioritasBaterai,
        include_detail: includeDetail,
      };

      const response = await api.getRecommendations(payload);

      // Arahkan ke halaman hasil dengan membawa data rekomendasi
      navigate('/hasil', {
        state: {
          rekomendasiData: response,
          inputQuery: {
            ...payload,
            anggaranFormatted: tampilanRupiah,
          },
        },
      });
    } catch (err) {
      setServerError(err.message || 'Gagal memproses rekomendasi.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto py-8">
      <div className="mb-8 text-center">
        <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
          Cari Rekomendasi Laptop Mahasiswa
        </h1>
        <p className="mt-2 text-sm text-slate-600">
          Isi preferensi anggaran dan kebutuhan perkuliahan Anda. Logika Fuzzy Mamdani akan menghitung skor kelayakan terbaik.
        </p>
      </div>

      {serverError && (
        <div className="mb-6 p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-xs flex items-center gap-3">
          <AlertCircle className="w-5 h-5 text-rose-600 flex-shrink-0" />
          <span>{serverError}</span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="bg-white rounded-3xl border border-slate-200 shadow-sm p-6 sm:p-10 space-y-8">
        {/* 1. Batas Anggaran Maksimum */}
        <div className="space-y-2">
          <label className="block text-sm font-bold text-slate-900">
            Batas Anggaran Maksimum (Rupiah) <span className="text-rose-500">*</span>
          </label>
          <div className="relative">
            <span className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-slate-400 font-bold text-sm">
              Rp
            </span>
            <input
              type="text"
              name="anggaran_maks"
              value={nominalAnggaran > 0 ? nominalAnggaran.toLocaleString('id-ID') : ''}
              onChange={handleAnggaranChange}
              placeholder="Contoh: 10.000.000"
              className={`w-full pl-12 pr-4 py-3.5 rounded-xl border text-base font-semibold transition-all ${
                errors.anggaran
                  ? 'border-rose-400 bg-rose-50/30 focus:ring-rose-200'
                  : 'border-slate-300 focus:border-indigo-600 focus:ring-2 focus:ring-indigo-100'
              }`}
            />
          </div>
          {nominalAnggaran > 0 && (
            <p className="text-xs text-indigo-700 font-semibold pl-1">
              Terbaca: {tampilanRupiah}
            </p>
          )}
          {errors.anggaran && (
            <p className="text-xs text-rose-600 font-medium pl-1 flex items-center gap-1">
              <AlertCircle className="w-3.5 h-3.5" />
              {errors.anggaran}
            </p>
          )}
        </div>

        {/* 2. Kebutuhan Utama Mahasiswa */}
        <div className="space-y-3">
          <label className="block text-sm font-bold text-slate-900">
            Kebutuhan Utama Penggunaan <span className="text-rose-500">*</span>
          </label>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {opsiKebutuhan.map((opsi) => {
              const selected = kebutuhan === opsi.id;
              return (
                <div
                  key={opsi.id}
                  onClick={() => setKebutuhan(opsi.id)}
                  className={`cursor-pointer p-4 rounded-2xl border transition-all ${
                    selected
                      ? 'border-indigo-600 bg-indigo-50/50 ring-2 ring-indigo-100'
                      : 'border-slate-200 hover:border-slate-300 hover:bg-slate-50'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-bold text-xs sm:text-sm text-slate-900">{opsi.label}</span>
                    <input
                      type="radio"
                      name="kebutuhan"
                      checked={selected}
                      onChange={() => setKebutuhan(opsi.id)}
                      className="text-indigo-600 focus:ring-indigo-500"
                    />
                  </div>
                  <p className="text-[11px] text-slate-500 leading-tight mb-2">{opsi.desc}</p>
                  <span className="inline-block px-2 py-0.5 rounded bg-white text-[10px] font-mono font-medium text-indigo-700 border border-indigo-100">
                    {opsi.recom}
                  </span>
                </div>
              );
            })}
          </div>
        </div>

        {/* 3. Preferensi Spesifikasi Minimum (Filter Awal) */}
        <div className="pt-4 border-t border-slate-100 space-y-4">
          <h3 className="text-sm font-bold text-slate-900">
            Preferensi Tambahan (Opsional)
          </h3>
          <p className="text-xs text-slate-500">
            Biarkan kosong / "Bebas" bila ingin mengikuti standar otomatis profil kebutuhan Anda.
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            {/* RAM Minimum */}
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1 flex items-center gap-1.5">
                <MemoryStick className="w-3.5 h-3.5 text-indigo-600" />
                RAM Minimum
              </label>
              <select
                value={ramMin}
                onChange={(e) => setRamMin(e.target.value)}
                className="w-full p-2.5 rounded-xl border border-slate-300 text-xs font-medium focus:border-indigo-600 focus:ring-1 focus:ring-indigo-200"
              >
                <option value="">Bebas (Otomatis)</option>
                <option value="4">Minimal 4 GB</option>
                <option value="8">Minimal 8 GB</option>
                <option value="16">Minimal 16 GB</option>
                <option value="32">Minimal 32 GB</option>
              </select>
            </div>

            {/* Penyimpanan Minimum */}
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1 flex items-center gap-1.5">
                <HardDrive className="w-3.5 h-3.5 text-indigo-600" />
                Penyimpanan Minimum
              </label>
              <select
                value={penyimpananMin}
                onChange={(e) => setPenyimpananMin(e.target.value)}
                className="w-full p-2.5 rounded-xl border border-slate-300 text-xs font-medium focus:border-indigo-600 focus:ring-1 focus:ring-indigo-200"
              >
                <option value="">Bebas (Otomatis)</option>
                <option value="256">Minimal 256 GB</option>
                <option value="512">Minimal 512 GB</option>
                <option value="1000">Minimal 1 TB (1000 GB)</option>
              </select>
            </div>

            {/* Performa Prosesor */}
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1 flex items-center gap-1.5">
                <Cpu className="w-3.5 h-3.5 text-indigo-600" />
                Performa Prosesor
              </label>
              <select
                value={prosesorMin}
                onChange={(e) => setProsesorMin(e.target.value)}
                className="w-full p-2.5 rounded-xl border border-slate-300 text-xs font-medium focus:border-indigo-600 focus:ring-1 focus:ring-indigo-200"
              >
                <option value="">Bebas (Otomatis)</option>
                <option value="rendah">Rendah (Hemat Daya / Dasar)</option>
                <option value="sedang">Sedang (Multitasking Standar)</option>
                <option value="tinggi">Tinggi (Performa Maksimal)</option>
              </select>
            </div>
          </div>

          {/* Opsi Toggle Tambahan */}
          <div className="pt-2 flex flex-col sm:flex-row sm:items-center justify-between gap-4 text-xs text-slate-700">
            <label className="flex items-center gap-2 cursor-pointer select-none">
              <input
                type="checkbox"
                checked={prioritasBaterai}
                onChange={(e) => setPrioritasBaterai(e.target.checked)}
                className="rounded border-slate-300 text-indigo-600 focus:ring-indigo-500 w-4 h-4"
              />
              <span className="flex items-center gap-1">
                <Battery className="w-3.5 h-3.5 text-indigo-600" />
                Prioritaskan Daya Tahan Baterai (&gt; 8 jam)
              </span>
            </label>

            <label className="flex items-center gap-2 cursor-pointer select-none">
              <input
                type="checkbox"
                checked={includeDetail}
                onChange={(e) => setIncludeDetail(e.target.checked)}
                className="rounded border-slate-300 text-indigo-600 focus:ring-indigo-500 w-4 h-4"
              />
              <span>Sertakan rincian perhitungan fuzzy (α-predikat & aturan)</span>
            </label>
          </div>
        </div>

        {/* Tombol Eksekusi Submit */}
        <div className="pt-4">
          <button
            type="submit"
            disabled={loading}
            className="w-full py-4 px-6 rounded-2xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-sm shadow-lg shadow-indigo-600/30 transition-all flex items-center justify-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed"
          >
            {loading ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                Menjalankan Logika Fuzzy Mamdani...
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                Proses Rekomendasi
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
