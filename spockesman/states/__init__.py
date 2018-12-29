from .awaiting_state import AwaitingState
from .base import initial
from .commands import *
from .state import WrongCommandException, NoHandlerException, State
from .metastates import META_STATES, export


def generate_states(states):
    for name, config in states.items():
        attr_dict = {}
        # TODO: process all custom attributes, maybe add feature to specify parsing for custom attrs
        for key, item in config.items():
            if key == 'Commands':
                attr_dict[key.lower()] = {Command[key]: value for key, value in config['Commands'].items()}
                continue
            elif key == 'Type':
                continue
            attr_dict[key.lower()] = Command[item]
        type(META_STATES[config['Type']])(name, (META_STATES[config['Type']],), attr_dict)
