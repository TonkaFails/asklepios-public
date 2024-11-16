import requests
import json
from langchain_huggingface import HuggingFaceEmbeddings
import chromadb
import dill
from langchain.embeddings import HuggingFaceEmbeddings

# Replace with your actual API token
API_TOKEN = "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"

embedding_function = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")
API_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/BAAI/bge-base-en-v1.5"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def get_embeddings(texts):
    response = requests.post(API_URL, headers=headers, json={"inputs": texts})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Request failed: {response.status_code}, {response.text}")

# Example texts
with open('/Users/timon/asklepios/backend/data/guidelines/pymupdf_4096.pkl', 'rb') as f:
    all_chunks = list(dill.load(f))
ids = range(len(all_chunks))
texts = [chunk.page_content for chunk in all_chunks]
embeddings = get_embeddings(texts)

# Initialize the Chroma client
client = chromadb.Client()

# Create a collection with the embedding function
collection_name = 'text_collection'
collection = client.create_collection(
    name=collection_name,
    embedding_function=embedding_function
)

collection.add(
    embeddings = embeddings,
    documents = texts,
    metadatas = [chunk.metadata for chunk in all_chunks],
    ids = ids
)
