import os
from tqdm import tqdm


def rename_files_in_subdirs_of_path(path: str):
    """
    This function iterates over the subdirs of the path, for each of the subdirs, iterate over the files and renames
    them with an alphanumerical value
    :param path: Path that will contain the subdirs and the files
    :return: None
    """
    # Iterate over the files in path
    for path_index, walk_set in tqdm(enumerate(os.walk(path))):
        root, subdir, files = walk_set
        if len(files) > 0:
            for file_index, file_name in enumerate(files):
                try:
                    # Extract the text of each pdf or txt file
                    file_extension = "." + file_name.split(".")[-1]
                    old_file_path = os.path.join(root, file_name)
                    new_file_path = os.path.join(root, str(path_index) + "." + str(file_index) + file_extension)
                    os.rename(old_file_path, new_file_path)

                except Exception as e:
                    print("Error renaming ", os.path.join(root, file_name))
                    print(e)
                    continue


if __name__ == '__main__':
    base_path = "your_path"
    rename_files_in_subdirs_of_path(base_path)
