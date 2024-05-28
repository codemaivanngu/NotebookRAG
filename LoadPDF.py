import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import requests
from bs4 import BeautifulSoup
import threading
from time import perf_counter
from playwright.sync_api import sync_playwright
import preview_web
# Function to convert PDF to image
def pdf_to_image(pdf_data):
    pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
    first_page = pdf_document.load_page(0)
    pix = first_page.get_pixmap()
    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return image