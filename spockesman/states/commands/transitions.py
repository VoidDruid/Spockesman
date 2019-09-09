from .util import default_context_transform
from .commands_bindings import add_global, add_bound


def handler(command):
    def decorator(func):
        def wrapper_state(state):
            def wrapper(context, user_input, *call_args):
                default_context_transform(context, state, command)
                return func(context, user_input, *call_args)
            return wrapper
        add_bound(command, wrapper_state)
        return wrapper_state
    return decorator


def global_command(command, state=None):
    def decorator(func):
        def wrapper(context, user_input, *call_args):
            if state:
                context.state = state.__name__
            context.command = command.name
            return func(context, user_input, *call_args)
        add_global(command, wrapper)
        return wrapper
    return decorator
