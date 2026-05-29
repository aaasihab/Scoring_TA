import os
from flask import Flask, render_template, request, send_file, redirect, url_for
from engine.retrieval import search_similar
from utils.history import save_to_history, load_history

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():

    results = None
    error = None
    saved = False

    if request.method == "POST":

        judul = request.form.get("judul", "").strip()
        deskripsi = request.form.get("deskripsi", "").strip()
        mode = request.form.get("mode", "judul")

        # ============================
        # Validasi input kosong
        # ============================
        if mode == "judul" and not judul:
            error = "Judul Tugas Akhir wajib diisi."
        elif mode == "deskripsi" and not deskripsi:
            error = "Deskripsi Penelitian wajib diisi."
        elif mode == "kombinasi" and (not judul or not deskripsi):
            missing = []
            if not judul:
                missing.append("Judul")
            if not deskripsi:
                missing.append("Deskripsi")
            error = f"{' dan '.join(missing)} wajib diisi untuk mode Kombinasi."
        else:
            try:
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


@app.route("/history")
def history():
    data = load_history()
    return render_template("history.html", history=data)


@app.route("/history/download")
def download_history():
    history_file = os.path.join(os.path.dirname(__file__), "dataset", "history.xlsx")
    if os.path.exists(history_file):
        return send_file(
            history_file,
            as_attachment=True,
            download_name="history_pengujian.xlsx"
        )
    return redirect(url_for("history"))


if __name__ == "__main__":
    app.run(debug=True)