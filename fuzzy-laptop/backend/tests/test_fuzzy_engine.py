"""
Unit test untuk modul fuzzy/engine.py.
Menguji operator min (AND), max (agregasi), defuzzifikasi centroid,
dan memverifikasi 5 kasus uji terhadap perhitungan manual.
"""

import pytest
import numpy as np
from app.fuzzy.engine import FuzzyEngine, filter_and_rank_laptops
from app.fuzzy.membership import triangular_membership, trapezoidal_membership


@pytest.fixture
def engine():
    return FuzzyEngine(resolution=0.5)


def test_min_and_max_aggregation(engine):
    """Menguji bahwa evaluasi aturan menggunakan operator minimum dan agregasi menggunakan maksimum."""
    # Definisikan dummy membership
    memberships = {
        "rasio_harga": {"Hemat": 0.8, "Sesuai": 0.2, "Melebihi": 0.0},
        "ram_gb": {"Kecil": 0.0, "Sedang": 0.3, "Besar": 0.7},
        "skor_prosesor": {"Rendah": 0.0, "Sedang": 0.4, "Tinggi": 0.6},
        "penyimpanan_gb": {"Kecil": 0.0, "Sedang": 0.5, "Besar": 0.5},
    }

    dummy_rules = [
        # R1: min(0.8, 0.7, 0.6) = 0.6 (Tinggi)
        {
            "id": "R1",
            "nama": "Rule 1",
            "kondisi": {"rasio_harga": "Hemat", "ram_gb": "Besar", "skor_prosesor": "Tinggi"},
            "output": "Tinggi",
        },
        # R2: min(0.8, 0.3, 0.4) = 0.3 (Sedang)
        {
            "id": "R2",
            "nama": "Rule 2",
            "kondisi": {"rasio_harga": "Hemat", "ram_gb": "Sedang", "skor_prosesor": "Sedang"},
            "output": "Sedang",
        },
    ]

    active = engine.evaluate_rules(memberships, dummy_rules)
    assert len(active) == 2
    assert active[0]["alpha"] == 0.6
    assert active[1]["alpha"] == 0.3

    # Agregasi
    skor, aggregated = engine.aggregate_and_defuzzify(active)
    # Kurva agregasi pada titik z=50 (puncak Sedang): alpha Sedang = 0.3 -> nilai agregasi harus 0.3
    idx_50 = int(50.0 / engine.resolution)
    assert aggregated[idx_50] == pytest.approx(0.3, abs=0.01)

    # Kurva agregasi pada titik z=90 (puncak Tinggi): alpha Tinggi = 0.6 -> nilai agregasi harus 0.6
    idx_90 = int(90.0 / engine.resolution)
    assert aggregated[idx_90] == pytest.approx(0.6, abs=0.01)


def test_kasus_manual_1_high_spec_hemat(engine):
    """
    KASUS 1: Laptop Spesifikasi Tinggi dengan Harga Hemat
    Input:
      - Anggaran: Rp 10.000.000
      - Harga Laptop: Rp 6.000.000 (rasio = 0.6)
      - RAM: 16 GB
      - Skor Prosesor: 9
      - Penyimpanan: 1000 GB
    Perhitungan Manual:
      - rasio_harga 0.6:
          Hemat (0, 0, 0.6, 0.85) -> mu = 1.0
          Sesuai (0.7, 0.9, 1.1) -> mu = 0.0
          Melebihi -> mu = 0.0
      - ram_gb 16:
          Besar (12, 16, 64, 64) -> mu = 1.0
          Sedang -> mu = 0.0
      - skor_prosesor 9:
          Tinggi (6, 8, 10, 10) -> mu = 1.0
      - penyimpanan_gb 1000:
          Besar (400, 768, 4000, 4000) -> mu = 1.0
      - Aturan aktif:
          R1: Hemat(1.0) & RAM Besar(1.0) & Prosesor Tinggi(1.0) -> alpha = 1.0 (Tinggi)
          R6: Prosesor Tinggi(1.0) & Penyimpanan Besar(1.0) -> alpha = 1.0 (Tinggi)
          R9: Hemat(1.0) & RAM Besar(1.0) & Penyimpanan Besar(1.0) -> alpha = 1.0 (Tinggi)
      - Agregasi: Himpunan Tinggi (trapesium 60, 80, 100, 100) terpotong di level 1.0 penuh.
      - Defuzzifikasi Centroid:
          z dari 60 ke 100.
          Luas segitiga (60-80) = 0.5 * 20 * 1 = 10; x_bar = 60 + 2/3 * 20 = 73.333
          Luas kotak (80-100) = 20 * 1 = 20; x_bar = 90
          Centroid z* = (10 * 73.333 + 20 * 90) / 30 = 2533.33 / 30 = 84.444 -> 84.4
    """
    laptop = {
        "id": 101,
        "nama_laptop": "Super Laptop A",
        "merek": "TestBrand",
        "harga": 6000000,
        "ram_gb": 16,
        "skor_prosesor": 9,
        "penyimpanan_gb": 1000,
        "tipe_penyimpanan": "SSD",
    }
    hasil = engine.evaluate_laptop(laptop, anggaran_maks=10000000, kebutuhan="programming", include_detail=True)
    assert hasil["skor_rekomendasi"] == pytest.approx(84.4, abs=0.2)
    assert hasil["label"] == "Sangat direkomendasikan"


def test_kasus_manual_2_low_spec_melebihi(engine):
    """
    KASUS 2: Laptop Spesifikasi Rendah dengan Harga Melebihi Anggaran
    Input:
      - Anggaran: Rp 4.000.000
      - Harga Laptop: Rp 6.000.000 (rasio = 1.5)
      - RAM: 4 GB
      - Skor Prosesor: 2
      - Penyimpanan: 128 GB
    Perhitungan Manual:
      - rasio_harga 1.5:
          Hemat -> mu = 0.0
          Sesuai -> mu = 0.0
          Melebihi (0.95, 1.15, 2.0, 2.0) -> mu = 1.0
      - ram_gb 4:
          Kecil (0, 0, 4, 8) -> mu = 1.0
          Sedang -> mu = 0.0
      - skor_prosesor 2:
          Rendah (0, 0, 2, 4) -> mu = 1.0
      - penyimpanan_gb 128:
          Kecil (0, 0, 128, 256) -> mu = 1.0
      - Aturan aktif:
          R5: Melebihi(1.0) & RAM Kecil(1.0) & Prosesor Rendah(1.0) -> alpha = 1.0 (Rendah)
          R7: RAM Kecil(1.0) & Penyimpanan Kecil(1.0) -> alpha = 1.0 (Rendah)
          R12: Prosesor Rendah(1.0) & RAM Kecil(1.0) -> alpha = 1.0 (Rendah)
      - Agregasi: Himpunan Rendah (trapesium 0, 0, 20, 40) terpotong di level 1.0 penuh.
      - Defuzzifikasi Centroid:
          Simetris terhadap himpunan Tinggi di Kasus 1:
          Kotak (0-20): luas = 20, x_bar = 10
          Segitiga (20-40): luas = 10, x_bar = 20 + 1/3 * 20 = 26.667
          Centroid z* = (20 * 10 + 10 * 26.667) / 30 = 466.67 / 30 = 15.556 -> 15.6
    """
    laptop = {
        "id": 102,
        "nama_laptop": "Basic Laptop B",
        "merek": "TestBrand",
        "harga": 6000000,
        "ram_gb": 4,
        "skor_prosesor": 2,
        "penyimpanan_gb": 128,
        "tipe_penyimpanan": "eMMC",
    }
    hasil = engine.evaluate_laptop(laptop, anggaran_maks=4000000, kebutuhan="kuliah_umum", include_detail=True)
    assert hasil["skor_rekomendasi"] == pytest.approx(15.6, abs=0.2)
    assert hasil["label"] == "Kurang direkomendasikan"


def test_kasus_manual_3_mid_spec_sesuai(engine):
    """
    KASUS 3: Laptop Menengah dengan Harga Sesuai Anggaran
    Input:
      - Anggaran: Rp 8.000.000
      - Harga Laptop: Rp 7.200.000 (rasio = 0.9)
      - RAM: 10 GB (Sedang simetris puncak)
      - Skor Prosesor: 5 (Sedang simetris puncak)
      - Penyimpanan: 384 GB (Sedang simetris puncak)
    Perhitungan Manual:
      - rasio_harga 0.9:
          Sesuai (0.7, 0.9, 1.1) -> mu = 1.0 (puncak)
          Hemat -> mu = 0.0
          Melebihi -> mu = 0.0
      - ram_gb 10:
          Sedang (6, 10, 16) -> mu = 1.0 (puncak)
      - skor_prosesor 5:
          Sedang (3, 5, 7) -> mu = 1.0 (puncak)
      - penyimpanan_gb 384:
          Sedang (200, 384, 512) -> mu = 1.0 (puncak)
      - Aturan aktif:
          R4: Sesuai(1.0) & RAM Sedang(1.0) & Prosesor Sedang(1.0) -> alpha = 1.0 (Sedang)
          R10: Sesuai(1.0) & Penyimpanan Sedang(1.0) & RAM Sedang(1.0) -> alpha = 1.0 (Sedang)
      - Agregasi: Himpunan Sedang (segitiga simetris 30, 50, 70) dengan alpha = 1.0 penuh.
      - Defuzzifikasi Centroid:
          Karena segitiga simetris dengan puncak di 50.0, titik beratnya adalah persis 50.0.
    """
    laptop = {
        "id": 103,
        "nama_laptop": "Mid Laptop C",
        "merek": "TestBrand",
        "harga": 7200000,
        "ram_gb": 10,
        "skor_prosesor": 5,
        "penyimpanan_gb": 384,
        "tipe_penyimpanan": "SSD",
    }
    hasil = engine.evaluate_laptop(laptop, anggaran_maks=8000000, kebutuhan="kuliah_umum", include_detail=True)
    assert hasil["skor_rekomendasi"] == pytest.approx(50.0, abs=0.2)
    assert hasil["label"] == "Cukup direkomendasikan"


def test_kasus_manual_4_high_spec_melebihi(engine):
    """
    KASUS 4: Laptop Spesifikasi Tinggi tetapi Harga Melebihi Anggaran
    Input:
      - Anggaran: Rp 10.000.000
      - Harga Laptop: Rp 14.000.000 (rasio = 1.4)
      - RAM: 16 GB (Besar mu=1.0)
      - Skor Prosesor: 9 (Tinggi mu=1.0)
      - Penyimpanan: 256 GB (Kecil mu=1.0)
    Perhitungan Manual:
      - rasio_harga 1.4 -> Melebihi (mu = 1.0)
      - Aturan aktif:
          R8: Melebihi(1.0) & Prosesor Tinggi(1.0) & RAM Besar(1.0) -> alpha = 1.0 (Sedang)
      - Agregasi: Output Sedang (segitiga 30, 50, 70) terpotong di level 1.0.
      - Centroid: 50.0.
    """
    laptop = {
        "id": 104,
        "nama_laptop": "Over Budget High Spec D",
        "merek": "TestBrand",
        "harga": 14000000,
        "ram_gb": 16,
        "skor_prosesor": 9,
        "penyimpanan_gb": 256,
        "tipe_penyimpanan": "SSD",
    }
    hasil = engine.evaluate_laptop(laptop, anggaran_maks=10000000, kebutuhan="programming", include_detail=True)
    assert hasil["skor_rekomendasi"] == pytest.approx(50.0, abs=0.2)
    assert hasil["label"] == "Cukup direkomendasikan"


def test_kasus_manual_5_campuran_deterministik(engine):
    """
    KASUS 5: Pengujian sifat deterministik dan konsistensi agregasi majemuk
    Input berulang dengan nilai yang sama persis harus menghasilkan skor dan alasan yang identik.
    """
    laptop = {
        "id": 105,
        "nama_laptop": "Test Consistency E",
        "merek": "TestBrand",
        "harga": 8500000,
        "ram_gb": 16,
        "skor_prosesor": 7,
        "penyimpanan_gb": 512,
        "tipe_penyimpanan": "SSD",
    }
    hasil_1 = engine.evaluate_laptop(laptop, anggaran_maks=9000000, kebutuhan="programming")
    hasil_2 = engine.evaluate_laptop(laptop, anggaran_maks=9000000, kebutuhan="programming")
    assert hasil_1["skor_rekomendasi"] == hasil_2["skor_rekomendasi"]
    assert hasil_1["alasan"] == hasil_2["alasan"]
    assert 0.0 <= hasil_1["skor_rekomendasi"] <= 100.0


def test_fallback_when_filter_strictly_excludes_all():
    """Menguji penanganan ketika preferensi pengguna menyaring seluruh dataset (tidak ada yang lolos)."""
    dataset_mini = [
        {"id": 1, "nama_laptop": "Laptop Mini 1", "merek": "A", "harga": 5000000, "ram_gb": 4, "skor_prosesor": 3, "penyimpanan_gb": 256, "tipe_penyimpanan": "SSD"},
        {"id": 2, "nama_laptop": "Laptop Mini 2", "merek": "B", "harga": 7000000, "ram_gb": 8, "skor_prosesor": 5, "penyimpanan_gb": 512, "tipe_penyimpanan": "SSD"},
    ]
    # Filter mustahil: RAM min 64 GB
    hasil, pesan = filter_and_rank_laptops(
        laptops=dataset_mini,
        anggaran_maks=6000000,
        ram_min_gb=64,
        penyimpanan_min_gb=2000
    )
    # Harus mengembalikan fallback tanpa error
    assert pesan is not None
    assert "Tidak ditemukan laptop yang memenuhi spesifikasi minimum" in pesan
    assert len(hasil) > 0
