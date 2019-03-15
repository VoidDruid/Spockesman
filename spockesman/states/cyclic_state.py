from .commands import COMMANDS
from .state import State, WrongCommandException
from .metastates import export


@export('Cyclic')
class CyclicState(State):
    """
    All input this state gets
    will be automatically redirected to the specified command,
    unless it's another registered *Command* or in *GLOBAL_COMMANDS*
    """
    cycle = None

    const = ('cycle', )

    def __init__(self, context):
        super().__init__(context)

    def __call__(self, *args, **kwargs):
        text = args[0]
        try:
            return super().__call__(text)
        except WrongCommandException:
            return COMMANDS[self.cycle](self.__class__)(self._context, text)
