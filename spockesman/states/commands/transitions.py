from typing import Callable

from spockesman.context.context import Context
from spockesman.states.base_state import BaseState
from spockesman.states.commands.util import default_context_transform
from spockesman.states.commands.commands_bindings import add_global, add_bound
from spockesman.states.commands.command import CommandDescriptor
from spockesman.typings import HandlerResultType, InputType


def handler(command: CommandDescriptor) -> Callable:
    """
    :param command: Command that decorated function handles
    :return: callable - decorator closure
    """

    def decorator(func: Callable) -> Callable:
        """
        :param func: decorated function
        :return: callable, that binds handler to final state
        """

        def wrapper_state(state: BaseState) -> Callable:
            """
            :param state: state name or State instance
            :return: callable - wrapper around original function
            """

            def wrapper(context: Context, user_input: InputType, *call_args) -> HandlerResultType:
                """
                Actual wrapper for original function
                :param context: user's context, Context instance
                :param user_input: input, any object
                :param call_args: addition arguments, can be empty
                :return: Any
                """
                default_context_transform(context, state, command)
                return func(context, user_input, *call_args)

            return wrapper

        add_bound(command, wrapper_state)
        return wrapper_state

    return decorator


def global_command(command: CommandDescriptor, state: BaseState = None):
    """
    :param command: Command that decorated function handles
    :param state: state for user after execution of handler
    :return: callable - decorator closure
    """

    def decorator(func: Callable) -> Callable:
        """
        :param func: decorated function
        :return: callable - wrapper around original function
        """

        def wrapper(context: Context, user_input: InputType, *call_args) -> HandlerResultType:
            """
            Actual wrapper for original function
            :param context: user's context, Context instance
            :param user_input: input, any object
            :param call_args: addition arguments, can be empty
            :return: Any
            """
            if state:
                context.state = state.__name__
            context.command = command.name
            return func(context, user_input, *call_args)

        add_global(command, wrapper)
        return wrapper

    return decorator
