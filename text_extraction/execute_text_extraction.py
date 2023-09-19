import pdf_text_extractor
import pdf_tool_manager
import json


if __name__ == '__main__':
    config = json.load(open("../config/data_pipeline_config.json", "r", encoding="utf-8"))
    pdfs_path = config["text_extraction"]["pdfs_path"]
    output_path_for_extracted_text = config["text_extraction"]["output_path_for_extracted_text"]
    rename_files_flag = config["text_extraction"]["rename_files_flag"]
    extract_text_flag = config["text_extraction"]["extract_text_flag"]

    if rename_files_flag:
        pdf_tool_manager.rename_files_in_path(pdfs_path)

    if extract_text_flag:
        pdf_text_extractor.extract_text_from_pdfs_in_subdirs_path(pdfs_path, output_path_for_extracted_text)
