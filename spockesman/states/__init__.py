from .command import Command
from .state import WrongCommandException, NoHandlerException, State
from .awaiting_state import AwaitingState
from .transitions import handler, global_command
from .environment import state, initial


def generate_states(data):
    for state, config in data.items():
        print(state, config)
