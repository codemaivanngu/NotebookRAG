import shutil
import tempfile
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.schema.document import Document
from langchain_community.document_loaders import PyPDFLoader
import prepare_db 
# import rag_ollama.pdf_utilities
import pickle
import os.path
import pdf_utilities

from langchain_community.embeddings import GPT4AllEmbeddings
from gpt4all import Embed4All

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
vectorstore_path = "vectorstores/db_chroma"
embedding_model = GPT4AllEmbeddings(model_name="all-MiniLM-L6-v2.gguf2.f16.gguf",gpt4all_kwargs={'allow_download': 'True'})
PDF_store = {} #data path:doc, img
db = Chroma(
        persist_directory=vectorstore_path, embedding_function=embedding_model)

def save_uploaded_pdf(uploaded_file):
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    # Save the uploaded PDF file to the temporary directory
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def init_PDF_store():
    if os.path.isfile("./data/PDF/store.pkl"):
        PDF_store = pickle.load(open("./data/PDF/store.pkl", "rb"))
    else:
        PDF_store = {}
        with open("./data/PDF/store.pkl", "wb") as f:
            pickle.dump({},f)
    print("len PDF_store:",len(PDF_store))

def close_PDF_store():
    with open("data/PDF/store.pkl", "wb") as f:
        pickle.dump(PDF_store,f)
    print("len PDF_store:",len(PDF_store))
def clear_PDF_store():
    if os.path.exists(r'C:\Projects\NoteRAG\pages\data\PDF\store.pkl'):
        os.remove(r'C:\Projects\NoteRAG\pages\data\PDF\store.pkl')
    # os.makedirs('data/PDF/')
    init_PDF_store()
    close_PDF_store()
# clear_web_store()
init_PDF_store()

def extract_PDF(pdf_path):
    """
    Extract the text from a PDF file
    """
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    return documents

# def convert()

def split_documents(documents:list[Document]): #-> list[list[str]]:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50,length_function=len,is_separator_regex=False)
    # return [text_splitter.split_text(doc.text) for doc in documents]
    return text_splitter.split_documents(documents)

def create_chunks_with_ids(chunks):
    # This will create IDs like "data/pdf/monopoly.pdf:6:2"
    # Page Source : Page Number : Chunk Index

    last_page_id = None
    current_chunk_index = 0
    print(len(chunks))

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id

    return chunks

def remove_PDF(pdf_path):#web_store + vectordb
    print(pdf_path)
    #remove in web_store
    init_PDF_store()
    print("removing PDF:",len(PDF_store))
    documents,image = PDF_store[pdf_path] 
    del PDF_store[pdf_path]
    close_PDF_store()
    #remove in vectorstore
    documents = PyPDFLoader(pdf_path).load()
    chunks = split_documents(documents)
    chunks_with_ids = create_chunks_with_ids(chunks)
    existing_items = db.get(include=[])
    for chunk in chunks_with_ids:
        if chunk.metadata['id'] in existing_items:
            db.remove_by_id(chunk.metadata['id'])
    #remove temp file
    if os.path.exists(pdf_path):
        os.remove(pdf_path)


def add_PDF(pdf_path): #web_store + vectordb
    if pdf_path in PDF_store:
        remove_PDF(pdf_path)
    init_PDF_store()
    documents = extract_PDF(pdf_path)
    # print("yjtadsy")
    # return None
    image = pdf_utilities.pdf_to_image(pdf_path)
    PDF_store[pdf_path] = (documents,image)
    close_PDF_store()
    
    chunks = split_documents(documents)
    chunks_with_ids = create_chunks_with_ids(chunks)

    #add chunks to db
    existing_items = db.get(include=[])  # IDs are always included by default
    # print(dir(existing_items))
    existing_ids = set(existing_items["ids"])
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)
    print("@@@@@ New chunks", new_chunks)
    if len(new_chunks):
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        print(f"👉 IDs of new documents: {new_chunk_ids}")
        db.add_documents(new_chunks, ids=new_chunk_ids)
        print("✨ Done adding new documents")
        # db.persist()
    else:
        print("✅ No new documents to add")
    return documents,image


    

# def move_pdf(source_folder, destination_folder, filename):
#     # Construct source and destination paths
#     source_path = os.path.join(source_folder, filename)
#     destination_path = os.path.join(destination_folder, filename)
#     try:
#         # Move the file
#         shutil.move(source_path, destination_path)
#         print(f"Moved '{filename}' from {source_folder} to {destination_folder}.")
#     except FileNotFoundError:
#         print("File not found.")
#     except PermissionError:
#         print("Permission denied.")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# # Example usage:
# def remove_pdf(file_name,source_folder = 'data', destination_folder= 'deleted'):
#     move_pdf(source_folder, destination_folder, file_name)
#     #delete chunks added in db
#     document = pdf_utilities.load_document(file_path=source_folder+"\\"+file_name)
#     chunks = pdf_utilities.split_documents([document])
#     existing_items = db.get(include=[])
#     chunks_with_ids = prepare_db.calculate_chunk_ids(chunks)

#     for chunk in chunks_with_ids:
#         if chunk.metadata['id'] in existing_items:
#             db.remove_by_id(chunk.metadata['id'])

# def add_pdf(file_name):
#     document = pdf_utilities.load_document(file_path="data\\"+file_name)
#     chunks = pdf_utilities.split_documents([document])
#     existing_items = db.get(include=[])
#     chunks_with_ids = prepare_db.calculate_chunk_ids(chunks)

#     new_chunks = [chunk for chunk in chunks_with_ids
#         if chunk.metadata['id'] not in existing_items]
#     new_chunks_ids = [chunk.metadata['id'] for chunk in new_chunks]
#     db.add_documents(new_chunks,ids = new_chunks_ids)

    
