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
        #elif hasattr(self.data, 'to_dict'):  # FIXME, for now left as-is
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
            state_ = INITIAL_STATE.name
        if isinstance(state_, type):
            self.__state = state_.__name__
        else:
            self.__state = state_

    @classmethod
    def from_dict(cls, data):
        context = cls(data['user_id'], data['state'])
        context.input = data.get('input', False)
        context.command = data.get('command', None)
        context.data = data.get('data', {})
        return context

    def __getitem__(self, item):
        return self.data[item]
