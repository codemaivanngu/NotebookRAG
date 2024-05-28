import requests
from bs4 import BeautifulSoup
from io import BytesIO
from urllib.parse import urljoin
from PIL import Image

def get_favicon_image(url):
  """
  Retrieves the favicon image from a URL and returns it as a PNG image in memory.

  Args:
      url: The URL of the website.

  Returns:
      A BytesIO object containing the favicon image in PNG format, or None if an error occurs.
  """
  try:
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    favicon_link = soup.find('link', rel='icon') or soup.find('link', rel='shortcut icon')
    if favicon_link:
      favicon_url = favicon_link.get('href')
      # Ensure the favicon URL is absolute
      favicon_url = urljoin(url, favicon_url)

      favicon_response = requests.get(favicon_url)
      favicon_response.raise_for_status()

      # Convert the image to PNG format before returning
      image = Image.open(BytesIO(favicon_response.content))
      image_bytes = BytesIO()
      image.save(image_bytes, format="PNG")
      return image_bytes
    else:
      return None
  except Exception as e:
    print("Error:", e)
    return None

def save_image(image_bytes, filename):
    try:
        with open(filename, 'wb') as f:
            f.write(image_bytes.getvalue())
        print("Image saved successfully.")
    except Exception as e:
        print("Error:", e)

# url = 'https://docs.google.com/spreadsheets/d/1gH3yZqRUELBO2T5udL0vR8qiIrlPedM3Fl3avZlxzzY/edit#gid=0'
# favicon_image_bytes = get_favicon_image(url)
# if favicon_image_bytes:
#     print("Favicon image downloaded successfully.")
#     save_image(favicon_image_bytes, 'favicon.ico')
# else:
#     print("Favicon not found.")
