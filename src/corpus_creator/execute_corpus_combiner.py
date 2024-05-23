import json
import time
from src.corpus_creator.tools import dataframe_tools
from src.corpus_creator.corpus_combiner.corpus_combiner_tool import combine_multiple_corpus


def execute_corpus_combiner():
    """
        Pipeline to transform the clean text in the pipeline:
            clean -> transform
    """
    config_corpus_combiner = json.load(open("../../config/corpus_combiner_config.json", "r", encoding="utf-8"))
    config_corpus_creation = json.load(open("../../config/corpus_creation_config.json", "r", encoding="utf-8"))
    project_path = config_corpus_creation["base_path"]
    base_path = config_corpus_combiner["base_path"]
    clean_text_path = config_corpus_combiner["clean_path"]
    transform_text_path = config_corpus_combiner["transform_path"]
    lectura_facil_clean_text_name = config_corpus_combiner["clean_lectura_facil_name"]
    lenguaje_natural_clean_text_name = config_corpus_combiner["clean_lenguaje_natural_name"]
    transform_text_name = config_corpus_combiner["transform_text_name"]

    full_clean_path = project_path + base_path + clean_text_path
    full_transform_path = project_path + base_path + transform_text_path

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


if __name__ == '__main__':
    execute_corpus_combiner()
