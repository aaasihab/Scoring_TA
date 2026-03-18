import numpy as np


# ======================================
# Hitung Novelty Score
# ======================================

import numpy as np

def calculate_novelty(top_scores, min_sim=0.6, max_sim=1.0):

    top_scores = np.array(top_scores)

    # ==============================
    # Min-Max Scaling
    # ==============================

    scaled_scores = (top_scores - min_sim) / (max_sim - min_sim)

    # Clamp agar tidak keluar dari 0–1
    scaled_scores = np.clip(scaled_scores, 0, 1)

    # ==============================
    # Hitung Similarity (scaled)
    # ==============================

    avg_similarity = np.mean(scaled_scores)
    max_similarity = np.max(scaled_scores)

    # ==============================
    # Hitung Novelty
    # ==============================

    novelty_avg = 1 - avg_similarity
    novelty_max = 1 - max_similarity

    result = {
        "avg_similarity": round(float(avg_similarity), 2),
        "max_similarity": round(float(max_similarity), 2),
        "novelty_avg": round(float(novelty_avg), 2),
        "novelty_max": round(float(novelty_max), 2)
    }

    return result