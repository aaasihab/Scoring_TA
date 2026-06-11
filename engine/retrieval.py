import pandas as pd
import numpy as np

from engine.preprocessing import combine_text
from engine.embedding import encode_text
from engine.similarity import compute_similarity, get_top_k
from engine.unique import calculate_unique
from engine.preprocessing import preprocess_text

# Load Dataset
dataset = pd.read_excel("dataset/df_train.xlsx")

# Load Embeddings
embedding_judul = np.load("dataset/embeddings_title_train.npy")
embedding_deskripsi = np.load("dataset/embeddings_description_train.npy")
embedding_gabungan = np.load("dataset/embeddings_combined_train.npy")

# Search Similar
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
        query = combine_text(judul, deskripsi)
        query_text = query[0]
        query_judul = query[1]
        query_deskripsi = query[2]
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
            text_judul = dataset.iloc[idx]["judul_preprocessed"]
            text_deskripsi = dataset.iloc[idx]["deskripsi_preprocessed"]

        # Klasifikasi Skala
        score = round(float(score), 2)
        if score >= 0.8:
            label = "Sangat Mirip"
        elif score >= 0.6:
            label = "Mirip"
        else:
            label = "Tidak Mirip"

        # Simpan hasil
        result_item = {
            "text": text_result,
            "score": score,
            "label": label
        }

        if mode == "kombinasi":
            result_item["text_judul"] = text_judul
            result_item["text_deskripsi"] = text_deskripsi

        results.append(result_item)
    unique = calculate_unique(top_scores)

    result_dict = {
        "raw_query": raw_query,
        "query": query_text,
        "mode": mode,
        "results": results,
        "unique": unique
    }

    if mode == "kombinasi":
        result_dict["query_judul"] = query_judul
        result_dict["query_deskripsi"] = query_deskripsi

    return result_dict