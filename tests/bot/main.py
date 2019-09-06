from tests.bot.bot import bot
from tests.bot.message import Message
import tests.bot.config as config

from spockesman import CyclicState, Command, State, global_command, handler, initial, setup, Context

setup(config)


@handler(Command.Echo)
def echo(context, user_input):
    return Message(user_input)


@handler(Command.Start)
def start(context, user_input):
    return Message('Привет!')


@handler(Command.End)
def end(context: Context, user_input):
    return Message('Пока!')


@global_command(Command.Hi)
def hi(context, user_input):
    return Message('Hello!')


class MainState(CyclicState):
    cycle = Command.Echo
    commands = {
            Command.End: 'InitialState',
        }


@initial
class InitialState(State):
    default = Message('Добро пожаловать в бота!')
    commands = {
            Command.Start: 'MainState',
        }


print('STARTING!')
bot.start_method()
