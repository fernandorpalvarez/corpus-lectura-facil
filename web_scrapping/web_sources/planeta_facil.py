from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urljoin
import os


def get_soup(url):
    page = urlopen(url)
    html = page.read().decode("utf-8")
    return BeautifulSoup(html, "html.parser")


def get_text_from_new(url):
    bs4_soup = get_soup(url)
    clean_text = clean_content(bs4_soup)
    name = url.split("/")[-1] + ".txt"
    save_new(clean_text, name)
    return clean_text


def clean_content(bs4_soup):
    extracted_text = bs4_soup.find_all('div', class_="entry-content texto-lector-general")
    text_no_html = ""
    for text in extracted_text:
        text_no_html = text_no_html + " " + BeautifulSoup(str(text), "lxml").text
    return text_no_html


def save_new(text, name):
    text_file = open(name, "w", encoding="utf-8")

    # write string to file
    text_file.write(text)

    # close file
    text_file.close()


def execute_scrapping(base_url, path_to_new):
    soup = get_soup(base_url)

    i = 1
    j = 1
    raw_text_in_pages = []

    elements = soup.find_all('a', class_="eael-post-elements-readmore-btn")

    # Parse the url with beautifulsoup
    for card in elements:
        content_url = card['href']

        if (not content_url.startswith('http')) | (not content_url.startswith('https')):
            content_url = urljoin(base_url, content_url)

        content_soup = get_soup(content_url)
        try:
            file_name = os.path.join(path_to_new, f"file_{str(j)}.txt")
            while os.path.isfile(file_name):
                j += 1
                file_name = os.path.join(path_to_new, f"file_{str(j)}.txt")
            # file_name = content_url.split("/")[-2]
            text = clean_content(content_soup)
            save_new(text, file_name)

        except Exception as e:
            print("Could not retreive pdf from: ", content_url, ", due to: ", e)

    return raw_text_in_pages


if __name__ == '__main__':
    url = "https://planetafacil.plenainclusion.org/noticias/"
    path = 'C:/Users/ferna/Universidad Politécnica de Madrid/Linea Accesibilidad Cognitiva (Proyecto)-Corpus Lectura Fácil (2023) - Documentos/data/pdfs_from_web/planeta_facil/'
    raw_text_in_pages = execute_scrapping(url, path)
