from typing import Callable, Iterable, Union, Any, Tuple

from spockesman.context.context import Context
from spockesman.results import ABCResult

InputType = Union[Any, str]
_BaseHandlerResult = Union[Callable, str, ABCResult, type]
HandlerResultType = Union[_BaseHandlerResult, Iterable[_BaseHandlerResult]]
HandlerType = Callable[[Context, InputType, Tuple], HandlerResultType]
