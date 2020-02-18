import importlib
from types import ModuleType
from typing import Any, Callable, Dict, List, Optional, Union

from spockesman.context.backend import database
from spockesman.logger import log
from spockesman.states import Command
from spockesman.states.base import META_STATES
from spockesman.states.commands.command import CommandDescriptor, generate_commands
from spockesman.util.matchers import is_vector
from spockesman.util.string import upper_and_separate


# TODO, FIXME: bad check if string is a path to module. Refactor!
def is_module_path(path: str) -> bool:
    return '.' in path


def command_parser(item: str) -> CommandDescriptor:
    # 'Command' is actually subscriptable
    # pylint: disable=E1136
    return Command[item]  # type: ignore


def state_parser(item: str) -> str:
    return item


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

    commands: Dict
    context_backend: Dict
    context_backend_type: str
    states: Dict

    @classmethod
    def from_dict(cls: type, conf_dict: Dict) -> 'Configuration':
        self = cls()
        self.commands = conf_dict[COMMANDS_SECTION]
        self.context_backend = conf_dict[CONTEXT_BACKEND_SECTION]
        self.context_backend_type = conf_dict[CONTEXT_BACKEND_SECTION][TYPE_SECTION]
        self.states = conf_dict.get(STATES_SECTION, None)
        return self

    @classmethod
    def from_module(cls: type, module: ModuleType) -> 'Configuration':
        self = cls()
        self.commands = getattr(module, upper_and_separate(COMMANDS_SECTION))
        self.context_backend = getattr(module, upper_and_separate(CONTEXT_BACKEND_SECTION))
        self.context_backend_type = getattr(module, upper_and_separate(CONTEXT_BACKEND_SECTION))[
            TYPE_SECTION
        ]
        self.states = getattr(module, upper_and_separate(STATES_SECTION), None)
        return self


def config_from_object(obj: Union[Dict, ModuleType]) -> Configuration:
    """
    Create Configuration class from object with data
    :param obj: object with configuration data, module or dict
    :return: Configuration instance
    """
    dispatcher = {dict: Configuration.from_dict, ModuleType: Configuration.from_module}
    return dispatcher[type(obj)](obj)  # type: ignore


def setup(config_pointer: Union[str, ModuleType]) -> None:
    """
    Read config object and setup framework
    :param config_pointer: name of python module with configuration or module object
    :return: None
    """
    log.debug(f"Trying to read config from '{config_pointer}'")
    # if we got string, interpret it as path to something
    if isinstance(config_pointer, str):
        if is_module_path(config_pointer):
            data = importlib.import_module(config_pointer)
        else:
            raise TypeError('Config must be a valid python module')
    # else interpret it as config data
    else:
        data = config_pointer
    # try to load Configuration class from this data
    try:
        config = config_from_object(data)
    except KeyError:
        raise TypeError(f'Unsupported config object type: {type(data)}')
    # then generate commands, activate context backend, and generate states classes
    generate_commands(config.commands)
    database.load_backend(config.context_backend_type, config.context_backend)
