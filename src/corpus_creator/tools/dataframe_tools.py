import json
import os
import pandas as pd

_config = json.load(open("../../config/input_output_config.json", "r", encoding="utf-8"))
_read_sep = _config["read"]["separator"]
_write_sep = _config["write"]["separator"]
_read_ext = _config["read"]["default_extension"]
_write_ext = _config["write"]["default_extension"]
_read_encoding = _config["read"]["encoding"]
_write_encoding = _config["write"]["encoding"]


# Saving results
def write_dataframe(df, path, file_name, separator=_write_sep, encoding=_write_encoding):
    """
    Function that saves the specified df into a csv file
    :param df: Dataframe to save in path
    :param path: The output path where the df must be saved
    :param file_name: File name of the csv in which the df is going to be dumped
    :param separator: Separator for the csv file
    :param encoding: Encoding format for the function
    :return: None. Saves the result inside csv file, if not, raises an exception
    """
    if ".csv" not in file_name:
        file_name = file_name + _write_ext
    try:
        df.to_csv(os.path.join(path, file_name), sep=separator, index=False, encoding=encoding)
    except Exception as e:
        print(e)


# reading results
def read_dataframe(path, file_name, separator=_read_sep, encoding=_read_encoding):
    """
    Function that reads the specified path into a pandas DataFrame
    :param path: Path that contains the file to be read
    :param file_name: File name of the csv from which the df is going to be read
    :param separator: Separator for the csv file
    :param encoding: Encoding format for the function
    """
    if ".csv" not in file_name:
        file_name = file_name + _read_ext
    try:
        return pd.read_csv(os.path.join(path, file_name), sep=separator, encoding=encoding)
    except Exception as e:
        print(e)
