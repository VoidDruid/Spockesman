from .commands import Command, GLOBAL_COMMANDS, COMMANDS
from .base_state import BaseState
from .metastates import export


class WrongCommandException(Exception):
    pass


class NoHandlerException(Exception):
    pass


@export('Basic')
class State(BaseState):
    """Class representing general user state."""
    is_meta = True
    const = ('default',)

    default = None

    def __init__(self, context):
        self._context = context

    def __call__(self, *args, **kwargs):
        user_input = args[0]
        if self._context.input:
            command = Command[self._context.command]
        else:
            # TODO: optimize search for command
            for command in Command:
                if user_input in command.triggers:
                    self._context.command = command.name
                    break
            else:
                raise WrongCommandException(f'No such command: {user_input}')
        binding = GLOBAL_COMMANDS.get(command, None)
        if not binding:
            binding = self.transition(command)
        return self.run(binding, user_input)

    def run(self, binding, user_input):
        if not callable(binding) or isinstance(binding, type):
            if isinstance(binding, type) and not issubclass(binding, BaseState):
                raise TypeError(f'Incorrect command binding type! Got type: {type(binding)} '
                                f'for input: {user_input} in state {type(self).__name__}')
            return binding
        return binding(self._context, user_input)

    def transition(self, command):
        if command not in self.commands:
            raise WrongCommandException(
                f"Command '{command}' is not available in current state"
                )
        if command not in COMMANDS:
            raise NoHandlerException(
                f"No handler registered for command '{command}'"
            )
        return COMMANDS[command](self.commands[command])

    def get_context(self):
        return self._context
