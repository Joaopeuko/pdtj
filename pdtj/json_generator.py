import os
import __version__
from pdtj.files_finder import get_directory_type, files_parser
from pdtj.util import create_docs_and_pdtj_dir

import argparse


def get_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("--root",
                        type=str,
                        action="store")

    return vars(parser.parse_args())


def main():

    root = get_arguments()['root']

    create_docs_and_pdtj_dir()

    directory_dict = {root: {"type": get_directory_type(f"../{root}")}}
    path = f"./{root}"
    upper_file = root
    file_parser_result = files_parser(path, upper_file, directory_dict)

    path = os.path.join(os.getcwd(), '../docs')
    path = os.path.join(path, '')
    with open(os.path.join(path, f'{__version__.version}.json'), 'w') as file:
        file.write(str(file_parser_result))
