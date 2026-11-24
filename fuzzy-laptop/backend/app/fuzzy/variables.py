"""
Definisi variabel linguistik dan parameter himpunan fuzzy.
Semua batasan numerik dan parameter keanggotaan terpusat di sini
agar mudah disesuaikan tanpa kode ajaib (magic numbers) yang tersebar.
"""

from typing import Dict, Any

# Definisi himpunan fuzzy variabel input dan output
# Format parameter:
#   "segitiga": (a, b, c)
#   "trapesium": (a, b, c, d)

VARIABLES_CONFIG: Dict[str, Dict[str, Any]] = {
    "rasio_harga": {
        "nama": "Rasio Harga terhadap Anggaran",
        "domain": (0.0, 2.0),
        "himpunan": {
            "Hemat": {"tipe": "trapesium", "params": (0.0, 0.0, 0.6, 0.85)},
            "Sesuai": {"tipe": "segitiga", "params": (0.7, 0.9, 1.1)},
            "Melebihi": {"tipe": "trapesium", "params": (0.95, 1.15, 2.0, 2.0)},
        },
    },
    "ram_gb": {
        "nama": "Kapasitas RAM (GB)",
        "domain": (0.0, 64.0),
        "himpunan": {
            "Kecil": {"tipe": "trapesium", "params": (0.0, 0.0, 4.0, 8.0)},
            "Sedang": {"tipe": "segitiga", "params": (6.0, 10.0, 16.0)},
            "Besar": {"tipe": "trapesium", "params": (12.0, 16.0, 64.0, 64.0)},
        },
    },
    "skor_prosesor": {
        "nama": "Skor Performa Prosesor (1-10)",
        "domain": (0.0, 10.0),
        "himpunan": {
            "Rendah": {"tipe": "trapesium", "params": (0.0, 0.0, 2.0, 4.0)},
            "Sedang": {"tipe": "segitiga", "params": (3.0, 5.0, 7.0)},
            "Tinggi": {"tipe": "trapesium", "params": (6.0, 8.0, 10.0, 10.0)},
        },
    },
    "penyimpanan_gb": {
        "nama": "Kapasitas Penyimpanan (GB)",
        "domain": (0.0, 4000.0),
        "himpunan": {
            "Kecil": {"tipe": "trapesium", "params": (0.0, 0.0, 128.0, 256.0)},
            "Sedang": {"tipe": "segitiga", "params": (200.0, 384.0, 512.0)},
            "Besar": {"tipe": "trapesium", "params": (400.0, 768.0, 4000.0, 4000.0)},
        },
    },
    "baterai_jam": {
        "nama": "Daya Tahan Baterai (Jam)",
        "domain": (0.0, 24.0),
        "himpunan": {
            "Pendek": {"tipe": "trapesium", "params": (0.0, 0.0, 3.0, 5.0)},
            "Sedang": {"tipe": "segitiga", "params": (4.0, 7.0, 10.0)},
            "Lama": {"tipe": "trapesium", "params": (8.0, 12.0, 24.0, 24.0)},
        },
    },
    "skor_rekomendasi": {
        "nama": "Skor Rekomendasi Laptop (Output)",
        "domain": (0.0, 100.0),
        "himpunan": {
            "Rendah": {"tipe": "trapesium", "params": (0.0, 0.0, 20.0, 40.0)},
            "Sedang": {"tipe": "segitiga", "params": (30.0, 50.0, 70.0)},
            "Tinggi": {"tipe": "trapesium", "params": (60.0, 80.0, 100.0, 100.0)},
        },
    },
}

# Profil Kebutuhan Mahasiswa untuk mengisi nilai preferensi bawaan (default)
# dan menyusun narasi alasan rekomendasi
PROFIL_KEBUTUHAN: Dict[str, Dict[str, Any]] = {
    "kuliah_umum": {
        "label": "Kuliah Umum / Tugas Office",
        "ram_min_default": 4,
        "penyimpanan_min_default": 256,
        "prosesor_min_default": "rendah",
        "deskripsi_kebutuhan": "komputasi harian, pengetikan dokumen, dan browsing materi kuliah",
    },
    "programming": {
        "label": "Pemrograman / Coding",
        "ram_min_default": 8,
        "penyimpanan_min_default": 512,
        "prosesor_min_default": "sedang",
        "deskripsi_kebutuhan": "kompilasi kode, menjalankan IDE, virtualisasi ringan, dan multitasking",
    },
    "desain_grafis": {
        "label": "Desain Grafis / Ilustrasi",
        "ram_min_default": 16,
        "penyimpanan_min_default": 512,
        "prosesor_min_default": "tinggi",
        "deskripsi_kebutuhan": "olah grafis bitmap/vektor, color grading, dan rendering visual",
    },
    "editing_video": {
        "label": "Editing Video / Multimedia",
        "ram_min_default": 16,
        "penyimpanan_min_default": 512,
        "prosesor_min_default": "tinggi",
        "deskripsi_kebutuhan": "editing timeline video multi-track, rendering, dan komputasi grafis berat",
    },
    "mobilitas_tinggi": {
        "label": "Mobilitas Tinggi / Daya Tahan Baterai",
        "ram_min_default": 8,
        "penyimpanan_min_default": 256,
        "prosesor_min_default": "sedang",
        "deskripsi_kebutuhan": "portabilitas ringan dan daya tahan baterai seharian di kampus",
    },
}

# Pemetaan label skor rekomendasi
LABEL_SKOR = [
    (0.0, 39.9, "Kurang direkomendasikan"),
    (40.0, 59.9, "Cukup direkomendasikan"),
    (60.0, 79.9, "Direkomendasikan"),
    (80.0, 100.0, "Sangat direkomendasikan"),
]


def dapatkan_label_skor(skor: float) -> str:
    """Mengembalikan label rekomendasi berdasarkan rentang skor 0-100."""
    for min_val, max_val, label in LABEL_SKOR:
        if min_val <= skor <= max_val:
            return label
    if skor > 100.0:
        return "Sangat direkomendasikan"
    return "Kurang direkomendasikan"
