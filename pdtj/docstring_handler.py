import inspect

from pdtj.constants import DOCSTRING_ELEMENTS


def process_args(object_to_get):
    spec = inspect.getfullargspec(object_to_get)
    defaults = spec.defaults
    defaults = list(reversed(defaults)) if defaults is not None else []
    dict_args = {}
    for index, args in enumerate(reversed(spec.args)):
        if args != 'self':
            if args in spec.annotations.keys():
                dict_args[args + ":"] = {'type': spec.annotations[args]}
                if index < len(defaults):
                    dict_args[args + ":"]['default'] = defaults[index]
                else:
                    dict_args[args + ":"]['default'] = None

    return dict_args


def update_args(pre_processed_dict, args_pre_processed_dict, arg_dict):
    args_pre_processed_dict.pop('introduction')

    for arg in args_pre_processed_dict.keys():
        args_pre_processed_dict[arg] = {'description': args_pre_processed_dict[arg]}
        args_pre_processed_dict[arg].update(arg_dict[arg + ':'])

    pre_processed_dict['args'] = args_pre_processed_dict

    return pre_processed_dict


def get_elements_position(text: str, docstring_elements=DOCSTRING_ELEMENTS):
    elements_position_index = []

    # docstring_elements = DOCSTRING_ELEMENTS + args
    element_position = {0: 'introduction'}
    for element in docstring_elements:
        position = text.find(element)

        if position != -1:
            element_position[position] = element
            elements_position_index.append(position)

    return {key: element_position[key] for key in sorted(element_position)}  # sorted(elements_position_index)


def split_docstring_by_elements(text, elements_position):
    last_element = len(elements_position) - 1
    elements_list = list(elements_position.keys())
    result = {}
    if last_element != 0:
        for index, position in enumerate(elements_list):
            element = elements_position[position]
            if index == 0:
                result[element.replace(":", "").lower()] = (text[:elements_list[index + 1]].replace(element, ""))

            elif index == last_element:
                result[element.replace(":", "").lower()] = (text[elements_list[index]:].replace(element, ""))

            else:
                result[element.replace(":", "").lower()] = (
                    text[position:elements_list[index + 1]].replace(element, ""))

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


def parse_object(object_to_parse):
    raw_text_clean = get_text_documentation_from_element(object_to_parse)
    args_dict = process_args(object_to_parse)

    elements_position = get_elements_position(raw_text_clean)
    result = split_docstring_by_elements(raw_text_clean, elements_position)

    if 'args' in result.keys():
        elements_position = get_elements_position(result['args'], args_dict.keys())
        result_args = split_docstring_by_elements(result['args'], elements_position)
        result = update_args(result, result_args, args_dict)

    return result
