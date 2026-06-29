import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Hitung cosine similarity antara satu query embedding dan seluruh embedding dataset
def compute_similarity(query_embedding, dataset_embeddings):
    query_embedding = query_embedding.reshape(1, -1)
    similarities = cosine_similarity(
        query_embedding,
        dataset_embeddings
    )
    # Flatten dari 2D (1, N) ke 1D array
    return similarities.flatten()

# Ambil K indeks dan skor tertinggi dari array similarity (descending)
def get_top_k(similarity_scores, k=5):
    top_indices = np.argsort(similarity_scores)[::-1][:k]
    top_scores = similarity_scores[top_indices]
    return top_indices, top_scores