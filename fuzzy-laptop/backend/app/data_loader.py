"""
Modul pemuat dan validator dataset laptop dari file CSV.
Menyediakan akses data in-memory yang telah divalidasi untuk seluruh aplikasi.
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
import pandas as pd

# Path default ke file dataset CSV
DEFAULT_DATA_PATH = Path(__file__).resolve().parent / "data" / "dataset_laptop.csv"

# Daftar kolom yang wajib ada dalam dataset
KOLOM_WAJIB = [
    "id",
    "nama_laptop",
    "merek",
    "harga",
    "ram_gb",
    "penyimpanan_gb",
    "tipe_penyimpanan",
    "skor_prosesor",
    "gpu",
    "ukuran_layar",
    "berat_kg",
    "baterai_jam",
    "kategori_penggunaan",
    "sumber",
    "tanggal_data",
]


class DataLoader:
    """Kelas pengelola pemuatan, validasi, dan penyediaan data laptop."""

    def __init__(self, data_path: Optional[Path] = None):
        self.data_path = Path(data_path) if data_path else DEFAULT_DATA_PATH
        self._cache: Optional[List[Dict[str, Any]]] = None

    def load_data(self, force_reload: bool = False) -> List[Dict[str, Any]]:
        """
        Membaca dataset dari CSV, memvalidasi kolom dan tipe data,
        kemudian menyimpannya dalam cache memori.
        """
        if self._cache is not None and not force_reload:
            return self._cache

        if not self.data_path.exists():
            raise FileNotFoundError(f"File dataset tidak ditemukan pada path: {self.data_path}")

        df = pd.read_csv(self.data_path)

        # Validasi keberadaan kolom wajib
        missing_cols = [col for col in KOLOM_WAJIB if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Dataset tidak lengkap. Kolom hilang: {missing_cols}")

        # Validasi dataset tidak kosong
        if df.empty:
            raise ValueError("Dataset laptop kosong.")

        # Validasi tipe data dan batasan nilai
        df["id"] = df["id"].astype(int)
        df["harga"] = df["harga"].astype(int)
        df["ram_gb"] = df["ram_gb"].astype(int)
        df["penyimpanan_gb"] = df["penyimpanan_gb"].astype(int)
        df["skor_prosesor"] = df["skor_prosesor"].astype(int)
        df["ukuran_layar"] = df["ukuran_layar"].astype(float)
        df["berat_kg"] = df["berat_kg"].astype(float)
        df["baterai_jam"] = df["baterai_jam"].astype(float)

        # Periksa duplikasi ID
        if df["id"].duplicated().any():
            duplikat = df[df["id"].duplicated()]["id"].tolist()
            raise ValueError(f"Ditemukan ID duplikat pada dataset: {duplikat}")

        # Periksa batasan nilai masuk akal
        if (df["harga"] <= 0).any():
            raise ValueError("Terdapat harga laptop <= 0")
        if (df["ram_gb"] <= 0).any():
            raise ValueError("Terdapat RAM <= 0")
        if (df["penyimpanan_gb"] <= 0).any():
            raise ValueError("Terdapat penyimpanan <= 0")
        if not df["skor_prosesor"].between(1, 10).all():
            raise ValueError("Terdapat skor prosesor di luar rentang 1-10")

        # Konversi ke bentuk list of dictionaries
        records = df.to_dict(orient="records")
        self._cache = records
        return self._cache

    def get_all(self) -> List[Dict[str, Any]]:
        """Mengambil seluruh data laptop yang telah dimuat."""
        return self.load_data()

    def get_by_id(self, laptop_id: int) -> Optional[Dict[str, Any]]:
        """Mencari satu laptop berdasarkan ID unik."""
        data = self.load_data()
        for laptop in data:
            if laptop["id"] == laptop_id:
                return laptop
        return None


# Instance global tunggal untuk pemakaian bersama di router/aplikasi
data_loader = DataLoader()
