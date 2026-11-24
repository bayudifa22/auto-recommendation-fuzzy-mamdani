"""
Mesin Inferensi Fuzzy Mamdani (Fuzzy Mamdani Engine).
Mengimplementasikan tahapan:
1. Fuzzifikasi
2. Evaluasi Aturan (Alpha-Predikat / Operasi Minimum)
3. Agregasi Implikasi (Metode Clipping dan Operasi Maksimum)
4. Defuzzifikasi Centroid (Center of Gravity)
5. Penyusunan Alasan Rekomendasi Otomatis
Dibuat secara manual menggunakan NumPy tanpa dependensi scikit-fuzzy.
"""

from typing import Dict, List, Any, Tuple, Optional
import numpy as np

from app.fuzzy.membership import triangular_membership, trapezoidal_membership
from app.fuzzy.variables import VARIABLES_CONFIG, PROFIL_KEBUTUHAN, dapatkan_label_skor
from app.fuzzy.rules import dapatkan_aturan


class FuzzyEngine:
    """Mesin inferensi Fuzzy Mamdani untuk penilaian laptop mahasiswa."""

    def __init__(self, resolution: float = 0.5):
        """
        Inisialisasi mesin fuzzy dengan domain output dan fungsi keanggotaan keluaran yang telah dipra-hitung.
        resolution: resolusi diskritisasi domain z (default 0.5 poin, domain 0-100).
        """
        self.resolution = resolution
        self.z_domain = np.arange(0.0, 100.0 + resolution, resolution)

        # Pra-hitung kurva fungsi keanggotaan output pada domain z
        output_cfg = VARIABLES_CONFIG["skor_rekomendasi"]["himpunan"]
        self.output_mf = {
            "Rendah": trapezoidal_membership(self.z_domain, *output_cfg["Rendah"]["params"]),
            "Sedang": triangular_membership(self.z_domain, *output_cfg["Sedang"]["params"]),
            "Tinggi": trapezoidal_membership(self.z_domain, *output_cfg["Tinggi"]["params"]),
        }

    def fuzzify(self, inputs: Dict[str, float], use_battery: bool = False) -> Dict[str, Dict[str, float]]:
        """
        Menghitung derajat keanggotaan untuk setiap variabel input.

        inputs: dictionary berisi { 'rasio_harga': float, 'ram_gb': float, 'skor_prosesor': float, ... }
        Return: dictionary bersarang { variabel: { himpunan: derajat_keanggotaan } }
        """
        memberships: Dict[str, Dict[str, float]] = {}

        variabel_target = ["rasio_harga", "ram_gb", "skor_prosesor", "penyimpanan_gb"]
        if use_battery and "baterai_jam" in inputs:
            variabel_target.append("baterai_jam")

        for var_name in variabel_target:
            val = float(inputs.get(var_name, 0.0))
            cfg = VARIABLES_CONFIG.get(var_name, {})
            himpunan_dict = cfg.get("himpunan", {})

            memberships[var_name] = {}
            for himpunan_nama, h_info in himpunan_dict.items():
                tipe = h_info["tipe"]
                params = h_info["params"]
                if tipe == "segitiga":
                    mu = triangular_membership(val, *params)
                elif tipe == "trapesium":
                    mu = trapezoidal_membership(val, *params)
                else:
                    mu = 0.0
                memberships[var_name][himpunan_nama] = round(float(mu), 4)

        return memberships

    def evaluate_rules(
        self,
        memberships: Dict[str, Dict[str, float]],
        rules: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Mengevaluasi aturan fuzzy menggunakan operator AND (minimum).
        Mengembalikan daftar aturan yang aktif (alpha > 0).
        """
        active_rules = []
        for r in rules:
            kondisi = r["kondisi"]
            # Hitung nilai minimum dari semua kondisi yang ada dalam aturan
            alphas = []
            for var_nama, himpunan_nama in kondisi.items():
                if var_nama in memberships and himpunan_nama in memberships[var_nama]:
                    alphas.append(memberships[var_nama][himpunan_nama])
                else:
                    # Jika ada variabel kondisi yang tidak tersedia
                    alphas.append(0.0)

            alpha = min(alphas) if alphas else 0.0
            if alpha > 0.0:
                active_rules.append({
                    "id": r["id"],
                    "nama": r["nama"],
                    "alpha": round(float(alpha), 4),
                    "output": r["output"],
                })

        return active_rules

    def aggregate_and_defuzzify(self, active_rules: List[Dict[str, Any]]) -> Tuple[float, np.ndarray]:
        """
        Melakukan agregasi pemotongan (clipping/min) dan penggabungan (max),
        kemudian menghitung defuzzifikasi centroid z*.
        """
        # Inisialisasi kurva agregasi dengan nilai 0
        aggregated = np.zeros_like(self.z_domain, dtype=float)

        for rule in active_rules:
            alpha = rule["alpha"]
            out_label = rule["output"]
            if out_label in self.output_mf:
                clipped = np.minimum(alpha, self.output_mf[out_label])
                aggregated = np.maximum(aggregated, clipped)

        # Defuzzifikasi Centroid: z* = sum(mu(z) * z) / sum(mu(z))
        total_mu = np.sum(aggregated)
        if total_mu <= 0.0:
            return 0.0, aggregated

        z_star = np.sum(aggregated * self.z_domain) / total_mu
        return round(float(z_star), 1), aggregated

    def generate_reason(
        self,
        laptop: Dict[str, Any],
        memberships: Dict[str, Dict[str, float]],
        kebutuhan: str
    ) -> str:
        """
        Membangun kalimat alasan rekomendasi berdasarkan derajat keanggotaan tertinggi
        dan profil kebutuhan pengguna.
        """
        # Cari himpunan dengan derajat keanggotaan tertinggi untuk masing-masing variabel
        def top_set(var: str) -> str:
            var_dict = memberships.get(var, {})
            if not var_dict:
                return ""
            return max(var_dict.items(), key=lambda item: item[1])[0]

        top_harga = top_set("rasio_harga")
        top_ram = top_set("ram_gb")
        top_cpu = top_set("skor_prosesor")
        top_storage = top_set("penyimpanan_gb")

        bagian_alasan = []

        # Alasan RAM
        if top_ram == "Besar":
            bagian_alasan.append(f"RAM besar {laptop['ram_gb']} GB yang leluasa untuk multitasking")
        elif top_ram == "Sedang":
            bagian_alasan.append(f"RAM memadai {laptop['ram_gb']} GB")
        else:
            bagian_alasan.append(f"RAM {laptop['ram_gb']} GB")

        # Alasan Prosesor
        if top_cpu == "Tinggi":
            bagian_alasan.append(f"prosesor bertenaga tinggi (skor performa {laptop['skor_prosesor']}/10)")
        elif top_cpu == "Sedang":
            bagian_alasan.append(f"prosesor cukup gesit (skor {laptop['skor_prosesor']}/10)")
        else:
            bagian_alasan.append(f"prosesor efisien (skor {laptop['skor_prosesor']}/10)")

        # Alasan Penyimpanan
        tipe_storage = laptop.get("tipe_penyimpanan", "SSD")
        storage_gb = laptop.get("penyimpanan_gb", 512)
        storage_str = f"{storage_gb // 1000} TB" if storage_gb >= 1000 else f"{storage_gb} GB"
        if top_storage == "Besar":
            bagian_alasan.append(f"penyimpanan luas {storage_str} {tipe_storage}")
        else:
            bagian_alasan.append(f"penyimpanan {storage_str} {tipe_storage}")

        # Alasan Harga
        if top_harga == "Hemat":
            bagian_alasan.append("harga sangat ramah kantong di bawah anggaran")
        elif top_harga == "Sesuai":
            bagian_alasan.append("harga sesuai anggaran")
        else:
            bagian_alasan.append("spesifikasi unggul mendekati batas anggaran")

        gabungan = ", ".join(bagian_alasan)

        profil = PROFIL_KEBUTUHAN.get(kebutuhan, {})
        fokus = profil.get("deskripsi_kebutuhan", "kegiatan perkuliahan")

        return f"{gabungan.capitalize()}, sangat mendukung {fokus}."

    def evaluate_laptop(
        self,
        laptop: Dict[str, Any],
        anggaran_maks: float,
        kebutuhan: str,
        use_battery: bool = False,
        include_detail: bool = False
    ) -> Dict[str, Any]:
        """
        Memproses satu laptop melalui seluruh rangkaian Fuzzy Mamdani.
        Mengembalikan kamus hasil rekomendasi untuk laptop tersebut.
        """
        harga = float(laptop["harga"])
        rasio_harga = harga / float(anggaran_maks) if anggaran_maks > 0 else 2.0

        fuzzy_inputs = {
            "rasio_harga": rasio_harga,
            "ram_gb": float(laptop["ram_gb"]),
            "skor_prosesor": float(laptop["skor_prosesor"]),
            "penyimpanan_gb": float(laptop["penyimpanan_gb"]),
        }
        if use_battery:
            fuzzy_inputs["baterai_jam"] = float(laptop.get("baterai_jam", 6.0))

        # 1. Fuzzifikasi
        memberships = self.fuzzify(fuzzy_inputs, use_battery=use_battery)

        # 2. Evaluasi aturan
        rules = dapatkan_aturan(gunakan_baterai=use_battery)
        active_rules = self.evaluate_rules(memberships, rules)

        # 3 & 4. Agregasi dan Defuzzifikasi
        skor_akhir, _ = self.aggregate_and_defuzzify(active_rules)

        # 5. Label skor
        label = dapatkan_label_skor(skor_akhir)

        # Alasan rekomendasi
        alasan = self.generate_reason(laptop, memberships, kebutuhan)

        hasil = {
            "id": laptop["id"],
            "nama_laptop": laptop["nama_laptop"],
            "merek": laptop["merek"],
            "harga": laptop["harga"],
            "ram_gb": laptop["ram_gb"],
            "penyimpanan_gb": laptop["penyimpanan_gb"],
            "tipe_penyimpanan": laptop["tipe_penyimpanan"],
            "skor_prosesor": laptop["skor_prosesor"],
            "gpu": laptop.get("gpu", "-"),
            "ukuran_layar": laptop.get("ukuran_layar", 14.0),
            "berat_kg": laptop.get("berat_kg", 1.5),
            "baterai_jam": laptop.get("baterai_jam", 6.0),
            "kategori_penggunaan": laptop.get("kategori_penggunaan", "kuliah_umum"),
            "sumber": laptop.get("sumber", ""),
            "tanggal_data": laptop.get("tanggal_data", ""),
            "skor_rekomendasi": skor_akhir,
            "label": label,
            "alasan": alasan,
        }

        if include_detail:
            hasil["detail_fuzzy"] = {
                "inputs_ternormalisasi": {
                    "rasio_harga": round(rasio_harga, 4),
                    "ram_gb": laptop["ram_gb"],
                    "skor_prosesor": laptop["skor_prosesor"],
                    "penyimpanan_gb": laptop["penyimpanan_gb"],
                    **({"baterai_jam": laptop.get("baterai_jam", 6.0)} if use_battery else {}),
                },
                "derajat_keanggotaan": memberships,
                "aturan_aktif": active_rules,
            }

        return hasil


# Instance global default fuzzy engine
fuzzy_engine = FuzzyEngine()


def filter_and_rank_laptops(
    laptops: List[Dict[str, Any]],
    anggaran_maks: float,
    kebutuhan: str = "kuliah_umum",
    ram_min_gb: Optional[int] = None,
    penyimpanan_min_gb: Optional[int] = None,
    performa_prosesor: Optional[str] = None,
    prioritas_baterai: bool = False,
    include_detail: bool = False,
    max_results: int = 10
) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    """
    Menyaring dan meranking daftar laptop berdasarkan preferensi dan metode fuzzy.

    Return:
        (hasil_laptop, pesan_opsional)
    """
    # Terapkan profil default jika pengguna tidak menetapkan preferensi minimum
    profil = PROFIL_KEBUTUHAN.get(kebutuhan, PROFIL_KEBUTUHAN["kuliah_umum"])
    eff_ram_min = ram_min_gb if ram_min_gb is not None else profil["ram_min_default"]
    eff_storage_min = penyimpanan_min_gb if penyimpanan_min_gb is not None else profil["penyimpanan_min_default"]

    # Pemetaan preferensi performa prosesor ke skor minimal
    prosesor_min_skor = 1
    prosesor_preferensi = performa_prosesor or profil["prosesor_min_default"]
    if prosesor_preferensi == "tinggi":
        prosesor_min_skor = 7
    elif prosesor_preferensi == "sedang":
        prosesor_min_skor = 4
    else:
        prosesor_min_skor = 1

    # Langkah 1: Penyaringan (Filter) berdasarkan preferensi pengguna
    kandidat_lolos = []
    for l in laptops:
        if l["ram_gb"] >= eff_ram_min and l["penyimpanan_gb"] >= eff_storage_min and l["skor_prosesor"] >= prosesor_min_skor:
            kandidat_lolos.append(l)

    pesan_fallback: Optional[str] = None
    target_laptops = kandidat_lolos

    # Jika tidak ada yang lolos filter, jangan error: fallback ke 5 laptop terdekat
    if not kandidat_lolos:
        pesan_fallback = (
            f"Tidak ditemukan laptop yang memenuhi spesifikasi minimum (RAM >= {eff_ram_min} GB, "
            f"Penyimpanan >= {eff_storage_min} GB, Prosesor min '{prosesor_preferensi}'). "
            "Sistem menyarankan untuk melonggarkan filter preferensi Anda. "
            "Berikut ditampilkan 5 alternatif laptop terbaik berdasarkan skor kelayakan."
        )
        target_laptops = laptops  # Nilai seluruh laptop untuk diambil 5 teratas

    # Langkah 2: Hitung skor fuzzy untuk setiap laptop target
    hasil_dinilai = []
    for laptop in target_laptops:
        hasil = fuzzy_engine.evaluate_laptop(
            laptop=laptop,
            anggaran_maks=anggaran_maks,
            kebutuhan=kebutuhan,
            use_battery=prioritas_baterai,
            include_detail=include_detail
        )
        hasil_dinilai.append(hasil)

    # Langkah 3: Urutkan hasil berdasarkan skor rekomendasi secara menurun (descending)
    hasil_dinilai.sort(key=lambda x: x["skor_rekomendasi"], reverse=True)

    # Batasi jumlah output (5 jika fallback, atau max_results jika normal)
    limit = 5 if pesan_fallback else max_results
    hasil_akhir = hasil_dinilai[:limit]

    return hasil_akhir, pesan_fallback
