import pandas as pd


def combine_multiple_corpus(df_list: list[pd.DataFrame]) -> pd.DataFrame:
    """
    Function that concatenates the different DataFrames in the input list and returns it
    :param df_list: List of dataframes to be combined
    :return: Return a dataframe with the combined text and classes from the input list dataframes
    """
    all_cols_from_df_list = [list(df.columns) for df in df_list]
    for columns in all_cols_from_df_list:
        if sorted(columns) != sorted(all_cols_from_df_list[0]):
            raise Exception("Some of the DataFrames passed as input contains different columns")

    min_df_len = min([len(df) for df in df_list])
    df_list = [df.sample(n=min_df_len, random_state=1) for df in df_list]

    return pd.concat(df_list).dropna().drop_duplicates()
