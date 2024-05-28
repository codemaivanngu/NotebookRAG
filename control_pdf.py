import shutil
import os
from langchain_community.embeddings import GPT4AllEmbeddings
from gpt4all import Embed4All
# import rag_ollama.prepare_db as prepare_db
# import  rag_ollama.pdf_utilities as pdf_utilities 
from rag_ollama import pdf_utilities 
from rag_ollama import prepare_db
from langchain_community.vectorstores import Chroma

embedding_model =GPT4AllEmbeddings(model_name="all-MiniLM-L6-v2.gguf2.f16.gguf",gpt4all_kwargs={'allow_download': 'True'})
db = Chroma(
    persist_directory=prepare_db.vectorstore_path, embedding_function=embedding_model)


def move_pdf(source_folder, destination_folder, filename):
    # Construct source and destination paths
    source_path = os.path.join(source_folder, filename)
    destination_path = os.path.join(destination_folder, filename)
    try:
        # Move the file
        shutil.move(source_path, destination_path)
        print(f"Moved '{filename}' from {source_folder} to {destination_folder}.")
    except FileNotFoundError:
        print("File not found.")
    except PermissionError:
        print("Permission denied.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
def remove_pdf(file_name,source_folder = 'data', destination_folder= 'deleted'):
    move_pdf(source_folder, destination_folder, file_name)
    #delete chunks added in db
    document = pdf_utilities.load_document(file_path=source_folder+"\\"+file_name)
    chunks = pdf_utilities.split_documents([document])
    existing_items = db.get(include=[])
    chunks_with_ids = prepare_db.calculate_chunk_ids(chunks)

    for chunk in chunks_with_ids:
        if chunk.metadata['id'] in existing_items:
            db.remove_by_id(chunk.metadata['id'])

def add_pdf(file_name):
    document = pdf_utilities.load_document(file_path="data\\"+file_name)
    chunks = pdf_utilities.split_documents([document])
    existing_items = db.get(include=[])
    chunks_with_ids = prepare_db.calculate_chunk_ids(chunks)

    new_chunks = [chunk for chunk in chunks_with_ids
        if chunk.metadata['id'] not in existing_items]
    new_chunks_ids = [chunk.metadata['id'] for chunk in new_chunks]
    db.add_documents(new_chunks,ids = new_chunks_ids)

def empty_bins():
    shutil.rmtree('deleted')
    shutil.makedirs('deleted')
    
