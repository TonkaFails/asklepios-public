from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from tqdm import tqdm
from langchain_core.documents import Document
from typing import List
import re

MARKDOWN_SEPARATORS = [
    "\n#{1,6} ", "```\n", "\n\\*\\*\\*+\n", "\n---+\n", "\n___+\n",
    "\n\n", "\n", " ", ""
]

def clean_text(chunks: List[Document]):
    for chunk in chunks:
        text = chunk.page_content
        text = re.sub(r'\s+', ' ', text)
        text = text.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
        text = re.sub(r'[^\w\säöüÄÖÜß]', '', text)
        text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
        chunk.page_content = text.strip()
    return chunks

def load_and_split_documents(chunk_size, DATA_PATH):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=int(chunk_size / 10),
        add_start_index=True,
        strip_whitespace=True,
        separators=MARKDOWN_SEPARATORS,
        length_function=len,
    )

    all_chunks = []
    pdf_files = [f for f in os.listdir(DATA_PATH) if f.endswith('.pdf')]
    # uncomment for limiting pdfs
    #pdf_files = pdf_files[:1]
    
    for pdf_file in tqdm(pdf_files, desc="Processing PDFs"):
        try:
            pdf_path = os.path.join(DATA_PATH, pdf_file)
            document_loader = PyMuPDFLoader(pdf_path)
            documents = document_loader.load()
            chunks = text_splitter.split_documents(documents)
            clean_chunks = clean_text(chunks)
            all_chunks.extend(clean_chunks)
        except Exception as e:
            print(f"Error processing {pdf_file}: {e}")
    
    return all_chunks