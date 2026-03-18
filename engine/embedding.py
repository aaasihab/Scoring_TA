from sentence_transformers import SentenceTransformer

# ======================================
# Load Model IndoBERT SimCSE
# ======================================

MODEL_PATH = "model/simcse-indobert"

model = SentenceTransformer(MODEL_PATH)

# ======================================
# Encode Single Text
# ======================================

def encode_text(text):

    embedding = model.encode(
        text,
        normalize_embeddings=True
    )

    return embedding


# ======================================
# Encode Multiple Text
# ======================================

def encode_batch(text_list):

    embeddings = model.encode(
        text_list,
        normalize_embeddings=True
    )

    return embeddings