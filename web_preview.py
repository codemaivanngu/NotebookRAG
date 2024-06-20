from io import BytesIO
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from PIL import Image

# from playwright.sync_api import sync_playwright


def get_website_icon(url):
    """
    Attempts to retrieve the website's favicon or icon as a PNG image.

    This function tries three approaches to find a website icon:
      1. Checks for a favicon.ico file at the root of the website URL.
      2. Parses the website's HTML for a link element with rel="icon" or rel="shortcut icon".
      3. Return no_internet image.

    Args:
        url (str): The URL of the website to get the icon from.

    Returns:
        PIL.Image object: The retrieved icon as a PNG image, or \
            None if no icon is found or conversion fails.
    """
    # Try 1: Check for favicon.ico
    try:
        favicon_url = urljoin(url, "favicon.ico")
        response = requests.get(favicon_url)
        response.raise_for_status()

        # Attempt to convert retrieved data to PNG
        try:
            image = Image.open(BytesIO(response.content))
            # Assumes the downloaded favicon is a valid image format
            image_bytes = BytesIO()
            image.save(image_bytes, format="PNG")
            # image.show()
            return Image.open(image_bytes)  # Return converted PNG image
        except (IOError, OSError):
            pass  # Ignore errors and move to next approach

    except requests.exceptions.RequestException:
        pass  # Ignore exceptions and move to next approach

    # Try 2: Parse HTML for link element
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        favicon_link = soup.find('link', rel='icon') or soup.find(
            'link', rel='shortcut icon'
        )
        if favicon_link:
            favicon_url = urljoin(url, favicon_link.get('href'))
            response = requests.get(favicon_url)
            response.raise_for_status()

            # Attempt to convert retrieved data to PNG
            try:
                image = Image.open(BytesIO(response.content))
                image_bytes = BytesIO()
                image.save(image_bytes, format="PNG")
                # image.show()
                return Image.open(image_bytes)  # Return converted PNG image
            except (IOError, OSError):
                pass  # Ignore errors and move to optional fallback

    except requests.exceptions.RequestException:
        pass  # Ignore exceptions and move to optional fallback

    # Try 3 : return no_internet
    image = Image.open(r"C:\Projects\NoteRAG\data\app\no_internet_Dinosaur.png")
    return image


# get_website_icon("https://www.diffchecker.com/text-compare/").show()
# img.show()
def save_image(image_bytes, filename):
    """
    Saves the provided image bytes to a file with the specified filename.

    Args:
        image_bytes: A BytesIO object containing the image data.
        filename: The name of the file to save the image to.
    """
    try:
        with open(filename, 'wb') as f:
            f.write(image_bytes.getvalue())
        print("Image saved successfully as", filename)
    except Exception as e:
        print("Error:", e)


def get_website_title(url):
    """
    Extracts the title of a website from its HTML content.

    This function fetches the HTML content of the specified URL using a GET request
    and then parses it with BeautifulSoup. It attempts to extract the website title
    from the `<title>` tag within the HTML. If the title tag is not found, the
    function returns the original URL as a fallback.

    Args:
        url (str): The URL of the website to extract the title from.

    Returns:
        str: The extracted title of the website, or the original URL if no title is found.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.title.string if soup.title else url
    return title


# def url_to_image(url, viewport=None, selector=None):
#   """
#   Captures a screenshot of a website as an image.

#   This function uses Playwright to launch a headless browser, navigate to the
#   specified URL, and capture a screenshot of the entire page by default.  You can
#   optionally provide a viewport size and a CSS selector to capture a specific
#   area of the page.

#   Args:
#       url (str): The URL of the website to capture.
#       viewport (dict, optional): A dictionary specifying the viewport width
#           and height for the screenshot. Defaults to None (full page).
#       selector (str, optional): A CSS selector to capture a specific area
#           of the page. Defaults to None (full page).

#   Returns:
#       bytes: The captured screenshot image data in bytes.
#   """
#   with sync_playwright() as playwright:
#     browser = playwright.webkit.launch(headless=True)  # Run headless
#     page = browser.new_page()
#     if viewport:
#       page.set_viewport_size(viewport)
#     page.goto(url)
#     if selector:
#       # Capture the specified element or area
#       image = page.query_selector(selector).screenshot()
#     else:
#       # Capture the entire page
#       image = page.screenshot(full_page=True)
#     browser.close()
#     return image

# # # Example usage
# # image_data = url_to_image("https://www.google.com/")
# # # or capture a specific element
# # image_data = url_to_image("https://www.example.com/", selector="#main-content")
