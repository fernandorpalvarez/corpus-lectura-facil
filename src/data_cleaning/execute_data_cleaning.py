from src.data_cleaning.data_cleaning_pipeline import *
from src.tools import dataframe_tools
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

    # Get the text
    raw_text_df = dataframe_tools.read_dataframe(extracted_text_path, raw_file_name)
    # Preprocess it
    clean_text_df = apply_cleaning_pipeline(raw_text_df)
    # Save it
    dataframe_tools.write_dataframe(clean_text_df, clean_text_path, clean_file_name)
