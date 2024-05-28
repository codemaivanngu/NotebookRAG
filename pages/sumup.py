import streamlit as st

from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page

# from pages import document_space, chat_space,home

st.set_page_config(
    page_title="NoteRAG",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "https://github.com/ollama/NoteRAG",
    },
)
from langchain_community.llms.ollama import Ollama
llm = Ollama(model="gemma:2b")

def chat_space():
    import streamlit as st
    from langchain_core.messages import AIMessage, HumanMessage
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain.chains import create_history_aware_retriever,create_retrieval_chain
    from langchain.chains.combine_documents import create_stuff_documents_chain
    from langchain_community.llms.ollama import Ollama
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import GPT4AllEmbeddings

    data_path = "data"
    vectorstore_path = "vectorstores/db_chroma"
    embedding_model =GPT4AllEmbeddings(model_name="all-MiniLM-L6-v2.gguf2.f16.gguf",gpt4all_kwargs={'allow_download': 'True'})
    db = Chroma(
        persist_directory=vectorstore_path, embedding_function=embedding_model)
    
    def get_context_retriever_chain(db):
        retriever = db.as_retriever()
        prompt = ChatPromptTemplate.from_messages([
            MessagesPlaceholder(variable_name="chat_history"),#why placeholder: if not exist chat_history: -> None else chat_history
            ("user","{input}"),
            ("user","Given the above conversation, generate a search query to look up in order to get information relevant to the conversation"),
        ])
        retriever_chain = create_history_aware_retriever(llm,retriever,prompt)
        return retriever_chain

    def get_conversational_RAG_chain(retriever_chain):
        prompt = ChatPromptTemplate.from_messages([
            ("system","Answer the user's questions based on the below context:\n\n{context}"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user","{input}"),
        ])
        stuff_documents_chain =create_stuff_documents_chain(llm,prompt)
        #we don't have retrieved document yet
        return create_retrieval_chain(retriever_chain,stuff_documents_chain)

    def get_response(user_input):
        # create conversation chain
        retriever_chain = get_context_retriever_chain(st.session_state.db)
        conversation_RAG_chain = get_conversational_RAG_chain(retriever_chain)
        response = conversation_RAG_chain.invoke({
            "chat_history": st.session_state.chat_history,
            "input": user_query
        })
        return response['answer']


    #app config
    # st.set_page_config(page_title="Chat with websites", page_icon="")

    st.title("Chat with websites")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [AIMessage(content="Hello, I'm a bot. How can I help you?"),]

    #vector_store need to be persistent: in order to create vector_store we need to use embedding model -> avoid waste resource (we don't want to re-embedding the same content every single time)
    if "db" not in st.session_state:
        st.session_state.db = db #extract text from html



    #user input
    user_query = st.chat_input("Type your message here...")


    if user_query not in {None,""}:
        response = get_response(user_query)
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        st.session_state.chat_history.append(AIMessage(content=response))
        "just a test to print out the retrieved document"

    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)


def document_space():
    import streamlit as st
    import fitz  # PyMuPDF
    from PIL import Image
    import io
    import requests
    from bs4 import BeautifulSoup
    import threading
    from time import perf_counter
    # import web_preview
    if __name__ == "__main__":
        import pdf_utilities
        import web_preview
    else:
        from . import pdf_utilities
        from . import web_preview
        

    # Initialize session state for storing PDF and website images
    if 'pdf_images' not in st.session_state:
        st.session_state.pdf_images = []
    if 'website_images' not in st.session_state:
        st.session_state.website_images = []
    if 'uploaded_files_names' not in st.session_state:
        st.session_state.uploaded_files_names = []

    # Streamlit app
    st.title("Upload Note, PDF, Website,...")
    # Store previously uploaded files to detect removals
    previous_uploaded_files = st.session_state.uploaded_files_names.copy()
    uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)
    if uploaded_files is not None:
        uploaded_files_names = [uploaded_file.name for uploaded_file in uploaded_files]
        
        # Detect removed files
        removed_files = set(previous_uploaded_files) - set(uploaded_files_names)
        for removed_file in removed_files:
            st.session_state.pdf_images = [(name, img) for name, img in st.session_state.pdf_images if name != removed_file]
        
        # Update session state with current file names
        st.session_state.uploaded_files_names = uploaded_files_names

        for uploaded_file in uploaded_files:
            if uploaded_file.name not in [file[0] for file in st.session_state.pdf_images]:
                pdf_data = uploaded_file.read()
                image = pdf_utilities.pdf_to_image(pdf_data)
                # Store the image in the session state
                st.session_state.pdf_images.append((uploaded_file.name, image))

    # Website URL input
    website_url = st.text_input("Enter website URL")

    if website_url:
        name = web_preview.get_website_title(website_url)
        if name not in [name for name, img in st.session_state.website_images]:
            st.session_state.website_images.append((name, web_preview.get_website_icon(website_url)))

    # Display the uploaded PDFs and their thumbnails
    if st.session_state.pdf_images or st.session_state.website_images:
        st.header("Workspace")
        
        cols = st.columns(4)
        idx = 0
        for pdf_name, image in st.session_state.pdf_images:
            with cols[idx % 4]:
                st.image(image, caption=pdf_name, use_column_width=True)
            idx += 1

        for web_name, image in st.session_state.website_images:
            with cols[idx % 4]:
                st.image(image, caption=web_name, use_column_width=True)
            idx += 1





def home():
    st.write("Welcome to NoteRAG!")
    st.session_state.selected == "Home"
def run():
    # with st.sidebar:
    st.session_state.selected  = option_menu(
        menu_title=None,
        options=["Home", "Data", "Chat"],
        icons=["house", "book", "chat-left"],
        default_index=0,
        orientation="horizontal",
    )
    

    if st.session_state.selected == "Home":
        # switch_page("home")
        home()
    if st.session_state.selected == "Data":
        # switch_page("document_space")
        document_space()
    if st.session_state.selected == "Chat":
        # switch_page("chat_space")
        chat_space()
run()