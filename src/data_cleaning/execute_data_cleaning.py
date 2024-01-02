from src.data_cleaning.data_cleaning_pipeline import *
import json


if __name__ == '__main__':
    '''
    Pipeline to clean the raw text in the pipeline:
        raw -> clean
    '''
    config = json.load(open("../../config/data_cleaning_config.json", "r", encoding="utf-8"))
    extracted_text_path = config["extracted_text_path"]
    raw_file_name = config["raw_file_name"]
    clean_text_path = config["clean_text_path"]
    clean_file_name = config["clean_file_name"]
    separator = config["separator"]

    # Get the text
    raw_text_df = load_text_from_csv(os.path.join(extracted_text_path, raw_file_name), separator)
    # Preprocess it
    clean_text_df = apply_pipeline(raw_text_df)
    # Save it
    save_dataframe_in_path(clean_text_df, clean_text_path, clean_file_name, separator)
