![PyPI - Downloads](https://img.shields.io/pypi/dm/pdtj)
![PyPI](https://img.shields.io/pypi/v/pdtj)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/pdtj)
![PyPI - License](https://img.shields.io/pypi/l/pdtj)

# PDTJ - (Python Docstring To Json)

## Introduction

This project was created to solve a personal need for a flexible and simple tool to retrieve all
Python docstrings and convert them into a JSON format. The tool's design provides flexibility to
customize the parsing and documentation process, making it easy to navigate through the codebase's structure and
documentation.

This project aims to provide a powerful tool for parsing and documenting Python code within a directory. The tool works
by recursively traversing a directory and identifying all Python files contained within it. It then extracts the
docstrings of these files, organizing them into a dictionary format that captures the structure and documentation of the
entire codebase. This dictionary is then written to a JSON file, making it easy to view and access the information
it contains.
Whether you're a software developer or a codebase maintainer,
this tool can help you gain a deeper understanding of your Python code and streamline the documentation
process.

Moreover, this tool aims to simplify the process of generating a documentation webpage by
using the JSON file. It provides a clear overview of the codebase's structure and documentation,
allowing users to quickly navigate through the code and understand its functionality.
The project is designed to be flexible and customizable, enabling users to tailor the parsing
and documentation process to their specific needs. With this tool, you can easily generate comprehensive
documentation for your Python codebase and share it with others.

# How to Use

## Installation

To install the tool, run the following command:
```shell
pip install pdtj
```

Next, create a ```.pdtj.yaml``` file in the root directory of your project and specify the following information:
```shell
name: <project name> # replace <project name> with your project's name
shelve: <shelve name> # choose any name you like for <shelve name>
sub-project: <sub-project name> # choose any name you like for <sub-project name>
```

To use the library, you'll need to include a file named ```__version__.py``` in your app or project directory.
This file will be used by the library to generate a JSON file with the version name.
To ensure you have the necessary file and to view the generated output, you can check the ```pdtj/__version__py```
and ```docs/pdtj``` directories.

## Generating the Documentation
Once you have installed the tool and configured the ```.pdtj.yaml``` file, you can generate the documentation by running
the following command:

```shell
pdtj
```

If everything is set up correctly, the tool will traverse your project directory, extract the docstrings from all Python
files, and create a JSON file containing the documentation. The resulting file can be used to generate a
documentation webpage or for any other purpose.



# Features missing

- [ ] Log
- [ ] Unit tests

# License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/Joaopeuko/pdtj/blob/master/LICENSE) file for details.
