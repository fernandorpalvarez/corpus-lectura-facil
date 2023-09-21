import json
from web_scrapping import *


def extract_pdfs_from_webs():
    config = json.load(open("../config/data_pipeline_config.json", "r", encoding="utf-8"))
    sources = config["web_scrapping"]["sources"]
    for source in sources:
        if sources[source]["execute"]:
            print(sources[source]["url"])
