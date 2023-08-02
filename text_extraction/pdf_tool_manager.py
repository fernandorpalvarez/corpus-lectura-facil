import os
from tqdm import tqdm


def rename_files_in_path(folder_path):
    i = 0
    for file_path in tqdm(os.listdir(folder_path)):
        old_name = os.path.join(folder_path, file_path)
        new_name = os.path.join(folder_path, "pdf_" + str(i) + ".pdf")
        while os.path.isfile(new_name):
            i += 1
            new_name = os.path.join(folder_path, "pdf_" + str(i) + ".pdf")

        os.rename(old_name, new_name)
        i += 1