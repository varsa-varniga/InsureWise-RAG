import chromadb
from rag.embedder import get_embedding
import uuid

# ✅ Use the new PersistentClient
client = chromadb.PersistentClient(path="chroma_db")

def store_chunks(chunks: list, collection_name: str = "insurance_clauses"):
    # ❗ Delete existing collection if it exists to avoid embedding dimension mismatch
    try:
        client.delete_collection(name=collection_name)
    except Exception as e:
        if "does not exist" not in str(e):
            print(f"⚠️ Error deleting collection: {e}")

    # ✅ Create a new collection
    collection = client.create_collection(name=collection_name)

    # Store chunks one by one
    for i, chunk in enumerate(chunks):
        emb = get_embedding(chunk)  # Returns a list of float (embedding)
        collection.add(
            documents=[chunk],
            embeddings=[emb],
            ids=[str(uuid.uuid4())]
        )
        print(f"🧠 Embedded and stored chunk {i+1}/{len(chunks)}")
