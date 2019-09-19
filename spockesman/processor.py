from collections import Iterable
from typing import Callable, Optional, List, Union

from spockesman.results.result import ABCResult
from spockesman.states.base_state import BaseState
from spockesman.context import Context
from spockesman.context.backend import BackendNotLoaded, database
from spockesman.logger import log
from spockesman.states import InvalidCommandException, NoHandlerException
from spockesman.states.base import STATES
from spockesman.typings import InputType, HandlerResultType, ProcessingResult


def parse_callable(
        obj: Callable,
        context: Context,
        user_input: InputType,
        call_args: tuple
) -> ProcessingResult:
    return parse_result(obj(context, user_input, *call_args), context,  user_input, call_args)


def check_callable(
        obj: Union[Callable, ProcessingResult],
        context: Context,
        user_input: InputType,
        call_args: tuple
) -> ProcessingResult:
    if callable(obj):
        return parse_callable(obj, context, user_input, call_args)
    return obj


def parse_result(
        result: HandlerResultType,
        context: Context,
        user_input: InputType,
        call_args: tuple
) -> ProcessingResult:
    """
    Transform result received from state into Result or list of Results
    :param result: any object, received from processing user's input
    :param context: Context object
    :param user_input: User's input - can be any object
    :param call_args: additional arguments, received by 'process' previously, can be empty
    :return: None, ABCResult, List[ABCResult]
    """
    if isinstance(result, str):
        state = STATES.get(result, None)
        if state is None:
            raise TypeError(f"Got string {result} as result. Strings are only accepted if it's a state's name")
        result = state
    # if we got state, return its default
    if isinstance(result, type) and issubclass(result, BaseState):
        context.state = result.name
        return check_callable(result.default, context, user_input, call_args)
    elif not result or isinstance(result, ABCResult):
        return result
    elif isinstance(result, Iterable):
        return [parse_result(part, context, user_input, call_args) for part in result]
    # if we received callable, call it assuming the interface func(context, user_input, *args)
    # and parse its result
    elif callable(result):
        return parse_callable(result, context,  user_input, call_args)
    raise TypeError(f"Value {result} returned by state call is not valid type : {type(result)}")


def process(
        user_id: str,
        user_input: InputType,
        *call_args,
        context: Context = None,
        save: bool = True
) -> ProcessingResult:
    """
    Load user's context, find handler for input and execute it
    :param user_id: id of current user
    :param user_input: user's input, any object
    :param call_args: additional arguments, will be passed to handler, can be empty
    :param context: None if context should be loaded from backend storage, or Context object
    :param save: flag indicating if Context should be saved to backend after execution
    :return: None, ABCResult, List[ABCResult]
    """
    log.debug(f"Processing input: '{user_input}', user: '{user_id}'")
    # Try loading context from backend if it was not provided
    if not context:
        try:
            context = database.load(user_id)
        except BackendNotLoaded:
            raise BackendNotLoaded(
                f"Tried to process input '{user_input}', user: '{user_id}',"
                f"but context storage backend was not initialized and no context was passed"
            )
    try:
        # if we no context was found, create new one and return initial states default
        if not context:
            context = Context(user_id)
            result = context.state.default
        else:  # else - call state
            result = context.state(user_input, call_args)
        final_result = parse_result(result, context, user_input, call_args)
    # catch exceptions and add info messages.
    # we do it here to avoid duplicating error messages everywhere
    except TypeError:
        raise TypeError(
            f"Tried to process input '{user_input}', user: '{user_id}', "
            f"input is a command, handler was found, but returned value is invalid"
        )
    except InvalidCommandException:
        raise InvalidCommandException(
            f"Tried to process input '{user_input}', user: '{user_id}',"
            f"but input is neither global command, "
            f"or a command available in current state: {type(context.state).__name__}"
        )
    except NoHandlerException:
        raise NoHandlerException(
            f"Tried to process input '{user_input}', user: '{user_id}', "
            f"input is a command, but no handler for it was found."
        )
    else:
        if save:
            database.save(context)
        return final_result
