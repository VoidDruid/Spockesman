from typing import Callable, Iterable, Union, List, Any

from spockesman.results import ABCResult
from spockesman.states.base_state import BaseState

BaseHandlerResult = Union[Callable, str, ABCResult, BaseState, List, Iterable]
HandlerResultType = Union[BaseHandlerResult, Iterable[BaseHandlerResult]]

InputType = Union[Any, str]
