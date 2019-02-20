import yaml

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

PARSER_MAPPING = {
    'COMMAND': command_parser,
    'STATE': state_parser,
}

COMMANDS_SECTION = 'Commands'
CONTEXT_BACKEND_SECTION = 'ContextBackend'


def load_config(file):
    log.debug(f"Trying to read config from '{file}'")
    if isinstance(file, str):
        file = open(file, 'r')
    with file:
        data = yaml.load(file)
        generate_commands(data[COMMANDS_SECTION])
        database.load_backend(data[CONTEXT_BACKEND_SECTION]['Type'], data[CONTEXT_BACKEND_SECTION])
        states = data.get('States', None)
        if states:
            generate_states(states)


def generate_states(states):
    for name, config in states.items():
        attr_dict = {}
        for key, item in config.items():
            if key == 'Commands':
                attr_dict[key.lower()] = {command_parser(key): value for key, value in config['Commands'].items()}
                continue
            elif key == 'Type':
                continue
            else:
                attr_dict[key.lower()] = parse_item(item)
        type(META_STATES[config['Type']])(name, (META_STATES[config['Type']],), attr_dict)


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


