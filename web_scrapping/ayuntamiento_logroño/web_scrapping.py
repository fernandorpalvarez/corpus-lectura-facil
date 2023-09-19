from bs4 import BeautifulSoup
from urllib.request import urlopen
import PyPDF2
import io
import requests
import os


def get_soup(url):
    page = urlopen(url)
    html = page.read().decode("utf-8")
    return BeautifulSoup(html, "html.parser")


def extract_text(url):
    response = requests.get(url)

    # Crea un objeto de archivo en memoria para almacenar el contenido del PDF
    pdf_file = io.BytesIO(response.content)

    # Crea un objeto PDFReader de PyPDF2 y abre el PDF desde el archivo en memoria
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Lee cada página del PDF y extrae el texto
    texto_extraido = ""
    for page in pdf_reader.pages:
        texto_extraido += page.extract_text(keep_blank_chars=True)

    # Imprime el texto extraído del PDF
    return texto_extraido


def clean_text(text):
    text_cleaned = text.split("En LECTURA FÁCIL")[1]
    return text_cleaned


def save_new(text, name):
    text_file = open(name, "w", encoding="utf-8")

    # write string to file
    text_file.write(text)

    # close file
    text_file.close()


def execute_scrapping(base_url, path_to_new):
    i = 1
    soup = get_soup(base_url + str(i))
    elements = soup.find_all('a', {"data-type": "pdf"})
    pdfs_with_errors = []

    while len(get_soup(base_url + str(i)).find_all('a', {"data-type": "pdf"})) > 0:
        # Parse the url with beautifulsoup
        for card in elements:
            pdf_url = "https://logrono.es" + card['href']

            if '.pdf' in pdf_url:
                file_local_path = os.path.join(path_to_new, pdf_url.split('/')[-2])
                extracted_text = extract_text(pdf_url)
                cleaned_text = clean_text(extracted_text)
                with open(file_local_path, 'wb') as f:
                    print("Saving,", file_local_path)
                    f.write(response.content)

        i = i + 1


if __name__ == '__main__':
    url = "https://logrono.es/publicacion-de-buena-fuente?delta=10&start="
    path = './texts/'
    raw_text_in_pages = execute_scrapping(url, path)
