import importlib
import yaml
from types import ModuleType

from .context.backend import database
from .logger import log
from .states import Command
from .states.base import META_STATES
from .states.commands.command import generate_commands
from .util.string import upper_and_separate


def command_parser(item):
    return Command[item]


def state_parser(item):
    return str(item)


TYPE_SECTION = 'Type'
VALUE_SECTION = 'Value'
STATES_SECTION = 'States'
COMMANDS_SECTION = 'Commands'
CONTEXT_BACKEND_SECTION = 'ContextBackend'

PARSER_MAPPING = {
    'COMMAND': command_parser,
    'STATE': state_parser,
}


class Configuration:
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
        self.context_backend_type = getattr(module, upper_and_separate(CONTEXT_BACKEND_SECTION))[TYPE_SECTION]
        self.states = getattr(module, upper_and_separate(STATES_SECTION), None)
        return self


def config_from_object(obj):
    dispatcher = {
        dict: Configuration.from_dict,
        ModuleType: Configuration.from_module
    }
    return dispatcher[type(obj)](obj)


def is_module_path(path):  # TODO, FIXME: hacky way to check if path is a path to module. Refactor!
    return '.' in path


def setup(config_pointer):
    log.debug(f"Trying to read config from '{config_pointer}'")
    if isinstance(config_pointer, str):
        if config_pointer.endswith('.yaml'):
            with open(config_pointer, 'r') as config_file:
                data = yaml.load(config_file)
        elif is_module_path(config_pointer):
            data = importlib.import_module(config_pointer)
        else:
            raise TypeError('Only .py and .yaml are supported config formats')
    else:
        data = config_pointer
    try:
        config = config_from_object(data)
    except KeyError:
        raise TypeError(f'Unsupported raw confgi object type: {type(data)}')
    generate_commands(config.commands)
    database.load_backend(config.context_backend_type, config.context_backend)
    if config.states:
        generate_states(config.states)


def generate_states(states):
    for name, config in states.items():
        attr_dict = {}
        for key, item in config.items():
            if key == COMMANDS_SECTION:
                attr_dict[key.lower()] = {command_parser(key): value for key, value in config['Commands'].items()}
                continue
            elif key == TYPE_SECTION:
                continue
            else:
                attr_dict[key.lower()] = parse_item(item)
        state_type = config[TYPE_SECTION]
        if is_module_path(state_type):  # TODO, FIXME: hacky way to check if requested metastate is in plugin. Refactor!
            dot_pos = state_type.rfind('.')
            metastate = getattr(importlib.import_module(state_type[:dot_pos]), state_type[dot_pos:])
        else:
            metastate = META_STATES[state_type]
        type(metastate)(name, (metastate,), attr_dict)


def parse_item(item, parser=command_parser, parse_list=False):
    if isinstance(item, list):
        if not parse_list or not parser:
            return list(map(parse_item, item))
        return list(map(parser, item))
    if not isinstance(item, dict):
        if not parser:
            return item
        return parser(item)
    parser = None
    if TYPE_SECTION in item:
        parser = PARSER_MAPPING[item[TYPE_SECTION]]
        item.pop(TYPE_SECTION)
    result = {}
    for key, value in item.items():
        new_value = parse_item(value, parser, parse_list=True)
        if isinstance(new_value, list):
            new_value = attempt_dict_join(new_value)
        result[key] = new_value
    if isinstance(result, dict) and len(result) == 1 and VALUE_SECTION in result:
        return result[VALUE_SECTION]
    return result


def attempt_dict_join(attr_list):
    """
    Merges list of 1-element or empty dicts into one dict.
    If any element is not 0 or 1 elements long or not dict - returns unmodified argument
    """
    for item in attr_list:
        if not isinstance(item, dict) or not len(item) in (0, 1):
            break
    else:
        res = {}
        for item in attr_list:
            res = {**res, **item}
        return res
    return attr_list


