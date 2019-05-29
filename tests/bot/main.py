from tests.bot.bot import bot
from spockesman import CyclicState, Command, State, global_command, handler, initial, setup

setup('tests/bot/config.yaml')


@handler(Command.Start)
def start(context, user_input):
    return 'Привет!', None


@handler(Command.Echo)
def echo(context, user_input):
    return user_input, None


@handler(Command.End)
def end(context, user_input):
    return 'Пока!', None


@global_command(Command.Hi)
def hi(context, user_input):
    return 'Hello!', None


class MainState(CyclicState):
    Cyclic = Command.Echo
    commands = {
            Command.Echo: 'MainState',
            Command.End: 'InitialState'
        }


@initial
class InitialState(State):
    commands = {
            Command.Start: 'MainState'
        }