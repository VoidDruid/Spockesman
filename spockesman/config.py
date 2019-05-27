import importlib
import yaml
from types import ModuleType

from .context.backend import database
from .logger import log
from .states import META_STATES, Command
from .states.commands.command import generate_commands


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
        # TODO: load config from module
        return self


def config_from_object(obj):
    dispatcher = {
        dict: Configuration.from_dict,
        ModuleType: Configuration.from_module
    }
    return dispatcher[type(obj)](obj)


def setup(config_pointer):
    log.debug(f"Trying to read config from '{config_pointer}'")
    if isinstance(config_pointer, str):
        if config_pointer.endswith('.yaml'):
            with open(config_pointer, 'r') as config_file:
                data = yaml.load(config_file)
        elif config_pointer.endswith('.py'):
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
        type(META_STATES[config[TYPE_SECTION]])(name, (META_STATES[config[TYPE_SECTION]],), attr_dict)


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
            new_value = attempt_join(new_value)
        result[key] = new_value
    if isinstance(result, dict) and len(result) == 1 and VALUE_SECTION in result:
        return result[VALUE_SECTION]
    return result


def attempt_join(attr_list):
    for item in attr_list:
        if not isinstance(item, dict) or not len(item) in (0, 1):
            break
    else:
        res = {}
        for item in attr_list:
            res = {**res, **item}
        return res
    return attr_list


