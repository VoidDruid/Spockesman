from .commands import Command, GLOBAL_COMMANDS, COMMANDS
from .base import BaseState
from .metastates import export

class WrongCommandException(Exception):
    pass


class NoHandlerException(Exception):
    pass


@export('Basic')
class State(BaseState):
    """Class representing general user state."""
    commands = {}

    transform = ('commands',)

    def __init__(self, context):
        self._context = context

    def __call__(self, *args, **kwargs):
        text = args[0]
        if self._context.input:
            command = Command[self._context.command]
        else:
            for command in Command:
                if command.value == text:
                    self._context.command = command.name
                    break
            else:
                raise WrongCommandException(f'No such command: {text}')
        executor = GLOBAL_COMMANDS.get(command, None)
        if not executor:
            executor = self.transition(command)
        return executor(self._context, text)

    def transition(self, command):
        if command not in self.commands:
            raise WrongCommandException(
                f"Command '{command}' is not availiable in current state"
                )
        if command not in COMMANDS:
            raise NoHandlerException(
                f"No handler registered for command '{command}'"
            )
        return COMMANDS[command](self.commands[command])

    def get_context(self):
        return self._context
