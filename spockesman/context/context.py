from copy import deepcopy
from typing import Union, Optional

from spockesman.states.base import INITIAL_STATE, STATES
from spockesman.states.base_state import BaseState


# TODO:
#  - input to __input and methods is_input, set_input
#  - custom data classes, store data object class
#  - command to __command and property getter
class Context:
    """
    User context. Contains user's id, state, last command, and arbitrary additional data
    """
    def __init__(self, user_id: str, state: BaseState = None, data: Union[list, dict] = None):
        self.user_id = user_id
        self.__state = None
        self.state = state
        self.input = False
        self.command = None
        if data is None:
            self.data = {}
        else:
            self.data = data

    def to_dict(self) -> dict:
        data_dump = {}
        if isinstance(self.data, dict) or isinstance(self.data, list):
            data_dump = self.data
        # TODO - for now left as-is, so I don't forget the idea
        #elif hasattr(self.data, 'to_dict'):
        #    data_dump = self.data.to_dict()
        return {
            'state': self.__state,
            'input': self.input,
            'command': self.command,
            'user_id': self.user_id,
            'data': data_dump
        }

    def clone(self, context) -> None:
        self.__state = context.state
        self.input = context.input
        self.command = context.command
        self.data = deepcopy(context.data)

    @property
    def state(self) -> Optional[BaseState]:
        if self.__state is None:
            return None
        return STATES[self.__state](self)

    @state.setter
    def state(self, state_: Union[None, str, BaseState]):
        if not state_:
            self.__state = INITIAL_STATE.name
            return
        elif isinstance(state_, str):
            state_name = state_
        elif isinstance(state_, type) and issubclass(state_, BaseState):
            state_name = state_.name
        else:
            raise TypeError(
                f'State for context must be either a subclass of BaseState or string, '
                f'not a {type(state_)}'
            )
        if state_name not in STATES:
            raise ValueError(
                f"State {state_} is not registered! Maybe it's a metastate? "
                f"If so, set flag is_meta to False, or user concrete state"
            )
        self.__state = state_name

    @classmethod
    def from_dict(cls, data):
        context = cls(data['user_id'], data['state'])
        context.input = data.get('input', False)
        context.command = data.get('command', None)
        context.data = data.get('data', {})
        return context

    def __getitem__(self, item):
        return self.data[item]
