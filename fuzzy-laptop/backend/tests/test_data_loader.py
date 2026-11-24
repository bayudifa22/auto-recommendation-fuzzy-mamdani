"""
Unit test untuk modul data_loader.
"""

import tempfile
from pathlib import Path
import pytest
import pandas as pd
from app.data_loader import DataLoader, KOLOM_WAJIB, DEFAULT_DATA_PATH


def test_load_default_dataset():
    """Memastikan dataset default dapat dimuat dengan tepat 40 baris dan kolom lengkap."""
    loader = DataLoader(DEFAULT_DATA_PATH)
    data = loader.load_data()
    assert len(data) == 40
    for row in data:
        for col in KOLOM_WAJIB:
            assert col in row
        assert row["harga"] > 0
        assert 1 <= row["skor_prosesor"] <= 10
        assert row["ram_gb"] > 0
        assert row["penyimpanan_gb"] > 0


def test_get_by_id():
    """Memastikan pengambilan data berdasarkan ID berhasil dan mengembalikan None jika tidak ditemukan."""
    loader = DataLoader(DEFAULT_DATA_PATH)
    laptop_1 = loader.get_by_id(1)
    assert laptop_1 is not None
    assert laptop_1["id"] == 1

    laptop_none = loader.get_by_id(9999)
    assert laptop_none is None


def test_validation_missing_column():
    """Memastikan DataLoader melempar ValueError bila ada kolom wajib yang hilang."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        # Menulis CSV tanpa kolom 'skor_prosesor'
        f.write("id,nama_laptop,merek,harga,ram_gb,penyimpanan_gb,tipe_penyimpanan\n")
        f.write("1,Laptop A,MerekX,5000000,8,512,SSD\n")
        temp_path = Path(f.name)

    try:
        loader = DataLoader(temp_path)
        with pytest.raises(ValueError, match="Dataset tidak lengkap"):
            loader.load_data()
    finally:
        temp_path.unlink(missing_ok=True)


def test_validation_duplicate_id():
    """Memastikan DataLoader melempar ValueError jika terdapat duplikasi ID."""
    df = pd.read_csv(DEFAULT_DATA_PATH).head(3).copy()
    df.loc[1, "id"] = df.loc[0, "id"]  # buat duplikat id

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        df.to_csv(f.name, index=False)
        temp_path = Path(f.name)

    try:
        loader = DataLoader(temp_path)
        with pytest.raises(ValueError, match="Ditemukan ID duplikat"):
            loader.load_data()
    finally:
        temp_path.unlink(missing_ok=True)
