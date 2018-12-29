"""Abstract state, from which all others inherit."""

from abc import abstractmethod

from .base.metas import AbstractStateMeta
from .metastates import ignore


@ignore
class BaseState(metaclass=AbstractStateMeta):
    """Class representing general user state."""
    commands: {}
    transform: []

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass
