import streamlit as st

@st.dialog("Sie wollen sich abmelden?")
def logout_dialogue():
    if st.button("logout", type="primary"):
        st.session_state.logout = True
        st.rerun()

def create_navigation():
    with st.sidebar:
        pages = {
        "Admin":
            [
            st.Page(logout_dialogue, title="logout", icon=":material/logout:"),
        ],
        "Statistiken": [
            st.Page("admin/pages/user_statistics.py", title="Nutzerstatistik", icon=":material/forum:"),
            st.Page("admin/pages/medicine_statistics.py", title="Statistik zu Medikamenten", icon=":material/logout:"),
        ],
        "Nutzer": [
            st.Page("admin/pages/all_users.py", title="Nutzer anzeigen", icon=":material/lightbulb:"),
        ],
        }
        pg = st.navigation(pages)
        pg.run()
        