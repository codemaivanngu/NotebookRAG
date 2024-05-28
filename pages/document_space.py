import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import requests
from bs4 import BeautifulSoup
import threading
from time import perf_counter
import pdf_utilities
import web_preview
import pickle
import control_web
import control_pdf_on_data
# from streamlit_autorefresh import st_autorefresh
#auto refresh every 2000 milisecond, repeat 100 times
# count = st_autorefresh(interval=2500, limit=100000, key="fizzbuzzcounter")


# def app():
    
    
# st.session_state.selected == "Data"
control_web.clear_web_store()
# Initialize session state for storing PDF and website images
if 'pdf_images' not in st.session_state:
    st.session_state.pdf_images = []
if 'website_images' not in st.session_state:
    st.session_state.website_images = []
if 'uploaded_files_names' not in st.session_state:
    st.session_state.uploaded_files_names = []

# Streamlit app
st.title("Upload Note, PDF, Website,...")

# Store previously uploaded files to detect removals
previous_uploaded_files = st.session_state.uploaded_files_names.copy()


# if "file_uploader_key" not in st.session_state:
#     st.session_state["file_uploader_key"] = 0
# def F5PDF():
#     uploaded_file = st.session_state.loadPDF
#     st.session_state.loadPDF=None
#     # uploaded_files_names = [uploaded_file.name for uploaded_file in uploaded_files]
#     for uploaded_file in uploaded_files:
#         pdf_data = uploaded_file.read()
#         documents,image = control_pdf_on_data.add_PDF(pdf_data)
#         # if uploaded_file.name not in [file[0] for file in st.session_state.pdf_images]:
#         #     pdf_data = uploaded_file.read()
#         #     image = pdf_utilities.pdf_to_image(pdf_data)
#         #     # Store the image in the session state
#         #     st.session_state.pdf_images.append((uploaded_file.name, image))

# uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True,key=key=st.session_state["file_uploader_key"],on_change=F5PDF)
if "file_uploader_key" not in st.session_state:
    st.session_state["file_uploader_key"] = 0

if "uploaded_files" not in st.session_state:
    st.session_state["uploaded_files"] = []

files = st.file_uploader(
    "Upload some files",
    type="pdf",
    accept_multiple_files=True,
    key=st.session_state["file_uploader_key"],
)

if files:
    st.session_state["uploaded_files"] = files
    st.session_state["file_uploader_key"] += 1
    
    print(len(st.session_state["uploaded_files"]))
    for uploaded_file in st.session_state["uploaded_files"]:
        pdf_data = uploaded_file.read()
        documents,image = control_pdf_on_data.add_PDF(pdf_data)
    st.rerun()
# if st.button("Clear uploaded files"):
    
# if uploaded_files is not None:
#     uploaded_files_names = [uploaded_file.name for uploaded_file in uploaded_files]
    
#     # # Detect removed files
#     # removed_files = set(previous_uploaded_files) - set(uploaded_files_names)
#     # for removed_file in removed_files:
#     #     st.session_state.pdf_images = [(name, img) for name, img in st.session_state.pdf_images if name != removed_file]
    
#     # Update session state with current file names
#     # st.session_state.uploaded_files_names = uploaded_files_names

#     for uploaded_file in uploaded_files:
#         if uploaded_file.name not in [file[0] for file in st.session_state.pdf_images]:
#             pdf_data = uploaded_file.read()
#             image = pdf_utilities.pdf_to_image(pdf_data)
#             # Store the image in the session state
#             st.session_state.pdf_images.append((uploaded_file.name, image))

# Website URL input
# website_url = st.text_input("Enter website URL")
if "input_temp" not in st.session_state:
    st.session_state.input_temp = ""

def F5():
    control_web.add_web_page(st.session_state.input1,"input")
    st.session_state.input_temp=st.session_state.input1
    st.session_state.input1 = ""

website_url = st.text_input("Enter website URL",key="input1",on_change=F5)

# Display the uploaded PDFs and their thumbnails
if st.session_state.pdf_images or len(control_web.web_store):
    st.header("Workspace")
    
    cols = st.columns(4)
    idx = 0
    st.session_state.PDF_need_to_del ={}
    for pdf_data, image in control_pdf_on_data.PDF_store:
        documents = control_pdf_on_data.extract_PDF(pdf_data)
        with cols[idx % 4]:
            if st.session_state.PDF_need_to_del.get((pdf_data,image))==None:
                st.image(image, caption=documents[0].metadata['title'], use_column_width=True)
            if st.button(f"Remove {documents[0].metadata['title']}"):
                st.session_state.PDF_need_to_del[(pdf_data,image)]="1"
        idx += 1

    # show webpage
    st.session_state.web_need_to_del ={}
    for url,value in control_web.web_store.items():
        documents,image = value
        with cols[idx % 4]:
            if st.session_state.web_need_to_del.get(url)==None:
                st.image(image, caption=documents[0].metadata['title'], use_column_width=True)
            if st.button(f"Remove {url}", key=f"remove-url-{url}"):
                st.session_state.web_need_to_del[url]="1"
        idx += 1
    if len(st.session_state.web_need_to_del):
        for url in st.session_state.web_need_to_del.keys():
            control_web.remove_web_page(url)
        for key in st.session_state.PDF_need_to_del:
            control_pdf_on_data.remove_PDF(key)
        st.session_state.web_need_to_del ={}
        st.rerun()
        control_web.clear_web_store()