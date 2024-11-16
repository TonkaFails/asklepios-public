import streamlit as st
from admin.navigation import create_navigation
from dotenv import load_dotenv

OLD_CHATS_PATH = "../../data/old_chats.json"
load_dotenv('../.env')

# Main function to run the chatbot app
def admin_main():
    create_navigation()