import os
import fitz  # PyMuPDF
from transformers import BertTokenizer, BertModel
import torch
import numpy as np
import faiss

# Initialize BERT models and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
chunk_model = BertModel.from_pretrained('bert-base-uncased')
aggregation_model = BertModel.from_pretrained('bert-base-uncased')

def extract_text_from_pdf(pdf_path):
    try:
        doc_text = []
        with fitz.open(pdf_path) as doc:
            for page in doc:
                doc_text.append(page.get_text())
        return " ".join(doc_text)
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return None

def get_bert_embeddings(text, tokenizer, model, max_length=512):
    tokenized_text = tokenizer(text, add_special_tokens=True, return_tensors='pt', truncation=True, max_length=max_length)
    input_ids = tokenized_text['input_ids'][0]
    attention_mask = tokenized_text['attention_mask'][0]
    outputs = model(input_ids.unsqueeze(0), attention_mask.unsqueeze(0))
    return outputs.last_hidden_state.mean(1).detach()

def hierarchical_bert_processing(text, tokenizer, chunk_model, aggregation_model, max_chunk_length=512):
    tokens = tokenizer.tokenize(text)
    max_chunk_size = max_chunk_length - 2
    chunks = [tokens[i:i + max_chunk_size] for i in range(0, len(tokens), max_chunk_size)]
    chunk_embeddings = []

    for chunk in chunks:
        chunk_text = tokenizer.convert_tokens_to_string(chunk)
        embedding = get_bert_embeddings(chunk_text, tokenizer, chunk_model, max_length=max_chunk_length)
        chunk_embeddings.append(embedding.squeeze())

    if len(chunk_embeddings) > 1:
        aggregated_embeddings = torch.stack(chunk_embeddings).mean(0)
    else:
        aggregated_embeddings = chunk_embeddings[0]

    return aggregated_embeddings.numpy()

def build_vector_database(folder_path, index_file='vector_index.faiss', embedding_dim=768):
    pdf_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.pdf')]
    embeddings = []
    for pdf_file in pdf_files:
        text = extract_text_from_pdf(pdf_file)
        if text:
            document_embedding = hierarchical_bert_processing(text, tokenizer, chunk_model, aggregation_model)
            embeddings.append(document_embedding)

    if embeddings:
        embeddings_array = np.array(embeddings)
        index = faiss.IndexFlatL2(embedding_dim)
        index.add(embeddings_array)
        faiss.write_index(index, index_file)
        print(f"Index built and saved to {index_file}")
    else:
        print("No embeddings were generated.")
