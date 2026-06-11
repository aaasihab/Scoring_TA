import os
from datetime import datetime
from openpyxl import Workbook, load_workbook

HISTORY_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "dataset",
    "history.xlsx"
)

HEADERS = [
    "No", "Timestamp", "Mode", "Query (Raw)", "Query (Preprocessed)",
    "Unique Score (Max)", "Label Unique (Max)",
    "Top 1 - Text", "Top 1 - Score", "Top 1 - Label",
    "Top 2 - Text", "Top 2 - Score", "Top 2 - Label",
    "Top 3 - Text", "Top 3 - Score", "Top 3 - Label",
    "Top 4 - Text", "Top 4 - Score", "Top 4 - Label",
    "Top 5 - Text", "Top 5 - Score", "Top 5 - Label",
    "Top 1 - Judul", "Top 1 - Deskripsi",
    "Top 2 - Judul", "Top 2 - Deskripsi",
    "Top 3 - Judul", "Top 3 - Deskripsi",
    "Top 4 - Judul", "Top 4 - Deskripsi",
    "Top 5 - Judul", "Top 5 - Deskripsi",
]


def save_to_history(results):

    if os.path.exists(HISTORY_FILE):
        wb = load_workbook(HISTORY_FILE)
        ws = wb.active
        next_no = ws.max_row
    else:
        wb = Workbook()
        ws = wb.active
        ws.title = "History"
        ws.append(HEADERS)
        next_no = 1

    row = [
        next_no,
        datetime.now(),
        results["mode"],
        results["raw_query"],
        results["query"],
        results["unique"]["unique_max"],
        results["unique"]["label_max"],
    ]

    # Top 1-5
    for r in results["results"]:
        row.extend([
            r["text"],
            r["score"],
            r["label"]
        ])

    # Query Judul & Deskripsi
    row.append(results.get("raw_query_judul", ""))
    row.append(results.get("raw_query_deskripsi", ""))

    # Top 1-5 Judul & Deskripsi
    for r in results["results"]:
        row.extend([
            r.get("text_judul", ""),
            r.get("text_deskripsi", "")
        ])

    # Tambah data ke worksheet
    ws.append(row)

    # Format kolom Timestamp (kolom B)
    timestamp_cell = ws.cell(row=ws.max_row, column=2)
    timestamp_cell.number_format = "dd/mm/yyyy hh:mm"

    # Simpan file
    wb.save(HISTORY_FILE)


def load_history():

    if not os.path.exists(HISTORY_FILE):
        return []

    wb = load_workbook(HISTORY_FILE)
    ws = wb.active

    headers = [cell.value for cell in ws[1]]
    data = []

    for row in ws.iter_rows(min_row=2, values_only=True):
        record = dict(zip(headers, row))
        if isinstance(record.get("Timestamp"), datetime):
            record["Timestamp"] = record["Timestamp"].strftime("%d/%m/%Y %H:%M")
        data.append(record)

    data.reverse()  # Data terbaru di atas
    return data