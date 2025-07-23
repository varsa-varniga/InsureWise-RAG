from sentence_transformers import SentenceTransformer

# Load the model once globally (faster than loading on every call)
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text: str):
    """
    Returns the embedding of the given text using a local model.
    """
    embedding = model.encode(text)
    return embedding.tolist()