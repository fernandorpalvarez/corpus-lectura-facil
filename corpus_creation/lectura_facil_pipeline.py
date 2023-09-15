import os
import re
import pandas as pd
from bs4 import BeautifulSoup


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

# Lemmatizing or stemming

# Numeric characters removal
def apply_numeric_char_removal(df):
    df['text'] = df['text'].apply(lambda x: re.sub(r'[0-9]+', " ", str(x), 0, re.IGNORECASE))
    return df


# HTML tags removal
def apply_html_tag_removal(df):
    '''
    df['text'] = df['text'].str.replace('<.*?>', '')
    # Use re.sub() to replace matched URLs with an empty string
    patterns_to_apply = [r'\bhttp\.[^\s]+\b', r'\bwww\.[^\s]+\b', r'[^\s]+.http[^\s]+', r'[^\s]+.www[^\s]+',
                         r'[^\s]+.org[^\s]+', r'[^\s]+.org', r'[^\s]+.es[^\s]+', r'[^\s]+.es', r'[^\s]+.com[^\s]+',
                         r'[^\s]+.com', r'.com', r'www.']
    for pattern in patterns_to_apply:
        df['text'] = df['text'].apply(lambda x: re.sub(pattern, '', str(x)))
    '''
    df['text'] = df['text'].apply(lambda x: remove_html_tags(str(x)))
    return df


def remove_html_tags(text):
    # Eliminar etiquetas HTML
    soup = BeautifulSoup(text, 'html.parser')
    cleaned_text = soup.get_text()

    # Eliminar enlaces
    cleaned_text = re.sub(r'http\S+|www\S+|https\S+', '', cleaned_text, flags=re.MULTILINE)

    return cleaned_text


# 8. Empty or null values management
def apply_null_values_management(df):
    df = df[df['text'] != ""]
    df['text'] = df['text'].dropna()
    return df


# 9. Saving results
def save_dataframe_in_path(df, path):
    df.to_csv(os.path.join(path, "lectura_facil.csv"), sep="|", index=False, encoding="utf-8")
