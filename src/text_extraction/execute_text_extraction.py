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
    rename_files_flag = config["text_extraction"]["rename_files_flag"]
    extract_text_flag = config["text_extraction"]["extract_text_flag"]

    if rename_files_flag:
        pdf_tool_manager.rename_files_in_path(pdfs_path)

    if extract_text_flag:
        pdf_text_extractor.save_text_from_pdfs_in_subdirs_to_csv(pdfs_path, output_path_for_extracted_text)
