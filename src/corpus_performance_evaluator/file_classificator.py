import pickle
import pandas as pd
import warnings

from src.corpus_creator.text_extraction.file_text_extractor import extract_text_from_pdf
from src.corpus_creator.data_cleaning_impl.data_cleaning_pipeline import DataCleaningPipeline
from src.corpus_performance_evaluator.text_preprocessing import CorpusTrainingCleaningPipeline
from src.corpus_performance_evaluator.text_encoder import apply_embedding

warnings.filterwarnings('ignore')


def calculate_file_classification(model_path, file_path):
    """
    Function that loads a binary classification model contained in model_path, extract the text contained in the file
    that is in the file path and calculates a % that represents the proportion of the file that is written in easy read
    methodology, according to the model.
    :param model_path: Path that contains a pretrained model, trained with the module corpus_performance_evaluator.classification_model.py
    :param file_path: Path that contains the file to be classified
    :return: Float value that represents the proportion of the file that is written in easy lecture methodology
    """
    # Load model and text
    model_obj = pickle.load(open(model_path, 'rb'))
    text = extract_text_from_pdf(file_path, n_pages=0)
    text_df = pd.DataFrame(data=[[text, "", ""]], columns=["text", "class", "source"])

    # Clean the text
    pipeline_obj = DataCleaningPipeline()
    clean_text_df = pipeline_obj.apply_cleaning_pipeline(text_df)
    training_pipeline_obj = CorpusTrainingCleaningPipeline()
    clean_text_df = training_pipeline_obj.apply_cleaning_pipeline(clean_text_df)

    # Encode the text
    encoded_text_df = apply_embedding(clean_text_df,
                                      model_path='../../data/sbw_vectors.bin')
    encoded_text_df.drop(columns=["class"], inplace=True)

    # Classify text
    classifications = pd.DataFrame(columns=["class", "percentage"])
    for row in encoded_text_df.values:
        predicted_class = pd.DataFrame(data=[[model_obj.predict([row])[0], max(model_obj.predict_proba([row])[0])]],
                                       columns=["class", "percentage"])
        classifications = pd.concat([classifications, predicted_class])

    n_total = len(classifications)
    n_0 = classifications["class"].value_counts().loc[0]
    n_1 = classifications["class"].value_counts().loc[1]

    if max(n_0, n_1) > 0.6 * n_total:
        if n_0 > n_1:
            percentage = classifications[classifications["class"] == 0]["percentage"].mean()
            print(f"Predicted class: 'Lectura Fácil'")
            print(f"Percentage of accuracy: {percentage}")
        else:
            percentage = classifications[classifications["class"] == 1]["percentage"].mean()
            print(f"Predicted class: 'Lenguaje natural'")
            print(f"Percentage of accuracy: {percentage}")
    else:
        print("Model cannot give reliable classification, percentage of classification < 60% for both classes")
        percentage_0 = classifications[classifications["class"] == 0]["percentage"].mean()
        percentage_1 = classifications[classifications["class"] == 1]["percentage"].mean()
        print(f"Percentage of accuracy for 'Lectura Fácil' class: {percentage_0}")
        print(f"Percentage of accuracy for 'Lenguaje natural' class: {percentage_1}")


if __name__ == '__main__':
    m_path = "C:/Users/ferna/Universidad Politécnica de Madrid/Linea Accesibilidad Cognitiva (Proyecto)-Corpus Lectura Fácil (2023) - Documentos/data/corpus_performance_evaluator/classification_model/V3/random_forest.pkl"
    text_path = "C:/Users/ferna/Universidad Politécnica de Madrid/Linea Accesibilidad Cognitiva (Proyecto)-Corpus Lectura Fácil (2023) - Documentos/data/files_lectura_facil/plena_inclusion/9.0.pdf"
    calculate_file_classification(m_path, text_path)
