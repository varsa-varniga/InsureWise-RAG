import chromadb
from rag.embedder import get_embedding

# Reconnect to ChromaDB
client = chromadb.PersistentClient(path="chroma_db")

def retrieve_top_chunks(query: str, top_k: int = 5, collection_name: str = "insurance_clauses"):
    # Load collection
    collection = client.get_collection(name=collection_name)

    # Embed the query
    query_embedding = get_embedding(query)

    # Search for top-k similar documents
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "distances"]
    )

    # Pack results
    top_chunks = results["documents"][0]
    distances = results["distances"][0]

    return list(zip(top_chunks, distances))
