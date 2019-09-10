from example.bot import bot
from example.message import Message
import example.config as config

from spockesman import CyclicState, Command, State, global_command, handler, initial, setup, Context

setup(config)


@handler(Command.Echo)
def echo(context, user_input):
    return Message(user_input + ' Command.Echo')


@handler(Command.Start)
def start(context, user_input):
    return Message('Привет! Command.Start')


@handler(Command.End)
def end(context: Context, user_input):
    return Message('Пока! Command.End')


@global_command(Command.Hi)
def hi(context, user_input):
    return Message('Hey! Command.Hi')


@initial
class InitialState(State):
    default = Message('Добро пожаловать в бота!')
    commands = {
            Command.Start: 'MainState',
        }


class MainState(CyclicState):
    cycle = Command.Echo
    commands = {
            Command.End: 'InitialState',
        }


print('Starting!')
bot.start_method()
