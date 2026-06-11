import re
import pandas as pd

# Cleaning
def cleaning(text):
    if pd.isna(text):
        return ""
    text = str(text)

    # Line break/tab -> spasi
    text = text.replace("\r", " ").replace("\n", " ").replace("\t", " ")

    # Semua karakter selain huruf/angka/spasi/hyphen -> ganti spasi
    text = re.sub(r"[^a-zA-Z0-9\s\-]", " ", text)

    # 5) Normalisasi spasi
    text = re.sub(r"\s+", " ", text).strip()

    return text

# Case Folding
def case_folding(x):

    return str(x).lower()

# Pipeline Preprocessing
def preprocess_text(text):
    step1 = case_folding(text)
    step2 = cleaning(step1)
    return step2

# Gabungkan Judul + Deskripsi

def combine_text(judul, deskripsi):

    judul_clean = preprocess_text(judul)

    deskripsi_clean = preprocess_text(deskripsi)

    gabungan = judul_clean + " " + deskripsi_clean

    return gabungan, judul_clean, deskripsi_clean