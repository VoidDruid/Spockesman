"""
Defines commands enum of all available commands
paired with their text representations that user can send.
"""
from enum import Enum, auto

from spockesman.logger import log
from spockesman.util.singleton import singleton


# TODO: rewrite logic for triggers
class CommandDescriptor:
    def __init__(self, text, additional_triggers=None):
        self.text = text
        if additional_triggers is None:
            self.triggers = {text}
        else:
            self.triggers = {*additional_triggers, text}


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
    Command.inner_enum = Enum('Command', {key: (value if value else auto()) for key, value in config.items()},
                              module=__name__)
    log.debug(f'Loaded commands. Commands are: {list(Command.inner_enum)}')
