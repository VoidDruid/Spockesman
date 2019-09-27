from typing import Union

from spockesman.context.context import Context
from spockesman.states.base_state import BaseState
from spockesman.states.commands.command import CommandDescriptor


def default_context_transform(
    context: Context, state: BaseState, command: Union[CommandDescriptor, str]
) -> None:
    """
    Push user to new state and set last command's name
    :param context: Context object
    :param state: state name or State instance
    :param command: name of last command
    :return: None
    """
    context.state = state
    if not isinstance(command, str):
        command = command.name
    context.command = command
