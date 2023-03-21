import os
from typing import List

from pdtj.constants import REMOVE_ITEMS
from pdtj.docstring_handler import docstring_file_parser


def get_directory_type(possible_directory: str) -> str:
    """
    Determines the type of a given path.

    Args:
        possible_directory: A path to check for its type.

    Returns:
        The type of the given path. Either "directory" or "file".

    Example:
        >>> get_directory_type('/path/to/directory')
        'directory'
        >>> get_directory_type('/path/to/file.txt')
        'file'
    """
    return "directory" if os.path.isdir(possible_directory) else "file"


def list_directory(path: str) -> List[str]:
    """
    Returns a list of files and directories located in the specified path,
    excluding items in the REMOVE_ITEMS list.

    Args:
        path: The path to the directory to list.

    Returns:
        A list of files and directories in the directory, excluding REMOVE_ITEMS.
    """
    return list(set(os.listdir(path)).difference(REMOVE_ITEMS))


def loop_over_current_dictionary(module_path: str, result: dict) -> dict:
    """
    Given a module path and a dictionary to add, create nested dictionaries according to the module
    path and merge the result dictionary. Return the resulting nested dictionary.

    Args:
        module_path:
            A string representing the path of a module, separated by dots.
        result:
            A dictionary to merge with the nested dictionaries.

    Returns:
        A nested dictionary with the keys specified by the module path and the values specified
         by the result dictionary.
    """
    module_list = module_path.split(".")
    open_dictionary = {}
    for index, module in enumerate(reversed(module_list)):
        if index == 0:
            open_dictionary[module] = {}

        else:
            nested_dict = {module: open_dictionary}
            open_dictionary = nested_dict

    open_dictionary.update(result)
    return open_dictionary


def files_parser(path: str, upper_file: str, current_dictionary: dict) -> dict:
    """
    Recursively parses a directory and its subdirectories for Python files and extracts
    their docstrings as well as other metadata.

    Args:
        path:
            The path to the directory to be parsed.
        upper_file:
            The parent file name of the current directory.
        current_dictionary:
            A dictionary to store the metadata extracted from the files.

    Returns:
        The updated `current_dictionary` with the metadata extracted from the files.

    """
    update_dictionary = {upper_file: {"type": get_directory_type(path)}}

    files_in_directory = list_directory(path)
    for file_name in files_in_directory:
        current_path = f"{os.path.join(path, file_name)}"
        module_path = current_path.replace("./", "").replace("\\", ".").replace("/", ".")

        file_type = get_directory_type(current_path)
        if file_type == "directory":
            result = files_parser(current_path, file_name, current_dictionary)
            current_dictionary = loop_over_current_dictionary(module_path, result)

        elif file_type == "file":
            if file_name.endswith(".py"):
                python_type = "python file"
                docstring_dict = docstring_file_parser(module_path)

                update_dictionary[upper_file][file_name] = {"type": python_type}
                update_dictionary[upper_file][file_name].update(docstring_dict)

    current_dictionary.update(update_dictionary)
    return current_dictionary
