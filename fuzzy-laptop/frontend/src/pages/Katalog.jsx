import React, { useEffect, useState } from 'react';
import { Search, Filter, Layers } from 'lucide-react';
import { api } from '../services/api';
import LaptopCard from '../components/LaptopCard';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';

export default function Katalog() {
  const [laptops, setLaptops] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [search, setSearch] = useState('');
  const [selectedMerek, setSelectedMerek] = useState('');
  const [selectedKategori, setSelectedKategori] = useState('');

  const loadData = () => {
    setLoading(true);
    setError(null);
    api.getLaptops({
      merek: selectedMerek,
      kategori: selectedKategori,
      q: search,
    })
      .then((data) => setLaptops(data))
      .catch((err) => setError(err.message || 'Gagal memuat katalog laptop.'))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    const timer = setTimeout(() => {
      loadData();
    }, 200);
    return () => clearTimeout(timer);
  }, [search, selectedMerek, selectedKategori]);

  const daftarMerek = ['Asus', 'Lenovo', 'HP', 'Acer', 'Apple', 'Dell', 'MSI', 'Advan', 'Axioo'];
  const daftarKategori = [
    { id: 'kuliah_umum', label: 'Kuliah Umum' },
    { id: 'programming', label: 'Programming' },
    { id: 'desain_grafis', label: 'Desain Grafis' },
    { id: 'editing_video', label: 'Editing Video' },
    { id: 'mobilitas_tinggi', label: 'Mobilitas Tinggi' },
  ];

  return (
    <div className="space-y-8 py-6">
      {/* Header Katalog */}
      <div>
        <div className="flex items-center gap-2 text-xs font-semibold text-indigo-600 mb-1">
          <Layers className="w-3.5 h-3.5" />
          <span>Koleksi Data Laptop</span>
        </div>
        <h1 className="text-2xl md:text-3xl font-extrabold text-slate-900 tracking-tight">
          Katalog Lengkap Laptop Mahasiswa
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 mt-1">
          Jelajahi seluruh koleksi laptop dalam dataset beserta rincian harga dan spesifikasinya.
        </p>
      </div>

      {/* Filter & Pencarian Bar */}
      <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm space-y-4">
        <div className="flex flex-col sm:flex-row gap-3">
          {/* Input Pencarian */}
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Cari nama laptop (mis. Vivobook, IdeaPad, MacBook)..."
              className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-300 text-xs font-medium focus:border-indigo-600 focus:ring-1 focus:ring-indigo-100"
            />
          </div>

          {/* Filter Merek */}
          <select
            value={selectedMerek}
            onChange={(e) => setSelectedMerek(e.target.value)}
            className="p-2.5 rounded-xl border border-slate-300 text-xs font-medium bg-white focus:border-indigo-600"
          >
            <option value="">Semua Merek</option>
            {daftarMerek.map((m) => (
              <option key={m} value={m}>{m}</option>
            ))}
          </select>

          {/* Filter Kategori */}
          <select
            value={selectedKategori}
            onChange={(e) => setSelectedKategori(e.target.value)}
            className="p-2.5 rounded-xl border border-slate-300 text-xs font-medium bg-white focus:border-indigo-600"
          >
            <option value="">Semua Kategori</option>
            {daftarKategori.map((k) => (
              <option key={k.id} value={k.id}>{k.label}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Tampilan Konten */}
      {loading ? (
        <LoadingSpinner text="Memuat daftar laptop..." />
      ) : error ? (
        <ErrorMessage message={error} onRetry={loadData} />
      ) : laptops.length > 0 ? (
        <div className="space-y-4">
          <div className="text-xs text-slate-500 font-medium">
            Menampilkan <strong>{laptops.length}</strong> laptop
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {laptops.map((laptop) => (
              <LaptopCard
                key={laptop.id}
                laptop={laptop}
                showScore={false}
              />
            ))}
          </div>
        </div>
      ) : (
        <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center max-w-md mx-auto">
          <p className="text-slate-600 text-sm">Tidak ada laptop yang sesuai dengan kriteria filter.</p>
          <button
            onClick={() => { setSearch(''); setSelectedMerek(''); setSelectedKategori(''); }}
            className="mt-3 text-xs font-bold text-indigo-600 hover:underline"
          >
            Reset Semua Filter
          </button>
        </div>
      )}
    </div>
  );
}
