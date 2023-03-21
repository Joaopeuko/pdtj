import importlib.util
import inspect
from typing import Dict
from typing import List

from pdtj.constants import GOOGLE_DOCSTRING_ELEMENTS


def process_args(func: object) -> dict:
    """
    Extracts the arguments and their types from a function's signature.

    Args:
        func: The function to extract the arguments from.

    Returns:
        A dictionary mapping each argument name to its type and default value (if any).
    """
    args_with_types = {}
    try:
        argspec = inspect.getfullargspec(func)
        defaults = argspec.defaults or []
        defaults = list(reversed(defaults))
        for index, args in enumerate(reversed(argspec.args)):
            if args != "self":
                if args in argspec.annotations.keys():
                    args_with_types[args + ":"] = {"type": argspec.annotations[args]}
                    if index < len(defaults):
                        args_with_types[args + ":"]["default"] = defaults[index]
                    else:
                        args_with_types[args + ":"]["default"] = "No default argument"

        return args_with_types

    except ValueError:
        return args_with_types


def update_args(pre_processed_dict: dict, args_pre_processed_dict: dict, arg_dict: dict) -> dict:
    """
    Update the `args_pre_processed_dict` with the values from `arg_dict` and return the updated `pre_processed_dict`.

    Args:
        pre_processed_dict:
            A dictionary containing the pre-processed information.
        args_pre_processed_dict:
            A dictionary containing the pre-processed information for arguments.
        arg_dict:
            A dictionary containing the argument names and their descriptions and types.

    Returns:
        A dictionary containing the updated pre-processed information.
    """

    # Remove the introduction key from the args_pre_processed_dict
    args_pre_processed_dict.pop("introduction")

    for arg in args_pre_processed_dict.keys():
        args_pre_processed_dict[arg] = {"description": args_pre_processed_dict[arg]}
        args_pre_processed_dict[arg].update(arg_dict[arg + ":"])

    pre_processed_dict["args"] = args_pre_processed_dict

    return pre_processed_dict


def get_elements_position(text: str, docstring_elements: List[str] = GOOGLE_DOCSTRING_ELEMENTS) -> Dict[int, str]:
    """
    Return a dictionary containing the position of each docstring element in the text.

    Args:
        text:
            The docstring to parse.
        docstring_elements:
            A list of docstring elements to search for.
            Defaults to GOOGLE_DOCSTRING_ELEMENTS.

    Returns:
        A dictionary containing the position of each docstring element in the text.
    """
    elements_position_index = []

    element_position = {0: "introduction"}
    for element in docstring_elements:
        position = text.find(element)

        if position != -1:
            element_position[position] = element
            elements_position_index.append(position)

    return {key: element_position[key] for key in sorted(element_position)}


def split_docstring_by_elements(text: str, elements_position: Dict[int, str]) -> Dict[str, str]:
    """
    Splits a given docstring into sections based on the positions of specified elements.

    Args:
        text:
            The docstring to be split.
        elements_position:
            A dictionary containing the positions of the elements to split the docstring by.

    Returns:
        A dictionary containing the sections of the split docstring, where the key is the name of the
         section and the value is the text of the section.
    """
    last_element = len(elements_position) - 1
    elements_list = list(elements_position.keys())
    result = {}
    if last_element != 0:
        for index, position in enumerate(elements_list):
            element = elements_position[position]
            if index == 0:
                result[element.replace(":", "").lower()] = text[: elements_list[index + 1]].replace(element, "")

            elif index == last_element:
                result[element.replace(":", "").lower()] = text[elements_list[index] :].replace(element, "")

            else:
                result[element.replace(":", "").lower()] = text[position : elements_list[index + 1]].replace(
                    element, ""
                )

    elif len(elements_position) == 1:
        for element in elements_position.values():
            result[element.replace(":", "").lower()] = text

    return result


def get_text_documentation_from_element(element: object) -> str:
    """
    This function returns the cleaned-up text documentation of an element.

    Args:
        element: The element to extract the documentation from.

    Returns:
        The cleaned-up text documentation of the element.
    """
    docstring = inspect.getdoc(element)
    if docstring:
        return inspect.cleandoc(docstring)
    else:
        return ""


def parse_object(object_to_parse: object) -> dict:
    """
    Parses the docstring of an object and returns a dictionary with the parsed elements.

    Args:
        object_to_parse:
            The object to parse.

    Returns:
        A dictionary with the parsed elements of the object's docstring.
    """
    raw_text_clean = get_text_documentation_from_element(object_to_parse)
    args_dict = process_args(object_to_parse)

    elements_position = get_elements_position(raw_text_clean)
    result = split_docstring_by_elements(raw_text_clean, elements_position)

    if "args" in result.keys():
        elements_position = get_elements_position(result["args"], list(args_dict.keys()))
        result_args = split_docstring_by_elements(result["args"], elements_position)
        result = update_args(result, result_args, args_dict)

    return result


def docstring_file_parser(file: str) -> dict:
    """
    Parses the docstrings of the classes and functions defined in the given Python file.

    Args:
        file:
            The name of the Python file to parse.

    Returns:
        A dictionary with the parsed information. The dictionary keys are the names
        of the classes or functions defined in the file, and the values are dictionaries
        with the parsed information for each class or function.

    Example:
        Given a file `example.py` containing a class `ExampleClass` and a function
        `example_function`:

        >>> docstring_file_parser('example.py')
        {
            'ExampleClass': {
                'introduction': 'This is the docstring of the ExampleClass.',
                'method1': {
                    'introduction': 'This is the docstring of method1.',
                    'args': {
                        'arg1': {
                            'description': 'The first argument.',
                            'type': 'str'
                        },
                        'arg2': {
                            'description': 'The second argument.',
                            'type': 'int'
                        }
                    },
                    'return': {
                        'description': 'The result of the method.',
                        'type': 'float'
                    }
                }
            },
            'example_function': {
                'introduction': 'This is the docstring of example_function.',
                'args': {
                    'arg1': {
                        'description': 'The first argument.',
                        'type': 'str'
                    },
                    'arg2': {
                        'description': 'The second argument.',
                        'type': 'int'
                    }
                },
                'return': {
                    'description': 'The result of the function.',
                    'type': 'float'
                }
            }
        }
    """
    try:
        mod = importlib.import_module(f"{file.replace('.py', '')}", package=None)
        members = inspect.getmembers(mod, predicate=lambda x: inspect.isclass(x) or inspect.isfunction(x))
        member_dict = dict(members)

        dict_result = {}
        for key in member_dict:
            dict_result[key] = parse_object(member_dict[key])

            if inspect.isclass(member_dict[key]):
                class_members = inspect.getmembers(member_dict[key], predicate=inspect.isfunction)
                class_members_dict = dict(class_members)
                for class_key in class_members_dict:
                    dict_result[key][class_key] = parse_object(class_members_dict[class_key])

        return dict_result

    except FileNotFoundError:
        return {}
