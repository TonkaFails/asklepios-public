import streamlit as st
import json
import os
from datetime import datetime
from viewer.store_chat import update_chat_storage
import yaml
OLD_CHATS_PATH = "../../data/old_chats.json"

@st.dialog("Herzlich Willkommen 👨‍⚕️🩺")
def rechtliche_hinweise_dialogue():
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

@st.dialog("Sie wollen sich abmelden?")
def logout_dialogue():
    if st.button("logout", type="primary"):
        st.session_state.logout = True
        st.rerun()

@st.dialog("Sie wollen einen neuen Chat starten?")
def new_chat_dialogue():
    if 'current_chat_name' not in st.session_state:
        st.info("Ihr erster Chat steht zur Nutzung bereit.")
    elif st.session_state.current_chat_name not in st.session_state.chat_history:
        st.warning("Ihr derzeitiger Chat wurde noch nicht genutzt. Stellen Sie zunächst eine Frage, bevor Sie einen neuen Chat starten.")
    else:
        st.subheader("Sie sollten zunächst den aktuellen Chat speichern, bevor Sie einen neuen Chat starten.")
        chat_name = st.text_input(label="Legen Sie eine Bezeichnung für den letzten Chat an:", placeholder=f"{st.session_state.current_chat_name}")
        if st.button("speichern", type="primary"):
            #set the name of the current chat to the text input value
            chat_messages = st.session_state.chat_history.pop(st.session_state.current_chat_name)
            #set it in the first place of the dictionary, so it will be displayed as the latest chat in chat history
            st.session_state.chat_history = {chat_name: chat_messages, **st.session_state.chat_history}
            #update in storage
            update_chat_storage(st.session_state.chat_history)
            #update in last selection
            st.session_state['last_selection'] = chat_name
            #new chat
            st.session_state.messages = []
            st.session_state.current_chat_name = f'unknown_chat_{datetime.now().strftime("%d.%m.%Y_%H:%M:%S")}'
            st.session_state.chat_history = {st.session_state.current_chat_name: st.session_state.messages, **st.session_state.chat_history}
            update_chat_storage(st.session_state.chat_history)
            print(st.session_state.chat_history)
            st.rerun()

@st.dialog("Sie wollen sich registrieren?")
def new_user_dialogue():
    try:
        email_of_registered_user, \
        username_of_registered_user, \
        name_of_registered_user = st.session_state.authenticator.register_user(fields={
            'Form name':'Registrierung',
            'First name':'Vorname',
            'Last name':'Nachname',
            'Username':'Benutzername',
            'Email':'Email',
            'Password':'Passwort',
            'Repeat password':'Passwort wiederholen',
            'Password hint':'Tipp für das Passwort',
            'Register':'registrieren'
        },merge_username_email=True)
        
        if email_of_registered_user:
            with open('../config.yaml', 'w') as file:
                yaml.dump(st.session_state.config, file, default_flow_style=False)
            st.success('Sie haben sich erfolgreich registriert. Sie können sich jetzt einloggen.')
    except Exception as e:
        match e.message:
            case "First name is not valid":
                st.error('Der Vorname ist nicht gültig oder wurde nicht angegeben. Bitte ausschließlich Buchstaben verwenden.')
            case "Last name is not valid":
                st.error('Der Vorname ist nicht gültig oder wurde nicht angegeben. Bitte ausschließlich Buchstaben verwenden.')
            case "Email is not valid":
                st.error('Die Email ist nicht gültig oder wurde nicht angegeben. Bitte geben Sie eine gültige Email-Adresse an.')
            case "Username is not valid":
                st.error('Der Benutzername ist nicht gültig oder wurde nicht angegeben. Bitte ausschließlich Buchstaben oder Ziffern verwenden.')
            case "Password/repeat password fields cannot be empty":
                st.error('Passwort/Passwortwiederholung dürfen nicht leer sein.')
            case "Password does not meet criteria":
                st.error('Passwort entspricht nicht den Vorgaben.')
            case "Password does not meet criteria":
                st.error('Passwort entspricht nicht den Vorgaben.')
            case "Passwords do not match":
                st.error('Passwörter sind nicht gleich.')
            case "Password hint cannot be empty":
                st.error('Passworttipp darf nicht leer sein.')
            case "Captcha not entered":
                st.error('Captcha wurde nicht eingegeben.')
            case "Captcha entered incorrectly":
                st.error('Captcha wurde falsch eingegeben.')
            case "Email already taken":
                st.error('Email wird bereits verwendet. Bitte wählen Sie eine andere Email-Adresse.')
            case "Username/email already taken":
                st.error('Benutzername/Email wird bereits verwendet. Bitte wählen Sie einen anderen Benutzernamen oder eine andere Email-Adresse.')
            case _:
                st.error(e.message)
    st.markdown("""
                    **Passwort muss:**

                    - Zwischen 8 und 20 Zeichen lang sein
                    - Mindestens einen Kleinbuchstaben enthalten
                    - Mindestens einen Großbuchstaben enthalten
                    - Mindestens eine Ziffer enthalten
                    - Mindestens ein Sonderzeichen aus [@$!%*?&] enthalten
                    """)