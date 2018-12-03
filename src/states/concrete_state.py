from .command import Command
from .global_commands import GLOBAL_COMMANDS
from .state import State


class WrongCommandException(Exception):
    pass


class ConcreteState(State):
    """Class representing general user state."""
    __commands: {}

    def __init__(self, context):
        self._context = context

    def process_input(self, text):
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
        if command not in self.__commands:
            raise WrongCommandException(
                f'Command {command} is not availiable in current state'
                )
        return self.__commands[command]

    def set_commands(self, commands):
        self.__commands = commands

    def get_commands(self):
        return self.__commands

    def get_context(self):
        return self._context
