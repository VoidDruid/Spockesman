from ..states.environment import STATES, INITIAL_STATE


class Context:
    def __init__(self, user_id, state=INITIAL_STATE.name):
        self.user_id = user_id
        self.__state = None
        self.state = state
        self.input = False
        self.command = None

    def to_dict(self):
        return {
            'state': self.state,
            'input': self.input,
            'command': self.command,
            'user_id': self.user_id
        }

    @property
    def state(self):
        return STATES[self.__state]

    @state.setter
    def state(self, state_):
        if isinstance(state_, type):
            self.__state = state_.__name__
        else:
            self.__state = state_

    @classmethod
    def from_dict(cls, data):
        context = cls(data['user_id'], data['state'])
        context.input = data.get('input', False)
        context.command = data.get('command', None)
        return context
