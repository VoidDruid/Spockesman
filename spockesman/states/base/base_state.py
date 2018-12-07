"""Abstract state, from which all others inherit."""

from abc import abstractmethod

from .metas import AbstractStateMeta


class BaseState(metaclass=AbstractStateMeta):
    """Class representing general user state."""
    __commands__: {}

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass
