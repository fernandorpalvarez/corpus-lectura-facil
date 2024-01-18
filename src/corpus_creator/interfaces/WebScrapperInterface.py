from bs4 import BeautifulSoup


class WebScrapperInterface:
    def get_soup(self, url: str) -> BeautifulSoup:
        """
        Function that returns a bf4 boject with the html code of the input url
        :return: BeautifulSoup object
        """
        pass

    def execute_scrapping(self, url: str, saving_path: str):
        """
        Extracts the pdfs/txt from a website and saves it in the path
        :param url: Website from where extract the files
        :param saving_path: Path where saving the files extracted
        """
        pass
