from .awaiting_state import AwaitingState
from .base import initial
from .commands import *
from .state import WrongCommandException, NoHandlerException, State
from .metastates import META_STATES, export


def generate_states(states):
    for name, config in states:
        attr_dict = {}
        # TODO: process all custom attributes, maybe add feature to specify parsing for custom attrs
        for key, item in config:
            if key == 'Commands':
                attr_dict['Commands'] = {Command[key]: value for key, value in config['Commands']}
            attr_dict[key] = Command[item]
        type(name, META_STATES[config['Type']], attr_dict)
