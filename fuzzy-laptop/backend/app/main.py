"""
Aplikasi Utama FastAPI untuk Sistem Rekomendasi Laptop Mahasiswa.
Menangani konfigurasi CORS, routing API, penanganan error validasi kustom berbahasa Indonesia,
dan pemuatan awal dataset pada saat startup.
"""

from contextlib import asynccontextmanager
from typing import Dict, Any
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.data_loader import data_loader
from app.routers import laptops, recommendations


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Event lifecycle aplikasi: memuat dataset saat startup."""
    try:
        data = data_loader.load_data()
        print(f"[STARTUP] Dataset laptop berhasil dimuat: {len(data)} entri.")
    except Exception as e:
        print(f"[STARTUP ERROR] Gagal memuat dataset: {e}")
    yield


app = FastAPI(
    title="Sistem Rekomendasi Laptop Mahasiswa - API",
    description="Backend API Sistem Rekomendasi Laptop berbasis Logika Fuzzy Mamdani (Project UAS Kecerdasan Buatan)",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Konfigurasi CORS hanya untuk origin frontend
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Format ulang pesan error validasi Pydantic menjadi kalimat Bahasa Indonesia yang ramah.
    """
    error_messages = []
    for err in exc.errors():
        field = " -> ".join([str(x) for x in err.get("loc", []) if x != "body"])
        msg = err.get("msg", "Nilai input tidak valid.")

        # Penyesuaian pesan bawaan pydantic
        if "greater than 0" in msg or "greater than" in msg:
            msg = "harus berupa bilangan positif lebih besar dari 0."
        elif "value is not a valid integer" in msg or "input should be a valid integer" in msg:
            msg = "harus berupa angka/bilangan bulat."
        elif "Field required" in msg or "field required" in msg:
            msg = "wajib diisi dan tidak boleh kosong."

        error_messages.append(f"Kolom '{field}': {msg}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validasi input gagal.",
            "pesan_error": error_messages,
        },
    )


@app.get("/api/health", tags=["Health"])
def health_check() -> Dict[str, Any]:
    """Cek status kesehatan server API."""
    total_laptops = len(data_loader.get_all())
    return {
        "status": "ok",
        "app": "Sistem Rekomendasi Laptop Mahasiswa",
        "version": "1.0.0",
        "dataset_total": total_laptops,
    }


# Registrasi router
app.include_router(laptops.router)
app.include_router(recommendations.router)
