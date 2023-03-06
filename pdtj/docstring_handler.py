import inspect

from pdtj.constants import DOCSTRING_ELEMENTS


def process_args(object_to_get):
    spec = inspect.getfullargspec(object_to_get)
    defaults = spec.defaults
    defaults = list(reversed(defaults)) if defaults is not None else []
    dict_args = {}
    for index, args in enumerate(reversed(spec.args)):
        if args != 'self':
            dict_args[args + ":"] = {'type': spec.annotations[args]}
            if index < len(spec.defaults):
                dict_args[args + ":"]['default'] = defaults[index]
            else:
                dict_args[args + ":"]['default'] = None

    return dict_args


def update_args(pre_processed_dict, args_pre_processed_dict):
    args_pre_processed_dict.pop('introduction')

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

    for index, position in enumerate(elements_list):
        element = elements_position[position]
        if index == 0:
            result[element.replace(":", "").lower()] = (text[:elements_list[index + 1]].replace(element, ""))

        elif index == last_element:
            result[element.replace(":", "").lower()] = (text[elements_list[index]:].replace(element, ""))

        else:
            result[element.replace(":", "").lower()] = (text[position:elements_list[index + 1]].replace(element, ""))

    return result
