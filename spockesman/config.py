import importlib
from typing import Union, List

import yaml
from types import ModuleType

from spockesman.context.backend import database
from spockesman.logger import log
from spockesman.states import Command
from spockesman.states.commands.command import CommandDescriptor
from spockesman.states.base import META_STATES
from spockesman.states.commands.command import generate_commands
from spockesman.util.string import upper_and_separate
from spockesman.util.matchers import is_vector


def is_module_path(path) -> bool:  # TODO, FIXME: bad check if string is a path to module. Refactor!
    return '.' in path


def command_parser(item) -> CommandDescriptor:
    return Command[item]


def state_parser(item) -> str:
    return str(item)


TYPE_SECTION = 'Type'
VALUE_SECTION = 'Value'
STATES_SECTION = 'States'
COMMANDS_SECTION = 'Commands'
CONTEXT_BACKEND_SECTION = 'ContextBackend'

PARSER_MAPPING = {'COMMAND': command_parser, 'STATE': state_parser}


class Configuration:
    """
    Container for raw configuration data
    """

    commands: dict
    context_backend: dict
    context_backend_type: str
    states: dict

    @classmethod
    def from_dict(cls, conf_dict):
        self = cls()
        self.commands = conf_dict[COMMANDS_SECTION]
        self.context_backend = conf_dict[CONTEXT_BACKEND_SECTION]
        self.context_backend_type = conf_dict[CONTEXT_BACKEND_SECTION][TYPE_SECTION]
        self.states = conf_dict.get(STATES_SECTION, None)
        return self

    @classmethod
    def from_module(cls, module):
        self = cls()
        self.commands = getattr(module, upper_and_separate(COMMANDS_SECTION))
        self.context_backend = getattr(module, upper_and_separate(CONTEXT_BACKEND_SECTION))
        self.context_backend_type = getattr(module, upper_and_separate(CONTEXT_BACKEND_SECTION))[
            TYPE_SECTION
        ]
        self.states = getattr(module, upper_and_separate(STATES_SECTION), None)
        return self


def config_from_object(obj) -> Configuration:
    """
    Create Configuration class from object with data
    :param obj: object with configuration data, module or dict
    :return: Configuration instance
    """
    dispatcher = {dict: Configuration.from_dict, ModuleType: Configuration.from_module}
    return dispatcher[type(obj)](obj)


def setup(config_pointer) -> None:
    """
    Read config object and setup framework
    :param config_pointer: path to .yaml config or name of python module with configuration
    :return: None
    """
    log.debug(f"Trying to read config from '{config_pointer}'")
    # if we got string, interpret it as path to something
    if isinstance(config_pointer, str):
        if config_pointer.endswith('.yaml'):
            with open(config_pointer, 'r') as config_file:
                data = yaml.full_load(config_file)
        elif is_module_path(config_pointer):
            data = importlib.import_module(config_pointer)
        else:
            raise TypeError('Only .py and .yaml are supported config formats')
    # else interpret it as config data
    else:
        data = config_pointer
    # try to load Configuration class from this data
    try:
        config = config_from_object(data)
    except KeyError:
        raise TypeError(f'Unsupported raw config object type: {type(data)}')
    # then generate commands, activate context backend, and generate states classes
    generate_commands(config.commands)
    database.load_backend(config.context_backend_type, config.context_backend)
    if config.states:
        generate_states(config.states)


def generate_states(states):
    """
    Read states config object and create states classes from it
    :param states: dict with states data
    :return: None
    """
    for name, config in states.items():
        attr_dict = {}
        for key, item in config.items():
            if key == COMMANDS_SECTION:
                attr_dict[key.lower()] = {
                    command_parser(key): value for key, value in config['Commands'].items()
                }
                continue
            elif key == TYPE_SECTION:
                continue
            else:
                attr_dict[key.lower()] = parse_item(item)
        state_type = config[TYPE_SECTION]
        if is_module_path(
            state_type
        ):  # TODO, FIXME: hacky way to check if requested metastate is in plugin. Refactor!
            dot_pos = state_type.rfind('.')
            metastate = getattr(importlib.import_module(state_type[:dot_pos]), state_type[dot_pos:])
        else:
            metastate = META_STATES[state_type]
        type(metastate)(name, (metastate,), attr_dict)


def parse_item(
    item: Union[dict, list], parser=command_parser, parse_list=False
) -> Union[dict, CommandDescriptor, str, List]:
    """
    Get raw item data and try to parse it to appropriate objects
    :param item: data to parse (dict, iterable, or single object)
    :param parser: callable, that takes raw value and returns it's interpretation
    :param parse_list: flag, indicating if function should return iterables unmodified
    :return: parsed configuration object
    """
    # if item is iterable - try to parse each element
    if is_vector(item):
        if not parse_list or not parser:
            return list(map(parse_item, item))
        return list(map(parser, item))
    # if item is simple object - pass it to parser
    if not isinstance(item, dict):
        if not parser:
            return item
        return parser(item)
    # if item is dict - try to parse it
    parser = None
    # choose parser based on items type
    if TYPE_SECTION in item:
        parser = PARSER_MAPPING[item[TYPE_SECTION]]
        item.pop(TYPE_SECTION)
    # recursively parse each item in object
    result = {}
    for key, value in item.items():
        new_value = parse_item(value, parser, parse_list=True)
        if isinstance(new_value, list):
            new_value = attempt_dict_join(new_value)
        result[key] = new_value
    # if we got {'value': object} return only object
    if isinstance(result, dict) and len(result) == 1 and VALUE_SECTION in result:
        return result[VALUE_SECTION]
    return result


def attempt_dict_join(attr_list: list) -> Union[list, dict]:
    """
    Merges list of 1-element or empty dicts into one dict.
    If any element is not 0 or 1 elements long or not dict - returns unmodified argument
    :param attr_list: list to try join
    :return: same list or joined dict
    """
    joined = {}
    for item in attr_list:
        if not isinstance(item, dict) or not len(item) in (0, 1):
            return attr_list
        joined.update(item)
    return joined
