from src.corpus_creator.web_scrapping_impl import web_scrapping_manager
import time


if __name__ == '__main__':
    start_time = time.time()

    web_scrapping_manager.extract_pdfs_from_webs()

    finish_time = time.time()

    total_time = finish_time - start_time

    print(f"Complete!: {total_time}")
