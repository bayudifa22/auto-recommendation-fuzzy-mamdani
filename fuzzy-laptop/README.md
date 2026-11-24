# Sistem Rekomendasi Laptop Mahasiswa (Fuzzy Mamdani)

Aplikasi web sistem pendukung keputusan rekomendasi laptop untuk mahasiswa berbasis **Logika Fuzzy Mamdani**. Sistem ini mengevaluasi batas anggaran belanja dan preferensi kebutuhan mahasiswa terhadap spesifikasi laptop menggunakan mesin inferensi fuzzy manual yang dibangun dengan **NumPy** (tanpa pustaka otomatis seperti *scikit-fuzzy*), sehingga setiap tahapan matematis transparan dan dapat dipertanggungjawabkan dalam laporan akademik.

Project ini dikembangkan untuk memenuhi tugas akhir (**Project UAS**) mata kuliah **Kecerdasan Buatan**.

---

## 🚀 Fitur Utama

1. **Inferensi Fuzzy Mamdani Transparan**:
   - Fuzzifikasi menggunakan fungsi keanggotaan trapesium dan segitiga.
   - Evaluasi aturan anteseden berbasis logika konjungsi AND (operator minimum).
   - Agregasi implikasi menggunakan pemotongan level alpha (*clipping*) dan penggabungan operator maksimum (MAX).
   - Defuzzifikasi Center of Gravity (Centroid / COG) diskrit domain $0 - 100$ dengan resolusi $0.5$ poin.
2. **Profil Kebutuhan Mahasiswa**:
   - Kuliah Umum / Office, Pemrograman / Coding, Desain Grafis, Editing Video, dan Mobilitas Tinggi.
   - Mengisi preferensi default dan menjadi konteks peracikan narasi alasan rekomendasi otomatis.
3. **Penyaringan & Fallback Ramah Pengguna**:
   - Menyaring laptop berdasarkan kriteria minimum.
   - Apabila filter pengguna terlalu ketat sehingga tidak ada laptop yang lolos, sistem tidak memunculkan pesan error, melainkan memberikan 5 alternatif terdekat beserta saran pelonggaran filter.
4. **Panel Transparansi Perhitungan (*Fuzzy Breakdown*)**:
   - Menampilkan derajat keanggotaan $\mu$, daftar aturan aktif beserta nilai $\alpha$-predikat, dan langkah centroid untuk pengujian dosen/penguji.
5. **REST API FastAPI Terstruktur**:
   - Dilengkapi validasi otomatis Pydantic v2 dengan pesan error berbahasa Indonesia.
   - Dokumentasi interaktif Swagger UI bawaan di `/docs`.
6. **Frontend Responsif**:
   - Dibangun dengan React 18, Vite, React Router v6, dan Tailwind CSS.
   - Tampilan adaptif di layar smartphone maupun komputer desktop.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.11+ / 3.13+, FastAPI, Uvicorn, Pydantic v2, NumPy, Pandas, Pytest
- **Frontend**: React 18, Vite 5, React Router DOM v6, Tailwind CSS v3, Vitest, Testing Library
- **Dataset**: File CSV (`dataset_laptop.csv`) dibaca saat startup aplikasi
- **DevOps (Opsional)**: Docker & Docker Compose

---

## 📂 Struktur Folder

```text
fuzzy-laptop/
├── backend/
│   ├── app/
│   │   ├── main.py                     # Entry point FastAPI + CORS + Exception Handler
│   │   ├── schemas.py                  # Skema validasi Pydantic v2 (Request/Response)
│   │   ├── data_loader.py              # Pemuat, parser, dan validator dataset CSV
│   │   ├── routers/
│   │   │   ├── laptops.py              # Endpoint GET /api/laptops & /api/laptops/{id}
│   │   │   └── recommendations.py      # Endpoint POST /api/recommendations & GET /api/method-info
│   │   ├── fuzzy/
│   │   │   ├── membership.py           # Fungsi keanggotaan segitiga & trapesium NumPy
│   │   │   ├── variables.py            # Variabel input/output, domain & profil kebutuhan
│   │   │   ├── rules.py                # Basis 12 aturan fuzzy tersimpan sebagai list data
│   │   │   └── engine.py               # Fuzzifikasi, inferensi, clipping, centroid COG
│   │   └── data/
│   │       ├── dataset_laptop.csv      # Dataset 40 data laptop contoh
│   │       └── kasus_uji_fuzzy.csv     # Ekspor hasil uji 8 skenario
│   ├── scripts/
│   │   └── export_kasus_uji.py         # Skrip ekspor 8 skenario pengujian ke CSV
│   ├── tests/
│   │   ├── test_data_loader.py         # Unit test dataset & validasi ID/kolom
│   │   ├── test_fuzzy_membership.py    # Unit test kurva segitiga & trapesium
│   │   ├── test_fuzzy_engine.py        # Unit test inferensi & 5 kasus hitung manual
│   │   └── test_api.py                 # Integration test endpoint REST API
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/                 # Navbar, Footer, LaptopCard, ScoreBadge, FuzzyDetailPanel
│   │   ├── pages/                      # Home, FormRekomendasi, Hasil, DetailLaptop, Tentang, Katalog
│   │   ├── services/
│   │   │   └── api.js                  # Klien HTTP fetch dengan baseURL dinamis
│   │   ├── test/                       # Unit test Vitest (FormRekomendasi & LaptopCard)
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
├── docker-compose.yml
└── README.md
```

---

## ⚙️ Prasyarat Sistem

- **Python**: Versi 3.11 atau lebih baru (direkomendasikan Python 3.11 – 3.13)
- **Node.js**: Versi 18 atau lebih baru (direkomendasikan Node.js 20+)
- **NPM**: Versi 9+

---

## 🏃 Cara Instalasi dan Menjalankan Aplikasi

### 1. Menjalankan Backend (FastAPI)

Buka terminal baru di folder `fuzzy-laptop/backend`:

```bash
cd fuzzy-laptop/backend

# (Opsional) Buat dan aktifkan virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependensi
pip install -r requirements.txt

# Jalankan server FastAPI dengan Uvicorn
uvicorn app.main:app --reload --port 8000
```

Server backend akan berjalan di:
- **API Base URL**: `http://localhost:8000`
- **Dokumentasi Swagger UI**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/api/health`

### 2. Menjalankan Frontend (React + Vite)

Buka terminal terpisah di folder `fuzzy-laptop/frontend`:

```bash
cd fuzzy-laptop/frontend

# Install dependensi JavaScript
npm install

# Jalankan dev server Vite
npm run dev
```

Aplikasi frontend akan aktif di:
- **Web App**: `http://localhost:5173`

---

## 🧪 Menjalankan Pengujian Otomatis (Testing)

### Pengujian Backend (pytest)
Semua unit test matematika fuzzy, pemuatan dataset, dan endpoint API dapat dijalankan dengan:

```bash
# Dari folder fuzzy-laptop/backend
pytest -v
```
*Total 26 test suite mencakup fungsi keanggotaan, perhitungan 5 kasus uji manual, validasi skema error 422, dan endpoint API.*

### Pengujian Frontend (Vitest)
Unit test komponen form validasi dan rendering kartu laptop dijalankan dengan:

```bash
# Dari folder fuzzy-laptop/frontend
npm test
```

### Ekspor Kasus Uji ke CSV (Untuk Perbandingan Spreadsheet / Laporan Dosen)
Jalankan skrip ekspor 8 skenario:

```bash
python fuzzy-laptop/backend/scripts/export_kasus_uji.py
```
Output tersimpan di `fuzzy-laptop/backend/data/kasus_uji_fuzzy.csv`.

---

## 🐳 Menjalankan dengan Docker Compose (Opsional)

Jika Docker terpasang di komputer Anda, jalankan seluruh backend dan frontend hanya dengan satu perintah:

```bash
cd fuzzy-laptop
docker compose up --build
```
Aplikasi web siap diakses di `http://localhost:5173` dan backend API di `http://localhost:8000`.

---

## 📡 Contoh Request cURL ke REST API

### 1. Cek Kesehatan Server
```bash
curl -X GET "http://localhost:8000/api/health"
```

### 2. Meminta Rekomendasi Laptop
```bash
curl -X POST "http://localhost:8000/api/recommendations" \
     -H "Content-Type: application/json" \
     -d '{
       "anggaran_maks": 12000000,
       "kebutuhan": "programming",
       "ram_min_gb": 8,
       "penyimpanan_min_gb": 512,
       "performa_prosesor": "sedang",
       "prioritas_baterai": false,
       "include_detail": true
     }'
```

### 3. Mengambil Detail Satu Laptop
```bash
curl -X GET "http://localhost:8000/api/laptops/1"
```

### 4. Mengambil Metadata Metodologi Fuzzy
```bash
curl -X GET "http://localhost:8000/api/method-info"
```

---

## 📊 Cara Mengganti / Memperbarui Dataset

Dataset laptop disimpan dalam file CSV:
`fuzzy-laptop/backend/app/data/dataset_laptop.csv`

Format kolom yang **wajib** dipertahankan:
1. `id`: Integer unik
2. `nama_laptop`: String nama dan seri laptop
3. `merek`: String merek (Asus, Acer, Lenovo, HP, Dell, Apple, dll.)
4. `harga`: Integer harga dalam Rupiah (mis. 8500000)
5. `ram_gb`: Integer kapasitas RAM dalam GB (mis. 8, 16)
6. `penyimpanan_gb`: Integer kapasitas penyimpanan dalam GB (mis. 256, 512, 1000)
7. `tipe_penyimpanan`: String (SSD / HDD)
8. `skor_prosesor`: Integer nilai performa skala 1 sampai 10
9. `gpu`: String jenis kartu grafis
10. `ukuran_layar`: Float ukuran layar dalam inci (mis. 14.0)
11. `berat_kg`: Float bobot laptop dalam kg (mis. 1.45)
12. `baterai_jam`: Float perkiraan daya tahan baterai dalam jam (mis. 7.5)
13. `kategori_penggunaan`: String (`kuliah_umum`, `programming`, `desain_grafis`, `editing_video`, `mobilitas_tinggi`)
14. `sumber`: String sumber rujukan data
15. `tanggal_data`: Format tanggal `YYYY-MM-DD`

Setelah memperbarui file CSV, muat ulang server backend (uvicorn akan me-reload otomatis).

---

## 📌 Asumsi yang Digunakan

1. **Rasio Harga**: Dihitung sebagai $\text{harga\_laptop} / \text{anggaran\_maks}$. Jika rasio $\le 0.85$ tergolong *Hemat*, $0.7 - 1.1$ tergolong *Sesuai*, dan $\ge 0.95$ tergolong *Melebihi*.
2. **Skor Prosesor**: Menggunakan skala ternormalisasi $1 - 10$ yang merepresentasikan kelas prosesor (1-3: prosesor hemat daya tugas dasar; 4-7: prosesor komputasi harian dan multitasking menengah; 8-10: prosesor berperforma tinggi untuk tugas berat).
3. **Penyimpanan**: Satuan penyimpanan menggunakan Gigabyte (GB), di mana 1 TB ditulis sebagai 1000 GB untuk konsistensi perhitungan keanggotaan fuzzy.
4. **Variabel Baterai**: Berfungsi sebagai variabel ekstensi opsional saat pengguna mengaktifkan toggle prioritas daya tahan baterai pada form rekomendasi.
5. **Kondisi Tanpa Hasil (Fallback)**: Jika spesifikasi minimum yang diminta pengguna menyaring seluruh isi dataset, sistem mengambil 5 laptop dengan skor kelayakan tertinggi dari seluruh dataset disertai pesan saran pelonggaran filter agar pengguna tetap mendapatkan rekomendasi alternatif.

---

## ⚠️ Batasan Produk

- **Harga Tidak Real-Time**: Harga laptop pada dataset merupakan harga referensi pasar saat data dikumpulkan dan tidak terhubung langsung dengan API live toko daring atau marketplace.
- **Dataset Terbatas**: Dataset awal berisi 40 entri data contoh sebagai representasi simulasi akademik untuk menguji metode inferensi Fuzzy Mamdani.
- **Bukan Pengganti Konsultasi Profesional**: Rekomendasi dihasilkan oleh pemodelan matematis logika fuzzy berbasis spesifikasi teknis dan bukan merupakan garansi mutlak kesesuaian unit fisik di lapangan.
