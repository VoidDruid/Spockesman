from spockesman.logger import log

GLOBAL_COMMANDS = {}

COMMANDS = {}


def add_bound(command, handler) -> None:
    """
    Adds command handler to global dict
    :param command: handled Command
    :param handler: callable, generator funtion that accepts state and returns handler (state graph's edge)
    :return: Any
    """
    log.debug(f'Adding bound command: {command}')
    COMMANDS[command] = handler


def add_global(command, handler) -> None:
    """
    Adds command handler to global dict
    :param command: handled Command
    :param handler: callable, commands handler
    :return: Any
    """
    log.debug(f'Adding global command: {command}')
    GLOBAL_COMMANDS[command] = handler
