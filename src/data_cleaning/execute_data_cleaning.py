from src.data_cleaning.data_cleaning_pipeline import *
import json


if __name__ == '__main__':
    '''
    Pipeline to clean the raw text in the pipeline:
        raw -> clean
    '''
    config = json.load(open("../../config/data_cleaning_config.json", "r", encoding="utf-8"))
    extracted_text_path = config["data_cleaning_config"]["extracted_text_path"]
    clean_text_path = config["data_cleaning_config"]["clean_text_path"]

    # Get the text
    raw_text_df = load_text_in_lectura_facil_from_path(extracted_text_path)
    # Preprocess it
    clean_text_df = apply_pipeline(raw_text_df[:10])
    # Save it
    save_dataframe_in_path(clean_text_df, clean_text_path)
