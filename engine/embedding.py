from sentence_transformers import SentenceTransformer

# Load Model IndoBERT SimCSE
MODEL_PATH = "model/simcse-indobert"
model = SentenceTransformer(MODEL_PATH)
def encode_text(text):
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding