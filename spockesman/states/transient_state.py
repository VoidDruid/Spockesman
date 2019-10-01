from typing import Dict, Tuple

from spockesman.states.commands import COMMANDS
from spockesman.states.state import InvalidCommandException, State
from spockesman.typings import HandlerResultType, InputType


class TransientState(State):
    """
    Metastate, that pushes user to another state if handler for input was not found
    """

    is_meta = True
    name = 'Transient'
    const = 'transition'

    transition = {'Command': None, 'State': None}

    def __call__(
        self, user_input: InputType, call_args: Tuple, **kwargs: Dict
    ) -> HandlerResultType:
        try:
            return super().__call__(user_input, call_args)
        except InvalidCommandException:
            return COMMANDS[self.transition['Command']](self.transition['State'])(  # type: ignore
                self._context, user_input, *call_args
            )
