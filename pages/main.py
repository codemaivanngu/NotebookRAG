import streamlit as st

from streamlit_option_menu import option_menu

import document_space, chat_space,home

st.set_page_config(
    page_title="NoteRAG",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "https://github.com/ollama/NoteRAG",
    },
)
# st.write("g.ksdfjhdfkjjdfgs")
class MultiApp:
    def __init__(self):
        self.apps = []
    def add_app(self, title, func, icon=None):
        # app = st.expander(title)
        # with app:
        #     func()
        self.apps.append({
            "title": title,
            "function": function,
        })
    def run():
        selected = option_menu(
            menu_title=None,
            options=["Home", "Data", "Chat"],
            icons=["house", "book", "chat-left"],
            default_index=0,
            orientation="horizontal",
        )

        if selected == "Home":
            home.app()
        if selected == "Data":
            document_space.app()
        if selected == "Chat":
            chat_space.app()
    run()