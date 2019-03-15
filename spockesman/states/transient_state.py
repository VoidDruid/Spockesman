from .commands import COMMANDS
from .state import State, WrongCommandException
from .metastates import export


@export('Transient')
class TransientState(State):
    transition = {
        'Command': None,
        'State': None
    }

    const = ('transition',)

    def __call__(self, *args, **kwargs):
        text = args[0]
        try:
            return super().__call__(text)
        except WrongCommandException:
            return COMMANDS[self.transition['Command']](self.transition['State'])(self._context, text)
