# 📋 Dokumentasi Fitur Aplikasi (Agile Methodology)

Dokumentasi ini disusun dalam struktur **Epic** dan **Fitur** (Features) agar memudahkan Anda dalam memecahnya menjadi *User Stories* pada metodologi Agile (misal: Scrum atau Kanban).

---

## 🚀 Epic 1: Pengecekan Kemiripan & Keunikan (Core Engine)
Epic ini mencakup fungsi utama aplikasi untuk membandingkan input pengguna dengan dataset Tugas Akhir yang ada, guna menemukan tingkat kemiripan dan menilai keunikannya.

*   **Fitur 1.1: Pencarian Berdasarkan Judul**
    *   Pengguna dapat memasukkan judul Tugas Akhir (TA) untuk dicari kemiripannya dengan dataset judul TA terdahulu.
*   **Fitur 1.2: Pencarian Berdasarkan Deskripsi**
    *   Pengguna dapat memasukkan deskripsi atau latar belakang penelitian untuk dianalisis kemiripannya secara semantik.
*   **Fitur 1.3: Pencarian Berdasarkan Kombinasi**
    *   Aplikasi dapat menggabungkan judul dan deskripsi sekaligus untuk mendapatkan analisis pencarian yang lebih komprehensif.
*   **Fitur 1.4: Sistem Pencarian Top-5 (Retriever)**
    *   Sistem secara otomatis menampilkan 5 dokumen dengan skor kemiripan tertinggi (Top 5) beserta skor *Cosine Similarity* dan klasifikasi label (Sangat Mirip, Mirip, Tidak Mirip).
*   **Fitur 1.5: Deteksi Skor Keunikan (Unique Score)**
    *   Sistem menghitung nilai keunikan berdasarkan seberapa mirip input dengan dataset tertinggi (Max Similarity).
    *   Sistem memberikan klasifikasi label keunikan secara otomatis: *Sangat Menarik, Cukup Menarik, Kurang Menarik, Tidak Menarik*.

---

## 🧠 Epic 2: Pipeline Pemrosesan Teks & Model AI (NLP)
Epic ini berfokus pada teknologi di balik layar yang memproses input bahasa alami dari pengguna sebelum dikomputasi.

*   **Fitur 2.1: Preprocessing Teks Otomatis**
    *   Teks yang diinputkan pengguna otomatis dibersihkan melalui proses *case folding* (huruf kecil) dan *cleaning* (menghapus tanda baca, baris baru, serta karakter non-alfanumerik).
*   **Fitur 2.2: Text Embedding dengan IndoBERT SimCSE**
    *   Sistem mengubah teks yang sudah dibersihkan menjadi representasi vektor numerik (*embeddings*) secara real-time menggunakan model bahasa `sentence-transformers` berbahasa Indonesia.

---

## 📊 Epic 3: Manajemen Riwayat Pengujian (History & Reporting)
Epic ini menaungi seluruh fungsionalitas untuk melacak, menyimpan, dan mengekspor log pengujian yang dilakukan pengguna.

*   **Fitur 3.1: Auto-Save Riwayat ke Excel**
    *   Setiap kali pengguna berhasil melakukan pengecekan, sistem otomatis menyimpannya sebagai satu baris data (record) ke dalam file `dataset/history.xlsx`.
*   **Fitur 3.2: Halaman Daftar Riwayat**
    *   Terdapat halaman khusus (`/history`) yang menampilkan tabel riwayat pengecekan (Waktu, Mode, Query, Skor Unik, Label Unik).
*   **Fitur 3.3: Detail Riwayat Terlipat (Expandable Row)**
    *   Pada tabel riwayat, pengguna dapat mengklik sebuah baris untuk melihat rincian "Top 5" hasil kemiripan untuk pengecekan tersebut tanpa harus pindah halaman.
*   **Fitur 3.4: Ekspor Dokumen Laporan (Download)**
    *   Terdapat tombol untuk langsung mengunduh seluruh data riwayat dalam format spreadsheet (`.xlsx`) ke komputer lokal pengguna.

---

## 🎨 Epic 4: Antarmuka & Pengalaman Pengguna (UI/UX)
Epic ini mencakup bagaimana pengguna berinteraksi secara visual dengan aplikasi web.

*   **Fitur 4.1: Formulir Input Dinamis (Dynamic Form State)**
    *   Formulir input otomatis mengaktifkan/menonaktifkan (disable/enable) kolom "Judul" dan "Deskripsi" tergantung dari *Mode Pengecekan* yang dipilih oleh pengguna, untuk mencegah kesalahan input.
*   **Fitur 4.2: Notifikasi Interaktif (Feedback UI)**
    *   Menampilkan pop-up / toast notifikasi hijau berbunyi *"Hasil berhasil disimpan ke riwayat"* yang akan hilang secara otomatis dalam 4 detik, serta peringatan merah jika terjadi *Error*.
*   **Fitur 4.3: Desain Web Responsif & Modern**
    *   UI dirancang dengan *Tailwind CSS* menggunakan prinsip desain bersih (clean design), efek hover *glass-morphism*, indikator warna dinamis berdasarkan label (merah untuk bahaya, hijau untuk aman), dan tipografi modern (Plus Jakarta Sans).

---

### Saran Pembuatan User Story (Contoh)
Jika Anda menggunakan *Scrum*, Anda bisa memformat fitur di atas seperti ini:
> **Title**: Ekspor Riwayat Pengujian
> **As a** pengguna sistem,
> **I want to** mengunduh riwayat pengujian saya dalam format Excel,
> **So that** saya dapat melampirkan hasil pengecekan tersebut pada laporan evaluasi judul.
> **Acceptance Criteria**:
> - Ada tombol "Download Excel" di halaman riwayat.
> - Ketika tombol diklik, file `history_pengujian.xlsx` akan terunduh.
> - File berisi header tabel dan seluruh histori data pengujian.
