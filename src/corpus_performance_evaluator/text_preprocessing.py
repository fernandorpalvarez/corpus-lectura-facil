import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from src.corpus_creator.interfaces.DataCleaningInterface import DataCleaningInterface


class CorpusTrainingCleaningPipeline(DataCleaningInterface):
    def __init__(self):
        pass

    def apply_cleaning_pipeline(self, df: pd.DataFrame):
        """
        Function for applying different preprocessing steps to an input dataframe
        :param df: Pandas DataFrame which contains raw text
        :return: Pandas DataFrame with cleaned text
        """
        df.dropna(subset=["text"], inplace=True)

        # Apply pipeline over the data
        df = self.apply_lowercase(df)
        df = self.apply_remove_non_word_characters(df)
        df = self.apply_remove_numeric_characters(df)
        df = self.apply_tokenization(df)
        df = self.apply_stop_word_removal(df)
        df = self.apply_stem_words(df)

        return df

    @staticmethod
    def apply_lowercase(df: pd.DataFrame):
        """
        Lowercase text column in df
        :param df: Pandas DataFrame that contains text to lowercase
        :return: Pandas DataFrame with lowercase text
        """
        return df.applymap(lambda x: x.lower() if isinstance(x, str) else x)

    @staticmethod
    def apply_remove_non_word_characters(df: pd.DataFrame):
        """
        Remove non word characters from df
        :param df: Pandas DataFrame
        :return: Pandas DataFrame with non word characters
        """
        return df.replace(to_replace=r'[^\w\s]', value='', regex=True)

    @staticmethod
    def apply_remove_numeric_characters(df: pd.DataFrame):
        """
        Remove numeric characters
        :param df: Pandas DataFrame
        :return: Pandas DataFrame with no numbers
        """
        return df.replace(to_replace=r'\d', value='', regex=True)

    @staticmethod
    def apply_tokenization(df: pd.DataFrame):
        """
        Tokenize text
        :param df: Pandas DataFrame
        :return: Pandas DataFrame with tokenized text
        """
        df['text'] = df['text'].apply(word_tokenize)
        return df

    @staticmethod
    def apply_stop_word_removal(df: pd.DataFrame):
        """
        Remove stop words from text
        :param df: Pandas DataFrame
        :return: Pandas DataFrame with no stop words
        """
        stop_words = set(stopwords.words('spanish'))
        df['text'] = df['text'].apply(lambda x: [word for word in x if word not in stop_words])
        return df

    @staticmethod
    def apply_stem_words(df: pd.DataFrame):
        """
        Stem words from Pandas DataFrame
        :param df: Pandas DataFrame
        :return: Pandas DataFrame with stemmed words
        """
        # Initialize the Porter Stemmer
        stemmer = SnowballStemmer('spanish')

        # Define a function to perform stemming on the 'text' column
        def stem_words(words):
            return [stemmer.stem(word) for word in words]

        # Apply the function to the 'text' column and create a new column 'stemmed_text'
        df['stemmed_text'] = df['text'].apply(stem_words)
        return df


if __name__ == '__main__':
    base_path = ("C:/Users/ferna/Universidad Politécnica de Madrid/Linea Accesibilidad Cognitiva (Proyecto)-Corpus "
                 "Lectura Fácil (2023) - Documentos/data/")
    final_corpus_path = base_path + "extracted_text_pipeline/transformed/final_corpus.csv"
    final_corpus_df = pd.read_csv(final_corpus_path, sep="|", encoding="utf-8")
    pipeline_obj = CorpusTrainingCleaningPipeline()
    clean_corpus_df = pipeline_obj.apply_cleaning_pipeline(final_corpus_df)
    clean_corpus_df.to_csv(base_path + "corpus_performance_evaluator/preprocessing/preprocessed_text.csv", sep="|",
                           encoding="utf-8", index=False)
