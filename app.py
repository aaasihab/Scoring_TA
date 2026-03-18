from flask import Flask, render_template, request
from engine.retrieval import search_similar

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():

    results = None
    error = None

    if request.method == "POST":

        judul = request.form.get("judul")
        deskripsi = request.form.get("deskripsi")
        mode = request.form.get("mode")

        try:
            results = search_similar(judul, deskripsi, mode)
        except Exception as e:
            error = str(e)

    return render_template(
        "index.html",
        results=results,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)