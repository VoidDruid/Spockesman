from spockesman.states.commands import COMMANDS
from spockesman.states.state import State, InvalidCommandException


class CyclicState(State):
    """
    Metastate, that always calls handler of the same command,
    if it can't find another handler for input in self.commands or global commands
    """
    is_meta = True
    name = 'Cyclic'
    const = 'cycle'

    cycle = None

    def __init__(self, context):
        super().__init__(context)

    def __call__(self, *args, **kwargs):
        user_input, call_args = args[:2]
        try:
            return super().__call__(user_input, call_args)
        except InvalidCommandException:
            return COMMANDS[self.cycle](self.__class__)(self._context, user_input, *call_args)
