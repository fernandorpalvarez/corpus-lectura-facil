import os
import json
from src.corpus_creator.web_scrapping_impl.AsociacionLecturaFacilScrapper import AsociacionLecturaFacilScrapper
from src.corpus_creator.web_scrapping_impl.CedidScrapper import CedidScrapper
from src.corpus_creator.web_scrapping_impl.EasyNewsScrapper import EasyNewsScrapper
from src.corpus_creator.web_scrapping_impl.PlanetaFacilScrapper import PlanetaFacilScrapper
from src.corpus_creator.web_scrapping_impl.PlenaInclusionScrapper import PlenaInclusionScrapper
from src.corpus_creator.web_scrapping_impl.PlenaInclusionExtremaduraScrapper import PlenaInclusionExtremaduraScrapper
from src.corpus_creator.web_scrapping_impl.PlenaInclusionNoticiasScrapper import PlenaInclusionNoticiasScrapper
from src.corpus_creator.web_scrapping_impl.TransparenciaAragonScrapper import TransparenciaAragonScrapper
from src.corpus_creator.web_scrapping_impl.PlenaInclusionTurismoFacilScrapper import PlenaInclusionTurismoFacilScrapper
from src.corpus_creator.web_scrapping_impl.PlenaInclusionAragonNoticiasScrapper import \
    PlenaInclusionAragonNoticiasScrapper


def extract_pdfs_from_webs():
    # First get the config from the json file
    config = json.load(open("../../config/web_scrapping_config.json.json", "r", encoding="utf-8"))
    sources = config["web_scrapping"]["sources"]
    base_saving_path = config["web_scrapping"]["saving_path"]

    # Iterate over the sources and execute their respective script
    for source in sources:
        if sources[source]["execute"]:
            url = sources[source]["url"]
            saving_path = os.path.join(base_saving_path, source)

            if source == "asociacion_lectura_facil":
                AsociacionLecturaFacilScrapper().execute_scrapping(url, saving_path)
            elif source == "cedid":
                CedidScrapper().execute_scrapping(url, saving_path)
            elif source == "easy_news":
                EasyNewsScrapper().execute_scrapping(url, saving_path)
            elif source == "planeta_facil":
                PlanetaFacilScrapper.execute_scrapping(url, saving_path)
            elif source == "plena_inclusion":
                PlenaInclusionScrapper().execute_scrapping(url, saving_path)
            elif source == "plena_inclusion_aragon_noticias":
                PlenaInclusionAragonNoticiasScrapper().execute_scrapping(url, saving_path)
            elif source == "plena_inclusion_extremadura":
                PlenaInclusionExtremaduraScrapper().execute_scrapping(url, saving_path)
            elif source == "plena_inclusion_noticias":
                PlenaInclusionNoticiasScrapper().execute_scrapping(url, saving_path)
            elif source == "transparencia_aragon":
                TransparenciaAragonScrapper().execute_scrapping(url, saving_path)
            elif source == "plena_inclusion_turismo_facil":
                PlenaInclusionTurismoFacilScrapper().execute_scrapping(url, saving_path)
