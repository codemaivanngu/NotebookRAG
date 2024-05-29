import streamlit as st
import prepare_db
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from langchain_core.messages import AIMessage, HumanMessage

def app():

    vectorstore_path = prepare_db.vectorstore_path

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
        
        query_rag(query_text)

    def query_rag(query_text:str):
        print("query: ", query_text)
        results = db.similarity_search_with_score(query_text, k=3)
        context_text = "\n\n".join([doc.page_content for doc, _score in results])
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE_VI)
        prompt = prompt_template.format(context=context_text, question=query_text)
        
        response_text = model.invoke(prompt)

        sources = [doc.metadata.get("id", None) for doc, _score in results]
        formatted_response = f"Response: {response_text}\nSources: {sources}"
        print()
        print(formatted_response)

        # template = """Nội dung nằm ở: """
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