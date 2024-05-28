# import streamlit as st
# import fitz  # PyMuPDF
# from PIL import Image
# import io
# import requests
# from bs4 import BeautifulSoup
# from langchain.schema.document import Document
# from langchain_community.document_loaders import PyPDFLoader

# # Initialize session state for storing PDF and website images and URLs
# if 'pdf_images' not in st.session_state:
#     st.session_state.pdf_images = []
# if 'website_images' not in st.session_state:
#     st.session_state.website_images = []
# if 'uploaded_files_names' not in st.session_state:
#     st.session_state.uploaded_files_names = []
# if 'website_urls' not in st.session_state:
#     st.session_state.website_urls = []

# # Function to convert PDF to image
# def pdf_to_image(pdf_data):
#     pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
#     page = pdf_document.load_page(0)
#     pix = page.get_pixmap()
#     img_data = pix.tobytes("ppm")
#     img = Image.open(io.BytesIO(img_data))
#     return img

# # Function to get website title
# def get_website_title(url):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     return soup.title.string if soup.title else 'Unknown Title'

# # Function to get website icon
# def get_website_icon(url):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     icon_link = soup.find('link', rel='icon')
#     if icon_link:
#         icon_url = icon_link['href']
#         if not icon_url.startswith('http'):
#             icon_url = requests.compat.urljoin(url, icon_url)
#         icon_data = requests.get(icon_url).content
#         img = Image.open(io.BytesIO(icon_data))
#         return img
#     return None

# st.title("Upload Note, PDF, Website,...")

# # Store previously uploaded files to detect removals
# previous_uploaded_files = st.session_state.uploaded_files_names.copy()
# st.session_state.previous_removed = ""

# uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

# if uploaded_files is not None:
#     uploaded_files_names = [uploaded_file.name for uploaded_file in uploaded_files if uploaded_file.name != st.session_state.previous_removed]
    
#     # Detect removed files
#     removed_files = set(previous_uploaded_files) - set(uploaded_files_names)
#     for removed_file in removed_files:
#         st.session_state.pdf_images = [(name, img) for name, img in st.session_state.pdf_images if name != removed_file]
    
#     # Update session state with current file names
#     st.session_state.uploaded_files_names = uploaded_files_names

#     for uploaded_file in uploaded_files:
#         if uploaded_file.name not in [file[0] for file in st.session_state.pdf_images]:
#             pdf_data = uploaded_file.read()
#             print(dir(uploaded_file))
#             # print(pdf_data)
#             # loader = PyPDFLoader(pdf_data)
#             # documents = loader.load()
#             # print(documents[0])
#             image = pdf_to_image(pdf_data)
#             # Store the image in the session state
#             st.session_state.pdf_images.append((uploaded_file.name, image))

# # Website URL input
# website_url = st.text_input("Enter website URL")

# if st.button("Add URL"):
#     if website_url and website_url not in st.session_state.website_urls:
#         st.session_state.website_urls.append(website_url)
#         name = get_website_title(website_url)
#         icon = get_website_icon(website_url)
#         if icon:
#             st.session_state.website_images.append((name, icon))

# # Function to remove item
# def remove_item(item_name):
#     st.session_state.pdf_images = [(name, img) for name, img in st.session_state.pdf_images if name != item_name]
#     st.session_state.website_images = [(name, img) for name, img in st.session_state.website_images if name != item_name]
#     st.session_state.uploaded_files_names = [name for name in st.session_state.uploaded_files_names if name != item_name]
#     st.session_state.website_urls = [url for url in st.session_state.website_urls if get_website_title(url) != item_name]
#     st.experimental_rerun()

# # Display added website URLs
# if st.session_state.website_urls:
#     st.header("Added Website URLs")
#     for url in st.session_state.website_urls:
#         title = get_website_title(url)
#         st.markdown(f"- {title} ({url})")
#         if st.button(f"Remove {title}", key=f"remove-url-{url}"):
#             remove_item(title)

# # Display the uploaded PDFs and their thumbnails
# if st.session_state.pdf_images or st.session_state.website_images:
#     st.header("Workspace")

#     cols = st.columns(4)
#     idx = 0
#     for pdf_name, image in st.session_state.pdf_images:
#         with cols[idx % 4]:
#             st.image(image, caption=pdf_name, use_column_width=True)
#             if st.button("Remove", key=f"remove-{pdf_name}"):
#                 remove_item(pdf_name)
#         idx += 1

#     for web_name, image in st.session_state.website_images:
#         with cols[idx % 4]:
#             st.image(image, caption=web_name, use_column_width=True)
#             if st.button("Remove", key=f"remove-{web_name}"):
#                 remove_item(web_name)
#         idx += 1

import streamlit as st
from langchain.document_loaders import PyPDFLoader
from pages import control_pdf_on_data

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    path = control_pdf_on_data.save_uploaded_pdf(uploaded_file)
    # Create a PyPDFLoader instance
    loader = PyPDFLoader(path)
    # Load documents from the PDF
    documents = loader.load()
    # Accumulate text from all pages
    text = ""
    for document in documents:
        text += document.page_content
    return text

# Display a file uploader widget
uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

# Extract text from the uploaded PDF file
if uploaded_file is not None:
    extracted_text = extract_text_from_pdf(uploaded_file)
    st.write("Extracted text:")
    st.write(extracted_text)