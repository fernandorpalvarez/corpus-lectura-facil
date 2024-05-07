from src.corpus_performance_evaluator.text_preprocessing import *
from src.corpus_performance_evaluator.text_encoder import *
from src.corpus_performance_evaluator.evaluation import CustomMetrics
from src.corpus_performance_evaluator.classification_model import ClassificationModel
from sklearn.ensemble import RandomForestClassifier


if __name__ == '__main__':
    # Preprocess text
    base_path = ("C:/Users/ferna/Universidad Politécnica de Madrid/Linea Accesibilidad Cognitiva (Proyecto)-Corpus "
                 "Lectura Fácil (2023) - Documentos/data/")
    final_corpus_path = base_path + "extracted_text_pipeline/transformed/final_corpus.csv"
    final_corpus_df = pd.read_csv(final_corpus_path, sep="|", encoding="utf-8")
    pipeline_obj = CorpusTrainingCleaningPipeline()
    clean_corpus_df = pipeline_obj.apply_cleaning_pipeline(final_corpus_df)
    clean_corpus_df.to_csv(base_path + "corpus_performance_evaluator/preprocessing/preprocessed_text.csv", sep="|",
                           encoding="utf-8", index=False)

    # Text encoder
    base_path = ("C:/Users/ferna/Universidad Politécnica de Madrid/Linea Accesibilidad Cognitiva (Proyecto)-Corpus "
                 "Lectura Fácil (2023) - Documentos/data/corpus_performance_evaluator/")
    final_corpus_path = base_path + "preprocessing/preprocessed_text.csv"
    df = pd.read_csv(final_corpus_path, sep="|", encoding="utf-8")
    df = apply_embedding(df, model_path='C:/Users/ferna/PycharmProjects/corpus-lectura-facil/data/sbw_vectors.bin')
    df.to_csv(base_path + "encoding/encoded_text.csv", sep="|", encoding="utf-8", index=False)

    # Train model
    path = ("C:/Users/ferna/Universidad Politécnica de Madrid/Linea Accesibilidad Cognitiva (Proyecto)-Corpus "
            "Lectura Fácil (2023) - Documentos/data/corpus_performance_evaluator/")
    RF_obj = ClassificationModel(RandomForestClassifier, path)

    RF_obj.save_split_data()
    RF_obj.train_model()
    RF_obj.save_model()

    # Model metrics
    actual = None
    predicted = None
    custom_metrics_obj = CustomMetrics(actual, predicted)
