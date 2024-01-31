from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urljoin
from src.corpus_creator.interfaces.WebScrapperInterface import WebScrapperInterface
import os


class PlanetaFacilScrapper(WebScrapperInterface):
    def __init__(self):
        self.decoder = "utf-8"
        self.bf4_parser = "html.parser"
        self.clean_html_class = "entry-content texto-lector-general"

    def get_soup(self, url):
        page = urlopen(url)
        html = page.read().decode(self.decode)
        return BeautifulSoup(html, self.bf4_parser)

    def get_text_from_new(self, url):
        bs4_soup = self.get_soup(url)
        clean_text = self.clean_content(bs4_soup)
        name = url.split("/")[-1] + ".txt"
        self.save_new(clean_text, name)
        return clean_text

    def clean_content(self, bs4_soup):
        extracted_text = bs4_soup.find_all('div', class_=self.clean_html_class)
        text_no_html = ""
        for text in extracted_text:
            text_no_html = text_no_html + " " + BeautifulSoup(str(text).replace("<br/>", " "), "lxml").text
        return text_no_html

    def save_new(self, text, name):
        text_file = open(name, "w", encoding=self.decoder)

        # write string to file
        text_file.write(text)

        # close file
        text_file.close()

    def execute_scrapping(self, base_url, path_to_new):
        soup = self.get_soup(base_url)
        j = 1
        elements = soup.find_all('a', class_="eael-post-elements-readmore-btn")

        # Parse the url with beautifulsoup
        for card in elements:
            content_url = card['href']

            if (not content_url.startswith('http')) | (not content_url.startswith('https')):
                content_url = urljoin(base_url, content_url)

            content_soup = self.get_soup(content_url)
            try:
                file_name = os.path.join(path_to_new, f"file_{str(j)}.txt")
                while os.path.isfile(file_name):
                    j += 1
                    file_name = os.path.join(path_to_new, f"file_{str(j)}.txt")
                text = self.clean_content(content_soup)
                self.save_new(text, file_name)

            except Exception as e:
                print("Could not retrieve pdf from: ", content_url, ", due to: ", e)
