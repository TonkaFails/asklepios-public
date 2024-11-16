import streamlit as st
import os
import requests
from collections import defaultdict
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()
@st.dialog("Herzlich Willkommen 👨‍⚕️🩺")
def rechtliche_hinweise_Dialog():
    tab1, tab2 = st.tabs(["Hallo", "rechtliche Hinweise"])
    with tab1:
        st.success("""Herzlich willkommen auf unserer Website! Wir freuen uns, dass Sie unseren Chatbot nutzen, um mehr über verschiedene Gesundheitsthemen zu erfahren.
                    Die Informationen, die Ihnen unser Chatbot bereitstellt, basieren auf aktuellen medizinischen Leitlinien und sind darauf ausgelegt, Sie bestmöglich zu unterstützen.
                    """)
    with tab2:
        st.info("""
                **Die Nutzung des Chatbots ersetzt nicht die persönliche Beratung durch eine Ärztin/einen Arzt oder Apothekerin/Apotheker.
                Die bereitgestellten Informationen dienen ausschließlich allgemeinen Informationszwecken und stellen keine medizinische Beratung oder Diagnose dar.
                Wir übernehmen keine Haftung für Entscheidungen, die auf Basis der vom Chatbot bereitgestellten Informationen getroffen werden.**
                """
                )
        agree = st.checkbox("Ich habe die rechtlichen Hinweise gelesen und stimme diesen zu.")
        if st.button("Bestätigen", disabled = not agree):
            st.session_state.agreed_to_terms = {"agreed": True}
            st.rerun()

# Function to save conversations
def save_conversation(prompt, role, sources = None, context = None):
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({"role": role, 'sources': sources, "content": prompt, "context": context})
    else:
        st.session_state.messages.append({"role": role, 'sources': sources, "content": prompt, "context": context})

def increase_button_count():
    if "button_count" not in st.session_state:
        st.session_state.button_count = 0
    else:
        st.session_state.button_count += 1

def generate_streaming_response():
    flask_backend_url = "http://127.0.0.1:5001/api/query"
    #flask_backend_url = "https://anton-hofmeier.de/api/query"
    
    if 'messages' in st.session_state:
        query_text = st.session_state.messages[-1]["content"]
        
        # Stream the response from the Flask backend
        relevant_chat_history = [{k: v for k, v in message.items() if k not in ['context', 'sources']} for message in st.session_state.messages]
        response = requests.post(flask_backend_url, json={"query_text": query_text, "chat_history":relevant_chat_history}, stream=True, auth=HTTPBasicAuth(os.getenv("USERNAME"), os.getenv("PASSWORD")))
        print(relevant_chat_history)
        if response.status_code == 200:
            for chunk in response.iter_content(chunk_size=1024, decode_unicode=True):
                if chunk:
                    yield chunk
        else:
            yield "Error: Unable to fetch response from the backend."

def generate_download_link(guideline_paths, context):
    guideline_paths = guideline_paths.split(".pdf")
    guidelines = [guideline_path.split('/')[-1] for guideline_path in guideline_paths][:-1]
    context = context.split("<context>")[1:]

    sources = list(zip(guidelines, context))
    
    sources = [(key, [v for k, v in sources if k == key]) for key in {k for k, _ in sources}]
    
    pdf_folder = os.path.join(os.path.dirname(__file__), 'guidelines')
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
def generate_chat_history():
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
# Main function to run the chatbot app
def main():
    if "agreed_to_terms" not in st.session_state:
        rechtliche_hinweise_Dialog()
        
    if "agreed_to_terms" in st.session_state:
        
        st.title("Medical Assistant Chatbot")
        generate_chat_history()

        # Accept user input
        if prompt := st.chat_input("Hallo, stell mir eine Frage."):
            with st.chat_message("user", avatar="👨‍💻"):
                st.markdown(prompt)
                save_conversation(prompt, 'user')

            # Stream the response from the backend
            with st.chat_message("bot", avatar="🤖"):
                response_placeholder = st.empty()  # Placeholder for the response
                full_response = ""
                guideline_paths = None
                context = ""
                for chunk in generate_streaming_response():
                    if "Bitte stellen Sie eine klare medizinisch oder gesundheitlich relevante Frage" in full_response:
                        break
                    elif 'Sources' not in chunk and '<|eot_id|>' not in chunk and not guideline_paths:
                        full_response += chunk
                    elif 'Sources' in chunk:
                        chunk = chunk.split("<context>")
                        guideline_paths = chunk[0]
                        if len(chunk) > 1:
                            first_context = chunk[1]
                            context = "<context>" + first_context
                    else:
                        context += chunk
                    response_placeholder.markdown(full_response)  
                if guideline_paths:
                    generate_download_link(guideline_paths, context)
                save_conversation(full_response, 'bot', guideline_paths, context)
    else:       
        st.error("Es wurde nicht zugestimmt. Um den Chatbot zu nutzen, stimmen Sie den rechtlichen Hinweisen zu.")
        if st.button("zum Dialog...",):
            st.rerun()
if __name__ == "__main__":
    main()