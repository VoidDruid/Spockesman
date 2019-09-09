from .results.result import ABCResult
from .states.base_state import BaseState
from .context import Context
from .context.backend import BackendNotLoaded, database
from .logger import log
from .states import InvalidCommandException, NoHandlerException
from .states.base import STATES


def check_callable(obj, context, user_input):
    if callable(obj):
        return obj(context, user_input)
    return obj


# transforms result received from state into Result or list of Results [Message, Message, ...]
def parse_result(result, context, user_input):
    if isinstance(result, str):
        state = STATES.get(result, None)
        if state is None:
            raise TypeError(f"Got string {result} as result. Strings are only accepted if it's a state's name")
        result = state
    # if we got state, return its default
    if issubclass(result, BaseState):
        context.state = result.name
        return check_callable(result.default, context, user_input)
    elif not result or isinstance(result, ABCResult):
        return result
    elif isinstance(result, list):
        return [parse_result(part, context, user_input) for part in result]
    # if we received callable, call it assuming the interface func(context, user_input) and parse its result
    elif callable(result):
        return parse_result(result(context, user_input), context,  user_input)
    raise TypeError(f"Value {result} returned by state call is not valid type : {type(result)}")


def process(user_id, user_input, *call_args, context=None, save=True):
    log.debug(f"Processing input: '{user_input}', user: '{user_id}'")
    if not context:
        try:
            context = database.load(user_id)
        except BackendNotLoaded:
            raise BackendNotLoaded(f"Tried to process input '{user_input}', user: '{user_id}',"
                                   f"but context storage backend was not initialized and no context was passed")
    no_exceptions = False
    try:
        if not context:
            context = Context(user_id)
            result = context.state.default
        else:
            result = context.state(user_input, call_args)
        final_result = parse_result(result, context, user_input)
    except TypeError:
        raise TypeError(f"Tried to process input '{user_input}', user: '{user_id}', "
                        f"input is a command, handler was found, but returned value is invalid")
    except InvalidCommandException:
        raise InvalidCommandException(
            f"Tried to process input '{user_input}', user: '{user_id}', but input is neither global command, "
            f"or a command available in current state: {type(context.state).__name__}"
        )
    except NoHandlerException:
        raise NoHandlerException(f"Tried to process input '{user_input}', user: '{user_id}', "
                                 f"input is a command, but no handler for it was found.")
    else:
        no_exceptions = True
        return final_result
    finally:
        if save and no_exceptions:
            database.save(context)
