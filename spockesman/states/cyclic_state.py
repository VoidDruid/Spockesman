from typing import Tuple, Dict

from spockesman.states.commands import COMMANDS
from spockesman.states.state import State, InvalidCommandException
from spockesman.typings import HandlerResultType, InputType


class CyclicState(State):
    """
    Metastate, that always calls handler of the same command,
    if it can't find another handler for input in self.commands or global commands
    """

    is_meta = True
    name = 'Cyclic'
    const = 'cycle'

    cycle = None

    def __call__(
        self, user_input: InputType, call_args: Tuple, **kwargs: Dict
    ) -> HandlerResultType:
        try:
            return super().__call__(user_input, call_args)
        except InvalidCommandException:
            return COMMANDS[self.cycle](self.__class__)(  # type: ignore
                self._context, user_input, *call_args
            )
