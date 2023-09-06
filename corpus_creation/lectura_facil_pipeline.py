import os
import re
import pandas as pd


# 1. Data gathering
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
                separator_pattern = r'\.\n+'

                # Split the string into records using the separator pattern
                records = re.split(separator_pattern, data)

                # Cleanup jump line characters
                records = [r.replace("\n", " ") for r in records]

                # Create a DataFrame from the records
                df = pd.DataFrame({'text': records})

                # Combine the results
                combined_df = pd.concat([combined_df, df])

    return combined_df


def apply_pipeline(df):
    df = apply_minor_casing(df)
    return df


# 2. Special characters removal

# 3. Tokenization

# 4. Minor case conversion
def apply_minor_casing(df):
    return df['text'].str.lower()


# 5. Stopwords removal

# 6. Lemmatizing or stemming

# 7. Numeric characters removal

# 8. HTML tags removal

# 9. Empty or null values management

# 10. Saving results
def save_dataframe_in_path(df, path):
    df.to_csv(os.path.join(path, "lectura_facil.csv"), sep="|", index=False, encoding="utf-8")
