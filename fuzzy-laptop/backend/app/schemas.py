"""
Skema validasi data request dan response menggunakan Pydantic v2.
Semua pesan error divalidasi dan disajikan dalam Bahasa Indonesia yang jelas.
"""

from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field, field_validator


KebutuhanEnum = Literal[
    "kuliah_umum",
    "programming",
    "desain_grafis",
    "editing_video",
    "mobilitas_tinggi"
]

PerformaProsesorEnum = Literal["rendah", "sedang", "tinggi"]


class RecommendationRequest(BaseModel):
    """Skema input request untuk rekomendasi laptop mahasiswa."""

    anggaran_maks: int = Field(
        ...,
        description="Batas anggaran belanja laptop maksimum dalam rupiah (harus lebih besar dari 0)",
        examples=[10000000]
    )
    kebutuhan: KebutuhanEnum = Field(
        default="kuliah_umum",
        description="Profil kebutuhan utama mahasiswa",
        examples=["programming"]
    )
    ram_min_gb: Optional[int] = Field(
        default=None,
        ge=4,
        le=64,
        description="Preferensi kapasitas RAM minimum dalam GB (opsional)"
    )
    penyimpanan_min_gb: Optional[int] = Field(
        default=None,
        ge=128,
        le=4000,
        description="Preferensi kapasitas penyimpanan SSD minimum dalam GB (opsional)"
    )
    performa_prosesor: Optional[PerformaProsesorEnum] = Field(
        default=None,
        description="Preferensi performa prosesor: rendah, sedang, atau tinggi (opsional)"
    )
    prioritas_baterai: bool = Field(
        default=False,
        description="Apakah memprioritaskan daya tahan baterai sebagai variabel tambahan fuzzy"
    )
    include_detail: bool = Field(
        default=False,
        description="Apakah menyertakan rincian perhitungan fuzzy Mamdani (derajat keanggotaan & aturan aktif)"
    )

    @field_validator("anggaran_maks")
    @classmethod
    def validasi_anggaran(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Anggaran maksimum harus berupa bilangan positif lebih besar dari Rp 0.")
        if v < 1000000:
            raise ValueError("Anggaran maksimum minimal Rp 1.000.000 untuk rekomendasi laptop realistis.")
        return v


class LaptopBase(BaseModel):
    """Model data lengkap untuk satu laptop."""

    id: int
    nama_laptop: str
    merek: str
    harga: int
    ram_gb: int
    penyimpanan_gb: int
    tipe_penyimpanan: str
    skor_prosesor: int
    gpu: str
    ukuran_layar: float
    berat_kg: float
    baterai_jam: float
    kategori_penggunaan: str
    sumber: str
    tanggal_data: str


class LaptopRecommendationItem(LaptopBase):
    """Model item laptop yang telah memiliki skor dan alasan rekomendasi."""

    skor_rekomendasi: float
    label: str
    alasan: str
    detail_fuzzy: Optional[Dict[str, Any]] = None


class RecommendationResponse(BaseModel):
    """Skema response rekomendasi laptop."""

    total: int
    hasil: List[LaptopRecommendationItem]
    pesan: Optional[str] = None


class MethodInfoResponse(BaseModel):
    """Skema response informasi metodologi Fuzzy Mamdani dan dataset."""

    metode: str
    tahapan: List[str]
    rumus_defuzzifikasi: str
    variabel_fuzzy: Dict[str, Any]
    aturan_fuzzy: List[Dict[str, Any]]
    profil_kebutuhan: Dict[str, Any]
    info_dataset: Dict[str, Any]
    disclaimer: str
