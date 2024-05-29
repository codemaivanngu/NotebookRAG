import os
import shutil
vectorstore_path = r".\vectorstores\db_chroma"

def clear_database():
    if os.path.exists(vectorstore_path):
        shutil.rmtree(vectorstore_path)

if __name__ =="__main__":
    clear_database()