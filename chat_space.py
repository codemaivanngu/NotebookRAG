import argparse
import os
import shutil
import subprocess
# from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from pdf_utilities import *
from langchain_community.embeddings import GPT4AllEmbeddings
from gpt4all import Embed4All
import prepare_db
import streamlit as st
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from langchain_core.messages import AIMessage, HumanMessage

def app():

    # data_path = prepare_db.data_path
    vectorstore_path = prepare_db.vectorstore_path
    # print("chat_space:",vectorstore_path)

    #start ollama server
    # os.system('$env:OLLAMA_HOST="127.0.0.1:12345"')
    # os.system('set OLLAMA_HOST=127.0.0.1:12345')
    # os.environ['OLLAMA_HOST'] = '127.0.0.1:12345'
    # os.system("ollama pull nomic-embed-text")
    # process = subprocess.Popen(['ollama', 'serve'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # embedding_model = OllamaEmbeddings(model='all-minilm:latest',model_kwargs={'allow_download': 'True'})

    PROMPT_TEMPLATE_EN = """
    Answer the question based only on the following context:
    {context}

    ---
    Answer the question based on the above context:{question}
    """
    PROMPT_TEMPLATE_VI =\
    """
    <|im_start|>system
    Hãy sử dụng thông tin sau đây để trả lời câu hỏi một cách ngắn gọn bằng tiếng Việt. Nếu bạn không thể trả lời, hãy nói "Tôi không thể trả lời được" và không được trả lời.
    {context}
    <|im_end|>
    <|im_start|>user
    {question}<|im_end|>
    <|im_start|>assistant
    """
    # """
    # Trả lời câu hỏi dựa trên thông tin sau:
    # {context}
    # ---
    # Trả lời câu hỏi dựa trên thông tin trên:{question}
    # """
    db = Chroma(
        persist_directory=vectorstore_path, embedding_function=prepare_db.embedding_model)
    model = Ollama(model="llama3")
    def main():
        query_text = "Số vốn vay được hỗ trợ lãi suất là bao nhiêu??"
        """
        Response: Mức phụ cấp được quy định tại Thông tư 06/2024/T T-BYT ngà y 16/5/2024 của Bộ trưởng Bộ Y tế.
        Sources: ['data\\Mức phụ cấp với Trưởng, Phó Trưởng trạm y tế xã, Phó trưởng khoa, phòng, điều dưỡng trưởng, hộ sinh trưởng,... áp dụng từ ngày 1_7.pdf:0:0:4238894112', 'data\\Mức phụ cấp với Trưởng, Phó Trưởng trạm y tế xã, Phó trưởng khoa, phòng, điều dưỡng trưởng, hộ sinh trưởng,... áp dụng từ ngày 1_7.pdf:0:1:4238894112', 'data\\Mức phụ cấp với Trưởng, Phó Trưởng trạm y tế xã, Phó trưởng khoa, phòng, điều dưỡng trưởng, hộ sinh trưởng,... áp dụng từ ngày 1_7.pdf:1:0:4238894112']
        """
        query_rag(query_text)

    def query_rag(query_text:str):
        print("query: ", query_text)
        results = db.similarity_search_with_score(query_text, k=3)
        context_text = "\n\n".join([doc.page_content for doc, _score in results])
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE_VI)
        prompt = prompt_template.format(context=context_text, question=query_text)
        # print(context_text)
        # print("###########################################################")
        # print("Prompt:",prompt)

        
        response_text = model.invoke(prompt)

        sources = [doc.metadata.get("id", None) for doc, _score in results]
        formatted_response = f"Response: {response_text}\nSources: {sources}"
        print()
        print(formatted_response)
        return response_text


    st.title("Chat with websites")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [AIMessage(content="Hello, I'm a bot. How can I help you?"),]


    user_query = st.chat_input("Type your message here...")

    if user_query not in {None,""}:
        response = query_rag(user_query)
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

    # if __name__ == "__main__":
    #     from time import perf_counter
    #     tin = perf_counter()
    #     main()
    #     tout = perf_counter()
    #     print("Time: ", tout - tin) 