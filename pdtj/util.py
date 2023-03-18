import os


def check_dir_existence(path: str, file_name: str) -> bool:
    """
    Checks whether a file or directory exists at the specified path.

    Args:
        path:
            The path to the directory containing the file or directory to check.
        file_name:
            The name of the file or directory to check for existence.

    Returns:
        True if the file or directory exists, False otherwise.
    """
    return os.path.exists(os.path.join(path, file_name))


def create_single_dir(path: str, folder_name: str) -> None:
    """
    Creates a single directory with the given `folder_name` at the specified `path`.

    Args:
        path:
            The path to create the directory at.
        folder_name:
            The name of the directory to create.

    Returns:
        None
    """
    os.makedirs(os.path.join(path, folder_name))


def create_docs_and_pdtj_dir() -> None:
    """Create 'docs' and 'pdtj' directories if they do not already exist.

    This function checks whether the 'docs' and 'pdtj' directories exist in the current working directory.
     If they do not exist, the function creates them using the 'os.makedirs()' method.

    Args:
        None

    Returns:
        None
    """
    current_path = os.getcwd()
    for folder_name in ["docs", "pdtj"]:
        if not check_dir_existence(current_path, folder_name):
            create_single_dir(current_path, folder_name)

        current_path = os.path.join(current_path, folder_name)
