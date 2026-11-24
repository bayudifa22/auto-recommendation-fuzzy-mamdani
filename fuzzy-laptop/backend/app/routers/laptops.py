"""
Router endpoint untuk data laptop.
Menyediakan endpoint untuk membaca daftar laptop dan melihat detail spesifik satu laptop.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status

from app.data_loader import data_loader
from app.schemas import LaptopBase

router = APIRouter(prefix="/api/laptops", tags=["Laptops"])


@router.get(
    "",
    response_model=List[LaptopBase],
    summary="Mengambil semua data laptop",
    description="Mengembalikan seluruh data laptop yang terdaftar di sistem. Mendukung filter berdasarkan merek atau kategori."
)
def get_all_laptops(
    merek: Optional[str] = Query(None, description="Filter berdasarkan nama merek laptop"),
    kategori: Optional[str] = Query(None, description="Filter berdasarkan kategori penggunaan"),
    q: Optional[str] = Query(None, description="Pencarian kata kunci pada nama laptop")
):
    laptops = data_loader.get_all()

    if merek:
        merek_lower = merek.strip().lower()
        laptops = [l for l in laptops if l["merek"].lower() == merek_lower]

    if kategori:
        kategori_lower = kategori.strip().lower()
        laptops = [l for l in laptops if l["kategori_penggunaan"].lower() == kategori_lower]

    if q:
        query_lower = q.strip().lower()
        laptops = [l for l in laptops if query_lower in l["nama_laptop"].lower()]

    return laptops


@router.get(
    "/{laptop_id}",
    response_model=LaptopBase,
    summary="Mengambil detail satu laptop",
    description="Mengembalikan detail spesifikasi lengkap laptop berdasarkan ID unik."
)
def get_laptop_by_id(laptop_id: int):
    laptop = data_loader.get_by_id(laptop_id)
    if not laptop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Laptop dengan ID {laptop_id} tidak ditemukan dalam sistem."
        )
    return laptop
