import streamlit as st
import os
from datetime import datetime
from viewer.navigation import create_navigation

from dotenv import load_dotenv

from viewer.generate_chat import save_conversation, generate_streaming_response, generate_old_messages, generate_download_link
from viewer.store_chat import update_chat_storage, get_stored_user

OLD_CHATS_PATH = "../../data/old_chats.json"
load_dotenv('../.env')

# Main function to run the chatbot app
def viewer_main():
    if "current_chat_name" not in st.session_state:
        st.session_state.current_chat_name = f'unknown_chat_{datetime.now().strftime("%d.%m.%Y_%H:%M:%S")}'
    get_stored_user()
    create_navigation()
    
    st.title("Medizinischer Assistenz-Chatbot")
    generate_old_messages()
    # Accept user input
    if prompt := st.chat_input("Hallo, stell mir eine Frage."):
        with st.chat_message("user", avatar="👨‍💻"):
            st.markdown(prompt)
            save_conversation(prompt, 'user')
            update_chat_storage(st.session_state.chat_history)

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
            update_chat_storage(st.session_state.chat_history)