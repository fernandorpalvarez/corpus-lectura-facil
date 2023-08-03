import os
from tqdm import tqdm


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