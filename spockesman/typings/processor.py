from typing import Optional, Union, List

from spockesman.results import ABCResult

ProcessingResult = Optional[Union[ABCResult, List[ABCResult]]]
