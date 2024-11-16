import streamlit as st
from viewer.dialogues import logout_dialogue, new_chat_dialogue


def create_navigation():
    with st.sidebar:
        if st.button("neuer Chat", key="new_chat_button", icon=":material/edit_square:"):
            new_chat_dialogue()
        pages = {
        "Account": [
            st.Page("viewer/pages/chat_history.py", title="alte Chats", icon=":material/forum:"),
            st.Page(logout_dialogue, title="logout", icon=":material/logout:"),
        ],
        "Nützliches": [
            st.Page("viewer/pages/learn_more.py", title="erfahre mehr über asklepios", icon=":material/lightbulb:"),
            st.Page("viewer/pages/impressum.py", title="Impressum", icon=":material/alternate_email:"),
        ],
        }
        pg = st.navigation(pages)
        pg.run()
        
        