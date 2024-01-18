from src.corpus_creator.text_extraction import pdf_text_extractor
import json
from src.corpus_creator.tools import dataframe_tools

if __name__ == '__main__':
    '''
       Pipeline to extract the raw text from the pdf files:
           pdf -> raw
    '''
    config = json.load(open("../../config/text_extraction_config.json", "r", encoding="utf-8"))
    pdfs_path = config["pdfs_path"]
    output_path_for_extracted_text = config["output_path_for_extracted_text"]
    file_name = config["file_name"]
    rename_files_flag = config["rename_files_flag"]

    if rename_files_flag:
        pdf_text_extractor.rename_files_in_path(pdfs_path)

    # First extract the text from all the pdfs in the subdirs
    full_text_df = pdf_text_extractor.extract_text_from_pdfs_in_subdirs_to_df(pdfs_path)
    # Lastly save the extracted text into csv file
    dataframe_tools.write_dataframe(full_text_df, output_path_for_extracted_text, file_name)
