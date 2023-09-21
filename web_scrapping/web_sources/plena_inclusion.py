from bs4 import BeautifulSoup
from urllib.request import urlopen
from tqdm import tqdm
import requests
import os

def get_soup(url):
    page = urlopen(url)
    html = page.read().decode("utf-8")
    return BeautifulSoup(html, "html.parser")

def web_scrapping():
    # Getting the url to the content subpages
    base_url = "https://www.plenainclusion.org/publicaciones/buscador/?_sfm_descargable_lectura_facil=1&sf_paged="

    i = 1
    content_file_urls = []

    while len(get_soup(base_url + str(i)).find_all('h3', class_="card__title")) > 0:
        # Get the html content
        url = base_url + str(i)
        soup = get_soup(url)

        # Parse the url with beautifulsoup
        for card in tqdm(soup.find_all('h3', class_="card__title")):
            content_url = card.find_all(['a'])[0]['href']
            content_soup = get_soup(content_url)
            content_file_urls.append(
                content_soup.find_all('a', class_="btn btn_principal btn_principal--naranja")[0]['href'])

        print(i)
        i += 1

    # Saving files list in memory
    try:
        if content_file_urls:
            with open(r'./content_list.txt', 'w') as fp:
                for item in tqdm(content_file_urls):
                    # write each item on a new line
                    fp.write("%s\n" % item)
    except Exception as e:
        print(e)

    # Reading files list from memory
    try:
        with open('./content_list.txt') as f:
            content_file_urls = f.read().splitlines()
    except Exception as e:
        print(e)

    # 567 out of the 679 pages with 'lectura fácil' contains usable .pdf files

    counter_pdf = 0

    for url in content_file_urls:
        if '.pdf' in url:
            counter_pdf += 1


    # Saving pdf content from urls into memory
    path_to_local_files = "C:/Users/ferna/Universidad Politécnica de Madrid/Linea Accesibilidad Cognitiva (Proyecto)-Corpus Lectura Fácil (2023) - Documentos/data/pdfs_from_web/plena_inclusion_turismo_facil"
    pdfs_with_errors = []

    for url in tqdm(content_file_urls):
        if '.pdf' in url:
            try:
                response = requests.get(url)
                file_local_path = os.path.join(path_to_local_files, url.split('/')[-1])

                with open(file_local_path, 'wb') as f:
                    f.write(response.content)

            except Exception as e:
                print(e)
                pdfs_with_errors.append(url)


if __name__ == '__main__':
    web_scrapping()