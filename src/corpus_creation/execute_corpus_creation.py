from corpus_combiner import *
import json


if __name__ == '__main__':
    '''
        Pipeline to transform the clean text in the pipeline:
            clean -> transform
    '''
    config = json.load(open("../../config/corpus_creation_config.json", "r", encoding="utf-8"))
    extracted_text_path = config["extracted_text_path"]
    corpus_lectura_facil_path = config["corpus_lectura_facil_path"]
