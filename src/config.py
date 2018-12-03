import yaml

from .states.command import generate_commands, Command
from .context.backend import database

COMMANDS_SECTION = 'Commands'
CONTEXT_BACKEND_SECTION = 'ContextBackend'


def load_config(file):
    if isinstance(file, str):
        file = open(file, 'r')
    data = yaml.load(file)
    generate_commands(data[COMMANDS_SECTION])
    database.load_backend(data[CONTEXT_BACKEND_SECTION]['Type'], data[CONTEXT_BACKEND_SECTION])
