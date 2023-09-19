import json


def extract_pdfs_from_webs():
    config = json.load(open("../config/data_pipeline_config.json", "r", encoding="utf-8"))
