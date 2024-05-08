import json

from src.corpus_creator import execute_corpus_combiner
from src.corpus_creator import execute_data_cleaning
from src.corpus_creator import execute_text_extraction
from src.corpus_creator import execute_web_scrapping


def create_corpus():
    """
    This function works as a wrapper to execute only the steps in the corpus creation pipeline that the user previously
    specified in the config
    """
    config = json.load(open("../../config/corpus_creation_config.json", "r", encoding="utf-8"))
    ex_web_scrapping_flag = config["ex_web_scrapping_flag"]
    ex_text_extraction_flag = config["ex_text_extraction_flag"]
    ex_data_cleaning_flag = config["ex_data_cleaning_flag"]
    ex_corpus_combiner_flag = config["ex_corpus_combiner_flag"]

    if ex_web_scrapping_flag:
        execute_web_scrapping.execute_web_scrapping()
    if ex_text_extraction_flag:
        execute_text_extraction.execute_text_extraction()
    if ex_data_cleaning_flag:
        execute_data_cleaning.execute_data_cleaning()
    if ex_corpus_combiner_flag:
        execute_corpus_combiner.execute_corpus_combiner()
