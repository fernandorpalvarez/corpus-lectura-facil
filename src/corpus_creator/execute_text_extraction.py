from src.corpus_creator.text_extraction import file_text_extractor
from src.corpus_creator.tools import dataframe_tools
import json
import time


def execute_text_extraction():
    """
       Pipeline to extract the raw text from the pdf files:
           pdf -> raw
    """
    config_text_extraction = json.load(open("../../config/text_extraction_config.json", "r", encoding="utf-8"))
    config_corpus_creation = json.load(open("../../config/corpus_creation_config.json", "r", encoding="utf-8"))
    project_path = config_corpus_creation["base_path"]
    output_path_for_extracted_text = config_text_extraction["output_path_for_extracted_text"]
    lectura_facil_path = config_text_extraction["lectura_facil_path"]
    lenguaje_natural_path = config_text_extraction["lenguaje_natural_path"]
    lectura_facil_file_name = config_text_extraction["lectura_facil_file_name"]
    lenguaje_natural_file_name = config_text_extraction["lenguaje_natural_file_name"]
    parallelize_flag = config_text_extraction["parallelize_flag"]

    # Build the complete paths for both data sources
    full_lectura_facil_path = project_path + lectura_facil_path
    full_lenguaje_natural_path = project_path + lenguaje_natural_path

    print("Extracting text from raw files...")

    start_time = time.time()

    # First extract the text from all the pdfs in the subdirs
    lectura_facil_raw_text_df = file_text_extractor.extract_text_from_pdfs_in_subdirs_to_df(full_lectura_facil_path,
                                                                                            parallelize_flag)

    # Then extract the text from the 'lenguaje natural' source (a .txt file)
    lenguaje_natural_raw_text_df = file_text_extractor.lenguaje_natural_text_extractor(full_lenguaje_natural_path)

    # Tag the dataframes
    lectura_facil_raw_text_df = file_text_extractor.tag_data(lectura_facil_raw_text_df, 0)
    lenguaje_natural_raw_text_df = file_text_extractor.tag_data(lenguaje_natural_raw_text_df, 1)

    # Lastly save the extracted text into csv file
    dataframe_tools.write_dataframe(lectura_facil_raw_text_df, project_path + output_path_for_extracted_text, lectura_facil_file_name)
    dataframe_tools.write_dataframe(lenguaje_natural_raw_text_df, project_path + output_path_for_extracted_text, lenguaje_natural_file_name)

    finish_time = time.time()

    total_time = finish_time - start_time

    print(f"Complete!: {total_time}")


if __name__ == '__main__':
    execute_text_extraction()
