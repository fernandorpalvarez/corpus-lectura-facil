import json

from src.corpus_creator.web_scrapping_impl import web_scrapping_manager
import time


def execute_web_scrapping():
    start_time = time.time()

    # First get the config from the json file
    config_web_scrapping = json.load(open("../../config/web_scrapping_config.json.json", "r", encoding="utf-8"))
    config_corpus_creation = json.load(open("../../config/corpus_creation_config.json", "r", encoding="utf-8"))
    project_path = config_corpus_creation["base_path"]
    sources = config_web_scrapping["web_scrapping"]["sources"]
    base_saving_path = config_web_scrapping["web_scrapping"]["saving_path"]

    base_path = project_path + base_saving_path
    web_scrapping_manager.extract_pdfs_from_webs(base_path, sources)

    finish_time = time.time()
    total_time = finish_time - start_time
    print(f"Complete!: {total_time}")


if __name__ == '__main__':
    execute_web_scrapping()
