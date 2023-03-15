import os

from pdtj.docstring_handler import docstring_file_parser

REMOVE_ITEMS = ['__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__',
                '__spec__', '__init__', '__pycache__', '__init__.py']


def get_directory_type(possible_directory):
    return 'directory' if os.path.isdir(possible_directory) else 'file'


def list_directory(path):
    return list(set(os.listdir(path)).difference(REMOVE_ITEMS))


def loop_over_current_dictionary(module_path, result):
    module_list = module_path.split('.')
    open_dictionary = {}
    for index, module in enumerate(reversed(module_list)):
        if index == 0:
            open_dictionary[module] = {}

        else:
            nested_dict = {module: open_dictionary}
            open_dictionary = nested_dict

    open_dictionary.update(result)
    return open_dictionary


def files_parser(path, upper_file, current_dictionary):
    update_dictionary = {upper_file: {"type": get_directory_type(path)}}

    files_in_directory = list_directory(path)
    for file_name in files_in_directory:

        current_path = f'{os.path.join(path, file_name)}'
        module_path = current_path.replace('./', '').replace('\\', '.').replace('/', '.')

        file_type = get_directory_type(current_path)
        if file_type == 'directory':
            result = files_parser(current_path, file_name, current_dictionary)
            current_dictionary = loop_over_current_dictionary(module_path, result)

        elif file_type == 'file':
            if file_name.endswith(".py"):
                python_type = 'python file'
                docstring_dict = docstring_file_parser(module_path)

                update_dictionary[upper_file][file_name] = {"type": python_type}
                update_dictionary[upper_file][file_name].update(docstring_dict)

    current_dictionary.update(update_dictionary)
    return current_dictionary
