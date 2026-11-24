# DOKUMENTASI SISTEM REKOMENDASI LAPTOP MAHASISWA
## Berbasis Logika Fuzzy Mamdani (Python FastAPI + React Vite)
**Mata Kuliah:** Kecerdasan Buatan (Project UAS)  
**Versi Dokumen:** 1.0  
**Tanggal:** 24 November 2026  
**Penyusun:** Senior Full-Stack AI Engineer

---

## DAFTAR ISI
1. [Pendahuluan dan Latar Belakang](#1-pendahuluan-dan-latar-belakang)
2. [Arsitektur dan Alur Sistem](#2-arsitektur-dan-alur-sistem)
3. [Landasan Teori Logika Fuzzy Mamdani](#3-landasan-teori-logika-fuzzy-mamdani)
4. [Perancangan Variabel dan Himpunan Fuzzy](#4-perancangan-variabel-dan-himpunan-fuzzy)
5. [Perancangan Basis Aturan Fuzzy (Rule Base)](#5-perancangan-basis-aturan-fuzzy-rule-base)
6. [Struktur Dataset Laptop](#6-struktur-dataset-laptop)
7. [Dokumentasi REST API](#7-dokumentasi-rest-api)
8. [Arsitektur Frontend React](#8-arsitektur-frontend-react)
9. [Hasil Pengujian Sistem](#9-hasil-pengujian-sistem)
10. [Analisis dan Pembahasan](#10-analisis-dan-pembahasan)
11. [Kesimpulan dan Batasan Sistem](#11-kesimpulan-dan-batasan-sistem)

---

## 1. Pendahuluan dan Latar Belakang

### 1.1 Latar Belakang
Pemilihan laptop bagi kalangan mahasiswa seringkali menjadi keputusan yang kompleks. Faktor yang mempengaruhi tidak hanya berpusat pada harga laptop, melainkan juga kapasitas RAM, performa prosesor, kapasitas penyimpanan (SSD), serta daya tahan baterai. Selain itu, bidang studi mahasiswa menciptakan variasi kebutuhan yang spesifik:
- Mahasiswa Ilmu Komputer/Informatika membutuhkan kapasitas RAM leluasa dan prosesor mumpuni untuk kompilasi kode dan multitasking IDE.
- Mahasiswa Desain Komunikasi Visual (DKV) atau Multimedia mengutamakan akurasi layar, GPU diskrit, dan kapasitas penyimpanan besar.
- Mahasiswa bidang sosial dan humaniora lebih mengutamakan efisiensi daya baterai, portabilitas ringan, dan keterjangkauan harga.

Metode penyaringan konvensional (*Boolean crisp filtering*) seringkali memunculkan kelemahan: laptop yang memiliki harga sedikit melampaui batas anggaran pengguna langsung dieliminasi, padahal spesifikasi dan nilai kelayakannya sangat tinggi. 

### 1.2 Tujuan Proyek
1. Mengimplementasikan penalaran cerdas **Logika Fuzzy Mamdani secara manual menggunakan NumPy** tanpa ketergantungan pada *library black-box* seperti *scikit-fuzzy*.
2. Membangun arsitektur web modern yang memisahkan backend performa tinggi (**Python FastAPI**) dengan antarmuka pengguna interaktif (**React Vite + Tailwind CSS**).
3. Memberikan transparansi matematis penuh ke hadapan penguji/dosen melalui panel rincian perhitungan derajat keanggotaan ($\mu$), evaluasi aturan aktif, dan titik defuzzifikasi *Center of Gravity*.

---

## 2. Arsitektur dan Alur Sistem

### 2.1 Diagram Alur Data (*Data Flow Diagram*)

```mermaid
flowchart TD
    A["Pengguna (Mahasiswa)"] -->|"Input Anggaran & Kebutuhan"| B["Frontend React (Vite)"]
    B -->|"Validasi Sisi Klien"| C{"Valid?"}
    C -- "Tidak" -->|"Tampilkan Error"| B
    C -- "Ya" -->|"POST /api/recommendations"| D["Backend FastAPI"]
    D -->|"Validasi Skema Pydantic v2"| E["Data Loader (CSV)"]
    E -->|"Saring Kriteria Minimum"| F{"Ada Lolos?"}
    F -- "Ya" --> G["Kandidat Laptop Terpilih"]
    F -- "Tidak" --> H["Fallback: 5 Laptop Terdekat + Pesan"]
    G --> I["Mesin Fuzzy Mamdani (NumPy)"]
    H --> I
    subgraph "Proses Fuzzy Mamdani Per Laptop"
        I1["1. Fuzzifikasi: Hitung mu"] --> I2["2. Evaluasi Aturan: min(mu)"]
        I2 --> I3["3. Agregasi Implikasi: MAX(clipping)"]
        I3 --> I4["4. Defuzzifikasi Centroid COG"]
        I4 --> I5["5. Klasifikasi Skor & Penjana Alasan"]
    end
    I --> I1
    I5 --> J["Pengurutan Ranking Skor Menurun"]
    J -->|"Response JSON"| B
    B -->|"Render Hasil & Panel Breakdown"| A
```

### 2.2 Struktur Modul Backend
Pemisahan fungsionalitas diatur secara modular:
- `app/fuzzy/membership.py`: Fungsi keanggotaan murni (segitiga dan trapesium).
- `app/fuzzy/variables.py`: Konfigurasi numerik domain dan parameter himpunan.
- `app/fuzzy/rules.py`: Basis pengetahuan (12 aturan) sebagai struktur data terindeks.
- `app/fuzzy/engine.py`: Mesin agregasi logika dan defuzzifikasi centroid.
- `app/routers/`: Penyedia endpoint HTTP RESTful.

---

## 3. Landasan Teori Logika Fuzzy Mamdani

Metode Fuzzy Mamdani (sering disebut metode *Max-Min*) diperkenalkan oleh Ebrahim Mamdani pada tahun 1975. Alur perhitungan terbagi menjadi 4 tahapan matematis:

### 3.1 Fungsi Keanggotaan (*Membership Functions*)

#### a. Fungsi Keanggotaan Segitiga (*Triangular*)
Didefinisikan oleh tiga parameter $[a, b, c]$ di mana $a \le b \le c$:
$$\mu(x) = \begin{cases} 
0, & x \le a \text{ atau } x \ge c \\
\frac{x - a}{b - a}, & a < x \le b \\
\frac{c - x}{c - b}, & b < x < c 
\end{cases}$$

#### b. Fungsi Keanggotaan Trapesium (*Trapezoidal*)
Didefinisikan oleh empat parameter $[a, b, c, d]$ di mana $a \le b \le c \le d$:
$$\mu(x) = \begin{cases} 
0, & x \le a \text{ atau } x \ge d \\
\frac{x - a}{b - a}, & a < x < b \\
1, & b \le x \le c \\
\frac{d - x}{d - c}, & c < x < d 
\end{cases}$$

### 3.2 Operasi Logika Konjungsi (AND)
Pada aturan fuzzy dengan beberapa anteseden yang dihubungkan dengan kata hubung **AND**, digunakan operasi *fuzzy intersection* (operasi minimum):
$$\alpha_k = \min \left( \mu_{A_{1}}(x_1), \mu_{A_{2}}(x_2), \dots, \mu_{A_{n}}(x_n) \right)$$
Nilai $\alpha_k$ disebut sebagai nilai $\alpha$-predikat (derajat kebenaran aturan ke-$k$).

### 3.3 Agregasi Implikasi (Metode Clipping / Max-Min)
Setiap konsekuensi aturan $C_k$ dipotong (*clipping*) setinggi $\alpha_k$:
$$\mu_{C'_k}(z) = \min \left( \alpha_k, \mu_{C_k}(z) \right)$$
Seluruh kurva aturan aktif kemudian digabungkan dengan operasi maksimum (union):
$$\mu_{\text{gabungan}}(z) = \max_{k} \left( \mu_{C'_k}(z) \right)$$

### 3.4 Defuzzifikasi Centroid (*Center of Gravity / COG*)
Defuzzifikasi mengubah kurva fuzzy agregasi $\mu_{\text{gabungan}}(z)$ menjadi satu nilai tegas (crisp value) $z^* \in [0, 100]$. Dihitung secara numerik diskrit dengan resolusi $\Delta z = 0.5$:
$$z^* = \frac{\sum_{i} \mu_{\text{gabungan}}(z_i) \cdot z_i}{\sum_{i} \mu_{\text{gabungan}}(z_i)}$$
Apabila $\sum \mu(z_i) = 0$, maka $z^* = 0$.

---

## 4. Perancangan Variabel dan Himpunan Fuzzy

Semua parameter numerik terpusat di `app/fuzzy/variables.py` agar adaptif dan mudah diuji.

| Nama Variabel | Tipe Data | Domain | Himpunan Linguistik | Bentuk Kurva | Parameter Kurva |
| :--- | :--- | :---: | :--- | :---: | :--- |
| **rasio_harga** | Input | $[0.0, 2.0]$ | **Hemat**<br>**Sesuai**<br>**Melebihi** | Trapesium<br>Segitiga<br>Trapesium | $[0.0, 0.0, 0.6, 0.85]$<br>$[0.7, 0.9, 1.1]$<br>$[0.95, 1.15, 2.0, 2.0]$ |
| **ram_gb** | Input | $[0.0, 64.0]$ | **Kecil**<br>**Sedang**<br>**Besar** | Trapesium<br>Segitiga<br>Trapesium | $[0.0, 0.0, 4.0, 8.0]$<br>$[6.0, 10.0, 16.0]$<br>$[12.0, 16.0, 64.0, 64.0]$ |
| **skor_prosesor** | Input | $[1.0, 10.0]$ | **Rendah**<br>**Sedang**<br>**Tinggi** | Trapesium<br>Segitiga<br>Trapesium | $[0.0, 0.0, 2.0, 4.0]$<br>$[3.0, 5.0, 7.0]$<br>$[6.0, 8.0, 10.0, 10.0]$ |
| **penyimpanan_gb** | Input | $[0, 4000]$ | **Kecil**<br>**Sedang**<br>**Besar** | Trapesium<br>Segitiga<br>Trapesium | $[0, 0, 128, 256]$<br>$[200, 384, 512]$<br>$[400, 768, 4000, 4000]$ |
| **baterai_jam** *(opsional)* | Input | $[0.0, 24.0]$ | **Pendek**<br>**Sedang**<br>**Lama** | Trapesium<br>Segitiga<br>Trapesium | $[0.0, 0.0, 3.0, 5.0]$<br>$[4.0, 7.0, 10.0]$<br>$[8.0, 12.0, 24.0, 24.0]$ |
| **skor_rekomendasi** | Output | $[0.0, 100.0]$ | **Rendah**<br>**Sedang**<br>**Tinggi** | Trapesium<br>Segitiga<br>Trapesium | $[0.0, 0.0, 20.0, 40.0]$<br>$[30.0, 50.0, 70.0]$<br>$[60.0, 80.0, 100.0, 100.0]$ |

### Kategori Label Skor Rekomendasi
- $80.0 - 100.0$: **Sangat direkomendasikan** (Badge Hijau Zamrud)
- $60.0 - 79.9$: **Direkomendasikan** (Badge Biru Indigo)
- $40.0 - 59.9$: **Cukup direkomendasikan** (Badge Amber / Kuning)
- $0.0 - 39.9$: **Kurang direkomendasikan** (Badge Merah Mawar)

---

## 5. Perancangan Basis Aturan Fuzzy (Rule Base)

Aturan direpresentasikan sebagai objek data terstruktur di `app/fuzzy/rules.py`:

```python
RULES_BASE = [
    # R1: Harga Hemat, RAM Besar, Prosesor Tinggi -> Tinggi
    {"id": "R1", "kondisi": {"rasio_harga": "Hemat", "ram_gb": "Besar", "skor_prosesor": "Tinggi"}, "output": "Tinggi"},
    # R2: Harga Sesuai, RAM Besar, Prosesor Tinggi -> Tinggi
    {"id": "R2", "kondisi": {"rasio_harga": "Sesuai", "ram_gb": "Besar", "skor_prosesor": "Tinggi"}, "output": "Tinggi"},
    # R3: Harga Hemat, RAM Sedang, Prosesor Sedang -> Sedang
    {"id": "R3", "kondisi": {"rasio_harga": "Hemat", "ram_gb": "Sedang", "skor_prosesor": "Sedang"}, "output": "Sedang"},
    # R4: Harga Sesuai, RAM Sedang, Prosesor Sedang -> Sedang
    {"id": "R4", "kondisi": {"rasio_harga": "Sesuai", "ram_gb": "Sedang", "skor_prosesor": "Sedang"}, "output": "Sedang"},
    # R5: Harga Melebihi, RAM Kecil, Prosesor Rendah -> Rendah
    {"id": "R5", "kondisi": {"rasio_harga": "Melebihi", "ram_gb": "Kecil", "skor_prosesor": "Rendah"}, "output": "Rendah"},
    # R6: Prosesor Tinggi, Penyimpanan Besar -> Tinggi
    {"id": "R6", "kondisi": {"skor_prosesor": "Tinggi", "penyimpanan_gb": "Besar"}, "output": "Tinggi"},
    # R7: RAM Kecil, Penyimpanan Kecil -> Rendah
    {"id": "R7", "kondisi": {"ram_gb": "Kecil", "penyimpanan_gb": "Kecil"}, "output": "Rendah"},
    # R8: Harga Melebihi, Prosesor Tinggi, RAM Besar -> Sedang
    {"id": "R8", "kondisi": {"rasio_harga": "Melebihi", "skor_prosesor": "Tinggi", "ram_gb": "Besar"}, "output": "Sedang"},
    # R9: Harga Hemat, RAM Besar, Penyimpanan Besar -> Tinggi
    {"id": "R9", "kondisi": {"rasio_harga": "Hemat", "ram_gb": "Besar", "penyimpanan_gb": "Besar"}, "output": "Tinggi"},
    # R10: Harga Sesuai, Penyimpanan Sedang, RAM Sedang -> Sedang
    {"id": "R10", "kondisi": {"rasio_harga": "Sesuai", "penyimpanan_gb": "Sedang", "ram_gb": "Sedang"}, "output": "Sedang"},
    # R11: Harga Melebihi, RAM Sedang -> Rendah
    {"id": "R11", "kondisi": {"rasio_harga": "Melebihi", "ram_gb": "Sedang"}, "output": "Rendah"},
    # R12: Prosesor Rendah, RAM Kecil -> Rendah
    {"id": "R12", "kondisi": {"skor_prosesor": "Rendah", "ram_gb": "Kecil"}, "output": "Rendah"},
]
```

---

## 6. Struktur Dataset Laptop

Dataset tersimpan di `app/data/dataset_laptop.csv` dan memuat **40 data laptop contoh realistis** dengan variasi harga 3 – 25 juta rupiah dari 9 merek terkemuka (Asus, Lenovo, Acer, HP, Dell, Apple, MSI, Advan, Axioo).

### Kamus Data
| Nama Kolom | Tipe Data | Keterangan & Batasan |
| :--- | :--- | :--- |
| `id` | Integer | Kunci primer unik, tidak boleh duplikat |
| `nama_laptop` | String | Nama model dan varian laptop |
| `merek` | String | Produsen (Asus, Lenovo, HP, Acer, Dell, Apple, MSI, Advan, Axioo) |
| `harga` | Integer | Harga pasar referensi dalam satuan Rupiah ($> 0$) |
| `ram_gb` | Integer | Kapasitas memori utama ($4, 8, 12, 16, 18, 32$) |
| `penyimpanan_gb` | Integer | Kapasitas media simpan ($128, 256, 512, 1000$) |
| `tipe_penyimpanan`| String | SSD / eMMC / NVMe |
| `skor_prosesor` | Integer | Skor performa ternormalisasi skala 1 – 10 |
| `gpu` | String | Nama kartu grafis terintegrasi / diskrit |
| `ukuran_layar` | Float | Diagonal layar dalam satuan inci |
| `berat_kg` | Float | Bobot unit dalam satuan kilogram |
| `baterai_jam` | Float | Estimasi daya tahan pemakaian dalam jam |
| `kategori_penggunaan`| String | `kuliah_umum`, `programming`, `desain_grafis`, `editing_video`, `mobilitas_tinggi` |
| `sumber` | String | Status metadata rujukan data |
| `tanggal_data` | Date | Tanggal pembaruan data (`YYYY-MM-DD`) |

---

## 7. Dokumentasi REST API

Backend FastAPI menyajikan dokumentasi OpenAPI interaktif bawaan di `http://localhost:8000/docs`.

### 7.1 Daftar Endpoint
- `GET /api/health`: Status operasional server dan jumlah dataset.
- `GET /api/laptops`: Mengambil seluruh daftar laptop (mendukung filter query `?merek=`, `?kategori=`, dan `?q=`).
- `GET /api/laptops/{id}`: Mengambil spesifikasi lengkap satu laptop (mengembalikan 404 jika ID tidak ada).
- `POST /api/recommendations`: Mengirim preferensi pengguna dan menerima perangkingan Fuzzy Mamdani.
- `GET /api/method-info`: Metadata parameter fuzzy, daftar aturan, profil, dan disclaimer.

### 7.2 Contoh Payload `POST /api/recommendations`
```json
{
  "anggaran_maks": 12000000,
  "kebutuhan": "programming",
  "ram_min_gb": 8,
  "penyimpanan_min_gb": 512,
  "performa_prosesor": "sedang",
  "prioritas_baterai": false,
  "include_detail": true
}
```

### 7.3 Contoh Respons Sukses
```json
{
  "total": 10,
  "hasil": [
    {
      "id": 12,
      "nama_laptop": "Lenovo IdeaPad Slim 3 14IAH8",
      "merek": "Lenovo",
      "harga": 8299000,
      "ram_gb": 16,
      "penyimpanan_gb": 512,
      "tipe_penyimpanan": "SSD",
      "skor_prosesor": 7,
      "gpu": "Intel UHD Graphics",
      "ukuran_layar": 14.0,
      "berat_kg": 1.43,
      "baterai_jam": 6.5,
      "kategori_penggunaan": "programming",
      "sumber": "DATA CONTOH - GANTI DENGAN DATA ASLI",
      "tanggal_data": "2026-11-24",
      "skor_rekomendasi": 82.5,
      "label": "Sangat direkomendasikan",
      "alasan": "RAM besar 16 GB yang leluasa untuk multitasking, prosesor cukup gesit (skor 7/10), penyimpanan 512 GB SSD, harga ramah kantong di bawah anggaran, sangat mendukung kebutuhan coding, kompilasi, dan multitasking.",
      "detail_fuzzy": {
        "inputs_ternormalisasi": {
          "rasio_harga": 0.6916,
          "ram_gb": 16,
          "skor_prosesor": 7,
          "penyimpanan_gb": 512
        },
        "derajat_keanggotaan": {
          "rasio_harga": { "Hemat": 0.6337, "Sesuai": 0.0, "Melebihi": 0.0 },
          "ram_gb": { "Kecil": 0.0, "Sedang": 0.0, "Besar": 1.0 },
          "skor_prosesor": { "Rendah": 0.0, "Sedang": 0.0, "Tinggi": 0.5 },
          "penyimpanan_gb": { "Kecil": 0.0, "Sedang": 0.0, "Besar": 0.3043 }
        },
        "aturan_aktif": [
          { "id": "R1", "nama": "Jika Harga Hemat, RAM Besar, dan Prosesor Tinggi, maka Rekomendasi Tinggi", "alpha": 0.5, "output": "Tinggi" },
          { "id": "R6", "nama": "Jika Prosesor Tinggi dan Penyimpanan Besar, maka Rekomendasi Tinggi", "alpha": 0.3043, "output": "Tinggi" },
          { "id": "R9", "nama": "Jika Harga Hemat, RAM Besar, dan Penyimpanan Besar, maka Rekomendasi Tinggi", "alpha": 0.3043, "output": "Tinggi" }
        ]
      }
    }
  ],
  "pesan": null
}
```

---

## 8. Arsitektur Frontend React

Frontend dibangun menggunakan **React 18** berbasis arsitektur Single Page Application (SPA):
- `services/api.js`: Lapisan perantara panggilan HTTP fetch yang membaca environment variable `VITE_API_URL` dan menangani *graceful offline fallback*.
- `components/Navbar.jsx`: Menu navigasi dengan indikator status koneksi API secara *real-time*.
- `components/LaptopCard.jsx`: Kartu laptop responsif dengan format rupiah mata uang `id-ID` dan visualisasi spesifikasi teknis.
- `components/FuzzyDetailPanel.jsx`: Komponen akordeon yang menampilkan visualisasi persentase derajat keanggotaan dan tabel aturan aktif.
- `pages/FormRekomendasi.jsx`: Formulir interaktif dengan *instant Rupiah parser* dan validasi pesan kesalahan sebelum request dikirim.

---

## 9. Hasil Pengujian Sistem

### 9.1 Ringkasan Pengujian Backend (pytest)
Seluruh 26 pengujian pada `fuzzy-laptop/backend/tests` berhasil lulus 100%:
- **Fungsi Keanggotaan**: Nilai di titik puncak ($\mu=1$), titik kaki ($\mu=0$), sisi miring, tepi kiri/kanan terbuka, dan array NumPy.
- **Kasus Uji Manual (5 Skenario)**:
  - Kasus 1 (High Spec + Hemat): Centroid $84.4$ (*Sangat direkomendasikan*).
  - Kasus 2 (Low Spec + Melebihi): Centroid $15.6$ (*Kurang direkomendasikan*).
  - Kasus 3 (Mid Spec + Sesuai): Centroid $50.0$ (*Cukup direkomendasikan*).
  - Kasus 4 (Over-budget High Spec): Centroid $50.0$ (*Cukup direkomendasikan*).
  - Kasus 5 (Campuran Majemuk): Konsistensi dan determinisme hasil.
- **REST API Endpoints**: Status 200, penolakan 422 untuk anggaran negatif/kosong, 404 laptop tidak ada, dan fallback 5 laptop terdekat saat filter terlalu ketat.

### 9.2 Ringkasan Pengujian Frontend (Vitest)
Seluruh 3 pengujian komponen React pada `src/test/` berhasil lulus:
- Rendering kartu laptop, format harga Rupiah, dan badge skor.
- Validasi input form rekomendasi dan pesan peringatan saat input tidak valid.

### 9.3 Hasil Ekspor 8 Skenario Kasus Uji ke CSV
Dihasilkan oleh skrip `backend/scripts/export_kasus_uji.py` dan tersimpan di `backend/data/kasus_uji_fuzzy.csv`. Mencakup 8 profil representatif (Office Murah, Programming Menengah, Desain Grafis Tinggi, Editing Video Pro, Mobilitas Baterai, Over-budget High Spec, Mahasiswa Teknik, dan Kuliah Fleksibel).

---

## 10. Analisis dan Pembahasan

1. **Perilaku Penalaran Fuzzy vs Crisp**:
   Pada skenario 6 (Anggaran Rp 6.000.000, laptop harga Rp 14.000.000), sistem penyaringan biasa akan langsung membuang laptop tersebut. Namun pada sistem Fuzzy Mamdani, aturan `R8` (*Jika Harga Melebihi, Prosesor Tinggi, dan RAM Besar, maka Rekomendasi Sedang*) tetap aktif dengan $\alpha = 1.0$, menghasilkan skor $71.0$ (*Direkomendasikan*). Ini memberikan fleksibilitas kepada mahasiswa untuk mempertimbangkan laptop tersebut apabila mereka bersedia menambah anggaran sedikit demi performa yang jauh lebih tinggi.
2. **Kinerja Komputasi**:
   Waktu komputasi rata-rata per laptop adalah $\approx 0.5 \text{ ms}$. Untuk menyaring dan menilai 40 laptop dalam dataset, waktu total yang dibutuhkan hanya $\approx 0.02 \text{ detik}$, jauh di bawah batas NFR (1 detik).
3. **Determinisme dan Kestabilan**:
   Karena seluruh logika fuzzy dibangun menggunakan operasi aljabar NumPy yang murni deterministik, pengujian berulang dengan masukan identik selalu menghasilkan skor dan urutan ranking yang sama persis tanpa deviasi acak.

---

## 11. Kesimpulan dan Batasan Sistem

### 11.1 Kesimpulan
Sistem Rekomendasi Laptop Mahasiswa berbasis Logika Fuzzy Mamdani telah berhasil dibangun secara utuh:
- Mesin inferensi manual NumPy berjalan transparan, akurat, dan telah divalidasi dengan perhitungan matematis manual.
- REST API FastAPI dan Frontend React terintegrasi secara harmonis dengan penanganan kondisi *empty-state*, *loading*, dan pesan kesalahan yang ramah.
- Proyek ini memenuhi seluruh kriteria fungsional dan non-fungsional dokumen PRD untuk Project UAS Kecerdasan Buatan.

### 11.2 Batasan Sistem
- Data harga dan ketersediaan laptop pada dataset merupakan data contoh referensi dan tidak diperbarui secara otomatis dari API marketplace.
- Skor prosesor menggunakan skala penilaian normalisasi 1–10.
- Rekomendasi ini adalah sistem pendukung keputusan (*decision support*) dan bukan pengganti konsultasi profesional mendalam.
