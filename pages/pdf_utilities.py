from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document

import fitz  # PyMuPDF
from PIL import Image
from bs4 import BeautifulSoup

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

data_path = "data"
vectorstore_path = "vectorstores/db_chroma"

def load_documents():
    document_loader = PyPDFDirectoryLoader(data_path)
    return document_loader.load()

def load_document(file_path):
    document_loader = PyPDFDirectoryLoader(data_path)
    return document_loader.load()

def split_documents(documents:list[Document]): #-> list[list[str]]:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50,length_function=len,is_separator_regex=False)
    # return [text_splitter.split_text(doc.text) for doc in documents]
    return text_splitter.split_documents(documents)

# Function to convert PDF to image
def pdf_to_image(pdf_data):
    pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
    first_page = pdf_document.load_page(0)
    pix = first_page.get_pixmap()
    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return image

# def remove_document(pdf_path):
