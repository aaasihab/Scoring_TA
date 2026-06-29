from sentence_transformers import SentenceTransformer

# Load model IndoBERT SimCSE
MODEL_PATH = "model/simcse-indobert"
model = SentenceTransformer(MODEL_PATH)
# Encode teks menjadi vektor embedding menggunakan model SimCSE IndoBERT
def encode_text(text):
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding