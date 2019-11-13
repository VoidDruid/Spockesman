import random
from copy import copy, deepcopy
from typing import List, Iterable as IterableType, Tuple, Iterable

from spockesman.typings import InputType


class ListProxy:
    def __init__(self, choices: List[InputType]) -> None:
        self.choices = choices

    @property
    def first(self) -> InputType:
        return copy(self.choices[0])

    @property
    def last(self) -> InputType:
        return copy(self.choices[-1])

    @property
    def any(self) -> InputType:
        return copy(random.choice(self.choices))

    @property
    def all(self) -> List[InputType]:
        return deepcopy(self.choices)

    def __contains__(self, item: InputType) -> bool:
        return item in self.choices


def flatten(sequence: IterableType) -> Tuple:
    result = []
    for item in sequence:
        if not isinstance(item, Iterable) or isinstance(item, str):
            result.append(item)
        else:
            result.extend(flatten(item))
    return tuple(result)
