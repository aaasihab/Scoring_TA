import pandas as pd
import numpy as np

from engine.embedding import encode_text
from engine.similarity import compute_similarity, get_top_k
from engine.unique import calculate_unique
from engine.preprocessing import preprocess_text

# Load dataset dan embedding saat modul pertama kali diimpor (sekali saja)
dataset = pd.read_excel("dataset/df_train.xlsx")
embedding_judul = np.load("dataset/embeddings_title_train.npy")
embedding_deskripsi = np.load("dataset/embeddings_description_train.npy")
embedding_gabungan = np.load("dataset/embeddings_combined_train.npy")


# Cari Top 5 teks paling mirip berdasarkan mode (judul/deskripsi/kombinasi)
def search_similar(judul, deskripsi, mode):

    # Tentukan query dan embedding dataset berdasarkan mode pencarian
    if mode == "judul":
        raw_query = judul
        query_text = preprocess_text(judul)
        dataset_embedding = embedding_judul

    elif mode == "deskripsi":
        raw_query = deskripsi
        query_text = preprocess_text(deskripsi)
        dataset_embedding = embedding_deskripsi

    elif mode == "kombinasi":
        raw_query = judul + " " + deskripsi
        # Preprocessing judul dan deskripsi secara terpisah, lalu gabungkan
        query_judul = preprocess_text(judul)
        query_deskripsi = preprocess_text(deskripsi)
        query_text = query_judul + " " + query_deskripsi
        dataset_embedding = embedding_gabungan

    else:
        raise ValueError("Mode tidak valid")

    # Encode query menjadi vektor embedding, reshape ke 2D untuk cosine similarity
    query_embedding = encode_text(query_text)
    query_embedding = query_embedding.reshape(1, -1)

    # Hitung cosine similarity antara query dan seluruh dataset
    similarities = compute_similarity(query_embedding, dataset_embedding)

    # Ambil 5 indeks dan skor tertinggi
    top_idx, top_scores = get_top_k(similarities, k=5)

    results = []

    for idx, score in zip(top_idx, top_scores):
        # Ambil teks hasil dari dataset sesuai mode
        if mode == "judul":
            text_result = dataset.iloc[idx]["judul_preprocessed"]

        elif mode == "deskripsi":
            text_result = dataset.iloc[idx]["deskripsi_preprocessed"]

        else:
            # Mode kombinasi: gabungkan judul + deskripsi, simpan juga terpisah
            text_result = (
                dataset.iloc[idx]["judul_preprocessed"] + " " +
                dataset.iloc[idx]["deskripsi_preprocessed"]
            )
            text_judul = dataset.iloc[idx]["judul_preprocessed"]
            text_deskripsi = dataset.iloc[idx]["deskripsi_preprocessed"]

        # Klasifikasi skor ke dalam label kemiripan
        score = round(float(score), 2)
        if score >= 0.8:
            label = "Sangat Mirip"
        elif score >= 0.6:
            label = "Mirip"
        else:
            label = "Tidak Mirip"

        # Susun dictionary hasil per item
        result_item = {
            "text": text_result,
            "score": score,
            "label": label
        }

        # Tambahkan judul & deskripsi terpisah untuk mode kombinasi
        if mode == "kombinasi":
            result_item["text_judul"] = text_judul
            result_item["text_deskripsi"] = text_deskripsi

        results.append(result_item)

    # Hitung skor keunikan berdasarkan Top 5 similarity scores
    unique = calculate_unique(top_scores)

    # Susun dictionary hasil akhir
    result_dict = {
        "raw_query": raw_query,
        "query": query_text,
        "mode": mode,
        "results": results,
        "unique": unique
    }

    # Sertakan query judul & deskripsi yang sudah dipreprocess (mode kombinasi)
    if mode == "kombinasi":
        result_dict["query_judul"] = query_judul
        result_dict["query_deskripsi"] = query_deskripsi

    return result_dict