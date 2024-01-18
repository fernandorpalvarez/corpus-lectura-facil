import os
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urljoin
from src.corpus_creator.interfaces import WebScrapperInterface


class PlenaInclusionExtremaduraScrapper(WebScrapperInterface):
    def __init__(self):
        self.decoder = "utf-8"
        self.bf4_parser = "html.parser"

    def get_soup(self, url):
        page = urlopen(url)
        html = page.read().decode(self.decoder)
        return BeautifulSoup(html, self.bf4_parser)

    def clean_content(self, bs4_soup):
        extracted_text = bs4_soup.find_all('div', {"id": "capa2"})
        text_no_html = ""
        for text in extracted_text:
            text_no_html = text_no_html + " " + BeautifulSoup(str(text).replace("<br/>", " ").replace("<", " <"), "lxml")\
                .text
        return text_no_html

    def save_new(self, text, name):
        text_file = open(name, "w", encoding=self.decoder)

        # write string to file
        text_file.write(text)

        # close file
        text_file.close()

    def execute_scrapping(self, base_url, path_to_new):
        i = 0
        base_url_paged = base_url + str(i)
        soup = self.get_soup(base_url_paged)

        while len(soup.find_all('div', class_="field-item even")) > 0:

            soup = self.get_soup(base_url + str(i))
            elements = soup.find_all('div', class_="field-item even")

            # Parse the url with beautifulsoup
            for card in elements:
                content_url = card.a['href']
                if (not content_url.startswith('http')) | (not content_url.startswith('https')):
                    content_url = urljoin("https://plenainclusionextremadura.org/", content_url)

                content_soup = self.get_soup(content_url)
                try:
                    file_name = content_url.split("/")[-1]
                    text = self.clean_content(content_soup)
                    if len(text) > 31:
                        new_path_to_new = os.path.join(path_to_new, file_name + '.txt')
                        self.save_new(text, new_path_to_new)

                except Exception as e:
                    print("Could not retrieve pdf from: ", content_url, ", due to: ", e)

            i += 1
