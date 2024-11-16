from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

GENERATOR_MODEL = 'facebook/bart-large-cnn'
tokenizer = AutoTokenizer.from_pretrained(GENERATOR_MODEL)
model = AutoModelForSeq2SeqLM.from_pretrained(GENERATOR_MODEL)
model.to('cpu')

def generate_response(query: str, relevant_docs: list):
    context = " ".join(relevant_docs)
    input_text = f"Question: {query}\nContext: {context}"
    inputs = tokenizer(input_text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    inputs = {k: v.to('cpu') for k, v in inputs.items()}  # Move inputs to CPU
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=512)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response
