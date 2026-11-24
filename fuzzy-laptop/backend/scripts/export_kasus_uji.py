"""
Skrip Ekspor Kasus Uji Fuzzy Mamdani ke CSV.
Menjalankan 8 skenario pengujian mahasiswa dan mengekspor:
- Skenario & Profil Pengguna
- Nama Laptop & Spesifikasi (Harga, RAM, Prosesor, Penyimpanan, Baterai)
- Nilai Input Ternormalisasi (Rasio Harga, dll.)
- Derajat Keanggotaan Fuzzy (Fuzzifikasi)
- Aturan-Aturan Aktif dan Nilai Alpha-Predikat
- Skor Rekomendasi (Defuzzifikasi Centroid) dan Label Kategori
Hasil diekspor ke file CSV untuk dibandingkan dan diverifikasi terhadap spreadsheet / perhitungan manual.
"""

import sys
import csv
from pathlib import Path

# Menambahkan direktori backend ke sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.data_loader import data_loader
from app.fuzzy.engine import fuzzy_engine, filter_and_rank_laptops

# Definisi 8 Skenario Uji Representatif
SKENARIO_PENGUJIAN = [
    {
        "id_skenario": 1,
        "nama": "Office / Kuliah Umum Anggaran Rendah",
        "anggaran_maks": 5000000,
        "kebutuhan": "kuliah_umum",
        "ram_min": 4,
        "penyimpanan_min": 256,
        "prosesor_min": "rendah",
        "prioritas_baterai": False,
        "deskripsi": "Mahasiswa baru mencari laptop terjangkau untuk mengetik tugas dan kuliah online.",
    },
    {
        "id_skenario": 2,
        "nama": "Pemrograman Menengah (Coding / Web Dev)",
        "anggaran_maks": 9000000,
        "kebutuhan": "programming",
        "ram_min": 8,
        "penyimpanan_min": 512,
        "prosesor_min": "sedang",
        "prioritas_baterai": False,
        "deskripsi": "Mahasiswa Informatika membutuhkan RAM leluasa dan SSD cepat untuk IDE dan compile kode.",
    },
    {
        "id_skenario": 3,
        "nama": "Desain Grafis Spesifikasi Tinggi",
        "anggaran_maks": 16000000,
        "kebutuhan": "desain_grafis",
        "ram_min": 16,
        "penyimpanan_min": 512,
        "prosesor_min": "tinggi",
        "prioritas_baterai": False,
        "deskripsi": "Mahasiswa DKV/Desain butuh performa prosesor tinggi dan RAM besar untuk Photoshop/Illustrator.",
    },
    {
        "id_skenario": 4,
        "nama": "Editing Video Profesional / Multimedia",
        "anggaran_maks": 22000000,
        "kebutuhan": "editing_video",
        "ram_min": 16,
        "penyimpanan_min": 1000,
        "prosesor_min": "tinggi",
        "prioritas_baterai": False,
        "deskripsi": "Render video resolusi tinggi multi-track butuh GPU dan performa maksimal.",
    },
    {
        "id_skenario": 5,
        "nama": "Mobilitas Tinggi & Daya Baterai Panjang",
        "anggaran_maks": 13000000,
        "kebutuhan": "mobilitas_tinggi",
        "ram_min": 8,
        "penyimpanan_min": 256,
        "prosesor_min": "sedang",
        "prioritas_baterai": True,
        "deskripsi": "Mahasiswa aktif organisasi membutuhkan laptop baterai awet (> 8 jam) dan bobot ringan.",
    },
    {
        "id_skenario": 6,
        "nama": "Spesifikasi Tinggi Harga Melebihi Anggaran",
        "anggaran_maks": 6000000,
        "kebutuhan": "programming",
        "ram_min": 4,
        "penyimpanan_min": 256,
        "prosesor_min": "rendah",
        "prioritas_baterai": False,
        "deskripsi": "Uji perilaku inferensi ketika laptop berspesifikasi tinggi harganya melebihi anggaran pengguna.",
    },
    {
        "id_skenario": 7,
        "nama": "Mahasiswa Teknik Anggaran Menengah",
        "anggaran_maks": 11000000,
        "kebutuhan": "programming",
        "ram_min": 8,
        "penyimpanan_min": 512,
        "prosesor_min": "sedang",
        "prioritas_baterai": False,
        "deskripsi": "Keseimbangan performa dan harga di rentang 10-11 juta rupiah.",
    },
    {
        "id_skenario": 8,
        "nama": "Kuliah Fleksibel Anggaran Cukup Longgar",
        "anggaran_maks": 14000000,
        "kebutuhan": "kuliah_umum",
        "ram_min": 8,
        "penyimpanan_min": 512,
        "prosesor_min": "sedang",
        "prioritas_baterai": False,
        "deskripsi": "Mencari laptop kuliah umum premium yang awet digunakan hingga lulus.",
    },
]


def jalankan_dan_ekspor():
    all_laptops = data_loader.get_all()
    output_dir = backend_dir / "data"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_csv = output_dir / "kasus_uji_fuzzy.csv"

    print("================================================================================")
    print(" MENJALANKAN 8 SKENARIO PENGUJIAN LOGIKA FUZZY MAMDANI UNTUK VALIDASI AKADEMIK")
    print("================================================================================\n")

    fieldnames = [
        "id_skenario",
        "nama_skenario",
        "anggaran_maks",
        "kebutuhan",
        "peringkat",
        "id_laptop",
        "nama_laptop",
        "merek",
        "harga",
        "ram_gb",
        "penyimpanan_gb",
        "skor_prosesor",
        "baterai_jam",
        "rasio_harga",
        "mu_harga_hemat",
        "mu_harga_sesuai",
        "mu_harga_melebihi",
        "mu_ram_kecil",
        "mu_ram_sedang",
        "mu_ram_besar",
        "mu_cpu_rendah",
        "mu_cpu_sedang",
        "mu_cpu_tinggi",
        "mu_storage_kecil",
        "mu_storage_sedang",
        "mu_storage_besar",
        "aturan_aktif_dan_alpha",
        "skor_rekomendasi_centroid",
        "label_kategori",
        "alasan_rekomendasi",
    ]

    total_baris_diekspor = 0

    with open(output_csv, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for skenario in SKENARIO_PENGUJIAN:
            print(f"[SKENARIO {skenario['id_skenario']}] {skenario['nama']}")
            print(f"  Anggaran: Rp {skenario['anggaran_maks']:,} | Kebutuhan: {skenario['kebutuhan']}")

            hasil_laptops, pesan = filter_and_rank_laptops(
                laptops=all_laptops,
                anggaran_maks=float(skenario["anggaran_maks"]),
                kebutuhan=skenario["kebutuhan"],
                ram_min_gb=skenario["ram_min"],
                penyimpanan_min_gb=skenario["penyimpanan_min"],
                performa_prosesor=skenario["prosesor_min"],
                prioritas_baterai=skenario["prioritas_baterai"],
                include_detail=True,
                max_results=3,  # Ekspor 3 laptop teratas per skenario
            )

            if pesan:
                print(f"  Peringatan Filter: {pesan}")

            for rank, lap in enumerate(hasil_laptops, start=1):
                dfz = lap.get("detail_fuzzy", {})
                inp = dfz.get("inputs_ternormalisasi", {})
                mu = dfz.get("derajat_keanggotaan", {})
                rules = dfz.get("aturan_aktif", [])

                aturan_str = "; ".join([f"{r['id']}(α={r['alpha']})" for r in rules])

                mu_harga = mu.get("rasio_harga", {})
                mu_ram = mu.get("ram_gb", {})
                mu_cpu = mu.get("skor_prosesor", {})
                mu_storage = mu.get("penyimpanan_gb", {})

                row = {
                    "id_skenario": skenario["id_skenario"],
                    "nama_skenario": skenario["nama"],
                    "anggaran_maks": skenario["anggaran_maks"],
                    "kebutuhan": skenario["kebutuhan"],
                    "peringkat": rank,
                    "id_laptop": lap["id"],
                    "nama_laptop": lap["nama_laptop"],
                    "merek": lap["merek"],
                    "harga": lap["harga"],
                    "ram_gb": lap["ram_gb"],
                    "penyimpanan_gb": lap["penyimpanan_gb"],
                    "skor_prosesor": lap["skor_prosesor"],
                    "baterai_jam": lap.get("baterai_jam", 0.0),
                    "rasio_harga": inp.get("rasio_harga", 0.0),
                    "mu_harga_hemat": mu_harga.get("Hemat", 0.0),
                    "mu_harga_sesuai": mu_harga.get("Sesuai", 0.0),
                    "mu_harga_melebihi": mu_harga.get("Melebihi", 0.0),
                    "mu_ram_kecil": mu_ram.get("Kecil", 0.0),
                    "mu_ram_sedang": mu_ram.get("Sedang", 0.0),
                    "mu_ram_besar": mu_ram.get("Besar", 0.0),
                    "mu_cpu_rendah": mu_cpu.get("Rendah", 0.0),
                    "mu_cpu_sedang": mu_cpu.get("Sedang", 0.0),
                    "mu_cpu_tinggi": mu_cpu.get("Tinggi", 0.0),
                    "mu_storage_kecil": mu_storage.get("Kecil", 0.0),
                    "mu_storage_sedang": mu_storage.get("Sedang", 0.0),
                    "mu_storage_besar": mu_storage.get("Besar", 0.0),
                    "aturan_aktif_dan_alpha": aturan_str,
                    "skor_rekomendasi_centroid": lap["skor_rekomendasi"],
                    "label_kategori": lap["label"],
                    "alasan_rekomendasi": lap["alasan"],
                }

                writer.writerow(row)
                total_baris_diekspor += 1

                print(f"    #{rank} {lap['nama_laptop']} - Skor: {lap['skor_rekomendasi']} ({lap['label']})")
                print(f"       Aturan Aktif: {aturan_str}")

            print()

    print(f"[SELESAI] Sebanyak {total_baris_diekspor} baris data kasus uji berhasil diekspor ke:")
    print(f"          -> {output_csv}\n")


if __name__ == "__main__":
    jalankan_dan_ekspor()
