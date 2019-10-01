from typing import Any, Callable, Iterable, Tuple, Union

from spockesman.context.context import Context
from spockesman.results import ABCResult

InputType = Union[Any, str]
_BaseHandlerResult = Union[Callable, str, ABCResult, type]
HandlerResultType = Union[_BaseHandlerResult, Iterable[_BaseHandlerResult]]
HandlerType = Callable[[Context, InputType, Tuple], HandlerResultType]
