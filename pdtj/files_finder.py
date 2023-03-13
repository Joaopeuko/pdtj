import os

REMOVE_ITEMS = ['__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__',
                '__spec__', '__init__', '__pycache__', '__init__.py']


def get_directory_type(possible_directory):
    return 'directory' if os.path.isdir(possible_directory) else 'python file'


def list_directory(path):
    return list(set(os.listdir(path)).difference(REMOVE_ITEMS))


def files_parser(path, upper_file, current_dictionary):
    update_dictionary = {upper_file: {"type": get_directory_type(path)}}

    files_in_directory = list_directory(path)
    for file_name in files_in_directory:

        current_path = f'{os.path.join(path, file_name)}'
        file_type = get_directory_type(current_path)
        if file_type == 'directory':
            current_dictionary[upper_file][file_name] = (files_parser(current_path, file_name, current_dictionary))

        elif file_type == 'python file':
            update_dictionary[upper_file][file_name] = {"type": file_type}

    current_dictionary.update(update_dictionary)
    return current_dictionary
