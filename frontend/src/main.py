import streamlit as st
import os
from datetime import datetime
from viewer.dialogues import rechtliche_hinweise_dialogue
from viewer.viewer_main import viewer_main
from admin.admin_main import admin_main
from authenticate import create_login
from dotenv import load_dotenv

from streamlit_js_eval import streamlit_js_eval



OLD_CHATS_PATH = "../../data/old_chats.json"
load_dotenv('../.env')

if __name__ == "__main__":
    create_login()
    if st.session_state.logout and st.session_state['authentication_status']:
        st.session_state.logout = False
        st.session_state.authenticator.logout(location="unrendered")
        streamlit_js_eval(js_expressions="parent.window.location.reload()")
    elif st.session_state['authentication_status']:
        if st.session_state['roles'] and ("admin" in st.session_state['roles']):
            admin_main()
        else:
            if "agreed_to_terms" not in st.session_state:
                rechtliche_hinweise_dialogue()
            elif "agreed_to_terms" in st.session_state:
                viewer_main()
            else:       
                st.error("Es wurde nicht zugestimmt. Um den Chatbot zu nutzen, stimmen Sie den rechtlichen Hinweisen zu.")
                if st.button("zum Dialog...",):
                    st.rerun()
    elif st.session_state['authentication_status'] is False:
        st.error('Benutzername oder Passwort sind falsch. Bitte versuchen Sie es erneut.')
    elif st.session_state['authentication_status'] is None:
        st.warning('Bitte geben Sie Ihre Email-Adresse und Ihr Passwort ein.')