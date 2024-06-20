import argparse
import os
import shutil
from langchain_community.vectorstores import Chroma
import pdf_utilities
from langchain_community.embeddings import GPT4AllEmbeddings

data_path = "data/pdf"
vectorstore_path = "vectorstores/db_chroma"

#start ollama server
# os.system('$env:OLLAMA_HOST="127.0.0.1:12345"')
# os.system('set OLLAMA_HOST=127.0.0.1:12345')
# os.environ['OLLAMA_HOST'] = '127.0.0.1:12345'
# os.system("ollama pull nomic-embed-text")
# process = subprocess.Popen(['ollama', 'serve'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# embedding_model = OllamaEmbeddings(model='all-minilm:latest',model_kwargs={'allow_download': 'True'})
embedding_model =GPT4AllEmbeddings(model_name="all-MiniLM-L6-v2.gguf2.f16.gguf",gpt4all_kwargs={'allow_download': 'True'})
def main():

    # Check if the database should be cleared (using the --clear flag).
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    if args.reset:
        print("✨ Clearing Database")
        clear_database()

    # Create (or update) the data store.
    documents = pdf_utilities.load_documents()
    print("📚 Loaded documents: ", len(documents))
    chunks = pdf_utilities.split_documents(documents)
    print("📝 Split documents into chunks: ", len(chunks))
    add_to_chroma(chunks)
    print("✨ Done!")

    # process.terminate()

documents = pdf_utilities.load_documents()
chunks = pdf_utilities.split_documents(documents)



def add_to_chroma(chunks):
    # Load the existing database.
    db = Chroma(
        persist_directory=vectorstore_path, embedding_function=embedding_model)
    # Calculate Page IDs.
    chunks_with_ids = calculate_chunk_ids(chunks)

    # Add or Update the documents.
    existing_items = db.get(include=[])  # IDs are always included by default
    print(dir(existing_items))
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

# Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)
    
    if len(new_chunks):
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        print(f"👉 IDs of new documents: {new_chunk_ids}")
        db.add_documents(new_chunks, ids=new_chunk_ids)
        print("✨ Done adding new documents")
        # db.persist()
    else:
        print("✅ No new documents to add")

    
    # db.persist() #automatically persisted


def calculate_chunk_ids(chunks):
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


def clear_database():
    if os.path.exists(vectorstore_path):
        shutil.rmtree(vectorstore_path)


if __name__ == "__main__":
    from time import perf_counter
    tin =  perf_counter()
    main()
    tout = perf_counter()
    print("Time taken: ", tout - tin)