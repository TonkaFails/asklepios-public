import streamlit as st
import streamlit_authenticator as stauth
from viewer.dialogues import new_user_dialogue
import yaml
import os
from yaml.loader import SafeLoader

def create_login():
    with open("../config.yaml") as file:
        config = yaml.load(file, Loader=SafeLoader)
        st.session_state.config = config
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )
    st.session_state.authenticator = authenticator
    try:
        authenticator.login(fields={
            'Form name':'Login',
            'Username':'Email',
            'Password':'Passwort',
            })
        if not st.session_state['authentication_status']:
            if st.button("Sie haben noch keinen Nutzeraccount? Klicken Sie hier um sich zu registrieren", use_container_width=True):
                new_user_dialogue()
    except Exception as e:
        st.error(e)

