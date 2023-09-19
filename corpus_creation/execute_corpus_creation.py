from lectura_facil_pipeline import *
import json


if __name__ == '__main__':
    config = json.load(open("../config/pdf_to_text_extraction_config.json", "r", encoding="utf-8"))
    extracted_text_path = config["corpus_creation"]["extracted_text_path"]
    corpus_lectura_facil_path = config["corpus_creation"]["corpus_lectura_facil_path"]

    # Get the text
    corpus_lectura_facil_df = load_text_in_lectura_facil_from_path(extracted_text_path)
    # Preprocess it
    corpus_lectura_facil_df = apply_pipeline(corpus_lectura_facil_df[:10])
    # Save it
    save_dataframe_in_path(corpus_lectura_facil_df, corpus_lectura_facil_path)
