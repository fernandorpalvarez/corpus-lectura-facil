import json
import os

import pandas as pd
import pandas.core.frame
from PyPDF2 import PdfReader
from tqdm import tqdm
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTTextBox
import fitz


def extract_text_from_pdf(pdf_path, pdf_extractor_engine="pdf_miner", n_pages=1):
    # defining the text variable
    text = ""
    if pdf_extractor_engine == "pypdf2":
        # creating a pdf reader object
        reader = PdfReader(pdf_path)
        # iterate over the pages in pdf file
        for page_num, page in enumerate(reader.pages):
            # Skip the first n pages
            if page_num > n_pages:
                # extracting text from page
                text += page.extract_text()

    elif pdf_extractor_engine == "pdf_miner":
        # iterate over the pages in pdf file
        for page_num, page_layout in enumerate(extract_pages(pdf_path)):
            # Skip the first n pages
            if page_num > n_pages:
                for element in page_layout:
                    if isinstance(element, LTTextContainer):
                        text += element.get_text()
                    elif isinstance(element, LTTextBox):
                        for line in element:
                            text += line.get_text()

    elif pdf_extractor_engine == "fitz":
        # open a document
        doc = fitz.open(pdf_path)
        # iterate the document pages
        for page_num, page in enumerate(doc):
            # Skip the first n pages
            if page_num > n_pages:
                # get plain text encoded as UTF-8
                text += page.get_text()

    else:
        raise Exception("You must specify a valid pdf extractor engine")

    return text


def keep_extracted_text_from_path_in_df(path: str, text_df: pandas.core.frame.DataFrame) -> pandas.core.frame.DataFrame:
    """
    Extract the text of the pdfs or txt files inside the path and returns them inside a pandas df
    :param path: path which contains the files with the text
    :param text_df: Optional parameter that contains the text already extracted from another path. The extracted text
    from the current path will be appended inside this dataframe
    :return: Pandas DataFrame with the extracted text
    """
    config = json.load(open("../../config/text_extraction_config.json", "r", encoding="utf-8"))
    pdf_extractor_engine = config["pdf_extractor_engine"]
    n_pages_to_skip = config["n_pages_to_skip"]

    # Iterate over the pdfs in path
    for pdf_name in tqdm(os.listdir(path)):
        # 1. Extract the text of each pdf or txt file
        if pdf_name.endswith(".pdf"):
            try:
                pdf_text = extract_text_from_pdf(os.path.join(path, pdf_name),
                                                 pdf_extractor_engine=pdf_extractor_engine,
                                                 n_pages=n_pages_to_skip)
            except Exception as e:
                print("Error extracting text from ", os.path.join(path, pdf_name))
                print(e)
                continue

        elif pdf_name.endswith(".txt"):
            with open(os.path.join(path, pdf_name), 'r', encoding='utf-8') as f:
                pdf_text = f.read()

        # 2. Save the extracted text into a pd df as a new row
        try:
            source = path.split("/")[-1] + "/" + pdf_name
            text_df.loc[len(text_df)] = [pdf_text, source]
        except UnboundLocalError as e:
            print(e)
            continue

    # Return the pd df
    return text_df


def extract_text_from_pdfs_in_subdirs_to_df(subdirs_path) -> pandas.core.frame.DataFrame:
    """
    Functions that iterates over the subdirs in the path, extract the text inside the pdfs and saves it in a pandas df
    :param subdirs_path: Path that contains the subdirs inside each of them containing the pdfs
    :return: Pandas DataFrame
    """
    full_text_df = pd.DataFrame(columns=["text", "source"])
    for root, subdir, files in os.walk(subdirs_path):
        if files:
            full_text_df = keep_extracted_text_from_path_in_df(root, full_text_df)

    return full_text_df


def save_dataframe_in_path(df, path, file_name="raw_text.csv", separator="|"):
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


def rename_files_in_path(folder_path):
    data_type = "pdf"
    i = 0
    for file_path in tqdm(os.listdir(folder_path)):
        old_name = os.path.join(folder_path, file_path)
        if old_name.endswith(".txt"):
            data_type = "txt"
        elif old_name.endswith(".pdf"):
            data_type = "pdf"

        new_name = os.path.join(folder_path, f"{data_type}_{str(i)}.{data_type}")
        while os.path.isfile(new_name):
            i += 1
            new_name = os.path.join(folder_path, f"{data_type}_{str(i)}.{data_type}")

        os.rename(old_name, new_name)
        i += 1


def tag_data(df: pd.DataFrame, tag: object) -> pd.DataFrame:
    """
    Function that append a new column called class to a dataframe
    :param df: DataFrame to which will add the new class column
    :param tag: Class to be associated to the whole dataset
    :return: pd.DataFrame
    """
    df["class"] = tag
    return df.copy(deep=True)


def lenguaje_natural_text_extractor(path):
    # Open the file in read mode ('r' stands for read)
    with open(path, 'r', encoding='utf-8') as file:
        # Read the contents of the file
        file_contents = file.read()

    # Split the long string based on a delimiter
    rows = file_contents.split("\n")

    # Return a DataFrame with a single column 'Text'
    return pd.DataFrame({'text': rows}).dropna(subset=['text'])
