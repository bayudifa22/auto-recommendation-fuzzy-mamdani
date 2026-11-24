import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import LaptopCard, { formatRupiah } from '../components/LaptopCard';

describe('LaptopCard Component', () => {
  const dummyLaptop = {
    id: 1,
    nama_laptop: 'Lenovo IdeaPad Slim 3',
    merek: 'Lenovo',
    harga: 8500000,
    ram_gb: 16,
    penyimpanan_gb: 512,
    tipe_penyimpanan: 'SSD',
    skor_prosesor: 7,
    gpu: 'Intel Iris Xe',
    ukuran_layar: 14.0,
    baterai_jam: 6.5,
    skor_rekomendasi: 82.5,
    label: 'Sangat direkomendasikan',
    alasan: 'RAM besar 16 GB, SSD 512 GB, harga di bawah anggaran.',
  };

  it('renders laptop name, brand, formatted price, and specs properly', () => {
    render(
      <BrowserRouter>
        <LaptopCard laptop={dummyLaptop} ranking={1} showScore={true} />
      </BrowserRouter>
    );

    expect(screen.getByText('Lenovo IdeaPad Slim 3')).toBeTruthy();
    expect(screen.getByText('Lenovo')).toBeTruthy();
    expect(screen.getByText('16 GB')).toBeTruthy();
    expect(screen.getByText('512 GB SSD')).toBeTruthy();
    expect(screen.getByText('7/10')).toBeTruthy();
    expect(screen.getByText('82.5')).toBeTruthy();
    expect(screen.getByText('Sangat direkomendasikan')).toBeTruthy();
  });

  it('formats Rupiah currency correctly', () => {
    const formatted = formatRupiah(8500000);
    expect(formatted).toContain('8.500.000');
  });
});
