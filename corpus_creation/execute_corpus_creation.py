from lectura_facil_pipeline import *


if __name__ == '__main__':
    # Get the text
    corpus_lectura_facil_df = load_text_in_lectura_facil_from_path("C:/Users/ferna/Universidad Politécnica de Madrid/Linea Accesibilidad Cognitiva (Proyecto)-Corpus Lectura Fácil (2023) - Documentos/data/extracted_text_from_pdfs")
    # Preprocess it
    corpus_lectura_facil_df = apply_pipeline(corpus_lectura_facil_df[:10])
    # Save it
    save_dataframe_in_path(corpus_lectura_facil_df, "C:/Users/ferna/Universidad Politécnica de Madrid/Linea Accesibilidad Cognitiva (Proyecto)-Corpus Lectura Fácil (2023) - Documentos/data/corpus_lectura_facil/")