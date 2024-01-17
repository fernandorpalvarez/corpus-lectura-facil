import pandas as pd

"""
    Script for tagging and combining natural language corpus and 'lectura facil' corpus
"""


def tag_data(df: pd.DataFrame, tag: object):
    df["class"] = tag

    return df.copy(deep=True)


def combine_corpus(df_list: list):
    return pd.concat(df_list)
