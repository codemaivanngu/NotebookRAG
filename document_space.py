import streamlit as st

import control_pdf_on_data
import control_web


def app():
    # control_web.clear_web_store()
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
    st.session_state.uploaded_files_names.copy()

    # uploaded_files = st.file_uploader("Upload PDF files", type="pdf",
    # accept_multiple_files=True,key=key=st.session_state["file_uploader_key"],on_change=F5PDF)
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

        for uploaded_file in st.session_state["uploaded_files"]:
            path = control_pdf_on_data.save_uploaded_pdf(uploaded_file)
            control_pdf_on_data.add_PDF(path)
        st.rerun()

    def F5():
        control_web.add_web_page(st.session_state.input1)
        st.session_state.input_temp = st.session_state.input1
        st.session_state.input1 = ""

    # website_url = st.text_input("Enter website URL", key="input1", on_change=F5)

    # Display the uploaded PDFs and their thumbnails
    if len(control_pdf_on_data.PDF_store) or len(control_web.web_store):
        st.header("Workspace")

        cols = st.columns(4)
        idx = 0
        st.session_state.PDF_need_to_del = {}
        for pdf_path, value in control_pdf_on_data.PDF_store.items():
            documents, image = value
            title = documents[0].metadata['source'].split("\\")[-1]
            with cols[idx % 4]:
                if st.session_state.PDF_need_to_del.get(pdf_path) is None:
                    st.image(image, caption=title, use_column_width=True)
                # if st.button(f"Remove {title}"):
                if st.button("Remove", key=f"remove-PDF-{title}"):
                    st.session_state.PDF_need_to_del[pdf_path] = "1"
            idx += 1
        if len(st.session_state.PDF_need_to_del):
            for key in st.session_state.PDF_need_to_del.keys():
                control_pdf_on_data.remove_PDF(key)
            st.session_state.PDF_need_to_del = {}
            # control_pdf_on_data.close_PDF_store()
            st.rerun()

        # show webpage
        st.session_state.web_need_to_del = {}
        for url, value in control_web.web_store.items():
            documents, image = value
            with cols[idx % 4]:
                if st.session_state.web_need_to_del.get(url) is None:
                    st.image(
                        image,
                        caption=documents[0].metadata['title'],
                        use_column_width=True,
                    )
                # if st.button(f"Remove {url}", key=f"remove-url-{url}"):
                if st.button("Remove", key=f"remove-url-{url}"):
                    st.session_state.web_need_to_del[url] = "1"
            idx += 1
        if len(st.session_state.web_need_to_del):
            for url in st.session_state.web_need_to_del.keys():
                control_web.remove_web_page(url)
            st.session_state.web_need_to_del = {}

            # control_web.close_web_store()
            st.rerun()
