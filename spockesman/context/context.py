from copy import deepcopy

from spockesman.states.base import INITIAL_STATE, STATES


# TODO:
#  - input to __input and methods is_input, set_input
#  - custom data classes, store data object class
#  - command to __command and property getter
class Context:
    def __init__(self, user_id, state=None, data=None):
        self.user_id = user_id
        self.__state = None
        self.state = state
        self.input = False
        self.command = None
        if data is None:
            self.data = {}
        else:
            self.data = data

    def to_dict(self):
        if isinstance(self.data, dict) or isinstance(self.data, list):
            data_dump = self.data
        #elif hasattr(self.data, 'to_dict'):
        #    data_dump = self.data.to_dict()
        return {
            'state': self.__state,
            'input': self.input,
            'command': self.command,
            'user_id': self.user_id,
            'data': data_dump
        }

    def clone(self, context):
        self.__state = context.state
        self.input = context.input
        self.command = context.command
        self.data = deepcopy(context.data)

    @property
    def state(self):
        return STATES[self.__state](self)

    @state.setter
    def state(self, state_):
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
