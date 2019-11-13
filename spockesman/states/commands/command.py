"""
Defines commands enum of all available commands
paired with their text representations that user can send.
"""
from collections.abc import Iterable
from copy import copy
from typing import Dict, Iterator, List, Optional

from spockesman.logger import log
from spockesman.typings import InputType
from spockesman.util.singleton import singleton
from spockesman.util.list import ListProxy


# TODO: rewrite logic for triggers, to accept *events*
class CommandDescriptor:
    """
    Name of the command and user input that should trigger it
    """

    def __init__(self, name: str, triggers: Optional[List[InputType]] = None):
        self.name = name
        if not isinstance(triggers, Iterable) or isinstance(triggers, str):
            triggers = [triggers]
        self.__triggers = triggers

    @property
    def triggers(self) -> ListProxy:
        return ListProxy(self.__triggers)

    @property
    def trigger(self) -> InputType:
        return copy(self.__triggers[0])

    def __repr__(self) -> str:
        return f'<CommandDescriptor: {self.name}, triggers: {self.__triggers}>'


class CommandContainer:
    """
    Storage for pairs 'CommandName': CommandDescriptor
    """

    def __init__(self, dictionary: Dict[str, CommandDescriptor]) -> None:
        assert isinstance(dictionary, dict), 'Pass values as a dictionary'
        self.__plain_dict = dictionary.copy()
        self.__descriptors = list(self.__plain_dict.values())

    def __getattr__(self, item: str) -> CommandDescriptor:
        try:
            return self.__plain_dict[item]
        except KeyError:
            raise AttributeError(f'Command {item} not found')

    def __getitem__(self, item: str) -> CommandDescriptor:
        return self.__plain_dict[item]

    def __iter__(self) -> Iterator[CommandDescriptor]:
        return iter(self.__descriptors)


@singleton
class Command:
    """
    Enum emulator.
    Allows us to refer to commands by Commands.X, instead of Command['command'],
    iterate over them, check for 'in', etc.
    """

    inner_enum: CommandContainer = {}  # type: ignore

    def __getitem__(self, item: str) -> CommandDescriptor:
        return self.inner_enum[item]

    def __iter__(self) -> Iterator[CommandDescriptor]:
        return iter(self.inner_enum)

    def __getattr__(self, item: str) -> CommandDescriptor:
        return getattr(self.inner_enum, item)

    def __contains__(self, item: str) -> bool:
        try:
            self.inner_enum[item]
        except KeyError:
            return False
        return True


Command = Command()  # type: ignore


def generate_commands(config: Dict[str, List[InputType]]) -> None:
    """
    Generate command's enum from config
    :param config: dict, command's configuration
    :return: None
    """
    Command.inner_enum = CommandContainer(
        {key: CommandDescriptor(key, value or None) for key, value in config.items()}
    )
    log.debug(f'Loaded commands. Commands are: {list(Command.inner_enum)}')
