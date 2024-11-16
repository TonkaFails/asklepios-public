import streamlit as st
import json
import os

OLD_CHATS_PATH = "../../data/old_chats.json"
def update_chat_storage(chat):
    chat_save = {st.session_state['username'] : chat}
    
    with open(OLD_CHATS_PATH, "r") as file:
        data = json.load(file)

    data.update(chat_save)

    with open(OLD_CHATS_PATH, "w") as file:
        json.dump(data, file, indent=4)

def get_stored_user():
    if os.path.exists(OLD_CHATS_PATH):
        with open(OLD_CHATS_PATH, "r") as file:
            all_chats = json.load(file)
            if st.session_state['username'] in all_chats:
                st.session_state.chat_history = all_chats[st.session_state['username']]
            else:
                update_chat_storage({st.session_state.current_chat_name:[]})
    else:
        with open(OLD_CHATS_PATH, "w") as file:
            json.dump({st.session_state['username']:{st.session_state.current_chat_name:[]}}, file, indent=4)