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

    def process_input(self, text):
        try:
            return super().process_input(text)
        except WrongCommandException:
            return self.transition(self.command)(self._context, text)
