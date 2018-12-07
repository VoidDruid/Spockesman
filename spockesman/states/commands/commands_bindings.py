from spockesman.logger import log

GLOBAL_COMMANDS = {}

COMMANDS = {}


def add_bound(command, handler):
    log.debug(f'Adding binded command: {command}')
    COMMANDS[command] = handler


def add_global(command, handler):
    log.debug(f'Adding global command: {command}')
    GLOBAL_COMMANDS[command] = handler
