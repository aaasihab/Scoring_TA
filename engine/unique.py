import numpy as np

# Klasifikasi skor keunikan menjadi label deskriptif
def classify_unique(score):
    if score >= 0.75:
        return "Sangat Unik"
    elif score >= 0.5:
        return "Cukup Unik"
    elif score >= 0.25:
        return "Kurang Unik"
    else:
        return "Tidak Unik"

# Hitung skor keunikan berdasarkan Top K similarity scores
# Keunikan = 1 - similarity tertinggi (setelah Min-Max Scaling)
def calculate_unique(top_scores, min_sim=0.6, max_sim=1.0):

    top_scores = np.array(top_scores)

    # Min-Max Scaling: normalisasi skor ke rentang [0, 1] berdasarkan batas min/max
    scaled_scores = (top_scores - min_sim) / (max_sim - min_sim)

    # Clamp agar tidak keluar dari rentang 0–1
    scaled_scores = np.clip(scaled_scores, 0, 1)

    # Ambil similarity tertinggi dari skor yang sudah di-scale
    max_similarity = np.max(scaled_scores)

    # Skor keunikan = kebalikan dari similarity tertinggi
    unique_max = 1 - max_similarity

    # Klasifikasi skor keunikan ke label
    label_max = classify_unique(unique_max)

    return {
        "max_similarity": round(float(max_similarity), 2),
        "unique_max": round(float(unique_max), 2),
        "label_max": label_max
    }
