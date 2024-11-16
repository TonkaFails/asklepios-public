from sympy import true
from transformers import AutoTokenizer, logging
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from llama_cpp import Llama
import warnings

warnings.filterwarnings('ignore')
logging.set_verbosity(50)

EMBEDDING_MODEL_NAME = "aari1995/German_Semantic_STS_V2"
TOKEN = "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"

llm = Llama(
      model_path="./models/Meta-Llama-3-8B-Instruct.Q4_K_M.gguf",
      n_gpu_layers=-1,
      n_ctx=2048,
      verbose=False,
)

embedding_model = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL_NAME,
    multi_process=True,
    model_kwargs={"device": "mps"}
)

def retrieve(user_query):
    knowledge_vector_database = FAISS.load_local("faiss_index", embedding_model, allow_dangerous_deserialization=true)
    retrieved_docs = knowledge_vector_database.similarity_search(query=user_query, k=5)

    retrieved_docs_text = [doc.page_content for doc in retrieved_docs]
    context = "\nExtracted documents:\n" + "".join([f"Document {str(i)}:::\n" + doc for i, doc in enumerate(retrieved_docs_text)])

    final_prompt = llm.create_chat_completion(
        messages=
        [
        {"role": "system", "content": """Using the information contained in the context, give a comprehensive answer to the question. Respond only to the question asked, response should be concise and relevant to the question. If the question is not related to medical issues or question, refuse to answer in a friendly maner and remind the user that you are here to answer questions about medical guidelines. In any case your response must be in the german language."""},
        {"role": "user", "content": f"Context:\n{context}\n---\nHier die Frage. Bitte antworte auf Deutsch \n\Frage: {user_query}"}
        ])

    print(final_prompt["choices"][0]["message"]["content"])

if __name__ == '__main__':
    print("Stell deine Frage")
    while True:
        user_query = input(">")
        retrieve(user_query)