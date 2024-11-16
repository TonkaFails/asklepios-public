import streamlit as st
import os
import requests
from requests.auth import HTTPBasicAuth

def save_conversation(prompt, role, sources = None, context = None):
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({"role": role, 'sources': sources, "content": prompt, "context": context})
    else:
        st.session_state.messages.append({"role": role, 'sources': sources, "content": prompt, "context": context})
    
    st.session_state.chat_history.update({st.session_state.current_chat_name: st.session_state['messages']})
    

def increase_button_count():
    if "button_count" not in st.session_state:
        st.session_state.button_count = 0
    else:
        st.session_state.button_count += 1

def generate_streaming_response():
    #flask_backend_url = "http://127.0.0.1:5001/query"
    flask_backend_url = "https://anton-hofmeier.de/api/query"
    
    if 'messages' in st.session_state:
        query_text = st.session_state.messages[-1]["content"]
        
        # Stream the response from the Flask backend
        relevant_chat_history = [{k: v for k, v in message.items() if k not in ['context', 'sources']} for message in st.session_state.messages]
        response = requests.post(flask_backend_url, json={"query_text": query_text, "chat_history":relevant_chat_history}, stream=True, auth=HTTPBasicAuth(os.getenv("USERNAME"), os.getenv("PASSWORD")))
        
        if response.status_code == 200:
            for chunk in response.iter_content(chunk_size=1024, decode_unicode=True):
                if chunk:
                    yield chunk
        else:
            yield "Error: Unable to fetch response from the backend."

def generate_old_messages():
    if "messages" in st.session_state:
        for message in st.session_state.messages:
            if message["sources"]:
                with st.chat_message(message["role"], avatar="🤖"):
                    st.markdown(message["content"])
                    generate_download_link(message["sources"], message["context"])
            else:
                if message["role"] == "user":
                    with st.chat_message(message["role"], avatar="👨‍💻"):
                        st.markdown(message["content"])
                else:
                    with st.chat_message(message["role"], avatar="🤖"):
                        st.markdown(message["content"])

def generate_download_link(guideline_paths, context):
    guideline_paths = guideline_paths.split(".pdf")
    guidelines = [guideline_path.split('/')[-1] for guideline_path in guideline_paths][:-1]
    context = context.split("<context>")[1:]

    sources = list(zip(guidelines, context))
    
    sources = [(key, [v for k, v in sources if k == key]) for key in {k for k, _ in sources}]
    
    pdf_folder = os.path.join(os.path.dirname(__file__), '../guidelines')
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
    selected_pdfs = [pdf for pdf in pdf_files if any(substring in pdf for substring in guidelines)]
    selected_pdf_paths = [os.path.join(pdf_folder, selected_pdf) for selected_pdf in selected_pdfs]
    sources = [(s,) + tupel[1:] for tupel in sources for s in selected_pdf_paths if tupel[0] in s]
    
    #Biete Datei zum Download an
    st.subheader("Quellen:")
    
    for pdf_path, context_texts in sources:
        document_name = pdf_path.split('/')[-1]
        st.caption(document_name)
        with st.popover("verwendete Textauszüge anzeigen"):
            for count, tab  in enumerate(st.tabs([f"{i+1}.Textauszug" for i in range(len(context_texts))])):
                tab.info(context_texts[count])
        increase_button_count()
        with open(pdf_path, 'rb') as f:
            pdf_data = f.read()
            st.download_button(
                label=f'Download der pdf Datei',
                data=pdf_data,
                file_name=pdf_path,
                mime='application/pdf',
                key=str(st.session_state.button_count)
            )