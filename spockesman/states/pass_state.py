from .commands import COMMANDS
from .state import State, WrongCommandException
from .metastates import export


@export('Pass')
class PassState(State):
    passer = {
        'Command': None,
        'State': None
    }

    const = ('passer',)

    def __call__(self, *args, **kwargs):
        text = args[0]
        try:
            return super().__call__(text)
        except WrongCommandException:
            return COMMANDS[self.passer['Command']](self.passer['State'])(self._context, text)
