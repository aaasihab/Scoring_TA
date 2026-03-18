import pandas as pd
import numpy as np

from engine.preprocessing import combine_text
from engine.embedding import encode_text
from engine.similarity import compute_similarity, get_top_k
from engine.novelty import calculate_novelty
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

        query_text = preprocess_text(judul)
        dataset_embedding = embedding_judul

    elif mode == "deskripsi":

        query_text = preprocess_text(deskripsi)
        dataset_embedding = embedding_deskripsi

    elif mode == "kombinasi":

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

        if mode == "judul":
            text_result = dataset.iloc[idx]["judul_preprocessed"]

        elif mode == "deskripsi":
            text_result = dataset.iloc[idx]["deskripsi_preprocessed"]

        else:
            text_result = dataset.iloc[idx]["judul_preprocessed"] + " " + dataset.iloc[idx]["deskripsi_preprocessed"]

        results.append({
            "text": text_result,
            "score": round(float(score), 2)
        })

    novelty = calculate_novelty(top_scores)

    return {
        "query": query_text,
        "mode": mode,
        "results": results,
        "novelty": novelty
    }