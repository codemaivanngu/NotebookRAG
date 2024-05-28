from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import GPT4AllEmbeddings
from gpt4all import Embed4All


import argparse
import os
import shutil
import subprocess
from langchain_community.embeddings.ollama import OllamaEmbeddings

os.environ['OLLAMA_HOST'] = '127.0.0.1:12345'
# os.system("ollama pull nomic-embed-text")
process = subprocess.Popen(['ollama', 'serve'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
embedding_model = OllamaEmbeddings(model='all-minilm:latest',model_kwargs={'allow_download': 'True'})



#khai báo biến
file_path = 'data'
vector_db_path = 'vectorstores/db_faiss'
#hàm 1: tạo ra vector db từ 1 đoạn text
def create_vector_db_from_text(text=""):
    raw_text ="In order to decide which clusters should be combined (for agglomerative), or where a cluster should be split (for divisive), a measure of dissimilarity between sets of observations is required. In most methods of hierarchical clustering, this is achieved by use of an appropriate distance d, such as the Euclidean distance, between single observations of the data set, and a linkage criterion, which specifies the dissimilarity of sets as a function of the pairwise distances of observations in the sets. The choice of metric as well as linkage can have a major impact on the result of the clustering, where the lower level metric determines which objects are most similar, whereas the linkage criterion influences the shape of the clusters. For example, complete-linkage tends to produce more spherical clusters than single-linkage."
    text_splitter = CharacterTextSplitter(
        separator='\n',
        chunk_size=500,
        chunk_overlap=50,
        # split_symbol=" ",
        # recursive=True,
        # recursive_split_symbol=" ",
        length_function=len
    )
    chunks = text_splitter.split_text(raw_text)

    #embedding
    # embedding_model = GPT4AllEmbeddings()
    embedding_model =GPT4AllEmbeddings(model_name="all-MiniLM-L6-v2.gguf2.f16.gguf",gpt4all_kwargs={'allow_download': 'True'})
    #Đưa vào FAISS
    db=FAISS.from_texts(texts=chunks, embedding=embedding_model)
    db.save_local(vector_db_path)
    return db
# create_vector_db_from_text()
def create_vector_db_from_file(pdf_data_path):
    #quets toàn bộ thư mục data
    loader = DirectoryLoader(pdf_data_path,glob="*.pdf",loader_cls=PyPDFLoader)
    documents = loader.load()
    print(type(documents),len(documents),type(documents[0]))
    text_splitter = RecursiveCharacterTextSplitter(
        # separator='\n',
        chunk_size=500,
        chunk_overlap=50,
    )
    # text_splitter = CharacterTextSplitter(
    #     separator='\n',
    #     chunk_size=500,
    #     chunk_overlap=50,
    #     # split_symbol=" ",
    #     # recursive=True,
    #     # recursive_split_symbol=" ",
    #     length_function=len
    # )
    chunks = text_splitter.split_documents(documents)
    print(type(chunks),len(chunks),"###")
    # embedding_model =GPT4AllEmbeddings(model_name="all-MiniLM-L6-v2.gguf2.f16.gguf",gpt4all_kwargs={'allow_download': 'True'})
    db=FAISS.from_documents(chunks, embedding=embedding_model)
    db.save_local(vector_db_path)
    return db


from time import perf_counter
tin = perf_counter()

create_vector_db_from_file(file_path)
tout = perf_counter()
print("Time taken: ", tout - tin)