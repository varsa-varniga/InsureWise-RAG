from fastapi import APIRouter
from pydantic import BaseModel
from rag.retriever import retrieve_top_chunks
from rag.reasoning import build_prompt, get_llm_response

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

@router.post("/")
def process_query(req: QueryRequest):
    query = req.query
    chunks = retrieve_top_chunks(query)
    prompt = build_prompt(query, chunks)
    response = get_llm_response(prompt)
    return {"query": query, "response": response}
