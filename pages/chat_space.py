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
llm = Ollama(model="gemma:2b")
def app():
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
    llm = Ollama(model="gemma:2b")
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
