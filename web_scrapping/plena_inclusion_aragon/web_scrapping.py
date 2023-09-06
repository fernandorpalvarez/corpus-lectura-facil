from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urljoin
import requests
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
    extracted_text = bs4_soup.find_all('div', {"id": "capa2"})
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


def execute_scrapping(base_url, sub_url_news, path_to_new):
    soup = get_soup(base_url + sub_url_news)
    elements = soup.find_all('div', class_="tooltipderecha")
    pdfs_with_errors = []
    i = 0

    # Parse the url with beautifulsoup
    for card in elements:
        content_url = base_url + card.a['href'][2:]
        if (not content_url.startswith('http')) | (not content_url.startswith('https')):
            content_url = urljoin("https://plenainclusionextremadura.org/", content_url)

        content_soup = get_soup(content_url)
        news_files = content_soup.find_all('a', {'target': '_blank'})
        for new in news_files:
            pdf_url = base_url + new['href'][2:]
            if '.pdf' in pdf_url:
                try:
                    response = requests.get(pdf_url)
                    file_local_path = os.path.join(path_to_new, pdf_url.split('/')[-1])
                    file_local_path = file_local_path.split(".pdf")[-2] + "_" + str(i) + ".pdf"
                    with open(file_local_path, 'wb') as f:
                        print("Saving,", file_local_path)
                        f.write(response.content)

                except Exception as e:
                    print(e)
                    pdfs_with_errors.append(pdf_url)


if __name__ == '__main__':
    url = "https://www.plenainclusionaragon.org/cea/lf/es/"
    sub_url_news = "index.php?id=1&seccion=noticias&tipo=periodico_aragon"
    path = 'C:/Users/ferna/Universidad Politécnica de Madrid/Linea Accesibilidad Cognitiva (Proyecto)-Corpus Lectura Fácil (2023) - Documentos/data/pdfs_from_web/plena_inclusion_aragon'
    raw_text_in_pages = execute_scrapping(url, sub_url_news, path)
