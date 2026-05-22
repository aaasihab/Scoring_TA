import pandas as pd
import numpy as np

from engine.preprocessing import combine_text
from engine.embedding import encode_text
from engine.similarity import compute_similarity, get_top_k
from engine.unique import calculate_unique
from engine.preprocessing import preprocess_text


# ======================================
# Load Dataset
# ======================================

dataset = pd.read_csv("dataset/df_train.csv")


# ======================================
# Load Embeddings
# ======================================

embedding_judul = np.load("dataset/embeddings_title_train.npy")
embedding_deskripsi = np.load("dataset/embeddings_description_train.npy")
embedding_gabungan = np.load("dataset/embeddings_combined_train.npy")


# ======================================
# Search Similar
# ======================================

def search_similar(judul, deskripsi, mode):

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
        query_text = combine_text(judul, deskripsi)
        dataset_embedding = embedding_gabungan

    else:
        raise ValueError("Mode tidak valid")


    # Encode query
    query_embedding = encode_text(query_text)
    query_embedding = query_embedding.reshape(1, -1)

    # Hitung similarity
    similarities = compute_similarity(query_embedding, dataset_embedding)

    # Top 5
    top_idx, top_scores = get_top_k(similarities, k=5)

    results = []

    for idx, score in zip(top_idx, top_scores):

        # ==============================
        # Ambil teks sesuai mode
        # ==============================

        if mode == "judul":
            text_result = dataset.iloc[idx]["judul_preprocessed"]
            raw_text_result = dataset.iloc[idx]["judul_ta"]

        elif mode == "deskripsi":
            text_result = dataset.iloc[idx]["deskripsi_preprocessed"]
            raw_text_result = dataset.iloc[idx]["deskripsi"]

        else:
            text_result = (
                dataset.iloc[idx]["judul_preprocessed"] + " " +
                dataset.iloc[idx]["deskripsi_preprocessed"]
            )
            raw_text_result = (
                dataset.iloc[idx]["judul_ta"] + " " +
                dataset.iloc[idx]["deskripsi"]
            )

        # ==============================
        # Klasifikasi Skala
        # ==============================

        score = round(float(score), 2)
        if score >= 0.8:
            label = "Sangat Mirip"
        elif score >= 0.6:
            label = "Mirip"
        else:
            label = "Tidak Mirip"

        # ==============================
        # Simpan hasil
        # ==============================

        results.append({
            "text": text_result,
            "score": score,
            "label": label
        })
    unique = calculate_unique(top_scores)

    return {
        "raw_query": raw_query,
        "query": query_text,
        "mode": mode,
        "results": results,
        "unique": unique
    }