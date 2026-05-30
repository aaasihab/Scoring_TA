# 📖 Dokumentasi Aplikasi — Sistem Penilaian Judul Tugas Akhir

> **Novelty Detection Web Application**
> Aplikasi web berbasis Flask untuk mengecek kemiripan dan keunikan judul Tugas Akhir menggunakan Cosine Similarity dan model IndoBERT SimCSE.

---

## Daftar Isi

1. [Gambaran Umum](#1-gambaran-umum)
2. [Arsitektur Sistem](#2-arsitektur-sistem)
3. [Struktur Direktori](#3-struktur-direktori)
4. [Penjelasan Setiap Modul](#4-penjelasan-setiap-modul)
5. [Alur Request → Response (Per Endpoint)](#5-alur-request--response-per-endpoint)
6. [Struktur Data Internal](#6-struktur-data-internal)
7. [Teknologi & Dependensi](#7-teknologi--dependensi)
8. [Cara Menjalankan Aplikasi](#8-cara-menjalankan-aplikasi)

---

## 1. Gambaran Umum

Aplikasi ini adalah **Sistem Penilaian Judul Tugas Akhir** yang membantu mahasiswa dan dosen mengevaluasi apakah judul TA yang diajukan sudah pernah ada (mirip) atau cukup unik. Sistem melakukan:

- **Pengecekan Kemiripan Semantik** — membandingkan input pengguna terhadap dataset judul TA yang sudah ada menggunakan cosine similarity pada embedding vektor.
- **Perhitungan Skor Keunikan (Novelty Score)** — menilai seberapa unik input berdasarkan skor kemiripan maksimum.
- **Penyimpanan Riwayat** — setiap hasil pengujian otomatis tersimpan ke file Excel untuk keperluan pelaporan.

### Mode Pengecekan

| Mode        | Input yang Digunakan       | Embedding yang Dibandingkan             |
|-------------|----------------------------|-----------------------------------------|
| `judul`     | Judul TA saja              | `embeddings_title_train.npy`            |
| `deskripsi` | Deskripsi penelitian saja  | `embeddings_description_train.npy`      |
| `kombinasi` | Judul + Deskripsi          | `embeddings_combined_train.npy`         |

---

## 2. Arsitektur Sistem

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          BROWSER (Client)                               │
│  ┌─────────────────────┐    ┌──────────────┐    ┌───────────────────┐  │
│  │  index.html (Form)  │    │ history.html │    │  Modal/Toast UI   │  │
│  └────────┬────────────┘    └──────┬───────┘    └───────────────────┘  │
│           │ POST /                 │ GET /history                      │
│           │ (judul, deskripsi,     │                                   │
│           │  mode)                 │ GET /history/download             │
└───────────┼────────────────────────┼──────────────────────────────────-┘
            │                        │
            ▼                        ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          FLASK SERVER (app.py)                          │
│                                                                         │
│  Route: /           ──► index()          ──► render index.html          │
│  Route: /history    ──► history()        ──► render history.html        │
│  Route: /history/   ──► download_history()──► send_file (Excel)        │
│         download                                                        │
└─────────┬───────────────────────────────────────────────────────────────┘
          │ (POST only)
          ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    ENGINE LAYER (engine/)                                │
│                                                                         │
│  ┌──────────────────┐                                                   │
│  │  retrieval.py    │  ◄── Orchestrator utama                           │
│  │  search_similar()│                                                   │
│  └──┬───┬───┬───┬───┘                                                   │
│     │   │   │   │                                                       │
│     ▼   │   │   │   ┌──────────────────┐                                │
│  preprocessing.py   │  preprocess_text() ── Case Folding + Cleaning     │
│     │   │   │       │  combine_text()    ── Gabung Judul + Deskripsi    │
│     │   │   │       └──────────────────┘                                │
│     │   ▼   │                                                           │
│     │  embedding.py ── encode_text()  ── Model SimCSE-IndoBERT          │
│     │       │                                                           │
│     │       ▼                                                           │
│     │  similarity.py                                                    │
│     │   ├─ compute_similarity() ── Cosine Similarity                    │
│     │   └─ get_top_k()          ── Top 5 terdekat                       │
│     │                                                                   │
│     ▼                                                                   │
│  unique.py                                                              │
│   ├─ calculate_unique()  ── Min-Max Scaling + Skor Unik                 │
│   └─ classify_unique()   ── Label Keunikan                              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    UTILS LAYER (utils/)                                  │
│                                                                         │
│  history.py                                                             │
│   ├─ save_to_history()  ── Simpan hasil ke dataset/history.xlsx         │
│   └─ load_history()     ── Baca semua data history dari Excel           │
│                                                                         │
│  loader.py                                                              │
│   └─ load_model()       ── Placeholder loader (tidak aktif dipakai)     │
└─────────────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    DATA & MODEL LAYER                                   │
│                                                                         │
│  dataset/                                                               │
│   ├─ df_train.xlsx                 ── Dataset judul TA (ground truth)   │
│   ├─ df_train.csv                  ── Dataset versi CSV                 │
│   ├─ embeddings_title_train.npy    ── Embedding judul (pre-computed)    │
│   ├─ embeddings_description_train.npy ── Embedding deskripsi           │
│   ├─ embeddings_combined_train.npy ── Embedding gabungan               │
│   └─ history.xlsx                  ── File riwayat (auto-generated)     │
│                                                                         │
│  model/simcse-indobert/            ── Model SimCSE-IndoBERT lokal       │
│   ├─ model.safetensors             ── Bobot model (~498MB)             │
│   ├─ config.json                   ── Konfigurasi arsitektur           │
│   ├─ tokenizer.json                ── Tokenizer                       │
│   └─ ...                                                                │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Struktur Direktori

```
novelty_detection_web_baru/
│
├── app.py                          # Entry point Flask server
├── requirements.txt                # Daftar dependensi Python
├── .gitignore
│
├── engine/                         # Modul inti pemrosesan
│   ├── preprocessing.py            # Pembersihan & normalisasi teks
│   ├── embedding.py                # Encoding teks → vektor (SimCSE)
│   ├── similarity.py               # Perhitungan cosine similarity
│   ├── unique.py                   # Perhitungan skor keunikan
│   └── retrieval.py                # Orchestrator pencarian kemiripan
│
├── utils/                          # Utilitas pendukung
│   ├── history.py                  # Manajemen riwayat (save/load Excel)
│   └── loader.py                   # Placeholder model loader
│
├── templates/                      # Template HTML (Jinja2)
│   ├── index.html                  # Halaman utama (form + hasil)
│   └── history.html                # Halaman riwayat pengujian
│
├── static/                         # Aset statis
│   └── unuja.png                   # Logo universitas
│
├── dataset/                        # Data & embedding
│   ├── df_train.xlsx               # Dataset utama judul TA
│   ├── df_train.csv                # Versi CSV
│   ├── embeddings_title_train.npy  # Pre-computed embedding judul
│   ├── embeddings_description_train.npy  # Pre-computed embedding deskripsi
│   ├── embeddings_combined_train.npy     # Pre-computed embedding kombinasi
│   └── history.xlsx                # File riwayat (auto-generated)
│
└── model/
    └── simcse-indobert/            # Model Sentence Transformer lokal
        ├── model.safetensors       # Bobot model (~498 MB)
        ├── config.json
        ├── tokenizer.json
        └── ...
```

---

## 4. Penjelasan Setiap Modul

### 4.1 `app.py` — Flask Application Server

Entry point aplikasi. Mendefinisikan 3 route:

| Route              | Method    | Fungsi                              |
|--------------------|-----------|-------------------------------------|
| `/`                | GET, POST | Halaman utama — form + hasil        |
| `/history`         | GET       | Halaman daftar riwayat pengujian    |
| `/history/download`| GET       | Download file history.xlsx          |

---

### 4.2 `engine/preprocessing.py` — Text Preprocessing Pipeline

Pipeline pembersihan teks input pengguna sebelum di-encode menjadi embedding.

| Fungsi              | Deskripsi                                                                  |
|---------------------|----------------------------------------------------------------------------|
| `case_folding(x)`   | Mengubah seluruh teks menjadi huruf kecil (lowercase)                      |
| `cleaning(text)`    | Menghapus karakter non-alfanumerik, normalisasi spasi, hapus line break    |
| `tokenize(text)`    | Memecah teks menjadi daftar kata (word tokenization)                       |
| `remove_stopwords(words)` | Menghapus kata-kata umum bahasa Indonesia (stopwords NLTK)            |
| `stem_text(words)`  | Stemming kata menggunakan Sastrawi (bahasa Indonesia)                      |
| `preprocess_text(text)` | **Pipeline utama** — menjalankan case_folding → cleaning               |
| `combine_text(judul, deskripsi)` | Preprocess & gabungkan judul + deskripsi menjadi satu teks    |

> **Catatan**: Langkah tokenize, stopword removal, dan stemming saat ini di-comment out dalam `preprocess_text()`. Pipeline hanya menjalankan case folding dan cleaning.

---

### 4.3 `engine/embedding.py` — Text Embedding (SimCSE-IndoBERT)

Mengubah teks yang sudah diproses menjadi vektor numerik (embedding) menggunakan model `SentenceTransformer` berbasis IndoBERT SimCSE yang disimpan lokal.

| Fungsi              | Input           | Output                         |
|---------------------|-----------------|--------------------------------|
| `encode_text(text)` | String teks     | Numpy array (1D vector, 768d)  |
| `encode_batch(text_list)` | List string | Numpy array (N × 768)         |

Model dimuat saat modul di-import:
```python
model = SentenceTransformer("model/simcse-indobert")
```

---

### 4.4 `engine/similarity.py` — Cosine Similarity Computation

Menghitung kesamaan semantik antara query embedding dan seluruh embedding dataset.

| Fungsi                  | Deskripsi                                                        |
|-------------------------|------------------------------------------------------------------|
| `compute_similarity(query_embedding, dataset_embeddings)` | Hitung cosine similarity (1 × N) |
| `get_top_k(similarity_scores, k=5)` | Ambil k indeks & skor tertinggi (descending)          |

---

### 4.5 `engine/unique.py` — Uniqueness/Novelty Scoring

Menghitung skor keunikan judul berdasarkan skor kemiripan tertinggi.

| Fungsi                      | Deskripsi                                                      |
|-----------------------------|----------------------------------------------------------------|
| `calculate_unique(top_scores, min_sim=0.6, max_sim=1.0)` | Hitung unique score via min-max scaling |
| `classify_unique(score)`    | Klasifikasi label berdasarkan skor                             |

**Formula Unique Score:**
```
scaled = (similarity - 0.6) / (1.0 - 0.6)    # Min-Max Scaling
scaled = clamp(scaled, 0, 1)                   # Batasi 0–1
unique_score = 1 - max(scaled)                 # Inverse
```

**Klasifikasi Label Keunikan:**

| Skor Unique       | Label              |
|--------------------|--------------------|
| ≥ 0.75            | Sangat Menarik     |
| ≥ 0.50            | Cukup Menarik      |
| ≥ 0.25            | Kurang Menarik     |
| < 0.25            | Tidak Menarik      |

---

### 4.6 `engine/retrieval.py` — Search Orchestrator

Modul utama yang meng-orchestrate seluruh proses pencarian kemiripan. Memuat dataset & embedding saat server pertama kali start.

**Data yang dimuat saat startup:**
```python
dataset = pd.read_excel("dataset/df_train.xlsx")
embedding_judul = np.load("dataset/embeddings_title_train.npy")
embedding_deskripsi = np.load("dataset/embeddings_description_train.npy")
embedding_gabungan = np.load("dataset/embeddings_combined_train.npy")
```

**Fungsi `search_similar(judul, deskripsi, mode)`:**
Orchestrator utama yang menjalankan seluruh pipeline:
1. Tentukan query text & embedding dataset berdasarkan mode
2. Preprocessing query
3. Encode query → embedding vector
4. Hitung cosine similarity
5. Ambil top 5 hasil
6. Klasifikasi label kemiripan per hasil
7. Hitung unique score
8. Return dictionary hasil lengkap

**Klasifikasi Label Kemiripan (per hasil):**

| Skor Similarity   | Label              |
|--------------------|--------------------|
| ≥ 0.80            | Sangat Mirip       |
| ≥ 0.60            | Mirip              |
| < 0.60            | Tidak Mirip        |

---

### 4.7 `utils/history.py` — History Management

Mengelola penyimpanan dan pembacaan riwayat pengujian dari file Excel.

| Fungsi              | Deskripsi                                                          |
|---------------------|--------------------------------------------------------------------|
| `save_to_history(results)` | Append 1 baris data ke `dataset/history.xlsx` (auto-create jika belum ada) |
| `load_history()`    | Baca semua data dari Excel, return list of dict (terbaru di atas)  |

**Kolom dalam file history.xlsx:**

| Kolom                        | Keterangan                          |
|------------------------------|-------------------------------------|
| No                           | Nomor urut                          |
| Timestamp                    | Waktu pengujian (YYYY-MM-DD HH:MM:SS) |
| Mode                         | Mode pengecekan (judul/deskripsi/kombinasi) |
| Query (Raw)                  | Input asli pengguna                 |
| Query (Preprocessed)         | Input setelah preprocessing         |
| Unique Score (Max)           | Skor keunikan                       |
| Label Unique (Max)           | Label klasifikasi keunikan          |
| Top 1–5 - Text               | Teks hasil kemiripan ke-1 s/d 5     |
| Top 1–5 - Score              | Skor similarity ke-1 s/d 5         |
| Top 1–5 - Label              | Label kemiripan ke-1 s/d 5         |
| Query (Raw Judul/Deskripsi)  | Khusus mode kombinasi               |
| Top 1–5 - Judul/Deskripsi    | Khusus mode kombinasi               |

---

### 4.8 Templates (Jinja2 HTML)

#### `templates/index.html`
Halaman utama dengan 2 panel:
- **Panel Form Input** — Mode selection (radio button), input judul, textarea deskripsi
- **Panel Hasil** — Menampilkan query, unique score, tabel top 5 kemiripan

Fitur UI:
- Validasi form client-side (JavaScript) + server-side (Flask)
- Dynamic form state — enable/disable input sesuai mode
- Shake animation pada validasi gagal
- Toast notifikasi auto-dismiss (4 detik)
- Modal untuk teks panjang (> 200 karakter)
- Auto-scroll ke hasil setelah submit
- Shortcut `Ctrl+Enter` untuk submit

#### `templates/history.html`
Halaman riwayat dengan:
- Tabel expandable row — klik baris untuk lihat detail Top 5
- Responsive mobile layout — tabel berubah menjadi card
- Tombol download Excel
- Modal untuk teks panjang

---

## 5. Alur Request → Response (Per Endpoint)

### 5.1 `GET /` — Menampilkan Halaman Utama (Kosong)

```
Browser                           Flask Server
  │                                    │
  │  ── GET / ──────────────────────►  │
  │                                    │
  │                              index() dipanggil
  │                              results = None
  │                              error = None
  │                              saved = False
  │                                    │
  │                              render_template("index.html",
  │                                  results=None,
  │                                  error=None,
  │                                  saved=False)
  │                                    │
  │  ◄─── HTML (form kosong + ──────  │
  │       empty state "Belum ada       │
  │       hasil")                      │
```

---

### 5.2 `POST /` — Cek Kemiripan (Alur Utama / Sukses)

Ini adalah alur inti aplikasi. Contoh: mode = `judul`, judul = `"Analisis Sentimen Media Sosial"`.

```
Browser                    Flask (app.py)              Engine Layer               Utils
  │                             │                           │                       │
  │  POST / ─────────────────► │                           │                       │
  │  form-data:                │                           │                       │
  │   judul="Analisis..."      │                           │                       │
  │   deskripsi=""             │                           │                       │
  │   mode="judul"             │                           │                       │
  │                             │                           │                       │
  │                        ┌────┴────────────────┐         │                       │
  │                        │ 1. VALIDASI INPUT   │         │                       │
  │                        │                     │         │                       │
  │                        │ mode == "judul"     │         │                       │
  │                        │ judul != "" ✓       │         │                       │
  │                        │ → Validasi LOLOS    │         │                       │
  │                        └────┬────────────────┘         │                       │
  │                             │                           │                       │
  │                             │  search_similar(          │                       │
  │                             │    judul, deskripsi,      │                       │
  │                             │    mode)                  │                       │
  │                             │  ─────────────────────►  │                       │
  │                             │                           │                       │
  │                        ┌────────────────────────────────┴──────────────────┐   │
  │                        │          2. RETRIEVAL PIPELINE                     │   │
  │                        │              (retrieval.py)                        │   │
  │                        │                                                    │   │
  │                        │  ┌──────────────────────────────────────────┐      │   │
  │                        │  │ Step 2a: Tentukan query & embedding      │      │   │
  │                        │  │                                          │      │   │
  │                        │  │ mode == "judul" →                        │      │   │
  │                        │  │   raw_query = "Analisis Sentimen..."     │      │   │
  │                        │  │   dataset_embedding = embedding_judul    │      │   │
  │                        │  │   (pre-loaded .npy file)                 │      │   │
  │                        │  └──────────────────────────────────────────┘      │   │
  │                        │                                                    │   │
  │                        │  ┌──────────────────────────────────────────┐      │   │
  │                        │  │ Step 2b: Preprocessing                   │      │   │
  │                        │  │          (preprocessing.py)              │      │   │
  │                        │  │                                          │      │   │
  │                        │  │ preprocess_text("Analisis Sentimen...")  │      │   │
  │                        │  │   ├─ case_folding()                      │      │   │
  │                        │  │   │  → "analisis sentimen media sosial"  │      │   │
  │                        │  │   └─ cleaning()                          │      │   │
  │                        │  │      → "analisis sentimen media sosial"  │      │   │
  │                        │  │                                          │      │   │
  │                        │  │ query_text = "analisis sentimen media    │      │   │
  │                        │  │               sosial"                    │      │   │
  │                        │  └──────────────────────────────────────────┘      │   │
  │                        │                                                    │   │
  │                        │  ┌──────────────────────────────────────────┐      │   │
  │                        │  │ Step 2c: Encoding                        │      │   │
  │                        │  │          (embedding.py)                  │      │   │
  │                        │  │                                          │      │   │
  │                        │  │ encode_text(query_text)                  │      │   │
  │                        │  │   → SentenceTransformer.encode()         │      │   │
  │                        │  │   → SimCSE-IndoBERT model                │      │   │
  │                        │  │   → query_embedding (1 × 768 vector)     │      │   │
  │                        │  └──────────────────────────────────────────┘      │   │
  │                        │                                                    │   │
  │                        │  ┌──────────────────────────────────────────┐      │   │
  │                        │  │ Step 2d: Cosine Similarity               │      │   │
  │                        │  │          (similarity.py)                 │      │   │
  │                        │  │                                          │      │   │
  │                        │  │ compute_similarity(                      │      │   │
  │                        │  │   query_embedding,     ← 1 × 768        │      │   │
  │                        │  │   embedding_judul      ← N × 768        │      │   │
  │                        │  │ )                                        │      │   │
  │                        │  │ → similarities (1D array, panjang N)     │      │   │
  │                        │  │                                          │      │   │
  │                        │  │ get_top_k(similarities, k=5)             │      │   │
  │                        │  │ → top_idx = [idx1, idx2, ..., idx5]      │      │   │
  │                        │  │ → top_scores = [0.92, 0.85, ...]        │      │   │
  │                        │  └──────────────────────────────────────────┘      │   │
  │                        │                                                    │   │
  │                        │  ┌──────────────────────────────────────────┐      │   │
  │                        │  │ Step 2e: Bangun Hasil per Top-K          │      │   │
  │                        │  │                                          │      │   │
  │                        │  │ Untuk setiap idx, score:                 │      │   │
  │                        │  │   text = dataset["judul_preprocessed"]   │      │   │
  │                        │  │   label = klasifikasi_skor(score)        │      │   │
  │                        │  │     ≥ 0.8 → "Sangat Mirip"              │      │   │
  │                        │  │     ≥ 0.6 → "Mirip"                     │      │   │
  │                        │  │     < 0.6 → "Tidak Mirip"               │      │   │
  │                        │  │   results.append({text, score, label})   │      │   │
  │                        │  └──────────────────────────────────────────┘      │   │
  │                        │                                                    │   │
  │                        │  ┌──────────────────────────────────────────┐      │   │
  │                        │  │ Step 2f: Hitung Unique Score             │      │   │
  │                        │  │          (unique.py)                     │      │   │
  │                        │  │                                          │      │   │
  │                        │  │ calculate_unique(top_scores)             │      │   │
  │                        │  │   ├─ Min-Max Scale (min=0.6, max=1.0)    │      │   │
  │                        │  │   ├─ max_similarity = max(scaled)        │      │   │
  │                        │  │   ├─ unique_max = 1 - max_similarity     │      │   │
  │                        │  │   └─ label = classify_unique(unique_max) │      │   │
  │                        │  │       → "Sangat Menarik" / "Cukup" / ... │      │   │
  │                        │  └──────────────────────────────────────────┘      │   │
  │                        │                                                    │   │
  │                        └────────────────────────────────────┬──────────────┘   │
  │                             │                               │                   │
  │                             │  ◄── return result_dict ────  │                   │
  │                             │                               │                   │
  │                             │  save_to_history(results)     │                   │
  │                             │  ──────────────────────────────────────────────► │
  │                             │                               │                   │
  │                        ┌────────────────────────────────────────────────────────┤
  │                        │  3. SAVE HISTORY (utils/history.py)                    │
  │                        │                                                        │
  │                        │  ├─ Cek apakah history.xlsx sudah ada                  │
  │                        │  ├─ Jika belum → buat Workbook baru + header           │
  │                        │  ├─ Jika sudah → load Workbook yang ada                │
  │                        │  ├─ Susun baris data dari result_dict                  │
  │                        │  ├─ ws.append(row)                                     │
  │                        │  └─ wb.save("dataset/history.xlsx")                    │
  │                        └────────────────────────────────────────────────────────┤
  │                             │                               │                   │
  │                             │  saved = True                 │                   │
  │                             │                               │                   │
  │                             │  render_template(             │                   │
  │                             │    "index.html",              │                   │
  │                             │    results=result_dict,       │                   │
  │                             │    error=None,                │                   │
  │                             │    saved=True                 │                   │
  │                             │  )                            │                   │
  │                             │                               │                   │
  │  ◄─── HTML ──────────────  │                               │                   │
  │  (hasil + toast "berhasil  │                               │                   │
  │   disimpan" + tabel top 5  │                               │                   │
  │   + unique score card)     │                               │                   │
```

---

### 5.3 `POST /` — Validasi Gagal (Input Kosong)

```
Browser                    Flask (app.py)
  │                             │
  │  POST / ─────────────────► │
  │  form-data:                │
  │   judul="" (kosong!)       │
  │   mode="judul"             │
  │                             │
  │                        mode == "judul" dan judul kosong
  │                        → error = "Judul Tugas Akhir wajib diisi."
  │                             │
  │                        render_template("index.html",
  │                            results=None,
  │                            error="Judul Tugas Akhir wajib diisi.",
  │                            saved=False)
  │                             │
  │  ◄─── HTML (error alert ── │
  │       merah ditampilkan)   │
```

> **Catatan:** Validasi juga terjadi di sisi client (JavaScript) sebelum form di-submit. Jika JavaScript aktif, form tidak akan terkirim dan field input akan bergoyang (shake animation) + border merah.

---

### 5.4 `POST /` — Mode Kombinasi

Alur sama dengan 5.2, dengan perbedaan:

```
Step 2a (retrieval.py):
  raw_query = judul + " " + deskripsi
  combine_text(judul, deskripsi)
    → query_text = preprocess(judul) + " " + preprocess(deskripsi)
    → query_judul = preprocess(judul)
    → query_deskripsi = preprocess(deskripsi)
  dataset_embedding = embedding_gabungan

Step 2e:
  Selain text & score, juga menyimpan:
    text_judul = dataset["judul_preprocessed"]
    text_deskripsi = dataset["deskripsi_preprocessed"]

Return dict tambahan:
  result_dict["query_judul"] = query_judul
  result_dict["query_deskripsi"] = query_deskripsi
```

Di sisi template, mode kombinasi menampilkan judul dan deskripsi secara terpisah dengan badge warna berbeda (biru untuk JUDUL, kuning untuk DESKRIPSI).

---

### 5.5 `GET /history` — Menampilkan Riwayat Pengujian

```
Browser                    Flask (app.py)           Utils (history.py)
  │                             │                        │
  │  GET /history ───────────► │                        │
  │                             │                        │
  │                             │  load_history()        │
  │                             │  ──────────────────►   │
  │                             │                        │
  │                             │                  Cek dataset/history.xlsx
  │                             │                  ├─ Jika tidak ada → return []
  │                             │                  ├─ Jika ada → load_workbook()
  │                             │                  ├─ Baca headers dari row 1
  │                             │                  ├─ Iterasi row 2+ → list of dict
  │                             │                  └─ data.reverse() (terbaru dulu)
  │                             │                        │
  │                             │  ◄── data ────────────│
  │                             │                        │
  │                             │  render_template(
  │                             │    "history.html",
  │                             │    history=data)
  │                             │
  │  ◄─── HTML ──────────────  │
  │  (tabel riwayat dengan     │
  │   expandable rows, atau    │
  │   empty state jika kosong) │
```

---

### 5.6 `GET /history/download` — Download File Excel

```
Browser                    Flask (app.py)
  │                             │
  │  GET /history/download ──► │
  │                             │
  │                        Cek: dataset/history.xlsx ada?
  │                        │
  │                        ├─ YA → send_file(
  │                        │        history.xlsx,
  │                        │        as_attachment=True,
  │                        │        download_name="history_pengujian.xlsx")
  │                        │
  │  ◄─── File download ──────│
  │  (history_pengujian.xlsx)  │
  │                             │
  │                        ├─ TIDAK → redirect(url_for("history"))
  │                        │
  │  ◄─── 302 Redirect ───────│
  │  → GET /history            │
```

---

## 6. Struktur Data Internal

### 6.1 `result_dict` — Output dari `search_similar()`

```python
# Mode: judul / deskripsi
{
    "raw_query": "Analisis Sentimen Media Sosial",
    "query": "analisis sentimen media sosial",
    "mode": "judul",
    "results": [
        {
            "text": "analisis sentimen twitter tentang ...",
            "score": 0.92,
            "label": "Sangat Mirip"
        },
        {
            "text": "sistem analisis opini media ...",
            "score": 0.85,
            "label": "Sangat Mirip"
        },
        # ... (total 5 item)
    ],
    "unique": {
        "max_similarity": 0.80,
        "unique_max": 0.20,
        "label_max": "Tidak Menarik"
    }
}

# Mode: kombinasi (field tambahan)
{
    # ... semua field di atas, plus:
    "query_judul": "analisis sentimen media sosial",
    "query_deskripsi": "penelitian ini bertujuan ...",
    "results": [
        {
            "text": "analisis sentimen ... penelitian ...",
            "score": 0.88,
            "label": "Sangat Mirip",
            "text_judul": "analisis sentimen twitter ...",       # tambahan
            "text_deskripsi": "penelitian ini membahas ..."      # tambahan
        },
        # ...
    ]
}
```

### 6.2 History Record (1 baris Excel)

```
| No | Timestamp           | Mode   | Query (Raw)  | Query (Preprocessed) | Unique Score | Label Unique    |
|----|---------------------|--------|--------------|----------------------|-------------|-----------------|
| 1  | 2026-05-30 08:00:00 | judul  | Analisis ... | analisis ...         | 0.20        | Tidak Menarik   |

| Top 1 Text | Top 1 Score | Top 1 Label  | Top 2 Text | Top 2 Score | ...
|------------|-------------|--------------|------------|-------------|----
| analisis...| 0.92        | Sangat Mirip | sistem ... | 0.85        | ...
```

---

## 7. Teknologi & Dependensi

### Backend
| Teknologi                | Versi   | Fungsi                                    |
|--------------------------|---------|-------------------------------------------|
| **Python**               | 3.x     | Bahasa pemrograman utama                  |
| **Flask**                | 3.1.3   | Web framework                             |
| **Jinja2**               | 3.1.6   | Template engine (HTML rendering)          |
| **Pandas**               | 2.3.3   | Manipulasi dataframe (dataset)            |
| **NumPy**                | 2.2.6   | Operasi array & matrix                    |
| **scikit-learn**         | 1.7.2   | Cosine similarity computation             |
| **sentence-transformers**| 5.3.0   | Framework embedding model                 |
| **transformers**         | 5.3.0   | HuggingFace model backend                 |
| **PyTorch**              | 2.10.0  | Deep learning engine                      |
| **NLTK**                 | 3.9.3   | Stopwords bahasa Indonesia                |
| **Sastrawi**             | 1.0.1   | Stemmer bahasa Indonesia                  |
| **openpyxl**             | 3.1.5   | Baca/tulis file Excel (.xlsx)             |
| **ftfy**                 | 6.3.1   | Fix text encoding issues                  |

### Frontend
| Teknologi                | Fungsi                                         |
|--------------------------|------------------------------------------------|
| **TailwindCSS** (CDN)    | Utility-first CSS framework                   |
| **Plus Jakarta Sans**    | Font utama (Google Fonts)                      |
| **IBM Plex Mono**        | Font monospace untuk kode/angka                |
| **Vanilla JavaScript**   | Validasi form, UI interaksi, modal             |

### Model AI
| Model                    | Keterangan                                     |
|--------------------------|------------------------------------------------|
| **SimCSE-IndoBERT**      | Model sentence embedding bahasa Indonesia      |
| Format: `safetensors`    | Ukuran: ~498 MB                                |
| Dimensi embedding: **768** | Normalized embeddings                        |

---

## 8. Cara Menjalankan Aplikasi

### Prasyarat
- Python 3.8+
- pip (package manager)

### Langkah-langkah

```bash
# 1. Clone/Masuk ke direktori proyek
cd novelty_detection_web_baru

# 2. Buat virtual environment
python -m venv venv

# 3. Aktifkan virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Install dependensi
pip install -r requirements.txt

# 5. Pastikan folder model/ dan dataset/ sudah berisi file yang diperlukan
#    - model/simcse-indobert/ (model SimCSE)
#    - dataset/df_train.xlsx (dataset judul TA)
#    - dataset/embeddings_*.npy (pre-computed embeddings)

# 6. Jalankan aplikasi
python app.py

# 7. Buka browser
# → http://localhost:5000
```

### Catatan Penting
- **Waktu startup pertama** mungkin agak lama karena model SimCSE-IndoBERT (~498 MB) dimuat ke memori.
- **File `dataset/history.xlsx`** akan dibuat otomatis saat pengguna pertama kali melakukan pengecekan.
- Aplikasi berjalan dalam **debug mode** (`app.run(debug=True)`) — matikan untuk produksi.

---

> **Dokumen ini dibuat secara otomatis pada 30 Mei 2026.**
> Untuk dokumentasi fitur dalam format Agile, lihat file `fitur_dokumentasi_agile.md`.
