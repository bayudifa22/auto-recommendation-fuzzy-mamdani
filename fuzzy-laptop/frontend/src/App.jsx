import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './pages/Home';
import FormRekomendasi from './pages/FormRekomendasi';
import Hasil from './pages/Hasil';
import DetailLaptop from './pages/DetailLaptop';
import Tentang from './pages/Tentang';
import Katalog from './pages/Katalog';

export default function App() {
  return (
    <BrowserRouter>
      <div className="flex flex-col min-h-screen bg-slate-50 text-slate-900 font-sans">
        <Navbar />
        <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/rekomendasi" element={<FormRekomendasi />} />
            <Route path="/hasil" element={<Hasil />} />
            <Route path="/laptop/:id" element={<DetailLaptop />} />
            <Route path="/tentang" element={<Tentang />} />
            <Route path="/katalog" element={<Katalog />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </BrowserRouter>
  );
}
