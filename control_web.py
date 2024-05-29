import prepare_db 
import web_preview 
import pickle
import os.path
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.schema.document import Document
from langchain_community.embeddings import GPT4AllEmbeddings

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
vectorstore_path = "vectorstores/db_chroma"
embedding_model = GPT4AllEmbeddings(model_name="all-MiniLM-L6-v2.gguf2.f16.gguf",gpt4all_kwargs={'allow_download': 'True'})
web_store = {} # A dictionary with type {url: (documents e.i. text information of website, image e.i. the icon of website)}
db = Chroma(
        persist_directory=vectorstore_path, embedding_function=embedding_model)

#3 elements function control the persistion of links
def init_web_store():
    if os.path.isfile("./data/web/store.pkl"):
        web_store = pickle.load(open("./data/web/store.pkl", "rb"))
    else:
        web_store = {}
        with open("./data/web/store.pkl", "wb") as f:
            pickle.dump({},f)
    print("len web_store:",len(web_store))

def close_web_store():
    with open("data/web/store.pkl", "wb") as f:
        pickle.dump(web_store,f)
    print("len web_store:",len(web_store))

def clear_web_store():
    if os.path.exists(r'.\data\web\store.pkl'):
        os.remove(r'.\data\web\store.pkl')
    init_web_store()
    close_web_store()

init_web_store()

def extract_web(url):
    """
    Extract the text from a webpage
    """
    loader = WebBaseLoader(url)
    documents = loader.load()
    return documents

def split_documents(documents:list[Document]): #-> list[list[str]]:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50,length_function=len,is_separator_regex=False)
    # return [text_splitter.split_text(doc.text) for doc in documents]
    return text_splitter.split_documents(documents)

def create_chunks_with_ids(chunks):
    #create reference format as ID like "url:line:line"
    existing_items = db.get(include=[])
    chunks_with_ids = prepare_db.calculate_chunk_ids(chunks)
    index=0
    id=""
    for chunk in chunks:
        source = chunk.metadata['source']
        line1 = max(0,index*CHUNK_SIZE-CHUNK_OVERLAP)
        line2 = index*CHUNK_SIZE
        index+=1
        id = f"{source}:{line1}:{line2}"
        chunk.metadata['id'] = id
    return chunks

def remove_web_page(url):#web_store + vectordb
    
    #remove in web_store
    init_web_store()
    print("removing:",len(web_store),url)
    documents,image= web_store[url]
    del web_store[url]
    close_web_store()
    #remove in vectorstore
    chunks = split_documents(documents)
    chunks_with_ids = create_chunks_with_ids(chunks)
    existing_items = db.get(include=[])
    for chunk in chunks_with_ids:
        if chunk.metadata['id'] in existing_items:
            db.remove_by_id(chunk.metadata['id'])
    
def add_web_page(url): #web_store + vectordb
    if url in web_store:
        remove_web_page(url)
    init_web_store()
    documents = extract_web(url)
    image = web_preview.get_website_icon(url)
    web_store[url]=[documents,image]
    close_web_store()

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
    
    #add to vectorstore
    

    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50, length_function=len, is_separator_regex=False)
    # chunks = text_splitter.split_text(documents)
    # return documents


def main():
    documents = extract_web("https://www.freecodecamp.org/news/how-to-check-if-a-file-exists-in-python/")
    # print(len(documents))
    print(documents[0].metadata)
    # chunks = split_documents(documents)
    # # print(len(chunks))
    # print(chunks[0].metadata)
    # add_web_page("https://www.freecodecamp.org/news/how-to-check-if-a-file-exists-in-python/")
close_web_store()
if __name__ == "__main__":
    main()
    # init_web_store()
    # add_web_page("https://www.google.com")
    # close_web_store()