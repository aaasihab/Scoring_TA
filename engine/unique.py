import numpy as np

# Klasifikasi Label
def classify_unique(score):

    if score >= 0.75:
        return "Sangat Unik"
    elif score >= 0.5:
        return "Cukup Unik"
    elif score >= 0.25:
        return "Kurang Unik"
    else:
        return "Tidak Unik"

# Hitung Unique Score
def calculate_unique(top_scores, min_sim=0.6, max_sim=1.0):

    top_scores = np.array(top_scores)

    # Min-Max Scaling
    scaled_scores = (top_scores - min_sim) / (max_sim - min_sim)

    # Clamp agar tidak keluar dari 0–1
    scaled_scores = np.clip(scaled_scores, 0, 1)

    # Hitung Similarity (scaled)

    max_similarity = np.max(scaled_scores)

    # Hitung Unique
    unique_max = 1 - max_similarity

    # Label Unique
    label_max = classify_unique(unique_max)

    # Output
    result = {
        "max_similarity": round(float(max_similarity), 2),
        "unique_max": round(float(unique_max), 2),
        "label_max": label_max
    }

    return result
