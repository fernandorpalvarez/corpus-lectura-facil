import pdf_text_extractor as pdf_te
import pdf_tool_manager


if __name__ == '__main__':
    pdfs_path = "C:/Users/ferna/Universidad Politécnica de Madrid/Linea Accesibilidad Cognitiva (Proyecto)-Corpus Lectura Fácil (2023) - Documentos/data/pdfs_from_web/plena_inclusion_extremadura"
    output_path_for_extracted_text = "C:/Users/ferna/Universidad Politécnica de Madrid/Linea Accesibilidad Cognitiva (Proyecto)-Corpus Lectura Fácil (2023) - Documentos/data/extracted_text_from_pdfs"

    pdf_tool_manager.rename_files_in_path(pdfs_path)
    # pdf_te.extract_text_from_pdfs_in_path(pdfs_path, output_path_for_extracted_text)
