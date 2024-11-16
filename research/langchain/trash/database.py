from pymongo import MongoClient
import numpy as np

DATABASE_URI = "mongodb://localhost:27017/"
DB_NAME = "asklepios"
COLLECTION_NAME = "embeddings"
client = MongoClient(DATABASE_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def save_embeddings(embeddings):
    for idx, embedding in enumerate(embeddings):
        record = {"_id": idx, "embedding": embedding.tolist()}
        collection.insert_one(record)

def retrieve_embedding(idx):
    record = collection.find_one({"_id": idx})
    if record:
        return np.array(record["embedding"])
    return None

def retrieve_all_embeddings():
    embeddings = []
    cursor = collection.find({})
    for record in cursor:
        embeddings.append(np.array(record["embedding"]))
    return embeddings
