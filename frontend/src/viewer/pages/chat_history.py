import streamlit as st
from streamlit_option_menu import option_menu

def on_change(selection):
    st.session_state.messages = st.session_state.chat_history[selection]
    st.session_state.current_chat_name = selection
    st.rerun()

def create_menu_entries():
    menu_entries_titles = []
    if "chat_history" in st.session_state:
        menu_entries_titles = list(st.session_state.chat_history.keys())
    if len(menu_entries_titles) > 0:
        selected = option_menu('alte Chats', menu_entries_titles,
                               key='select_menu', orientation="vertical")
        if selected != st.session_state.get('last_selection'):
            st.session_state['last_selection'] = selected
            on_change(selected)
    else:
        st.write('bisher keine Chats')

create_menu_entries()
