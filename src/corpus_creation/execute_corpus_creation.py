from corpus_combiner import *
import json
from src.corpus_creator.tools import dataframe_tools

if __name__ == '__main__':
    '''
        Pipeline to transform the clean text in the pipeline:
            clean -> transform
    '''
    config = json.load(open("../../config/corpus_creation_config.json", "r", encoding="utf-8"))
    clean_text_path = config["clean_text_path"]
    transform_text_path = config["transform_text_path"]
    clean_text_name = config["clean_text_name"]
    transform_text_name = config["transform_text_name"]

    # Get the text
    clean_text_df = dataframe_tools.read_dataframe(clean_text_path, clean_text_name)

    # Tag the dataframe
    clean_text_df = tag_data(clean_text_df, 1)

    # Combine with natural language
    final_corpus_df = combine_corpus([clean_text_df])  # TODO: Add natural language

    # Save the outputs
    dataframe_tools.write_dataframe(final_corpus_df, transform_text_path, transform_text_name)
