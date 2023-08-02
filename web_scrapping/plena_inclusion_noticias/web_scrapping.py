from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urljoin


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
    extracted_text = bs4_soup.find_all('section', class_="entry-content cf")
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
    i = 1
    base_url_paged = base_url + str(i)
    soup = get_soup(base_url_paged)
    raw_text_in_pages = []

    while len(soup.find_all('a', class_="elementor-post__thumbnail__link")) > 0:

        soup = get_soup(base_url + str(i))
        elements = soup.find_all('a', class_="elementor-post__thumbnail__link")

        # Parse the url with beautifulsoup
        for card in elements:
            content_url = card['href']

            if (not content_url.startswith('http')) | (not content_url.startswith('https')):
                content_url = urljoin(base_url, content_url)

            content_soup = get_soup(content_url)
            try:
                file_name = content_url.split("/")[-2]
                text = clean_content(content_soup)
                new_path_to_new = path_to_new + file_name + '.txt'
                save_new(text, new_path_to_new)

            except Exception as e:
                print("Could not retreive pdf from: ", content_url, ", due to: ", e)

        i += 1

    return raw_text_in_pages


if __name__ == '__main__':
    url = "https://www.plenainclusion.org/noticias/?sf_paged="
    path = '/corpus-lectura-facil/web_scrapping/plena_inclusion_noticias/texts/'
    raw_text_in_pages = execute_scrapping(url, path)
