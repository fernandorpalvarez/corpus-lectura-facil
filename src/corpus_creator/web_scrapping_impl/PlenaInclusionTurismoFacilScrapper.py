from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
from src.corpus_creator.interfaces import WebScrapperInterface


class PlenaInclusionTurismoFacilScrapper(WebScrapperInterface):
    def __init__(self):
        self.decoder = "utf-8"
        self.bf4_parser = "html.parser"

    def get_soup(self, link):
        page = urlopen(link)
        html = page.read().decode(self.decoder)
        return BeautifulSoup(html, self.bf4_parser)

    def execute_scrapping(self, base_url, saving_path):
        soup = self.get_soup(base_url)

        # Parse the url with beautifulsoup
        for e in soup.find_all('h3', class_="elementor-image-box-title"):
            content_url = e.a
            if content_url:
                content_url = content_url['href']
            else:
                continue

            # Get the pdf inside the url
            content_soup = self.get_soup(content_url)
            e_url = content_soup.find_all('a', class_="btn btn_principal btn_principal--naranja")
            if len(e_url) > 0:
                e_url = e_url[0]['href']
            else:
                continue

            # Logic to download the pdf
            if '.pdf' in e_url.lower():
                try:
                    response = requests.get(e_url)
                    response_name = e_url.split('/')[-1]
                    file_local_path = saving_path + "/" + response_name
                    with open(file_local_path, 'wb') as f:
                        f.write(response.content)

                except Exception as e:
                    print(e)
