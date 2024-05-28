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
import argparse
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama

data_path = prepare_db.data_path
vectorstore_path = prepare_db.vectorstore_path

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
PROMPT_TEMPLATE_VI ="""
Trả lời câu hỏi dựa trên thông tin sau:
{context}
---
Trả lời câu hỏi dựa trên thông tin trên:{question}
"""

def main():
    # Create CLI.
    # parser = argparse.ArgumentParser()
    # parser.add_argument("query_text", type=str, help="The query text.")
    # args = parser.parse_args()
    # query_text = args.query_text
    query_text = "mức phụ cấp được quy định tại thông tư nào?"
    """
    Response: Mức phụ cấp được quy định tại Thông tư 06/2024/T T-BYT ngà y 16/5/2024 của Bộ trưởng Bộ Y tế.
Sources: ['data\\Mức phụ cấp với Trưởng, Phó Trưởng trạm y tế xã, Phó trưởng khoa, phòng, điều dưỡng trưởng, hộ sinh trưởng,... áp dụng từ ngày 1_7.pdf:0:0:4238894112', 'data\\Mức phụ cấp với Trưởng, Phó Trưởng trạm y tế xã, Phó trưởng khoa, phòng, điều dưỡng trưởng, hộ sinh trưởng,... áp dụng từ ngày 1_7.pdf:0:1:4238894112', 'data\\Mức phụ cấp với Trưởng, Phó Trưởng trạm y tế xã, Phó trưởng khoa, phòng, điều dưỡng trưởng, hộ sinh trưởng,... áp dụng từ ngày 1_7.pdf:1:0:4238894112']
    """
    query_rag(query_text)

def query_rag(query_text:str):
    print("query: ", query_text)
    db = Chroma(
    persist_directory=vectorstore_path, embedding_function=prepare_db.embedding_model)
    results = db.similarity_search_with_score(query_text, k=3)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE_VI)
    prompt = prompt_template.format(context=context_text, question=query_text)
    

    model = Ollama(model="gemma:2b")
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    return response_text


if __name__ == "__main__":
    from time import perf_counter
    tin = perf_counter()
    main()
    tout = perf_counter()
    print("Time: ", tout - tin) 