import os.path
from bs4 import BeautifulSoup
from urllib.request import urlopen
from src.corpus_creator.interfaces import WebScrapperInterface


class EasyNewsScrapper(WebScrapperInterface):
    def __init__(self):
        self.decoder = "utf-8"
        self.bf4_parser = "html.parser"
        self.clean_html_class = "p-2 border-top"

    def get_soup(self, link):
        page = urlopen(link)
        html = page.read().decode(self.decoder)
        return BeautifulSoup(html, self.bf4_parser)

    def clean_content(self, bs4_soup):
        extracted_text = bs4_soup.find_all('div', class_=self.clean_html_class)[0]
        text_no_html = BeautifulSoup(str(extracted_text).replace("<br/>", " ").replace("<", " <"), "lxml").text
        return text_no_html

    def save_new(self, text, name):
        text_file = open(name, "w", encoding=self.decoder)

        # write string to file
        text_file.write(text)

        # close file
        text_file.close()

    def execute_scrapping(self, base_url, path_to_new):
        i = 1
        soup = self.get_soup(base_url)
        elements = soup.find_all('article', class_="noticia col-lg-5 shadow-sm")

        # Parse the url with beautifulsoup
        for e in elements:
            content_url = base_url.split("index")[0] + e.a['href']
            content_soup = self.get_soup(content_url)
            try:
                file_name = os.path.join(path_to_new, f"file_{str(i)}.txt")
                while os.path.isfile(file_name):
                    i = i+1
                    file_name = os.path.join(path_to_new, f"file_{str(i)}.txt")
                text = self.clean_content(content_soup)
                self.save_new(text, file_name)

            except Exception as e:
                print("Could not retrieve pdf from: ", content_url, ", due to: ", e)
