import fitz  # PyMuPDF
import os
from typing import List

def load_documents(folder_path: str) -> List[str]:
    texts = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            text = load_pdf_text(file_path)
            texts.append(text)
    return texts

def load_pdf_text(file_path: str) -> str:
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text
