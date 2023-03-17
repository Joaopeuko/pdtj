import os
import __version__
from pdtj.files_finder import get_directory_type, files_parser
from pdtj.parameters import parameters
from pdtj.util import create_docs_and_pdtj_dir

import argparse


def get_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("--project_name",
                        type=str,
                        action="store",
                        default=parameters['name'])

    return vars(parser.parse_args())


def main():

    project_name = get_arguments()['project_name']

    create_docs_and_pdtj_dir()

    directory_dict = {project_name: {"type": get_directory_type(f"../{project_name}")}}
    path = f"./{project_name}"
    upper_file = project_name
    file_parser_result = files_parser(path, upper_file, directory_dict)

    file_parser_result[project_name].update({"shelve": parameters['shelve'], "sub-project": parameters['sub-project']})

    path = os.path.join(os.getcwd(), 'docs')
    path = os.path.join(path, 'pdtj')
    with open(os.path.join(path, f'{__version__.version}.json'), 'w') as file:
        file.write(str(file_parser_result))
