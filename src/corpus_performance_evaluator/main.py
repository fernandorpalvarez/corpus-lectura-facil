from src.corpus_performance_evaluator.text_preprocessing import *
from src.corpus_performance_evaluator.text_encoder import *


if __name__ == '__main__':
    base_path = ("C:/Users/ferna/Universidad Politécnica de Madrid/Linea Accesibilidad Cognitiva (Proyecto)-Corpus "
                 "Lectura Fácil (2023) - Documentos/data/")
    final_corpus_path = base_path + "extracted_text_pipeline/transformed/final_corpus.csv"
    final_corpus_df = pd.read_csv(final_corpus_path, sep="|", encoding="utf-8")
    pipeline_obj = CorpusTrainingCleaningPipeline()
    clean_corpus_df = pipeline_obj.apply_cleaning_pipeline(final_corpus_df)
    clean_corpus_df.to_csv(base_path + "corpus_performance_evaluator/preprocessing/preprocessed_text.csv", sep="|",
                           encoding="utf-8", index=False)
