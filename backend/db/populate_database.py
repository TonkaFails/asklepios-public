from preprocess_pdfs import load_and_split_documents
from embedding_function import get_embedding_function
from langchain.schema.document import Document
from langchain_community.vectorstores.chroma import Chroma
from tqdm import tqdm
from dotenv import load_dotenv
import os
import chromadb

load_dotenv()

CHROMA_PATH = os.getenv("CHROMA_PATH")
DATA_PATH = os.getenv("DATA_PATH")

def main(chunksize: int, type: str):
    chunks = load_and_split_documents(chunksize, DATA_PATH)
    add_to_chroma(chunks, chunksize, type)

def calculate_chunk_ids(chunks):

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        chunk.metadata["id"] = chunk_id

    return chunks

def add_to_chroma(chunks: list[Document], chunksize: int, type: str):
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding_function(type), collection_name="guidelines"+str(chunksize)+type+"cosine", collection_metadata={"hnsw:space": "cosine"}
    )

    existing_items = db.get(include=[]) 
    existing_ids = set(existing_items["ids"])

    chunks_with_ids = calculate_chunk_ids(chunks)
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)
    print(f"{len(chunks_with_ids) - len(new_chunks)} chunks already in database.")

    if len(new_chunks):
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        max_batch_size = 5461
        chunk_size = len(chunks)
        for i in tqdm(range(0, chunk_size, max_batch_size), desc="Adding document chunks to Chroma"):
            batch = chunks[i:i + max_batch_size]
            batch_ids = new_chunk_ids[i:i + max_batch_size]
            db.add_documents(batch, ids=batch_ids)

if __name__ == "__main__":
    main(4096, "baseDe")