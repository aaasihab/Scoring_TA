# Sistem Penilaian Judul Tugas Akhir Berbasis IndoBERT

Aplikasi web untuk mengukur **kemiripan** dan **keunikan** judul Tugas Akhir menggunakan model **SimCSE-IndoBERT**. Sistem ini membantu mahasiswa dan dosen mengevaluasi apakah sebuah judul penelitian sudah pernah ada atau masih unik berdasarkan dataset judul yang tersimpan.

---

## Fitur Utama

- **Cek Kemiripan** — Menghitung cosine similarity antara query dengan dataset menggunakan embedding IndoBERT.
- **3 Mode Pengecekan:**
  - **Judul** — Cek berdasarkan judul saja.
  - **Deskripsi** — Cek berdasarkan deskripsi penelitian saja.
  - **Kombinasi** — Cek berdasarkan gabungan judul dan deskripsi.
- **Skor Keunikan** — Menghitung seberapa unik judul berdasarkan skor kemiripan tertinggi.
- **Top 5 Hasil** — Menampilkan 5 judul/deskripsi paling mirip beserta skor dan labelnya.
- **Riwayat Pengujian** — Menyimpan seluruh hasil pencarian ke file Excel dan dapat diunduh.
- **Antarmuka Responsif** — Tampilan modern yang dapat diakses dari desktop maupun mobile.

---

## Struktur Project

```
sistem_scoring_fix/
│
├── app.py                         # Entry point aplikasi Flask
├── requirements.txt               # Daftar library Python
├── README.md
│
├── engine/                        # Modul inti sistem
│   ├── preprocessing.py           # Cleaning & case folding teks
│   ├── embedding.py               # Encode teks ke vektor (SimCSE-IndoBERT)
│   ├── similarity.py              # Hitung cosine similarity & ambil Top K
│   ├── unique.py                  # Hitung skor keunikan
│   ├── retrieval.py               # Pipeline pencarian (menggabungkan semua modul)
│   └── history.py                 # Simpan & muat riwayat ke Excel
│
├── model/                         # Model IndoBERT (Git LFS)
│   └── simcse-indobert/
│       ├── model.safetensors      # Bobot model (~475 MB, disimpan via Git LFS)
│       ├── config.json
│       ├── tokenizer.json
│       ├── tokenizer_config.json
│       └── ...
│
├── dataset/                       # Data training & embedding
│   ├── df_train.xlsx              # Dataset judul & deskripsi
│   ├── embeddings_title_train.npy
│   ├── embeddings_description_train.npy
│   └── embeddings_combined_train.npy
│
├── templates/                     # Halaman HTML (Jinja2)
│   ├── index.html                 # Halaman utama (form & hasil)
│   └── history.html               # Halaman riwayat pengujian
│
└── static/                        # File statis
    └── unuja.png                  # Logo
```

---

## Prasyarat

Sebelum memulai, pastikan sistem Anda sudah memiliki:

- **Python 3.10** atau lebih baru
- **pip** (Python package manager)
- **Git** dengan **Git LFS** terinstal (untuk mengunduh file model)

### Instal Git LFS

Git LFS diperlukan karena file model (`model.safetensors`) berukuran ~475 MB dan disimpan menggunakan Git Large File Storage.

```bash
# Instal Git LFS (jika belum)
git lfs install
```

> **Catatan:** Jika Git LFS belum terinstal di sistem, unduh dari [git-lfs.com](https://git-lfs.com/) atau instal melalui package manager:
> - **Windows (winget):** `winget install GitHub.GitLFS`
> - **macOS (Homebrew):** `brew install git-lfs`
> - **Ubuntu/Debian:** `sudo apt install git-lfs`

---

## Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/aaasihab/Scoring_TA.git
cd Scoring_TA
```

> File model akan otomatis diunduh oleh Git LFS saat clone. Jika file model belum terunduh, jalankan:
> ```bash
> git lfs pull
> ```

### 2. Buat Virtual Environment

```bash
python -m venv venv
```

### 3. Aktifkan Virtual Environment

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
# Jika muncul error execution policy, jalankan dulu:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

> **Catatan:** Proses instalasi mungkin memerlukan waktu cukup lama karena library seperti `torch` dan `sentence-transformers` berukuran besar.

---

## Menjalankan Aplikasi

```bash
python app.py
```

Aplikasi akan berjalan di `http://127.0.0.1:5000/`. Buka alamat tersebut di browser.

> **Catatan:** Saat pertama kali dijalankan, proses loading model IndoBERT memerlukan waktu beberapa detik.

---

## Cara Penggunaan

### 1. Pilih Mode Pengecekan

Di halaman utama, pilih salah satu mode:

| Mode | Input yang Diperlukan | Keterangan |
|------|----------------------|------------|
| **Judul** | Judul Tugas Akhir | Mencari kemiripan berdasarkan judul saja |
| **Deskripsi** | Deskripsi Penelitian | Mencari kemiripan berdasarkan deskripsi saja |
| **Kombinasi** | Judul + Deskripsi | Mencari kemiripan berdasarkan gabungan keduanya |

### 2. Masukkan Query

Isi form sesuai mode yang dipilih, lalu klik tombol **"Cek Kemiripan"**.

### 3. Baca Hasil

Sistem akan menampilkan:

- **Skor Keunikan** — Seberapa unik judul Anda (0–1, semakin tinggi semakin unik).
- **Top 5 Hasil Teratas** — Daftar 5 judul/deskripsi paling mirip beserta skor dan label.

### Label Kemiripan

| Label | Skor | Arti |
|-------|------|------|
| 🔴 Sangat Mirip | ≥ 0.80 | Judul sangat mirip dengan yang sudah ada |
| 🟡 Mirip | 0.60 – 0.79 | Judul cukup mirip |
| 🟢 Tidak Mirip | < 0.60 | Judul berbeda / tidak mirip |

### Label Keunikan

| Label | Skor | Arti |
|-------|------|------|
| 🟢 Sangat Unik | ≥ 0.75 | Judul sangat unik dan original |
| 🟢 Cukup Unik | 0.50 – 0.74 | Judul cukup unik |
| 🟡 Kurang Unik | 0.25 – 0.49 | Judul kurang unik, perlu modifikasi |
| 🔴 Tidak Unik | < 0.25 | Judul sangat mirip dengan yang sudah ada |

### 4. Lihat Riwayat

Klik menu **"Riwayat"** di navigasi untuk melihat seluruh hasil pengujian sebelumnya. Riwayat juga dapat diunduh dalam format **Excel (.xlsx)**.

---

## Teknologi yang Digunakan

| Komponen | Teknologi |
|----------|-----------|
| Backend | Flask (Python) |
| Model NLP | SimCSE-IndoBERT (Sentence Transformers) |
| Similarity | Cosine Similarity (scikit-learn) |
| Preprocessing | Case Folding, Regex Cleaning |
| Data Storage | Excel via openpyxl, NumPy (.npy) |
| Frontend | HTML, TailwindCSS, Jinja2 |
| Model Storage | Git LFS |

---

## Alur Kerja Sistem

```
Input (Judul/Deskripsi)
        │
        ▼
┌─────────────────┐
│  Preprocessing   │  Case folding → Cleaning (regex)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Embedding     │  Encode teks → vektor (SimCSE-IndoBERT)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Similarity     │  Cosine similarity dengan dataset embeddings
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Top K & Score  │  Ambil 5 teratas + klasifikasi label
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Uniqueness     │  Skor keunikan = 1 - similarity tertinggi (scaled)
└────────┬────────┘
         │
         ▼
   Tampilkan Hasil + Simpan ke History
```
