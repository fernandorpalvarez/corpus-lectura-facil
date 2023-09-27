import os
import json
from web_scrapping.web_sources import *


def extract_pdfs_from_webs():
    # First get the config from the json file
    config = json.load(open("../config/data_pipeline_config.json", "r", encoding="utf-8"))
    sources = config["web_scrapping"]["sources"]
    base_saving_path = config["web_scrapping"]["saving_path"]

    # Iterate over the sources and execute their respective script
    for source in sources:
        if sources[source]["execute"]:
            url = sources[source]["url"]
            saving_path = os.path.join(base_saving_path, source)

            if source == "asociacion_lectura_facil":
                asociacion_lectura_facil.execute_scrapping(url, saving_path)
            elif source == "ayuntamiento_logroño":
                ayuntamiento_logroño.execute_scrapping(url, saving_path)
            elif source == "cedid":
                cedid.execute_scrapping(url, saving_path)
            elif source == "planeta_facil":
                planeta_facil.execute_scrapping(url, saving_path)
            elif source == "plena_inclusion":
                plena_inclusion.execute_scrapping(url, saving_path)
            elif source == "plena_inclusion_aragon":
                plena_inclusion_aragon.execute_scrapping(url, saving_path)
            elif source == "plena_inclusion_extremadura":
                plena_inclusion_extremadura.execute_scrapping(url, saving_path)
            elif source == "plena_inclusion_noticias":
                plena_inclusion_noticias.execute_scrapping(url, saving_path)
            elif source == "transparencia_aragon":
                transparencia_aragon.execute_scrapping(url, saving_path)
