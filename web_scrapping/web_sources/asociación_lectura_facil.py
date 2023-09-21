from bs4 import BeautifulSoup
from urllib.request import urlopen
from tqdm import tqdm
from urllib.parse import urljoin
import requests
import os


def get_soup(url):
    page = urlopen(url)
    html = page.read().decode("utf-8")
    return BeautifulSoup(html, "html.parser")


i = 0
base_url = "https://repositori.lecturafacil.net/es/taxonomy/term/1?page="
content_file_urls = []

while len(get_soup(base_url + str(i)).find_all('a', class_="btn btn-download")) > 0:

    # Get the html content
    url = base_url + str(i)
    soup = get_soup(url)

    # Parse the url with beautifulsoup
    for pdf in soup.find_all('a', class_="btn btn-download"):
        pdf_url = pdf['href']
        try:
            content_file_urls.append(pdf_url)
        except Exception as e:
            print("Could not retreive pdf from: ", pdf_url, ", due to: ", e)
    i += 1

# removing duplicates
content_file_urls = list(dict.fromkeys(content_file_urls))
print(len(content_file_urls), "pdfs doesn't have duplicates")

# Saving files list in memory
try:
    if content_file_urls:
        with open(r'../asociacion_lectura_facil/content_list.txt', 'w') as fp:
            for item in tqdm(content_file_urls):
                # write each item on a new line
                fp.write("%s\n" % item)
except Exception as e:
    print(e)

# Reading files list from memory
try:
    with open(
            '../asociacion_lectura_facil/content_list.txt') as f:
        content_file_urls = f.read().splitlines()
except Exception as e:
    print(e)

# 222 out of the 222 pages with 'lectura fácil' contains usable .pdf files

counter_pdf = 0

for url in content_file_urls:
    if '.pdf' in url or 'PDF' in url:
        counter_pdf += 1
    else:
        print(url)

print(counter_pdf)

# Saving pdf content from urls into memory
path_to_local_files = "C:/Users/ferna/Universidad Politécnica de Madrid/Documentos - Linea Accesibilidad Cognitiva (Proyecto)-Corpus Lectura Fácil (2023)/data/pdfs_from_web/asociacion_lectura_facil"
pdfs_with_errors = []

for url in tqdm(content_file_urls):
    if '.pdf' in url or 'PDF' in url:
        try:
            response = requests.get(url)
            file_local_path = os.path.join(path_to_local_files, url.split('/')[-1])
            with open(file_local_path, 'wb') as f:
                f.write(response.content)

        except Exception as e:
            print(e)
            pdfs_with_errors.append(url)

# 0 out of the 222 pdf files had some kind of problem when loading them

print(len(pdfs_with_errors))

with open(r'./pdfs_with_errors.txt', 'w') as fp:
    for item in tqdm(pdfs_with_errors):
        # write each item on a new line
        fp.write("%s\n" % item)