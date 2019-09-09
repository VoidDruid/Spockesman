"""
Defines commands enum of all available commands
paired with their text representations that user can send.
"""
import random
from collections.abc import Iterable
from copy import copy, deepcopy
from enum import Enum, auto

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
    def __init__(self, name, triggers=None):
        self.name = name
        if not isinstance(triggers, Iterable) or isinstance(triggers, str):
            triggers = [triggers]
        self.__triggers = triggers

    @property
    def triggers(self):
        return Proxy(self.__triggers)

    @property
    def trigger(self):
        return copy(self.__triggers[0])

    def __repr__(self):
        return f"<CommandDescriptor: {self.name}, triggers: {self.__triggers}>"


class CommandContainer:
    def __init__(self, dictionary):
        assert isinstance(dictionary, dict), 'Pass values as a dictionary'
        self.__plain_dict = dictionary.copy()
        self.__descriptors = list(self.__plain_dict.values())

    def __getattr__(self, item):
        try:
            return self.__plain_dict[item]
        except KeyError:
            raise AttributeError(f'Command {item} not found')

    def __getitem__(self, item):
        return self.__plain_dict[item]

    def __iter__(self):
        return iter(self.__descriptors)


@singleton
class Command:
    """
    User input that should trigger command
    and button names if command is intended to be a button
    Also, allows us to refer to commands by Commands.X, instead of "command".
    """
    inner_enum = {}

    def __getitem__(self, item):
        return self.inner_enum[item]

    def __iter__(self):
        return iter(self.inner_enum)

    def __getattr__(self, item):
        return getattr(self.inner_enum, item)

    def __contains__(self, item):
        try:
            self.inner_enum[item]
        except KeyError:
            return False
        return True


Command = Command()


def generate_commands(config):
    Command.inner_enum = CommandContainer({
        key: CommandDescriptor(key, value or None) for key, value in config.items()
    })
    log.debug(f'Loaded commands. Commands are: {list(Command.inner_enum)}')
