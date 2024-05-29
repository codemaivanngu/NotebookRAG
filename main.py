import streamlit as st
from streamlit_option_menu import option_menu
import document_space, chat_space, home
import control_db,control_pdf_on_data,control_web

st.set_page_config(
    page_title="NoteRAG",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "https://github.com/ollama/NoteRAG",
    },
)

def run():
    with st.sidebar:
        st.session_state.selected  = option_menu(
            menu_title=None,
            options=["Home", "Data", "Chat","Reset"],
            icons=["house", "book", "chat-left","arrow-clockwise"],
            default_index=0,
            # orientation="horizontal",
        )
    

    if st.session_state.selected == "Home":
        # switch_page("home")
        home.app()
    if st.session_state.selected == "Data":
        # switch_page("document_space")
        document_space.app()
    if st.session_state.selected == "Chat":
        # switch_page("chat_space")
        chat_space.app()
    if st.session_state.selected == "Reset":
        control_web.clear_web_store()
        control_pdf_on_data.clear_PDF_store()
        control_db.clear_database()

run()