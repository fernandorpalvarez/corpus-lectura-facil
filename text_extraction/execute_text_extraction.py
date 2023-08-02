import pdf_text_extractor as pdf_te
import pdf_tool_manager


if __name__ == '__main__':
    pdfs_path = "C:/Users/ferna/Universidad Politécnica de Madrid/Linea Accesibilidad Cognitiva (Proyecto)-Corpus Lectura Fácil (2023) - Documentos/files_in_lectura_facil/asociacion_lectura_facil"
    output_path_for_extracted_text = "C:/Users/ferna/Universidad Politécnica de Madrid/Linea Accesibilidad Cognitiva (Proyecto)-Corpus Lectura Fácil (2023) - Documentos/files_in_lectura_facil/extracted_text_from_pdfs"

    pdf_tool_manager.rename_files_in_path(pdfs_path)
    # pdf_te.extract_text_from_pdfs_in_path(pdfs_path, output_path_for_extracted_text)
