from typing import Callable, Tuple, Dict

from spockesman.context.context import Context
from spockesman.states.commands import Command, GLOBAL_COMMANDS, COMMANDS
from spockesman.states.commands.command import CommandDescriptor
from spockesman.states.base_state import BaseState
from spockesman.typings import HandlerResultType, InputType


class InvalidCommandException(Exception):
    pass


class NoHandlerException(Exception):
    pass


class State(BaseState):
    """
    Basic state.
    Represents a node in state's graph, for any input tries to find handler in self.commands,
    throws InvalidCommandException if does not find any.
    """

    is_meta = True
    name = 'Basic'

    def __init__(self, context: Context) -> None:
        """
        Created concrete state graph node for user with context
        :param context: user's context
        """
        self._context = context

    def __call__(
        self, user_input: InputType, call_args: Tuple, **kwargs: Dict
    ) -> HandlerResultType:
        """
        Executes state machine logic,
        for user with context passed to __init__, and triggered by user_input
        :param user_input: input, that triggered transition
        :param call_args: additional arguments
        :param kwargs: additional keyword arguments  TODO: use them
        :return:
        """
        if self._context.input:
            # 'Command' is actually subscriptable
            # pylint: disable=E1136
            command = Command[self._context.command]  # type: ignore
        else:
            # TODO: optimize search for command
            # 'Command' is actually iterable
            for command in Command:  # type: ignore # pylint: disable=E1133
                if user_input in command.triggers:
                    self._context.command = command.name
                    break
            else:
                raise InvalidCommandException(f'No such command: {user_input}')
        binding = GLOBAL_COMMANDS.get(command, None)
        if not binding:
            binding = self.find_transition(command)
        return self.run(binding, user_input, call_args)

    def run(self, binding: Callable, user_input: InputType, call_args: Tuple) -> HandlerResultType:
        """
        Runs transition, triggered by user.
        :param binding: callable, representing state graph's edge
        :param user_input: input, that triggered transition
        :param call_args: additional arguments
        :return: return value of binding
        """
        if not callable(binding) or isinstance(binding, type):
            if isinstance(binding, type) and not issubclass(binding, BaseState):
                raise TypeError(
                    f'Incorrect command binding type! Got type: {type(binding)} '
                    f'for input: {user_input} in state {type(self).__name__}'
                )
            return binding
        return binding(self._context, user_input, *call_args)

    def find_transition(self, command: CommandDescriptor) -> Callable:
        """
        Finds and returns callable, representing state graph's edge, bound to specified command
        :param command: command which we are looking for
        :return: callable, bound to command
        """
        if command not in self.commands:
            raise InvalidCommandException(f"Command '{command}' is not available in current state")
        if command not in COMMANDS:
            raise NoHandlerException(f"No handler registered for command '{command}'")
        return COMMANDS[command](self.commands[command])

    def get_context(self) -> Context:
        return self._context
