"""Abstract state, from which all others inherit."""

from abc import abstractmethod

from .base.metas import AbstractStateMeta, ConstantViolationException
from .metastates import ignore


@ignore
class BaseState(metaclass=AbstractStateMeta):
    """Class representing general user state."""
    commands: {}
    transform: []

    @classmethod
    def is_constant_attr(cls, name):
        if name in cls.__dict__.get('__const_list', {}):
            return True
        return False

    def __setattr__(self, name, value):
        if self.is_constant_attr(name):
            raise ConstantViolationException()
        super().__setattr__(name, value)

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass
