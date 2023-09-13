import os
import re
import pandas as pd


# 1. Data gathering (tokenization)
def load_text_in_lectura_facil_from_path(path):
    combined_df = pd.DataFrame()
    # Iterate over the path
    for root, subdirs, files in os.walk(path):
        if files:
            for file in files:
                # Read the entire text file into a single string
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    data = f.read()

                # Define the regular expression pattern for the separator
                separator_pattern = r'\.\n+|\?|\!\. +'

                # Split the string into records using the separator pattern
                tokens = re.compile(separator_pattern).split(data)

                # Cleanup jump line characters
                tokens = [r.replace("\n", " ") for r in tokens]

                # Create a DataFrame from the records
                df = pd.DataFrame({'text': tokens})

                # Combine the results
                combined_df = pd.concat([combined_df, df])

    return combined_df


def apply_pipeline(df):
    df = apply_special_char_removal(df)
    df = apply_minor_casing(df)
    df = apply_html_tag_removal(df)
    return df


# 2. Special characters removal
def apply_special_char_removal(df):
    df['text'] = df['text'].apply(lambda x: re.sub(r"^\w+( \w+)*$", "", str(x), 0, re.IGNORECASE))
    df['text'] = df['text'].apply(lambda x: " ".join(str(x).split()))
    df = df[df['text'] != ""]
    return df


# 3. Minor case conversion
def apply_minor_casing(df):
    df['text'] = df['text'].str.lower()
    return df


# 4. Stopwords removal

# 5. Lemmatizing or stemming

# 6. Numeric characters removal

# 7. HTML tags removal
def apply_html_tag_removal(df):
    df['text'] = df['text'].str.replace('<.*?>', '')
    # Use re.sub() to replace matched URLs with an empty string
    patterns_to_apply = [r'\bhttp\.[^\s]+\b', r'\bwww\.[^\s]+\b', r'[^\s]+.http[^\s]+', r'[^\s]+.www[^\s]+',
                         r'[^\s]+.org[^\s]+', r'[^\s]+.org', r'[^\s]+.es[^\s]+', r'[^\s]+.es', r'[^\s]+.com[^\s]+',
                         r'[^\s]+.com', r'.com', r'www.']
    for pattern in patterns_to_apply:
        df['text'] = df['text'].apply(lambda x: re.sub(pattern, '', str(x)))
    return df


# 8. Empty or null values management

# 9. Saving results
def save_dataframe_in_path(df, path):
    df.to_csv(os.path.join(path, "lectura_facil.csv"), sep="|", index=False, encoding="utf-8")
