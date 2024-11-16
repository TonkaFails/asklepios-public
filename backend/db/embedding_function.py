from langchain_community.embeddings.bedrock import BedrockEmbeddings
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

def get_embedding_function(name  = "baseDe"):
    embeddings = None
    if name == "bedrock":
        embeddings = BedrockEmbeddings(
            credentials_profile_name="default", region_name="us-east-1"
        )
    elif name == "ollama":
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
    elif name == "baseDe":
        embeddings = HuggingFaceEmbeddings(model_name="danielheinz/e5-base-sts-en-de")
    return embeddings