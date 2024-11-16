import os
from typing import List, Optional
import pandas as pd
from transformers import AutoTokenizer
from langchain.docstore.document import Document as LangchainDocument
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, PyPDFDirectoryLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy

os.environ['TOKENIZERS_PARALLELISM'] = 'false'

EMBEDDING_MODEL_NAME = "aari1995/German_Semantic_STS_V2"
MARKDOWN_SEPARATORS = [
    "\n#{1,6} ", "```\n", "\n\\*\\*\\*+\n", "\n---+\n", "\n___+\n",
    "\n\n", "\n", " ", ""
]

def split_documents(chunk_size: int, knowledge_base: List[LangchainDocument], tokenizer_name: Optional[str] = EMBEDDING_MODEL_NAME) -> List[LangchainDocument]:
    text_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
        AutoTokenizer.from_pretrained(tokenizer_name),
        chunk_size=chunk_size,
        chunk_overlap=int(chunk_size / 10),
        add_start_index=True,
        strip_whitespace=True,
        separators=MARKDOWN_SEPARATORS,
    )
    docs_processed = []
    for doc in knowledge_base:
        docs_processed += text_splitter.split_documents([doc])
    unique_texts = {}
    docs_processed_unique = []
    for doc in docs_processed:
        if doc.page_content not in unique_texts:
            unique_texts[doc.page_content] = True
            docs_processed_unique.append(doc)
    return docs_processed_unique

def main():
    pdf_path = "leitlinien"
    loader = PyPDFDirectoryLoader(pdf_path)
    data = loader.load()
    raw_text = [LangchainDocument(page_content=str(page), metadata={"source": "local"}) for page in data]
    docs_processed = split_documents(512, raw_text)
    embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME, multi_process=True, model_kwargs={"device": "mps"}, encode_kwargs={"normalize_embeddings": True})
    knowledge_vector_database = FAISS.from_documents(docs_processed, embedding_model, distance_strategy=DistanceStrategy.COSINE)
    knowledge_vector_database.save_local("faiss_index")

if __name__ == '__main__':
    main()
