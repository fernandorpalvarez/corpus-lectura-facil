import json
import re
from src.corpus_creator.interfaces.DataCleaningInterface import DataCleaningInterface


class DataCleaningPipeline(DataCleaningInterface):
    def __init__(self, df):
        self.df = df
        self.config = json.load(open("../../../config/data_cleaning_config.json", "r", encoding="utf-8"))

    def apply_cleaning_pipeline(self):
        print("Cleaning text from raw path...")

        # Get the config from json file
        min_len_for_line = self.config["min_len_for_line"]
        max_len_for_line = self.config["max_len_for_line"]
        min_dig_number = self.config["min_dig_number"]

        # Apply pipeline over the data
        self.apply_multiple_dots_substitution()
        self.apply_special_char_removal()
        self.apply_tokenization()
        self.apply_special_line_removal(min_dig_number=min_dig_number)
        self.remove_rows_based_on_length(min_l=min_len_for_line, max_l=max_len_for_line)
        self.apply_add_space_between_words()

        self.df.drop_duplicates(inplace=True)

        print("Complete!")

        return self.df

    # Special characters removal
    def apply_special_char_removal(self):
        # Pattern for replacing "…" character with three dots
        self.df['text'] = self.df['text'].apply(lambda x: str(x).replace("…", "..."))

        # Pattern that matches strings starting with numbers, numbers followed by ª or only ª or »
        pattern_multiline = r'^\d+ª|^\d+\s*|^ª|»'
        self.df['text'] = self.df['text'].apply(lambda x: re.sub(pattern_multiline, " ", str(x), 0, re.MULTILINE))

        # Patterns for unnicode matches
        patterns_ignorecase = [r'[^a-zA-Z0-9\s¿?¡!,.;:\u0080-\u024F]', r'\x83', r'\x92', r'\s+']
        for pattern in patterns_ignorecase:
            self.df['text'] = self.df['text'].apply(lambda x: re.sub(pattern, " ", str(x), 0, re.IGNORECASE))

    def apply_tokenization(self):
        """
        Apply tokenization based on pattern
        """
        pattern = r'\.\s+|\.\n+|\n'
        text_series = self.df['text'].str.split(pattern)
        self.df = self.df.assign(text=text_series).explode('text')
        self.df['text'] = self.df['text'].apply(lambda x: str(x).rstrip() + ".")
        self.df.reset_index(drop=True, inplace=True)

    def apply_special_line_removal(self, min_dig_number=3):
        """
        Function that removes the lines that contain more than n numerical digits
        :param min_dig_number: Minimum number of numerical digits that a row must contain to be filtered
        :return: Filtered DataFrame
        """
        # Create a boolean mask based on digit len
        mask = self.df['text'].str.count(r'\d') > min_dig_number

        # Filter DataFrame in order to keep only the rows that match the mask
        self.df = self.df[~mask]

        self.df = self.df[~self.df['text'].str.contains('©')]
        self.df = self.df[~self.df['text'].str.contains('www')]

    def remove_rows_based_on_length(self, min_l=None, max_l=None):
        if min_l:
            self.df = self.df[self.df['text'].map(len) > min_l]
        if max_l:
            self.df = self.df[self.df['text'].map(len) < max_l]

    def apply_add_space_between_words(self):
        # Use a regular expression to add a space after all minor-case characters followed by an uppercase characters
        self.df['text'] = self.df['text'].apply(lambda x: re.sub(r'([a-z])([A-Z])', r"\1 \2", str(x)))

    def apply_multiple_dots_substitution(self):
        # Use a regular expression to replace strings of more than 3 dots in a row with just one dot
        self.df['text'] = self.df['text'].apply(lambda x: re.sub(r'\.{4,}', r".", str(x)))
