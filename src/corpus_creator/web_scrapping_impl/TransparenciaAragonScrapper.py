from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
from src.corpus_creator.interfaces import WebScrapperInterface


class TransparenciaAragonScrapper(WebScrapperInterface):
    def __init__(self):
        self.decoder = "utf-8"
        self.bf4_parser = "html.parser"

    def get_soup(self, link):
        page = urlopen(link)
        html = page.read().decode(self.decoder)
        return BeautifulSoup(html, self.bf4_parser)

    def execute_scrapping(self, base_url, saving_path):
        soup = self.get_soup(base_url)
        for file in soup.find_all(['a']):
            try:
                file_url = file['href']
                # Logic to download the pdf
                if file_url.lower().endswith('.pdf'):
                    file_url = base_url.split("/GobiernoFacil")[0] + file_url
                    response = requests.get(file_url)
                    response_name = file_url.split('/')[-1]
                    file_local_path = saving_path + "/" + response_name
                    with open(file_local_path, 'wb') as f:
                        f.write(response.content)
            except Exception as e:
                print(e)
