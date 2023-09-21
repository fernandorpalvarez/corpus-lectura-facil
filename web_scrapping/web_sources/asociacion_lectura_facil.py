from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests


def get_soup(link):
    page = urlopen(link)
    html = page.read().decode("utf-8")
    return BeautifulSoup(html, "html.parser")


def execute_scrapping(base_url, saving_path):
    i = 0
    soup = get_soup(base_url + str(i))

    while len(soup.find_all('div', class_="item-titol")) > 0:
        # Parse the url with beautifulsoup
        for e in soup.find_all('div', class_="item-titol"):
            e_url_extension = e.a['href']
            e_url = base_url.split("/es/")[0] + e_url_extension

            # Get the content of the pdf introduction page
            e_soup = get_soup(e_url)
            e_html = e_soup.find_all("div",
                                     class_="field field-name-field-idioma field-type-taxonomy-term-reference "
                                            "field-label-above")

            # Ensuring that the element extracted contains the tag that specifies that it is in spanish
            if len(e_html) > 0:
                e_html = e_html[0]
                if e_html.a['href'] == '/es/taxonomy/term/32':
                    # Logic to download the pdf
                    btn_url = e_soup.find_all("a", class_="btn btn-download")
                    if len(btn_url) > 0:
                        pdf_url = btn_url[0]['href']
                        if '.pdf' in pdf_url.lower():
                            try:
                                response = requests.get(pdf_url)
                                response_name = pdf_url.split('/')[-1]
                                file_local_path = saving_path + "/" + response_name
                                with open(file_local_path, 'wb') as f:
                                    f.write(response.content)

                            except Exception as e:
                                print(e)

        # Get the next page in the url
        i += 1
        new_url = base_url + str(i)
        soup = get_soup(new_url)
