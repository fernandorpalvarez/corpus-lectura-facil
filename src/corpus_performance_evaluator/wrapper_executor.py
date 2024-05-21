import json

from src.corpus_performance_evaluator.text_preprocessing import *
from src.corpus_performance_evaluator.text_encoder import *
from src.corpus_performance_evaluator.evaluation import CustomMetrics
from src.corpus_performance_evaluator.classification_model import ClassificationModel
from src.corpus_creator.tools.dataframe_tools import read_dataframe, write_dataframe
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC


def execute_corpus_performance_evaluation():
    """
    This function works as a wrapper to execute only the steps in the corpus performance evaluation pipeline that the
    user previously specified in the config
    """
    config = json.load(open("../../config/corpus_performance_evaluator_config.json", "r", encoding="utf-8"))
    base_path = config["base_path"]
    input_corpus_name = config["input_corpus_name"]
    ex_preprocess_flag = config["ex_preprocess_flag"]
    ex_encoder_flag = config["ex_encoder_flag"]
    ex_train_classifier_flag = config["ex_train_classifier_flag"]
    ex_compute_model_metrics_flag = config["ex_compute_model_metrics_flag"]
    model_name = config["classification_model"]["model_name"]
    algorithm = config["classification_model"]["algorithm"]
    model_obj = None
    if algorithm == "rf":
        classification_model_class = RandomForestClassifier
    elif algorithm == "lr":
        classification_model_class = LogisticRegression
    elif algorithm == "svc":
        classification_model_class = SVC
    elif algorithm == "nb":
        classification_model_class = GaussianNB
    
    # Preprocess text
    if ex_preprocess_flag:
        final_corpus_path = base_path + "extracted_text_pipeline/transformed/"
        final_corpus_df = read_dataframe(final_corpus_path, input_corpus_name)
        pipeline_obj = CorpusTrainingCleaningPipeline()
        clean_corpus_df = pipeline_obj.apply_cleaning_pipeline(final_corpus_df)
        write_dataframe(clean_corpus_df,
                        base_path + "corpus_performance_evaluator/preprocessing/",
                        "preprocessed_text.csv")

    # Text encoder
    if ex_encoder_flag:
        preprocessed_text_path = base_path + "corpus_performance_evaluator/preprocessing/"
        encoded_text_df = read_dataframe(preprocessed_text_path, "preprocessed_text.csv")
        encoded_text_df = apply_embedding(encoded_text_df,
                                          model_path='C:/Users/ferna/PycharmProjects/corpus-lectura-facil/data/'
                                                     'sbw_vectors.bin')
        write_dataframe(encoded_text_df,
                        base_path + "corpus_performance_evaluator/encoding/",
                        "encoded_text.csv")

    models = {
        0: {
            "model": RandomForestClassifier,
            "alg": "rf",
            "model_name": "random_forest.pkl"
        },
        1: {
            "model": LogisticRegression,
            "alg": "lr",
            "model_name": "logistic_regression.pkl"
        },
        2: {
            "model": GaussianNB,
            "alg": "nb",
            "model_name": "naive_bayes.pkl"
        },
        3: {
            "model": SVC,
            "alg": "svc",
            "model_name": "support_vector_machine.pkl"
        }
    }
    for model in models.items():
        classification_model_class = model[1]["model"]
        algorithm = model[1]["alg"]
        model_name = model[1]["model_name"]
        # Train model
        if ex_train_classifier_flag:
            model_obj = ClassificationModel(classification_model_class, base_path + "corpus_performance_evaluator/")

            # model_obj.save_split_data()
            model_obj.load_split_data()
            model_obj.train_model()
            model_obj.save_model(model_name=model_name)

        # Model metrics
        if ex_compute_model_metrics_flag:
            if not model_obj:
                model_obj = ClassificationModel(classification_model_class, base_path + "corpus_performance_evaluator/")

            model_obj.load_model(model_name=model_name)
            model_obj.load_split_data()
            predicted = model_obj.predict(model_obj.X_test)

            cm_obj = CustomMetrics(model_obj.y_test["class"].array, predicted)
            cm_obj.calculate_metrics_report(path=(base_path + "corpus_performance_evaluator/classification_model/"
                                                              f"metrics_{algorithm}.csv"), save=True)
