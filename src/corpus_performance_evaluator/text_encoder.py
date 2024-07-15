import gensim
import pandas as pd
import numpy as np
from pandas import Series


def encode_text(text: str, embedding_model) -> Series:
    """
    Function that encoded a string using a pretrained embedding passed as input
    :param text: Text to be encoded
    :param embedding_model: Pretained embedding
    :return: List of encoded words
    """
    out_of_vocabulary_words = []
    encoded_text = []
    for w in text:
        try:
            embedded_word = embedding_model[w]
            encoded_text.append(embedded_word)
        except KeyError:
            out_of_vocabulary_words.append(w)
            pass

    with open("../../data/OOV.txt", "a", encoding="utf-8") as file:
        for w in out_of_vocabulary_words:
            file.write(w + "\n")

    return pd.Series(np.mean(encoded_text, axis=0))


def apply_embedding(text_df: pd.DataFrame, model_path: str) -> pd.DataFrame:
    """
    Adhoc function for encoding text column from DataFrame using pretrained embedding
    :param text_df: DataFrame that contains the text ready to be encoded
    :param model_path: Path that contains the pretrained embedding in binary format
    :return: A Pandas DataFrame which contains the encoded text
    """
    embedding_model = gensim.models.keyedvectors.KeyedVectors.load_word2vec_format(model_path, binary=True)
    new_text_df = text_df['stemmed_text'].apply(encode_text, args=(embedding_model,))
    new_text_df["class"] = text_df["class"]
    return new_text_df


if __name__ == '__main__':
    base_path = ("C:/Users/ferna/Universidad Politécnica de Madrid/Linea Accesibilidad Cognitiva (Proyecto)-Corpus "
                 "Lectura Fácil (2023) - Documentos/data/corpus_performance_evaluator/")
    final_corpus_path = base_path + "preprocessing/preprocessed_text.csv"
    df = pd.read_csv(final_corpus_path, sep="|", encoding="utf-8")
    df = apply_embedding(df, model_path='C:/Users/ferna/PycharmProjects/corpus-lectura-facil/data/sbw_vectors.bin')
    df.to_csv(base_path + "encoding/encoded_text.csv", sep="|", encoding="utf-8", index=False)
