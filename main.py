from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import List
import shutil
import os
import json

from rag.loader import load_pdf_text
from rag.chunker import chunk_text
from rag.embedder import get_embedding
from rag.vector_store import store_chunks
from rag.retriever import retrieve_top_chunks
from rag.reasoning import get_llm_response, build_prompt, build_definition_prompt
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    query: str

# === Utility to check if the query is informational ===
def is_informational_query(query: str) -> bool:
    lowered = query.lower()
    return lowered.startswith(("what is", "define", "explain", "meaning of", "how does"))

# === Upload and Index PDF Chunks ===
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    temp_path = f"temp/{file.filename}"
    os.makedirs("temp", exist_ok=True)
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = load_pdf_text(temp_path)
    chunks = chunk_text(text)
    store_chunks(chunks)
    os.remove(temp_path)

    return {"message": f"✅ Uploaded and stored {len(chunks)} chunks from {file.filename}"}

# === Query Endpoint ===
@app.post("/query/")
def query_llm(request: QueryRequest):
    query = request.query
    top_chunks = retrieve_top_chunks(query, top_k=5)

    if is_informational_query(query):
        prompt = build_definition_prompt(query, top_chunks)
    else:
        prompt = build_prompt(query, top_chunks)

    final_answer = get_llm_response(prompt)

    try:
        parsed_answer = json.loads(final_answer)
    except json.JSONDecodeError:
        parsed_answer = {
            "error": "LLM returned invalid JSON.",
            "raw": final_answer
        }

    return {
        "answer": parsed_answer,
        "context": top_chunks
    }
