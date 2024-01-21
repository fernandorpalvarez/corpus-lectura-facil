import json
import time
from src.corpus_creator.tools import dataframe_tools
from src.corpus_creator.corpus_combiner.corpus_combiner_tool import combine_multiple_corpus

if __name__ == '__main__':
    '''
        Pipeline to transform the clean text in the pipeline:
            clean -> transform
    '''
    config = json.load(open("../../config/corpus_combiner_config.json", "r", encoding="utf-8"))
    base_path = config["base_path"]
    clean_text_path = config["clean_path"]
    transform_text_path = config["transform_path"]
    lectura_facil_clean_text_name = config["clean_lectura_facil_name"]
    lenguaje_natural_clean_text_name = config["clean_lenguaje_natural_name"]
    transform_text_name = config["transform_text_name"]

    full_clean_path = base_path + clean_text_path
    full_transform_path = base_path + transform_text_path

    print("Combining dataframes...")

    start_time = time.time()

    # Get the text
    lectura_facil_clean_df = dataframe_tools.read_dataframe(full_clean_path, lectura_facil_clean_text_name)
    lenguaje_natural_clean_df = dataframe_tools.read_dataframe(full_clean_path, lenguaje_natural_clean_text_name)

    # Combine with natural language
    final_corpus_df = combine_multiple_corpus([lectura_facil_clean_df, lenguaje_natural_clean_df])

    # Save the outputs
    dataframe_tools.write_dataframe(final_corpus_df, full_transform_path, transform_text_name)

    finish_time = time.time()

    total_time = finish_time - start_time

    print(f"Complete!: {total_time}")
