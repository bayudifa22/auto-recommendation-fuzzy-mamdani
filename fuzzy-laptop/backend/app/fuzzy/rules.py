"""
Basis aturan fuzzy (Fuzzy Rule Base) untuk Sistem Rekomendasi Laptop Mahasiswa.
Aturan disimpan dalam bentuk struktur data list of dict (bukan hardcoded if-else)
agar mudah dibaca, diinspeksi, dan dievaluasi secara dinamis oleh mesin inferensi.
"""

from typing import List, Dict, Any

# Basis aturan utama (4 variabel: rasio_harga, ram_gb, skor_prosesor, penyimpanan_gb)
RULES_BASE: List[Dict[str, Any]] = [
    {
        "id": "R1",
        "nama": "Jika Harga Hemat, RAM Besar, dan Prosesor Tinggi, maka Rekomendasi Tinggi",
        "kondisi": {
            "rasio_harga": "Hemat",
            "ram_gb": "Besar",
            "skor_prosesor": "Tinggi",
        },
        "output": "Tinggi",
    },
    {
        "id": "R2",
        "nama": "Jika Harga Sesuai, RAM Besar, dan Prosesor Tinggi, maka Rekomendasi Tinggi",
        "kondisi": {
            "rasio_harga": "Sesuai",
            "ram_gb": "Besar",
            "skor_prosesor": "Tinggi",
        },
        "output": "Tinggi",
    },
    {
        "id": "R3",
        "nama": "Jika Harga Hemat, RAM Sedang, dan Prosesor Sedang, maka Rekomendasi Sedang",
        "kondisi": {
            "rasio_harga": "Hemat",
            "ram_gb": "Sedang",
            "skor_prosesor": "Sedang",
        },
        "output": "Sedang",
    },
    {
        "id": "R4",
        "nama": "Jika Harga Sesuai, RAM Sedang, dan Prosesor Sedang, maka Rekomendasi Sedang",
        "kondisi": {
            "rasio_harga": "Sesuai",
            "ram_gb": "Sedang",
            "skor_prosesor": "Sedang",
        },
        "output": "Sedang",
    },
    {
        "id": "R5",
        "nama": "Jika Harga Melebihi, RAM Kecil, dan Prosesor Rendah, maka Rekomendasi Rendah",
        "kondisi": {
            "rasio_harga": "Melebihi",
            "ram_gb": "Kecil",
            "skor_prosesor": "Rendah",
        },
        "output": "Rendah",
    },
    {
        "id": "R6",
        "nama": "Jika Prosesor Tinggi dan Penyimpanan Besar, maka Rekomendasi Tinggi",
        "kondisi": {
            "skor_prosesor": "Tinggi",
            "penyimpanan_gb": "Besar",
        },
        "output": "Tinggi",
    },
    {
        "id": "R7",
        "nama": "Jika RAM Kecil dan Penyimpanan Kecil, maka Rekomendasi Rendah",
        "kondisi": {
            "ram_gb": "Kecil",
            "penyimpanan_gb": "Kecil",
        },
        "output": "Rendah",
    },
    {
        "id": "R8",
        "nama": "Jika Harga Melebihi, Prosesor Tinggi, dan RAM Besar, maka Rekomendasi Sedang",
        "kondisi": {
            "rasio_harga": "Melebihi",
            "skor_prosesor": "Tinggi",
            "ram_gb": "Besar",
        },
        "output": "Sedang",
    },
    {
        "id": "R9",
        "nama": "Jika Harga Hemat, RAM Besar, dan Penyimpanan Besar, maka Rekomendasi Tinggi",
        "kondisi": {
            "rasio_harga": "Hemat",
            "ram_gb": "Besar",
            "penyimpanan_gb": "Besar",
        },
        "output": "Tinggi",
    },
    {
        "id": "R10",
        "nama": "Jika Harga Sesuai, Penyimpanan Sedang, dan RAM Sedang, maka Rekomendasi Sedang",
        "kondisi": {
            "rasio_harga": "Sesuai",
            "penyimpanan_gb": "Sedang",
            "ram_gb": "Sedang",
        },
        "output": "Sedang",
    },
    {
        "id": "R11",
        "nama": "Jika Harga Melebihi dan RAM Sedang, maka Rekomendasi Rendah",
        "kondisi": {
            "rasio_harga": "Melebihi",
            "ram_gb": "Sedang",
        },
        "output": "Rendah",
    },
    {
        "id": "R12",
        "nama": "Jika Prosesor Rendah dan RAM Kecil, maka Rekomendasi Rendah",
        "kondisi": {
            "skor_prosesor": "Rendah",
            "ram_gb": "Kecil",
        },
        "output": "Rendah",
    },
]

# Aturan tambahan jika variabel baterai diaktifkan
RULES_BATTERY_EXTENSION: List[Dict[str, Any]] = [
    {
        "id": "RB1",
        "nama": "Jika Baterai Lama dan Harga Hemat, maka Rekomendasi Tinggi",
        "kondisi": {
            "baterai_jam": "Lama",
            "rasio_harga": "Hemat",
        },
        "output": "Tinggi",
    },
    {
        "id": "RB2",
        "nama": "Jika Baterai Pendek dan Harga Melebihi, maka Rekomendasi Rendah",
        "kondisi": {
            "baterai_jam": "Pendek",
            "rasio_harga": "Melebihi",
        },
        "output": "Rendah",
    },
]


def dapatkan_aturan(gunakan_baterai: bool = False) -> List[Dict[str, Any]]:
    """
    Mengembalikan daftar aturan fuzzy.
    Jika gunakan_baterai bernilai True, aturan tambahan baterai digabungkan.
    """
    if gunakan_baterai:
        return RULES_BASE + RULES_BATTERY_EXTENSION
    return RULES_BASE
