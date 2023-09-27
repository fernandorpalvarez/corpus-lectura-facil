from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests


def get_soup(link):
    page = urlopen(link)
    html = page.read().decode("utf-8")
    return BeautifulSoup(html, "html.parser")


def execute_scrapping(base_url, saving_path):
    i = 1
    soup = get_soup(base_url + str(i))

    while len(soup.find_all("div", {"class": "row-fluid result clearfix"})) > 0:
        # Parse the url with beautifulsoup
        for e in soup.find_all('span', class_="urlsiis"):
            e_url = e.a['href']

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

        # Get the next page in the url
        i += 1
        new_url = base_url + str(i)
        soup = get_soup(new_url)
