from typing import Any, Callable

from spockesman.logger import log
from spockesman.states.base_state import BaseState
from spockesman.states.commands.command import CommandDescriptor
from spockesman.typings import HandlerType

GLOBAL_COMMANDS = {}

COMMANDS = {}


def add_bound(command: CommandDescriptor, handler: Callable[[BaseState], Any]) -> None:
    """
    Adds command handler to bound commands dict
    :param command: handled Command
    :param handler: callable, generator function that accepts state
                    and returns handler (state graph's edge)
    :return: Any
    """
    log.debug(f'Adding bound command: {command}')
    COMMANDS[command] = handler


def add_global(command: CommandDescriptor, handler: HandlerType) -> None:
    """
    Adds command handler to global dict
    :param command: handled Command
    :param handler: callable, commands handler
    :return: Any
    """
    log.debug(f'Adding global command: {command}')
    GLOBAL_COMMANDS[command] = handler
