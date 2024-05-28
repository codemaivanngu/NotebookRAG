import argparse
import os
import shutil
vectorstore_path = "vectorstores/db_chroma"

def clear_database():
    if os.path.exists(vectorstore_path):
        shutil.rmtree(vectorstore_path)