from typing import Optional, Iterable, Union

from spockesman.results import ABCResult

ProcessingResult = Optional[Union[ABCResult, Iterable[ABCResult]]]
