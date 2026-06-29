import os
from flask import Flask, render_template, request, send_file, redirect, url_for
from engine.retrieval import search_similar, dataset
from engine.history import save_to_history, load_history

app = Flask(__name__)

# Halaman utama: form input query dan menampilkan hasil kemiripan
@app.route("/", methods=["GET", "POST"])
def index():

    results = None
    error = None
    saved = False

    if request.method == "POST":
        judul = request.form.get("judul", "").strip()
        deskripsi = request.form.get("deskripsi", "").strip()
        mode = request.form.get("mode", "judul")

        # Validasi input kosong berdasarkan mode yang dipilih
        if mode == "judul" and not judul:
            error = "Judul Tugas Akhir wajib diisi."
        elif mode == "deskripsi" and not deskripsi:
            error = "Deskripsi Penelitian wajib diisi."
        elif mode == "kombinasi" and (not judul or not deskripsi):
            # Kumpulkan field yang kosong untuk pesan error yang informatif
            missing = []
            if not judul:
                missing.append("Judul")
            if not deskripsi:
                missing.append("Deskripsi")
            error = f"{' dan '.join(missing)} wajib diisi untuk mode Kombinasi."
        else:
            try:
                # Cari kemiripan dan simpan hasil ke history
                results = search_similar(judul, deskripsi, mode)
                save_to_history(results)
                saved = True
            except Exception as e:
                error = str(e)

    return render_template(
        "index.html",
        results=results,
        error=error,
        saved=saved
    )

# Halaman riwayat pengujian dengan pagination
@app.route("/history")
def history():
    data = load_history()

    # Pagination: 5 items per page
    per_page = 5
    total_items = len(data)
    # Hitung total halaman (ceiling division)
    total_pages = max(1, (total_items + per_page - 1) // per_page)

    # Ambil nomor halaman dari query string, clamp ke range valid
    page = request.args.get("page", 1, type=int)
    page = max(1, min(page, total_pages))

    # Potong data sesuai halaman saat ini
    start = (page - 1) * per_page
    end = start + per_page
    paginated_data = data[start:end]

    return render_template(
        "history.html",
        history=paginated_data,
        page=page,
        total_pages=total_pages,
        total_items=total_items
    )

# Download file history dalam format Excel
@app.route("/history/download")
def download_history():
    history_file = os.path.join(os.path.dirname(__file__), "dataset", "history.xlsx")
    if os.path.exists(history_file):
        return send_file(
            history_file,
            as_attachment=True,
            download_name="history_pengujian.xlsx"
        )
    # Redirect ke halaman history jika file belum ada
    return redirect(url_for("history"))

if __name__ == "__main__":
    app.run(debug=True)