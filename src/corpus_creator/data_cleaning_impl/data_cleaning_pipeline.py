import re

import numpy as np
import pandas as pd

from src.corpus_creator.interfaces.DataCleaningInterface import DataCleaningInterface


class DataCleaningPipeline(DataCleaningInterface):
    def __init__(self, min_len_for_line, max_len_for_line, min_dig_number):
        self.min_len_for_line = min_len_for_line
        self.max_len_for_line = max_len_for_line
        self.min_dig_number = min_dig_number

    def apply_cleaning_pipeline(self, df: pd.DataFrame):
        df.dropna(subset=["text"], inplace=True)

        # Apply pipeline over the data
        df = self.apply_multiple_dots_substitution(df)
        df = self.apply_special_char_removal(df)
        df = self.apply_tokenization(df)
        df = self.apply_special_line_removal(df, min_dig_number=self.min_dig_number)
        df = self.remove_rows_based_on_length(df, min_l=self.min_len_for_line, max_l=self.max_len_for_line)
        df = self.apply_add_space_between_words(df)
        df["text"] = df["text"] + "."

        df.drop_duplicates(inplace=True)

        return df

    @staticmethod
    def apply_special_char_removal(df):
        # Special characters removal
        # Pattern for replacing "…" character with three dots
        df['text'] = df['text'].apply(lambda x: str(x).replace("…", "..."))

        # Pattern that matches strings starting with numbers, numbers followed by ª or only ª or »
        pattern_multiline = r'^\d+ª|^\d+\s*|^ª|»'
        df['text'] = df['text'].apply(lambda x: re.sub(pattern_multiline, " ", str(x), 0, re.MULTILINE))

        # Patterns for unnicode matches
        patterns_ignorecase = [r'[^a-zA-Z0-9\s¿?¡!,.;:\u0080-\u024F]', r'\x83', r'\x92', r'\s+']
        for pattern in patterns_ignorecase:
            df['text'] = df['text'].apply(lambda x: re.sub(pattern, " ", str(x), 0, re.IGNORECASE))

        return df

    @staticmethod
    def apply_tokenization(df):
        """
        Apply tokenization based on pattern
        """
        pattern = r'.'
        text_series = df['text'].str.split(pattern)
        df.drop(columns=['text'], inplace=True)
        df = df.assign(text=text_series).explode('text')[['text', 'class']]
        df['text'].replace('', np.nan, inplace=True)
        df.dropna(subset=['text'], inplace=True)
        df['text'] = df['text'].apply(lambda x: str(x).rstrip())
        df.reset_index(drop=True, inplace=True)

        return df

    @staticmethod
    def apply_special_line_removal(df, min_dig_number=3):
        """
        Function that removes the lines that contain more than n numerical digits
        :param df: DataFrame over which apply the line removal
        :param min_dig_number: Minimum number of numerical digits that a row must contain to be filtered
        :return: Filtered DataFrame
        """
        # Create a boolean mask based on digit len
        mask = df['text'].str.count(r'\d') > min_dig_number

        # Filter DataFrame in order to keep only the rows that match the mask
        df = df[~mask]
        df = df[~df['text'].str.contains('[^a-zA-Z \náéíóúÁÉÍÓÚ]')]

        return df

    @staticmethod
    def remove_rows_based_on_length(df, min_l=None, max_l=None):
        # Remove lines in df if are more than a max or less than a min
        if min_l:
            df = df[df['text'].map(len) > min_l]
        if max_l:
            df = df[df['text'].map(len) < max_l]

        return df

    @staticmethod
    def apply_add_space_between_words(df):
        # Use a regular expression to add a space after all minor-case characters followed by an uppercase characters
        df['text'] = df['text'].apply(lambda x: re.sub(r'([a-z])([A-Z])', r"\1 \2", str(x)))

        return df

    @staticmethod
    def apply_multiple_dots_substitution(df):
        # Use a regular expression to replace strings of more than 3 dots in a row with just one dot
        df['text'] = df['text'].apply(lambda x: re.sub(r'\.{4,}', r".", str(x)))

        return df
