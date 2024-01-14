import json
import os
import re
import pandas as pd
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import stanza
from tqdm import tqdm


# nltk.download('stopwords')
# nltk.download('punkt')
# stanza.download("es")


def load_text_from_csv(path, separator="|"):
    return pd.read_csv(path, sep=separator, encoding="utf-8")


def apply_cleaning_pipeline(df):
    print("Cleaning text from raw path...")

    # Get the config from json file
    config = json.load(open("../../config/data_cleaning_config.json", "r", encoding="utf-8"))
    min_len_for_line = config["min_len_for_line"]
    max_len_for_line = config["max_len_for_line"]
    min_dig_number = config["min_dig_number"]

    # Apply pipeline over the data
    df = apply_multiple_dots_substitution(df)
    df = apply_special_char_removal(df)
    df = apply_tokenization(df)
    df = apply_special_line_removal(df, min_dig_number=min_dig_number)
    df = remove_rows_based_on_length(df, min_l=min_len_for_line, max_l=max_len_for_line)
    df = apply_add_space_between_words(df)

    df.drop_duplicates(inplace=True)

    print("Complete!")

    return df


# Special characters removal
def apply_special_char_removal(df):
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


def apply_tokenization(df):
    """
    Apply tokenization based on pattern
    :param df: DaraFrame to be tokenized
    :return: Tokenized DataFrame
    """
    pattern = r'\.\s+|\.\n+|\n'
    text_series = df['text'].str.split(pattern)
    df = df.assign(text=text_series).explode('text')
    df['text'] = df['text'].apply(lambda x: str(x).rstrip() + ".")

    return df.reset_index(drop=True)


def apply_special_line_removal(df, min_dig_number=3):
    """
    Function that removes the lines that contain more than n numerical digits
    :param df: DataFrame to be filtered.
    :param min_dig_number: Minimum number of numerical digits that a row must contain to be filtered
    :return: Filtered DataFrame
    """
    # Create a boolean mask based on digit len
    mask = df['text'].str.count(r'\d') > min_dig_number

    # Filter DataFrame in order to keep only the rows that match the mask
    df = df[~mask]

    df = df[~df['text'].str.contains('©')]
    df = df[~df['text'].str.contains('www')]

    return df


def remove_rows_based_on_length(df, min_l=None, max_l=None):
    if min_l:
        df = df[df['text'].map(len) > min_l]
    if max_l:
        df = df[df['text'].map(len) < max_l]
    return df


def apply_add_space_between_words(df):
    # Use a regular expression to add a space after all minorcase characters followed by an uppercase characters
    df['text'] = df['text'].apply(lambda x: re.sub(r'([a-z])([A-Z])', r"\1 \2", str(x)))

    return df


def apply_multiple_dots_substitution(df):
    # Use a regular expression to replace strings of more than 3 dots in a row with just one dot
    df['text'] = df['text'].apply(lambda x: re.sub(r'\.{4,}', r".", str(x)))

    return df

"""
    Functions for ML model data cleaning
"""


# Minor case conversion
def apply_minor_casing(df):
    df['text'] = df['text'].str.lower()
    return df


# Stopwords removal
def apply_stop_words_removal(df):
    stop_words_sp = set(stopwords.words('spanish'))

    def filter_stop_words(txt, stop_words):
        word_tokens = word_tokenize(txt)
        # converts the words in word_tokens to check whether
        # they are present in stop_words or not
        filtered_sentence = [w for w in word_tokens if not w in stop_words]
        return ' '.join(filtered_sentence)

    df['text'] = df['text'].apply(lambda x: filter_stop_words(str(x), stop_words_sp))

    return df


# Lemmatizing
def apply_lemmatizing(df):
    def lemmatization_for_row(row, nlp):
        lemmas = [word.lemma for sent in nlp(str(row)).sentences for word in sent.words]
        return " ".join(lemmas)

    tqdm.pandas()
    stanza_nlp = stanza.Pipeline(lang='es', processors='tokenize,mwt,pos,lemma')
    df['text'] = df['text'].progress_apply(lambda x: lemmatization_for_row(x, stanza_nlp))
    return df


# Numeric characters removal
def apply_numeric_char_removal(df):
    df['text'] = df['text'].apply(lambda x: re.sub(r'[0-9]+', " ", str(x), 0, re.IGNORECASE))
    return df


# HTML tags removal
def apply_html_tag_removal(df):
    def remove_html_tags(text):
        # Eliminar etiquetas HTML
        soup = BeautifulSoup(text, 'html.parser')
        cleaned_text = soup.get_text()

        # Eliminar enlaces
        cleaned_text = re.sub(r'http\S+|www\S+|https\S+', '', cleaned_text, flags=re.MULTILINE)

        return cleaned_text

    df['text'] = df['text'].apply(lambda x: remove_html_tags(str(x)))
    return df


# Empty or null values management
def apply_null_values_management(df):
    df = df[df['text'] != ""]
    df['text'] = df['text'].dropna()
    return df


# Apply ad hoc operation which are not included in any other sections
def apply_ad_hoc_operations(df):
    # Remove 1 len characters
    df['text'] = df['text'].apply(lambda x: remove_one_char_str(str(x)))
    return df


def remove_one_char_str(row):
    sp_stop_words = stopwords.words('spanish')

    def f(s):
        if len(s) == 1:
            if s in sp_stop_words:
                pass
            else:
                s = ""
        return s

    return " ".join(list(filter(None, list(map(f, row.split())))))


# Saving results
def save_dataframe_in_path(df, path, file_name="lectura_facil.csv", separator="|"):
    """
    Function that saves the specified df into a csv file
    :param df: Dataframe to save in path
    :param path: The output path where the df must be saved
    :param file_name: File name of the csv in which the df is going to be dumped
    :param separator: Separator for the csv file
    :return: None. Saves the result inside csv file, if not, raises an exception
    """
    try:
        df.to_csv(os.path.join(path, file_name), sep=separator, index=False, encoding="utf-8")
    except Exception as e:
        print(e)
