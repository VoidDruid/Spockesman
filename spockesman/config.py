import yaml

from .context.backend import database
from .logger import log
from .states import generate_states
from .states.command import generate_commands

COMMANDS_SECTION = 'Commands'
CONTEXT_BACKEND_SECTION = 'ContextBackend'


def load_config(file):
    log.debug(f"Trying to read config from '{file}'")
    if isinstance(file, str):
        file = open(file, 'r')
    with file:
        data = yaml.load(file)
        generate_commands(data[COMMANDS_SECTION])
        database.load_backend(data[CONTEXT_BACKEND_SECTION]['Type'], data[CONTEXT_BACKEND_SECTION])
        states = data.get('States', None)
        if states:
            generate_states(states)
