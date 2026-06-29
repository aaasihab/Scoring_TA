import re
import pandas as pd

# Membersihkan teks dari karakter khusus, line break, dan spasi berlebih
def cleaning(text):
    if pd.isna(text):
        return ""
    text = str(text)
    # Line break/tab -> spasi
    text = text.replace("\r", " ").replace("\n", " ").replace("\t", " ")
    # Semua karakter selain huruf/angka/spasi/hyphen -> ganti spasi
    text = re.sub(r"[^a-zA-Z0-9\s\-]", " ", text)
    # Normalisasi spasi
    text = re.sub(r"\s+", " ", text).strip()

    return text

# Mengubah seluruh teks menjadi huruf kecil
def case_folding(x):
    return str(x).lower()

# Pipeline preprocessing: case folding lalu cleaning
def preprocess_text(text):
    step1 = case_folding(text)
    step2 = cleaning(step1)
    return step2