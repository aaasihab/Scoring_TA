import numpy as np


# ======================================
# Hitung Novelty Score
# ======================================

def calculate_novelty(top_scores):

    """
    top_scores : similarity dari Top-K
    contoh: [0.82, 0.79, 0.75, 0.71, 0.68]
    """

    top_scores = np.array(top_scores)

    avg_similarity = np.mean(top_scores)
    max_similarity = np.max(top_scores)

    novelty_avg = 1 - avg_similarity
    novelty_max = 1 - max_similarity

    result = {
        "avg_similarity": round(float(avg_similarity), 2),
        "max_similarity": round(float(max_similarity), 2),
        "novelty_avg": round(float(novelty_avg), 2),
        "novelty_max": round(float(novelty_max), 2)
    }

    return result