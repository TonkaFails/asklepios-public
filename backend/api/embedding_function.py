from langchain_community.embeddings.bedrock import BedrockEmbeddings
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.embeddings.huggingface import HuggingFaceInferenceAPIEmbeddings
#from langchain_huggingface import HuggingFaceEmbeddings
# localBase for local debugging
def get_embedding_function(api_key, name):
    embeddings = None
    if name == "bedrock":
        embeddings = None
    elif name == "ollama":
        embeddings = None
    elif name == "baseDe":
        embeddings = HuggingFaceInferenceAPIEmbeddings(model_name="danielheinz/e5-base-sts-en-de", api_key=api_key)
    elif name == "localBaseDe":
        embeddings = None
        #embeddings = HuggingFaceEmbeddings(model_name="danielheinz/e5-base-sts-en-de")
    return embeddings