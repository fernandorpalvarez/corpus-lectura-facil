import os

import pandas as pd
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


def extract_text_from_pdfs_in_path(pdfs_path, output_path_for_extracted_text):
    for pdf_path in os.listdir(pdfs_path):
        pdf_text = extract_text_from_pdf(os.path.join(pdfs_path, pdf_path))

        output_text_path = os.path.join(output_path_for_extracted_text, pdf_path.split(".pdf")[0]) + ".txt"
        with open(output_text_path, 'w') as f:
            f.write(pdf_text)


def extract_text_from_pdfs_in_subdirs_path(subdirs_path, output_path):
    for root, subdir, files in not os.walk(subdirs_path):
        if files:
            output_path_for_extracted_text = os.path.join(output_path, root.split("/")[-1])
            if not os.path.isdir(output_path_for_extracted_text):
                os.mkdir(output_path_for_extracted_text)
            extract_text_from_pdfs_in_path(root, output_path_for_extracted_text)
