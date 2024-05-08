import json

from src.corpus_performance_evaluator.text_preprocessing import *
from src.corpus_performance_evaluator.text_encoder import *
from src.corpus_performance_evaluator.evaluation import CustomMetrics
from src.corpus_performance_evaluator.classification_model import ClassificationModel
from sklearn.ensemble import RandomForestClassifier


def execute_corpus_performance_evaluation():
    """
    This function works as a wrapper to execute only the steps in the corpus performance evaluation pipeline that the
    user previously specified in the config
    """
    config = json.load(open("../../config/corpus_performance_evaluator_config.json", "r", encoding="utf-8"))
    base_path = config["base_path"]
    ex_preprocess_flag = config["ex_preprocess_flag"]
    ex_encoder_flag = config["ex_encoder_flag"]
    ex_train_classifier_flag = config["ex_train_classifier_flag"]
    ex_compute_model_metrics_flag = config["ex_compute_model_metrics_flag"]
    rf_obj = None
    classification_model_class = RandomForestClassifier
    
    # Preprocess text
    if ex_preprocess_flag:
        final_corpus_path = base_path + "extracted_text_pipeline/transformed/final_corpus.csv"
        final_corpus_df = pd.read_csv(final_corpus_path, sep="|", encoding="utf-8")
        pipeline_obj = CorpusTrainingCleaningPipeline()
        clean_corpus_df = pipeline_obj.apply_cleaning_pipeline(final_corpus_df)
        clean_corpus_df.to_csv(base_path + "corpus_performance_evaluator/preprocessing/preprocessed_text.csv", sep="|",
                               encoding="utf-8", index=False)

    # Text encoder
    if ex_encoder_flag:
        final_corpus_path = base_path + "corpus_performance_evaluator/preprocessing/preprocessed_text.csv"
        df = pd.read_csv(final_corpus_path, sep="|", encoding="utf-8")
        df = apply_embedding(df, model_path='C:/Users/ferna/PycharmProjects/corpus-lectura-facil/data/sbw_vectors.bin')
        df.to_csv(base_path + "corpus_performance_evaluator/encoding/encoded_text.csv", sep="|", encoding="utf-8",
                  index=False)

    # Train model
    if ex_train_classifier_flag:
        rf_obj = ClassificationModel(classification_model_class, base_path + "corpus_performance_evaluator/")
        rf_obj.load_split_data()
        rf_obj.train_model()
        rf_obj.save_model()

    # Model metrics
    if ex_compute_model_metrics_flag:
        if not rf_obj:
            rf_obj = ClassificationModel(classification_model_class, base_path + "corpus_performance_evaluator/")

        rf_obj.load_model()
        rf_obj.load_split_data()
        predicted = rf_obj.predict(rf_obj.X_test)

        cm_obj = CustomMetrics(rf_obj.y_test["class"].array, predicted)
        cm_obj.calculate_metrics_report(path=(base_path + "classification_model/metrics.csv"), save=False)
