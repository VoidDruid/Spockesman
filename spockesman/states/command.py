"""
Defines commands enum of all available commands
paired with their text representations that user can send.
"""
from enum import Enum, auto

from ..logger import log
from ..util.singleton import singleton


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
