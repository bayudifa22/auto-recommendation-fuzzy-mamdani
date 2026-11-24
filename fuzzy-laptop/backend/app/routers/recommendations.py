"""
Router endpoint untuk sistem rekomendasi laptop berbasis Fuzzy Mamdani
dan penyedia informasi metodologi serta dataset.
"""

from fastapi import APIRouter
from app.data_loader import data_loader
from app.schemas import (
    RecommendationRequest,
    RecommendationResponse,
    MethodInfoResponse,
)
from app.fuzzy.variables import VARIABLES_CONFIG, PROFIL_KEBUTUHAN
from app.fuzzy.rules import dapatkan_aturan
from app.fuzzy.engine import filter_and_rank_laptops

router = APIRouter(prefix="/api", tags=["Rekomendasi & Metodologi"])


@router.post(
    "/recommendations",
    response_model=RecommendationResponse,
    summary="Memproses rekomendasi laptop dengan Fuzzy Mamdani",
    description="Menerima preferensi pengguna, menjalankan fuzzifikasi, evaluasi aturan AND, agregasi clipping MAX, dan defuzzifikasi centroid."
)
def create_recommendations(req: RecommendationRequest):
    all_laptops = data_loader.get_all()

    hasil, pesan = filter_and_rank_laptops(
        laptops=all_laptops,
        anggaran_maks=float(req.anggaran_maks),
        kebutuhan=req.kebutuhan,
        ram_min_gb=req.ram_min_gb,
        penyimpanan_min_gb=req.penyimpanan_min_gb,
        performa_prosesor=req.performa_prosesor,
        prioritas_baterai=req.prioritas_baterai,
        include_detail=req.include_detail,
        max_results=10,
    )

    return RecommendationResponse(
        total=len(hasil),
        hasil=hasil,
        pesan=pesan,
    )


@router.get(
    "/method-info",
    response_model=MethodInfoResponse,
    summary="Mendapatkan informasi metodologi Fuzzy Mamdani dan dataset",
    description="Menyediakan definisi variabel, himpunan keanggotaan, basis aturan, rumus centroid, profil kebutuhan, dan disclaimer akademik."
)
def get_method_info():
    all_laptops = data_loader.get_all()
    sample_item = all_laptops[0] if all_laptops else {}

    return MethodInfoResponse(
        metode="Fuzzy Logic Mamdani (Max-Min Inference)",
        tahapan=[
            "1. Fuzzifikasi: Menghitung derajat keanggotaan setiap variabel input terhadap fungsi trapesium dan segitiga.",
            "2. Evaluasi Aturan: Menggunakan operator logika AND (minimum) untuk menghitung nilai alpha-predikat tiap aturan.",
            "3. Agregasi Implikasi: Memotong (clipping) fungsi keanggotaan output dengan nilai alpha dan menggabungkannya dengan operator maksimum (MAX).",
            "4. Defuzzifikasi Centroid: Menghitung titik pusat gravitasi (Center of Gravity / COG) dari area agregasi.",
            "5. Klasifikasi Skor: Mengelompokkan nilai akhir 0-100 ke dalam 4 kategori rekomendasi.",
        ],
        rumus_defuzzifikasi="z* = Σ ( μ(z) · z ) / Σ μ(z), dengan z ∈ [0, 100] resolusi 0.5 poin.",
        variabel_fuzzy=VARIABLES_CONFIG,
        aturan_fuzzy=dapatkan_aturan(gunakan_baterai=True),
        profil_kebutuhan=PROFIL_KEBUTUHAN,
        info_dataset={
            "total_laptop": len(all_laptops),
            "sumber_placeholder": sample_item.get("sumber", "DATA CONTOH - GANTI DENGAN DATA ASLI"),
            "tanggal_pembaruan": sample_item.get("tanggal_data", "2026-11-24"),
            "keterangan": "Data ini adalah dataset contoh placeholder untuk simulasi pengujian UAS. Pengguna dapat menggantinya dengan dataset riil di data/dataset_laptop.csv.",
        },
        disclaimer=(
            "Aplikasi sistem rekomendasi ini dibangun untuk keperluan akademik (Project UAS Kecerdasan Buatan). "
            "Skor rekomendasi dihasilkan berdasarkan pemodelan inferensi Fuzzy Mamdani dan tidak mencerminkan ketersediaan stok riil atau promo harga terkini. "
            "Rekomendasi ini bukan pengganti konsultasi profesional atau review teknis mendalam."
        )
    )
