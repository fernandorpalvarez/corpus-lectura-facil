from bs4 import BeautifulSoup


def clean_content(bs4_soup):
    extracted_text = bs4_soup.find_all('section', class_="entry-content cf")
    text_no_html = ""
    for text in extracted_text:
        text_no_html = text_no_html + " " + BeautifulSoup(str(text).replace("<br/>", " "), "lxml").text
    return text_no_html
