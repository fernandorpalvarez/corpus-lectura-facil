import os
import re
import pandas as pd
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import stanza
from tqdm import tqdm

# nltk.download('stopwords')
# nltk.download('punkt')
# stanza.download("es")


# Data gathering (tokenization)
def load_text_in_lectura_facil_from_path(path):
    combined_df = pd.DataFrame()
    full_str = ""
    # Iterate over the path
    for root, subdirs, files in os.walk(path):
        if files:
            for file in files:
                # Read the entire text file into a single string
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    data = f.read()

                tokens = apply_tokenization(data)

                # Cleanup jump line characters
                tokens = [r.replace("\n", " ") for r in tokens]

                # Create a DataFrame from the records
                df = pd.DataFrame({'text': tokens})

                # Combine the results
                combined_df = pd.concat([combined_df, df])

                combined_df.reset_index(inplace=True, drop=True)

    return combined_df


def apply_tokenization(text):
    # Define the regular expression pattern for the separator
    separator_pattern = r'\.\n+|\?|\!\. +'

    # Split the string into records using the separator pattern
    tokens = re.compile(separator_pattern).split(text)

    return tokens


def apply_pipeline(df):
    df = apply_html_tag_removal(df)
    df = apply_add_space_before_uppercase(df)
    df = apply_numeric_char_removal(df)
    df = apply_special_char_removal(df)
    df = apply_minor_casing(df)
    df = apply_null_values_management(df)
    df = apply_stop_words_removal(df)
    df = apply_lemmatizing(df)
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df


def apply_add_space_before_uppercase(df):
    # Use a regular expression to add a space before all uppercase characters
    df['text'] = df['text'].apply(lambda x: re.sub(r'([A-Z])', r' \1', str(x)))
    return df


# Special characters removal
def apply_special_char_removal(df):
    df['text'] = df['text'].apply(lambda x: re.sub(r'\W', " ", str(x), 0, re.IGNORECASE))
    df['text'] = df['text'].apply(lambda x: re.sub(r"\s+", " ", str(x), 0, re.IGNORECASE))
    return df


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


# Pending
def apply_ad_hoc_operations(df):
    pass


# Saving results
def save_dataframe_in_path(df, path):
    df.to_csv(os.path.join(path, "lectura_facil.csv"), sep="|", index=False, encoding="utf-8")
