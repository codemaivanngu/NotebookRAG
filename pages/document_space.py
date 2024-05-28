import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import requests
from bs4 import BeautifulSoup
import threading
from time import perf_counter
# import web_preview
if __name__ == "__main__":
    import pdf_utilities
    import web_preview
else:
    from . import pdf_utilities
    from . import web_preview
def cb():st.session_state.selected == "Data"
def app():
    import streamlit as st
    import fitz  # PyMuPDF
    from PIL import Image
    import io
    import requests
    from bs4 import BeautifulSoup
    import threading
    from time import perf_counter
    # import web_preview
    if __name__ == "__main__":
        import pdf_utilities
        import web_preview
    else:
        from . import pdf_utilities
        from . import web_preview
        
    cb()

    # Initialize session state for storing PDF and website images
    if 'pdf_images' not in st.session_state:
        st.session_state.pdf_images = []
    if 'website_images' not in st.session_state:
        st.session_state.website_images = []
    if 'uploaded_files_names' not in st.session_state:
        st.session_state.uploaded_files_names = []

    # Streamlit app
    st.title("Upload Note, PDF, Website,...")
    cb()
    # Store previously uploaded files to detect removals
    previous_uploaded_files = st.session_state.uploaded_files_names.copy()
    cb()
    uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)
    cb()
    if uploaded_files is not None:
        cb()
        uploaded_files_names = [uploaded_file.name for uploaded_file in uploaded_files]
        
        # Detect removed files
        removed_files = set(previous_uploaded_files) - set(uploaded_files_names)
        for removed_file in removed_files:
            st.session_state.pdf_images = [(name, img) for name, img in st.session_state.pdf_images if name != removed_file]
        
        # Update session state with current file names
        st.session_state.uploaded_files_names = uploaded_files_names

        for uploaded_file in uploaded_files:
            if uploaded_file.name not in [file[0] for file in st.session_state.pdf_images]:
                pdf_data = uploaded_file.read()
                image = pdf_utilities.pdf_to_image(pdf_data)
                # Store the image in the session state
                st.session_state.pdf_images.append((uploaded_file.name, image))

    # Website URL input
    website_url = st.text_input("Enter website URL")

    if website_url:
        name = web_preview.get_website_title(website_url)
        if name not in [name for name, img in st.session_state.website_images]:
            st.session_state.website_images.append((name, web_preview.get_website_icon(website_url)))

    # Display the uploaded PDFs and their thumbnails
    if st.session_state.pdf_images or st.session_state.website_images:
        st.header("Workspace")
        cb()
        
        cols = st.columns(4)
        cb()
        idx = 0
        for pdf_name, image in st.session_state.pdf_images:
            with cols[idx % 4]:
                st.image(image, caption=pdf_name, use_column_width=True)
            idx += 1
            cb()

        for web_name, image in st.session_state.website_images:
            with cols[idx % 4]:
                st.image(image, caption=web_name, use_column_width=True)
            idx += 1
            cb()
