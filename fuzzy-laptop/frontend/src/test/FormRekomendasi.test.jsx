import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import FormRekomendasi from '../pages/FormRekomendasi';

describe('FormRekomendasi Component', () => {
  it('renders form inputs and validation errors when budget is empty', () => {
    render(
      <BrowserRouter>
        <FormRekomendasi />
      </BrowserRouter>
    );

    // Pastikan judul dan input ada
    expect(screen.getByText('Cari Rekomendasi Laptop Mahasiswa')).toBeTruthy();
    expect(screen.getByRole('button', { name: /Proses Rekomendasi/i })).toBeTruthy();

    const inputAnggaran = screen.getByPlaceholderText('Contoh: 10.000.000');
    expect(inputAnggaran).toBeTruthy();

    // Kosongkan anggaran dan submit
    fireEvent.change(inputAnggaran, { target: { value: '' } });
    const submitBtn = screen.getByRole('button', { name: /Proses Rekomendasi/i });
    fireEvent.click(submitBtn);

    // Pesan error validasi harus muncul
    expect(
      screen.getByText(/Anggaran maksimum wajib diisi dan harus lebih besar dari Rp 0/i)
    ).toBeTruthy();
  });
});
