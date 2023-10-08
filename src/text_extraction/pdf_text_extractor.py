import os
import shutil

import pandas as pd
import pandas.core.frame
from PyPDF2 import PdfReader


def extract_text_from_pdf(pdf_path):
    # defining the text variable
    text = ""

    # creating a pdf reader object
    reader = PdfReader(pdf_path)

    # iterate over the pages in pdf file
    for page in reader.pages:
        # extracting text from page
        text += page.extract_text()

    return text


def extract_and_save_text_from_pdfs_in_path(pdfs_path, output_path_for_extracted_text):
    for pdf_path in os.listdir(pdfs_path):
        # Extract text from pdfs into txt files
        if pdf_path.endswith(".pdf"):
            try:
                pdf_text = extract_text_from_pdf(os.path.join(pdfs_path, pdf_path))
                output_text_path = os.path.join(output_path_for_extracted_text, pdf_path.split(".pdf")[0]) + ".txt"
                with open(output_text_path, 'w', encoding='utf-8') as f:
                    f.write(pdf_text)
            except Exception as e:
                print(e)

        # Copy text files into new path
        elif pdf_path.endswith(".txt"):
            output_text_path = os.path.join(output_path_for_extracted_text, pdf_path)
            shutil.copy2(os.path.join(pdfs_path, pdf_path), output_text_path)


def extract_text_from_pdfs_in_subdirs_path(subdirs_path, output_path):
    for root, subdir, files in os.walk(subdirs_path):
        if files:
            output_path_for_extracted_text = os.path.join(output_path, root.split("/")[-1])
            if not os.path.isdir(output_path_for_extracted_text):
                os.mkdir(output_path_for_extracted_text)
            extract_and_save_text_from_pdfs_in_path(root, output_path_for_extracted_text)


def keep_extracted_text_from_path_in_df(path: str, text_df=None) -> pandas.core.frame.DataFrame:
    """
    Extract the text of the pdfs or txt files inside the path and returns them inside a pandas df
    :param path: path which contains the files with the text
    :param text_df: Optional parameter that contains the text already extracted from another path. The extracted text
    from the current path will be appended inside this dataframe
    :return: Pandas DataFrame with the extracted text
    """
    # Iterate over the pdfs in path
    for pdf_path in os.listdir(path):
        # 1. Extract the text of each pdf
        if pdf_path.endswith(".pdf"):
            try:
                pdf_text = extract_text_from_pdf(os.path.join(path, pdf_path))
            except Exception as e:
                print("Error extracting text from ", os.path.join(path, pdf_path))
                print(e)
                continue

        elif pdf_path.endswith(".txt"):
            with open(os.path.join(path, pdf_path), 'r', encoding='utf-8') as f:
                pdf_text = f.read()

        # 2. Save the extracted text into a pd df as a new row
        text_df.loc[len(text_df)] = [pdf_text]

    # Return the pd df
    return text_df


def extract_text_from_pdfs_in_subdirs_to_df(subdirs_path) -> pandas.core.frame.DataFrame:
    """
    Functions that iterates over the subdirs in the path, extract the text inside the pdfs and saves it in a pandas df
    :param subdirs_path: Path that contains the subdirs inside each of them containing the pdfs
    :return: Pandas DataFrame
    """
    full_text_df = pd.DataFrame(columns=["text"])
    for root, subdir, files in os.walk(subdirs_path):
        if files:
            full_text_df = keep_extracted_text_from_path_in_df(root, full_text_df)

    return full_text_df


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

