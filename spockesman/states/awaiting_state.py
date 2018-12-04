from .concrete_state import ConcreteState, WrongCommandException


class AwaitingState(ConcreteState):
    """
    All input this state gets
    will be automatically redirected to the specified command,
    unless it's another registered *Command* or in *GLOBAL_COMMANDS*
    """
    def __init__(self, context, command):
        super().__init__(context)
        self.command = command

    def __call__(self, *args, **kwargs):
        text = args[0]
        try:
            return super().__call__(text)
        except WrongCommandException:
            return self.transition(self.command)(self._context, text)
