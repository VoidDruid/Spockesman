from .commands import COMMANDS
from .state import State, InvalidCommandException


class TransientState(State):
    is_meta = True
    name = 'Transient'
    const = 'transition'

    transition = {
        'Command': None,
        'State': None
    }

    def __call__(self, *args, **kwargs):
        text = args[0]
        try:
            return super().__call__(text)
        except InvalidCommandException:
            return COMMANDS[self.transition['Command']](self.transition['State'])(self._context, text)
