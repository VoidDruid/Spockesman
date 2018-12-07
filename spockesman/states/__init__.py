from .awaiting_state import AwaitingState
from .base import initial
from .commands import *
from .state import WrongCommandException, NoHandlerException, State


def generate_states(data):
    for state, config in data.items():
        print(state, config)
