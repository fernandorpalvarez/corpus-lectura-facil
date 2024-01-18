import pandas as pd


class DataCleaningInterface:
    def apply_cleaning_pipeline(self) -> pd.DataFrame:
        """
        Core function of the interface. The idea is that the user can create different implementations of this pipeline
        adding or removing the steps that the user wants and on the order that the user wants.
        Key point -> This class aims to create a clean corpus, with understandable phrases, not the input for a NLP
        model, so there is no need to add encoders or steps to THIS pipeline that can reduce the raw useful info
        contained by the text.
        :return: A pd.DataFrame with the cleaned text
        """
        pass
