from .state import State, WrongCommandException


class AwaitingState(State):
    """
    All input this state gets
    will be automatically redirected to the specified command,
    unless it's another registered *Command* or in *GLOBAL_COMMANDS*
    """
    awaiting = None

    transform = ('awaiting', )

    def __init__(self, context):
        super().__init__(context)

    def __call__(self, *args, **kwargs):
        text = args[0]
        try:
            return super().__call__(text)
        except WrongCommandException:
            return self.transition(self.awaiting)(self._context, text)
