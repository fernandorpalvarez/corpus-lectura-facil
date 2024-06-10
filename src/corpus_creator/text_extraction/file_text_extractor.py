import json
import concurrent.futures
import os

import pandas as pd
import pandas.core.frame
from PyPDF2 import PdfReader
from tqdm import tqdm
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTTextBox
import fitz
import logging

logging.basicConfig(filename="../../data/errors.log",
                    filemode='w+',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.ERROR)


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


def keep_extracted_text_from_path_in_df(path: str, text_df: pandas.core.frame.DataFrame, parallelize=False) -> pandas.core.frame.DataFrame:
    """
    Extract the text of the pdfs or txt files inside the path and returns them inside a pandas df
    :param parallelize: Flag that indicates if you want to parallelize or not the execution
    :param path: path which contains the files with the text
    :param text_df: Optional parameter that contains the text already extracted from another path. The extracted text
    from the current path will be appended inside this dataframe
    :return: Pandas DataFrame with the extracted text
    """
    config = json.load(open("../../config/text_extraction_config.json", "r", encoding="utf-8"))
    pdf_extractor_engine = config["pdf_extractor_engine"]
    n_pages_to_skip = config["n_pages_to_skip"]

    if parallelize:
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            text_df = [executor.submit(extract_text_from_pdf,
                                       os.path.join(path, str(pdf_name)),
                                       text_df,
                                       pdf_extractor_engine,
                                       n_pages_to_skip) for pdf_name in tqdm(os.listdir(path))]

        return pd.concat(df.result() for df in text_df)

    else:
        for pdf_name in tqdm(os.listdir(path)):
            text_df = extract_text_from_pdf(os.path.join(path, str(pdf_name)),
                                                        text_df,
                                                        pdf_extractor_engine,
                                                        n_pages_to_skip)

        return text_df


def extract_text_from_pdf(pdf_path, text_df, pdf_extractor_engine, n_pages_to_skip):
    source = pdf_path.split("/")[-1]
    new_text_extracted = pd.DataFrame()
    # 1. Extract the text of each pdf or txt file
    if pdf_path.endswith(".pdf"):
        try:
            pdf_text = extract_text_from_pdf(os.path.join(pdf_path),
                                             pdf_extractor_engine=pdf_extractor_engine,
                                             n_pages=n_pages_to_skip)
            new_text_extracted["text"] = pdf_text,
            new_text_extracted["source"] = source
        except Exception as e:
            logging.error(f"Error extracting text from {pdf_path}, {e}")

    elif pdf_path.endswith(".txt"):
        try:
            with open(pdf_path, 'r', encoding='utf-8') as f:
                pdf_text = f.read()
            new_text_extracted["text"] = pdf_text,
            new_text_extracted["source"] = source
        except Exception as e:
            logging.error(f"Error extracting text from {pdf_path}, {e}")

    # TODO: This piece of code is adhoc for this project.
    # All files we are reading are .pdfs but this file that is a .tsv, it also has a specific column called
    # "text_e2r" which contains the easy to read text
    elif pdf_path.endswith(".tsv"):
        new_text_extracted = pd.read_csv(pdf_path, sep="\t")
        new_text_extracted = new_text_extracted[["text_e2r"]]
        new_text_extracted.rename(columns={"text_e2r": "text"}, inplace=True)
        new_text_extracted["source"] = source

    # 2. Save the extracted text into a pd df as a new row
    try:
        text_df = pd.concat([text_df, new_text_extracted])
    except UnboundLocalError as e:
        logging.error(f"Error extracting text from {pdf_path}, {e}")

    return text_df


def extract_text_from_pdfs_in_subdirs_to_df(subdirs_path, parallelize_flag) -> pandas.core.frame.DataFrame:
    """
    Functions that iterates over the subdirs in the path, extract the text inside the pdfs and saves it in a pandas df
    :param parallelize_flag: Flag that indicates if you want to execute the code with parallelization WOI
    :param subdirs_path: Path that contains the subdirs inside each of them containing the pdfs
    :return: Pandas DataFrame
    """
    full_text_df = pd.DataFrame(columns=["text", "source"])
    for root, subdir, files in os.walk(subdirs_path):
        if files:
            print(f"\nDirectory: {root.split('/')[-1]}...")
            full_text_df = keep_extracted_text_from_path_in_df(root, full_text_df, parallelize_flag)

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
    print(f"Directory: {path}...")
    # Open the file in read mode ('r' stands for read)
    with open(path, 'r', encoding='utf-8') as file:
        # Read the contents of the file
        file_contents = file.read()

    # Split the long string based on a delimiter
    rows = file_contents.split("\n")

    # Return a DataFrame with a single column 'Text'
    return pd.DataFrame({'text': rows, 'source': path.split("/")[-1]}).dropna(subset=['text'])
