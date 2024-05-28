from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from rag_ollama.prepare_db import *
import pickle

from langchain_community.embeddings import GPT4AllEmbeddings
from gpt4all import Embed4All

embedding_model = GPT4AllEmbeddings(model_name="all-MiniLM-L6-v2.gguf2.f16.gguf",gpt4all_kwargs={'allow_download': 'True'})
web_store = pickle.load(open("data/web/store.pkl", "rb"))
def extract_web(url):
    loader = WebBaseLoader(url=url, max_content_length=1000000)
    document = loader.load()
    # web_store[url]=document
    return document



def remove_web_page(url):#web_store + vectordb
    #remove in web_store
    document= web_store[url]
    del web_store[url]
    #remove in vectorstore

    pass

def add_web_page(url): #web_store + vectordb
    if url in web_store:
        remove_web_page(url)
    document = extract_web(url)
    web_store[url]=document
    #add to vectorstore
    

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50, length_function=len, is_separator_regex=False)
    chunks = text_splitter.split_text(document)
    return document

