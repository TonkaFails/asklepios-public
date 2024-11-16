from retriever import process_pdfs, index_pdfs, retrieve_relevant_docs
from database import save_embeddings
from trash.generator import generate_response

def main(folder_path: str):
    embeddings, documents = process_pdfs(folder_path)
    index = index_pdfs(embeddings)
    
    save_embeddings(embeddings)

    query = "Wie hoch ist das Risko einer Knieverletzung bei Adipositas?"
    relevant_docs = retrieve_relevant_docs(query, index, documents)
    generated_response = generate_response(query, relevant_docs)
    print(generated_response)

if __name__ == "__main__":
    import sys
    folder_path = "leitlinien"
    main(folder_path)
