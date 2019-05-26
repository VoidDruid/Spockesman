from .results.result import ABCResult
from .states.base_state import BaseState
from .context.backend import BackendNotLoaded, database
from .logger import log
from .states import WrongCommandException, NoHandlerException


def parse_callable(obj, context, user_input):
    if callable(obj):
        return obj(context, user_input)
    return obj


# transforms result received from state into Result or list of Results [Message, Message, ...]
def parse_result(result, context, user_input):
    if not result or issubclass(result, ABCResult):
        return result
    if isinstance(result, list):
        return [parse_result(part, context, user_input) for part in result]
    # if we got state, return its defaults
    elif issubclass(result, BaseState):
        context.state = result.get_name()
        return parse_callable(result.default, context, user_input)
    # if we received callable, call it assuming the interface func(context, user_input) and parse its result
    elif callable(result):
        return parse_result(result(context, user_input), context,  user_input)
    raise TypeError(f"Value {result} returned by state call is not valid type : {type(result)}")


def process(user_id, user_input, context=None, save=True):
    log.debug(f"Processing input: '{user_input}', user: '{user_id}'")
    if not context:
        try:
            context = database.load(user_id)
        except BackendNotLoaded:
            log.exception(f"Tried to process input '{user_input}', user: '{user_id}',"
                          f"but context storage backend was not initialized and no context was passed")
            return None
    try:
        result = parse_result(context.state(user_input), context, user_input)
    except TypeError:
        log.exception(f"Tried to process input '{user_input}', user: '{user_id}',"
                      f"input is a command, handler was found, but returned value is invalid")
        return None
    except WrongCommandException:
        log.exception(f"Tried to process input '{user_input}', user: '{user_id}', but input is neither global command, "
                      f"or a command available in current state: {type(context.state).__name__}")
        return None
    except NoHandlerException:
        log.exception(f"Tried to process input '{user_input}', user: '{user_id}',"
                      f"input is a command, but no handler for it was found.")
        return None
    finally:
        if save:
            database.save(user_id, context)
    return result
