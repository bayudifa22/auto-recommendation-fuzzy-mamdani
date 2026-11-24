"""
Unit and Integration Test untuk API Router dan Skema Pydantic.
Menguji endpoint functions, skema validasi input, penanganan error 404,
kasus fallback tanpa hasil, dan determinisme hasil rekomendasi.
"""

import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from app.main import health_check
from app.routers.laptops import get_all_laptops, get_laptop_by_id
from app.routers.recommendations import create_recommendations, get_method_info
from app.schemas import RecommendationRequest, RecommendationResponse


def test_health_check_function():
    """Memverifikasi fungsi health check mengembalikan status 'ok' dan total dataset 40."""
    res = health_check()
    assert res["status"] == "ok"
    assert res["dataset_total"] == 40
    assert "Sistem Rekomendasi Laptop" in res["app"]


def test_get_all_laptops_and_filters():
    """Memverifikasi pengambilan seluruh data laptop dan filtering berdasarkan merek & kategori."""
    all_items = get_all_laptops(merek=None, kategori=None, q=None)
    assert len(all_items) == 40

    # Filter merek
    asus_items = get_all_laptops(merek="Asus", kategori=None, q=None)
    assert len(asus_items) > 0
    for item in asus_items:
        assert item["merek"].lower() == "asus"

    # Filter kategori
    prog_items = get_all_laptops(merek=None, kategori="programming", q=None)
    assert len(prog_items) > 0
    for item in prog_items:
        assert item["kategori_penggunaan"].lower() == "programming"

    # Pencarian kata kunci
    query_items = get_all_laptops(merek=None, kategori=None, q="MacBook")
    assert len(query_items) >= 3
    for item in query_items:
        assert "macbook" in item["nama_laptop"].lower()


def test_get_laptop_by_id_success_and_404():
    """Memverifikasi get_laptop_by_id mengembalikan objek laptop atau 404 jika tidak ditemukan."""
    laptop_1 = get_laptop_by_id(1)
    assert laptop_1["id"] == 1
    assert "nama_laptop" in laptop_1

    with pytest.raises(HTTPException) as excinfo:
        get_laptop_by_id(99999)
    assert excinfo.value.status_code == 404
    assert "tidak ditemukan" in excinfo.value.detail.lower()


def test_recommendation_valid_request():
    """Memverifikasi pemrosesan rekomendasi dengan input valid menghasilkan peringkat skor menurun."""
    req = RecommendationRequest(
        anggaran_maks=12000000,
        kebutuhan="programming",
        ram_min_gb=8,
        penyimpanan_min_gb=256,
        performa_prosesor="sedang",
        prioritas_baterai=False,
        include_detail=True,
    )
    res: RecommendationResponse = create_recommendations(req)

    assert res.total > 0
    assert len(res.hasil) <= 10

    # Memastikan urutan skor menurun
    skors = [item.skor_rekomendasi for item in res.hasil]
    assert skors == sorted(skors, reverse=True)

    # Memastikan detail fuzzy disertakan jika diminta
    top_laptop = res.hasil[0]
    assert top_laptop.detail_fuzzy is not None
    assert "derajat_keanggotaan" in top_laptop.detail_fuzzy
    assert "aturan_aktif" in top_laptop.detail_fuzzy


def test_recommendation_deterministic():
    """Memverifikasi sifat deterministik dari endpoint rekomendasi."""
    req = RecommendationRequest(
        anggaran_maks=10000000,
        kebutuhan="kuliah_umum",
    )
    res1 = create_recommendations(req)
    res2 = create_recommendations(req)

    assert res1.total == res2.total
    assert res1.hasil[0].id == res2.hasil[0].id
    assert res1.hasil[0].skor_rekomendasi == res2.hasil[0].skor_rekomendasi


def test_recommendation_fallback_on_empty_filter():
    """Memverifikasi fallback ketika filter menyaring seluruh dataset."""
    req = RecommendationRequest(
        anggaran_maks=5000000,
        kebutuhan="desain_grafis",
        ram_min_gb=64,  # filter sangat ketat yang tidak dipenuhi laptop manapun di budget ini
        penyimpanan_min_gb=4000,
    )
    res = create_recommendations(req)
    assert res.pesan is not None
    assert "Tidak ditemukan laptop yang memenuhi spesifikasi minimum" in res.pesan
    assert len(res.hasil) <= 5


def test_validation_negative_or_zero_budget():
    """Memverifikasi validasi Pydantic menolak anggaran <= 0."""
    with pytest.raises(ValidationError) as excinfo:
        RecommendationRequest(anggaran_maks=-5000000, kebutuhan="kuliah_umum")
    assert "Anggaran maksimum harus berupa bilangan positif" in str(excinfo.value)

    with pytest.raises(ValidationError) as excinfo:
        RecommendationRequest(anggaran_maks=0, kebutuhan="kuliah_umum")
    assert "Anggaran maksimum harus berupa bilangan positif" in str(excinfo.value)


def test_validation_low_budget():
    """Memverifikasi validasi menolak anggaran di bawah Rp 1.000.000."""
    with pytest.raises(ValidationError) as excinfo:
        RecommendationRequest(anggaran_maks=500000, kebutuhan="kuliah_umum")
    assert "minimal Rp 1.000.000" in str(excinfo.value)


def test_validation_invalid_type_budget():
    """Memverifikasi validasi menolak tipe data non-angka."""
    with pytest.raises(ValidationError):
        RecommendationRequest(anggaran_maks="sepuluh juta", kebutuhan="kuliah_umum")  # type: ignore


def test_get_method_info():
    """Memverifikasi endpoint /api/method-info mengembalikan data metodologi lengkap."""
    info = get_method_info()
    assert "Fuzzy Logic Mamdani" in info.metode
    assert len(info.tahapan) == 5
    assert "z*" in info.rumus_defuzzifikasi
    assert "rasio_harga" in info.variabel_fuzzy
    assert len(info.aturan_fuzzy) >= 12
    assert "bukan pengganti" in info.disclaimer.lower()
