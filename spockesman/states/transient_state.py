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
        user_input, call_args = args[:2]
        try:
            return super().__call__(user_input, call_args)
        except InvalidCommandException:
            return COMMANDS[self.transition['Command']](self.transition['State'])(self._context, user_input, *call_args)
