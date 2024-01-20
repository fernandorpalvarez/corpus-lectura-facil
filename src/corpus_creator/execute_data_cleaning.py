from src.corpus_creator.data_cleaning_impl.data_cleaning_pipeline import *
from src.corpus_creator.tools import dataframe_tools
import json


if __name__ == '__main__':
    '''
    Pipeline to clean the raw text in the pipeline:
        raw -> clean
    '''
    config = json.load(open("../../config/data_cleaning_config.json", "r", encoding="utf-8"))
    base_path = config["base_path"]
    raw_path = config["raw_path"]
    clean_path = config["clean_path"]
    raw_file_name = config["raw_file_name"]
    clean_file_name = config["clean_file_name"]

    full_raw_path = base_path + raw_path
    full_clean_path = base_path + clean_path

    # Get the text
    raw_text_df = dataframe_tools.read_dataframe(full_raw_path, raw_file_name)
    # Preprocess it
    clean_text_df = DataCleaningPipeline().apply_cleaning_pipeline(raw_text_df)
    # Save it
    dataframe_tools.write_dataframe(clean_text_df, full_clean_path, clean_file_name)
