import torch
import os
import fitz
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

CHUNK_SIZE = 512
MODEL_NAME = 'all-MiniLM-L6-v2'
embedding_model = SentenceTransformer(MODEL_NAME)
embeddings = []
documents = []

def process_pdfs(folder_path: str):
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            process_pdf(pdf_path)
    return embeddings, documents

def process_pdf(pdf_path: str):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()

    chunks = chunk_text(text)
    for chunk in chunks:
        embedding = get_embedding(chunk)
        embeddings.append(embedding)
        documents.append(chunk)

def chunk_text(text: str):
    words = text.split()
    chunks = []
    for i in range(0, len(words), CHUNK_SIZE):
        chunk = " ".join(words[i:i + CHUNK_SIZE])
        chunks.append(chunk)
    return chunks

def get_embedding(text: str):
    return embedding_model.encode(text)

def index_pdfs(embeddings):
    embeddings_array = np.array(embeddings).astype('float32')
    index = faiss.IndexFlatL2(embeddings_array.shape[1])
    index.add(embeddings_array)
    return index

def retrieve_relevant_docs(query: str, index, documents):
    query_embedding = get_embedding(query).astype('float32')
    D, I = index.search(np.array([query_embedding]), 5)  # Top 5 relevant docs
    relevant_docs = [documents[i] for i in I[0]]
    return relevant_docs
