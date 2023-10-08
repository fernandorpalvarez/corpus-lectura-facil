import pdf_text_extractor
import pdf_tool_manager
import json


if __name__ == '__main__':
    '''
       Pipeline to extract the raw text from the pdf files:
           pdf -> raw
    '''
    config = json.load(open("../../config/text_extraction_config.json", "r", encoding="utf-8"))
    pdfs_path = config["text_extraction"]["pdfs_path"]
    output_path_for_extracted_text = config["text_extraction"]["output_path_for_extracted_text"]
    file_name = config["text_extraction"]["file_name"]
    separator = config["text_extraction"]["separator"]
    rename_files_flag = config["text_extraction"]["rename_files_flag"]

    if rename_files_flag:
        pdf_tool_manager.rename_files_in_path(pdfs_path)

    # First extract the text from all the pdfs in the subdirs
    full_text_df = pdf_text_extractor.extract_text_from_pdfs_in_subdirs_to_df(pdfs_path)
    # Lastly save the extracted text into csv file
    pdf_text_extractor.save_dataframe_in_path(full_text_df, output_path_for_extracted_text, file_name, separator)
