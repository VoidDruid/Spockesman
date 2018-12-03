"""Abstract state, from which all others inherit."""

from abc import ABCMeta, abstractmethod


class State(metaclass=ABCMeta):
    """Class representing general user state."""
    __commands: {}

    @abstractmethod
    def process_input(self, text):
        pass

    @abstractmethod
    def transition(self, command):
        pass

    @abstractmethod
    def set_commands(self, commands):
        pass

    @abstractmethod
    def get_commands(self):
        pass

    def get_context(self):
        pass
