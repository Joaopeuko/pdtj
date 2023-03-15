import os


def check_dir_existence(path, file_name):
    return os.path.exists(os.path.join(path, file_name))


def create_single_dir(path, folder_name):
    os.makedirs(os.path.join(path, folder_name))


def create_docs_and_pdtj_dir():
    """
    This function check if the folder docs and pdtj exist, if not, it creates it.
    Returns:
        It returns None, but it creates the folders mentioned above

    """
    current_path = os.getcwd()
    for folder_name in ['docs', 'pdtj']:

        if not check_dir_existence(current_path, folder_name):
            create_single_dir(current_path, folder_name)

        current_path = os.path.join(current_path, folder_name)
