import yaml

from .states.command import generate_commands


def read_commands(file):
    if isinstance(file, str):
        file = open(file, 'r')
    data = yaml.load(file)
