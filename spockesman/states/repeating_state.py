from .commands import COMMANDS
from .state import State, WrongCommandException
from .metastates import export


@export('Repeating')
class RepeatingState(State):
    """
    All input this state gets
    will be automatically redirected to the specified command,
    unless it's another registered *Command* or in *GLOBAL_COMMANDS*
    """
    repeating = None

    const = ('repeating', )

    def __init__(self, context):
        super().__init__(context)

    def __call__(self, *args, **kwargs):
        text = args[0]
        try:
            return super().__call__(text)
        except WrongCommandException:
            return COMMANDS[self.repeating](self.__class__)(self._context, text)
