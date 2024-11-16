import os
import re
import json
import fitz
import torch
from tqdm import tqdm
from transformers import pipeline

pdf_folder = './data/guidelines'

irrelevant_sections = [
    "Autor", "Danksagung", "Haftungsausschluss", "Literatur", 
    "Inhaltsverzeichnis", "Impressum", "Urheberrecht"
]

def preprocess_text(text):
    lines = text.splitlines()
    filtered_lines = []
    for line in lines:
        if not any(section in line for section in irrelevant_sections):
            filtered_lines.append(line)
    return "\n".join(filtered_lines)

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return preprocess_text(text)

def extract_text_from_pdfs(pdf_folder, max_pdfs):
    pdf_count = 0
    for filename in os.listdir(pdf_folder):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder, filename)
            yield filename, extract_text_from_pdf(pdf_path)
            pdf_count += 1
            if pdf_count >= max_pdfs:
                break

def split_into_chunks(text, chunk_size=500):
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunk, chunks = "", []
    for sentence in sentences:
        if len(chunk) + len(sentence) < chunk_size:
            chunk += " " + sentence
        else:
            chunks.append(chunk.strip())
            chunk = sentence
    if chunk:
        chunks.append(chunk.strip())
    return chunks

device = "mps" if torch.backends.mps.is_available() else "cpu"

qg_pipeline = pipeline('text2text-generation', model='mrm8488/t5-base-finetuned-question-generation-ap', device=0 if device == "mps" else -1)
qa_pipeline = pipeline('question-answering', model='smanjil/German-MedBERT', device=0 if device == "mps" else -1)

def generate_question(context):
    input_text = f"generate question: {context}"
    return qg_pipeline(input_text, max_new_tokens=50)[0]['generated_text']

def extract_answer(context, question):
    return qa_pipeline({'context': context, 'question': question})['answer']

def process_and_append_to_file(pdf_name, text_chunks, output_file):
    with open(output_file, 'a') as f:
        for chunk in tqdm(text_chunks, desc=f"Processing chunks in {pdf_name}"):
            question = generate_question(chunk)
            answer = extract_answer(chunk, question)
            if answer:
                qa_entry = {
                    'pdf_name': pdf_name,
                    'context': chunk,
                    'question': question,
                    'answer': answer
                }
                f.write(json.dumps(qa_entry) + '\n')

def main():
    output_file = 'qa_dataset.jsonl'
    
    for pdf_name, text in tqdm(extract_text_from_pdfs(pdf_folder, max_pdfs=1), desc="Processing PDFs"):
        text_chunks = split_into_chunks(text)
        process_and_append_to_file(pdf_name, text_chunks, output_file)
    
    print(f"QA dataset has been saved to '{output_file}' after processing each document.")

if __name__ == "__main__":
    main()
