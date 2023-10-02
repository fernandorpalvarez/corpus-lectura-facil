import os.path
from bs4 import BeautifulSoup
from urllib.request import urlopen


def get_soup(url):
    page = urlopen(url)
    html = page.read().decode("utf-8")
    return BeautifulSoup(html, "html.parser")


def clean_content(bs4_soup):
    extracted_text = bs4_soup.find_all('div', class_="p-2 border-top")[0]
    text_no_html = BeautifulSoup(str(extracted_text).replace("<br/>", " ").replace("<", " <"), "lxml").text
    return text_no_html


def save_new(text, name):
    text_file = open(name, "w", encoding="utf-8")

    # write string to file
    text_file.write(text)

    # close file
    text_file.close()


def execute_scrapping(base_url, path_to_new):
    i = 1
    soup = get_soup(base_url)
    elements = soup.find_all('article', class_="noticia col-lg-5 shadow-sm")

    # Parse the url with beautifulsoup
    for e in elements:
        content_url = base_url.split("index")[0] + e.a['href']
        content_soup = get_soup(content_url)
        try:
            file_name = os.path.join(path_to_new, f"file_{str(i)}.txt")
            while os.path.isfile(file_name):
                i = i+1
                file_name = os.path.join(path_to_new, f"file_{str(i)}.txt")
            text = clean_content(content_soup)
            save_new(text, file_name)

        except Exception as e:
            print("Could not retrieve pdf from: ", content_url, ", due to: ", e)


if __name__ == '__main__':
    execute_scrapping("https://easynewsportal.eu/index.php?lang=es", "C:/Users/ferna/Universidad Politécnica de Madrid/Linea Accesibilidad Cognitiva (Proyecto)-Corpus Lectura Fácil (2023) - Documentos/data/pdfs_from_web/easy_news")
