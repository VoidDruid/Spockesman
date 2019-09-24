"""
Defines commands enum of all available commands
paired with their text representations that user can send.
"""
import random
from collections.abc import Iterable
from copy import copy, deepcopy

from spockesman.logger import log
from spockesman.util.singleton import singleton


class Proxy:
    def __init__(self, choices):
        self.choices = choices

    @property
    def first(self):
        return copy(self.choices[0])

    @property
    def last(self):
        return copy(self.choices[-1])

    @property
    def any(self):
        return copy(random.choice(self.choices))

    @property
    def all(self):
        return deepcopy(self.choices)

    def __contains__(self, item):
        return item in self.choices


# TODO: rewrite logic for triggers, to accept *events*
class CommandDescriptor:
    """
    Name of the command and user input that should trigger it
    """

    def __init__(self, name, triggers=None):
        self.name = name
        if not isinstance(triggers, Iterable) or isinstance(triggers, str):
            triggers = [triggers]
        self.__triggers = triggers

    @property
    def triggers(self) -> Proxy:
        return Proxy(self.__triggers)

    @property
    def trigger(self):
        return copy(self.__triggers[0])

    def __repr__(self):
        return f"<CommandDescriptor: {self.name}, triggers: {self.__triggers}>"


class CommandContainer:
    """
    Storage for pairs 'CommandName': CommandDescriptor
    """

    def __init__(self, dictionary):
        assert isinstance(dictionary, dict), 'Pass values as a dictionary'
        self.__plain_dict = dictionary.copy()
        self.__descriptors = list(self.__plain_dict.values())

    def __getattr__(self, item) -> CommandDescriptor:
        try:
            return self.__plain_dict[item]
        except KeyError:
            raise AttributeError(f'Command {item} not found')

    def __getitem__(self, item) -> CommandDescriptor:
        return self.__plain_dict[item]

    def __iter__(self):
        return iter(self.__descriptors)


@singleton
class Command:
    """
    Enum emulator.
    Allows us to refer to commands by Commands.X, instead of Command['command'],
    iterate over them, check for 'in', etc.
    """

    inner_enum = {}

    def __getitem__(self, item) -> CommandDescriptor:
        return self.inner_enum[item]

    def __iter__(self):
        return iter(self.inner_enum)

    def __getattr__(self, item) -> CommandDescriptor:
        return getattr(self.inner_enum, item)

    def __contains__(self, item):
        try:
            self.inner_enum[item]
        except KeyError:
            return False
        return True


Command = Command()


def generate_commands(config: dict) -> None:
    """
    Generate command's enum from config
    :param config: dict, command's configuration
    :return: None
    """
    Command.inner_enum = CommandContainer(
        {key: CommandDescriptor(key, value or None) for key, value in config.items()}
    )
    log.debug(f'Loaded commands. Commands are: {list(Command.inner_enum)}')
