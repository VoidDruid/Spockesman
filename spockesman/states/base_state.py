"""Abstract state, from which all others inherit."""

from abc import ABCMeta, abstractmethod


class BaseState(metaclass=ABCMeta):
    """Class representing general user state."""
    __commands__: {}

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass

    @abstractmethod
    def transition(self, command):
        pass

    @abstractmethod
    def get_context(self):
        pass
