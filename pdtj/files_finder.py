import os

REMOVE_ITEMS = ['__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__',
                '__spec__', '__init__', '__pycache__', '__init__.py']


def get_directory_type(possible_directory):
    return 'directory' if os.path.isdir(possible_directory) else 'python file'


def list_directory(path):
    return list(set(os.listdir(path)).difference(REMOVE_ITEMS))


def files_parser(path, upper_file, current_dictionary):
    update_dictionary = {upper_file: {"type": get_directory_type(path)}}

    current_directory_files_list = list_directory(path)
    for directory in current_directory_files_list:

        current_path = f'{os.path.join(path, directory)}'
        directory_type = get_directory_type(current_path)
        if directory_type == 'directory':
            current_dictionary[upper_file][directory] = (files_parser(current_path, directory, current_dictionary))

        else:
            update_dictionary[upper_file][directory] = {"type": get_directory_type(current_path)}

    current_dictionary.update(update_dictionary)
    return current_dictionary
