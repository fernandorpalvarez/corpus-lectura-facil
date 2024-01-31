from bs4 import BeautifulSoup
from src.corpus_creator.interfaces.WebScrapperInterface import WebScrapperInterface
from urllib.request import urlopen
from urllib.parse import urljoin
import requests
import os


class PlenaInclusionAragonNoticiasScrapper(WebScrapperInterface):
    def __init__(self):
        self.decoder = "utf-8"
        self.bf4_parser = "html.parser"
        self.url_extra = "index.php?id=1&seccion=noticias&tipo=periodico_aragon"

    def get_soup(self, url):
        page = urlopen(url)
        html = page.read().decode(self.decoder)
        return BeautifulSoup(html, self.bf4_parser)

    def get_text_from_new(self, url):
        bs4_soup = self.get_soup(url)
        clean_text = self.clean_content(bs4_soup)
        name = url.split("/")[-1] + ".txt"
        self.save_new(clean_text, name)
        return clean_text

    def clean_content(self, bs4_soup):
        extracted_text = bs4_soup.find_all('div', {"id": "capa2"})
        text_no_html = ""
        for text in extracted_text:
            text_no_html = text_no_html + " " + BeautifulSoup(str(text), "lxml").text
        return text_no_html

    def save_new(self, text, name):
        text_file = open(name, "w", encoding=self.decoder)

        # write string to file
        text_file.write(text)

        # close file
        text_file.close()

    def execute_scrapping(self, base_url, path_to_new):
        soup = self.get_soup(base_url + self.url_extra)
        elements = soup.find_all('div', class_="tooltipderecha")
        i = 0

        # Parse the url with beautifulsoup
        for card in elements:
            content_url = base_url + card.a['href'][2:]
            if (not content_url.startswith('http')) | (not content_url.startswith('https')):
                content_url = urljoin("https://plenainclusionextremadura.org/", content_url)

            content_soup = self.get_soup(content_url)
            news_files = content_soup.find_all('a', {'target': '_blank'})
            for new in news_files:
                pdf_url = base_url + new['href'][2:]
                if '.pdf' in pdf_url:
                    try:
                        response = requests.get(pdf_url)
                        file_local_path = os.path.join(path_to_new, pdf_url.split('/')[-1])
                        file_local_path = file_local_path.split(".pdf")[-2] + "_" + str(i) + ".pdf"
                        with open(file_local_path, 'wb') as f:
                            f.write(response.content)

                    except Exception as e:
                        print(e)
