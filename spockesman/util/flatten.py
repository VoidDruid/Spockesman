from collections.abc import Iterable
from typing import Iterable as IterableType
from typing import Tuple


def flatten(sequence: IterableType) -> Tuple:
    result = []
    for item in sequence:
        if not isinstance(item, Iterable) or isinstance(item, str):
            result.append(item)
        else:
            result.extend(flatten(item))
    return tuple(result)
