import shutil
import os
from langchain_community.embeddings import GPT4AllEmbeddings
from gpt4all import Embed4All
from rag_ollama.prepare_db import *
from rag_ollama.pdf_utilities import load_documents

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
    document = load_document(file_path=source_folder+"\\"+file_name)
    chunks = split_documents([document])
    embedding_model =GPT4AllEmbeddings(model_name="all-MiniLM-L6-v2.gguf2.f16.gguf",gpt4all_kwargs={'allow_download': 'True'})
    db = Chroma(
        persist_directory=vectorstore_path, embedding_function=embedding_model)
    existing_items = db.get(include=[])
    chunks_with_ids_and_hashes = calculate_chunk_ids_and_hash(chunks)

    for chunk in chunks_with_ids_and_hashes:
        if chunk.metadata['id'] in existing_items:
            db.remove_by_id(chunk.metadata['id'])

def add_pdf(file_name):
    embedding_model =GPT4AllEmbeddings(model_name="all-MiniLM-L6-v2.gguf2.f16.gguf",gpt4all_kwargs={'allow_download': 'True'})
    db = Chroma(
        persist_directory=vectorstore_path, embedding_function=embedding_model)
    document = load_document(file_path="data\\"+file_name)
    chunks = split_documents([document])
    existing_items = db.get(include=[])
    chunks_with_ids_and_hashes = calculate_chunk_ids_and_hash(chunks)

    new_chunks = [chunk for chunk in chunks_with_ids_and_hashes
        if chunk.metadata['id'] not in existing_items]
    new_chunks_ids = [chunk.metadata['id'] for chunk in new_chunks]
    db.add_documents(new_chunks,ids = new_chunks_ids)

def empty_bins():
    shutil.rmtree('deleted')
    shutil.makedirs('deleted')
    
