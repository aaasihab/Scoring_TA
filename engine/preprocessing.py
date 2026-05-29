import re
import pandas as pd
from ftfy import fix_text
import nltk
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# =========================================
# Setup Stopwords & Stemmer
# =========================================

try:
    stopwords.words('indonesian')
except LookupError:
    nltk.download('stopwords')

list_stopwords = set(stopwords.words('indonesian'))

factory = StemmerFactory()
stemmer = factory.create_stemmer()

# =========================================
# 1. Cleaning
# =========================================

def cleaning(text):
    if pd.isna(text):
        return ""
    text = str(text)

    # 3) Line break/tab -> spasi
    text = text.replace("\r", " ").replace("\n", " ").replace("\t", " ")

    # 4) Semua karakter selain huruf/angka/spasi/hyphen -> ganti spasi
    text = re.sub(r"[^a-zA-Z0-9\s\-]", " ", text)

    # 5) Normalisasi spasi
    text = re.sub(r"\s+", " ", text).strip()

    return text


# =========================================
# 2. Case Folding
# =========================================

def case_folding(x):

    return str(x).lower()


# =========================================
# 3. Tokenize
# =========================================

def tokenize(text):

    return text.split()


# =========================================
# 4. Stopword Removal
# =========================================

def remove_stopwords(words):

    if not isinstance(words, list):
        return []

    filtered_words = [
        word for word in words
        if word not in list_stopwords
    ]

    return filtered_words


# =========================================
# 5. Stemming
# =========================================

def stem_text(words):

    if isinstance(words, list):
        text = " ".join(words)
    else:
        text = str(words)

    return stemmer.stem(text)


# =========================================
# 6. Pipeline Preprocessing
# =========================================

def preprocess_text(text):

    step1 = case_folding(text)

    step2 = cleaning(step1)

    # step3 = tokenize(step2)

    # step4 = remove_stopwords(step3)

    # step5 = stem_text(step4)

    return step2


# =========================================
# 7. Gabungkan Judul + Deskripsi
# =========================================

def combine_text(judul, deskripsi):

    judul_clean = preprocess_text(judul)

    deskripsi_clean = preprocess_text(deskripsi)

    gabungan = judul_clean + " " + deskripsi_clean

    return gabungan, judul_clean, deskripsi_clean