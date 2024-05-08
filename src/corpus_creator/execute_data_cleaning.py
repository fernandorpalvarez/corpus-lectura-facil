from src.corpus_creator.data_cleaning_impl.data_cleaning_pipeline import *
from src.corpus_creator.tools import dataframe_tools
import json
import time


def execute_data_cleaning():
    """
    Pipeline to clean the raw text in the pipeline:
        raw -> clean
    """
    config = json.load(open("../../config/data_cleaning_config.json", "r", encoding="utf-8"))
    base_path = config["base_path"]
    raw_path = config["raw_path"]
    clean_path = config["clean_path"]
    lectura_facil_raw_file_name = config["lectura_facil_raw_file_name"]
    lenguaje_natural_raw_file_name = config["lenguaje_natural_raw_file_name"]
    lectura_facil_clean_file_name = config["lectura_facil_clean_file_name"]
    lenguaje_natural_clean_file_name = config["lenguaje_natural_clean_file_name"]

    full_raw_path = base_path + raw_path
    full_clean_path = base_path + clean_path

    print("Executing data cleaning...")

    start_time = time.time()

    # Get the text
    lf_raw_text_df = dataframe_tools.read_dataframe(full_raw_path, lectura_facil_raw_file_name)
    ln_raw_text_df = dataframe_tools.read_dataframe(full_raw_path, lenguaje_natural_raw_file_name)

    # Initialize the two pipeline objects
    lf_data_cleaning_obj = DataCleaningPipeline(min_len_for_line=30, max_len_for_line=70, min_dig_number=4)
    ln_data_cleaning_obj = DataCleaningPipeline(min_len_for_line=30, max_len_for_line=120, min_dig_number=4)

    # Preprocess both dataframes
    lf_clean_text_df = lf_data_cleaning_obj.apply_cleaning_pipeline(lf_raw_text_df)
    ln_clean_text_df = ln_data_cleaning_obj.apply_cleaning_pipeline(ln_raw_text_df)

    # Save it
    dataframe_tools.write_dataframe(lf_clean_text_df, full_clean_path, lectura_facil_clean_file_name)
    dataframe_tools.write_dataframe(ln_clean_text_df, full_clean_path, lenguaje_natural_clean_file_name)

    finish_time = time.time()

    total_time = finish_time - start_time

    print(f"Complete!: {total_time}")


if __name__ == '__main__':
    execute_data_cleaning()
