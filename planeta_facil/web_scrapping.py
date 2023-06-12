from urllib.parse import urljoin

from bs4 import BeautifulSoup
from urllib.request import urlopen


def get_soup(url):
    page = urlopen(url)
    html = page.read().decode("utf-8")
    return BeautifulSoup(html, "html.parser")


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


if __name__ == '__main__':
    url = "https://planetafacil.plenainclusion.org/las-30-mejores-series-anime-japones-que-debes-ver"
    bs4_soup = get_soup(url)
    clean_text = clean_content(bs4_soup)
    name = url.split("/")[-1] + ".txt"
    save_new(clean_text, name)
    print(clean_text)

    base_url = 'https://planetafacil.plenainclusion.org/noticias/'
    soup = get_soup(base_url)

    i = 1
    content_file_urls = []

    while len(soup.find_all('a', class_="eael-post-elements-readmore-btn")) > 0:

        # Get the html content
        soup = get_soup(base_url)

        # Parse the url with beautifulsoup
        for card in soup.find_all('a', class_="eael-post-elements-readmore-btn"):
            content_url = card['href']
            print(content_url)
            '''
            if not content_url.startswith('http'):
                content_url = urljoin(base_url, content_url)

            content_soup = get_soup(content_url)
            try:
                content_file_urls.append(content_soup.find_all('a', class_="fulltext boton-descargar")[0]['href'])
            except Exception as e:
                print("Could not retreive pdf from: ", content_url, ", due to: ", e)
                '''
        i += 1



