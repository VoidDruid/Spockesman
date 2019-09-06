"""Abstract state, from which all others inherit."""

from abc import abstractmethod

from .base.metas import AbstractStateMeta, ConstantViolationException


class BaseState(metaclass=AbstractStateMeta):
    """Class representing general user state."""
    const = ('commands', 'is_meta', 'name', 'default')
    is_meta = True
    commands = {}
    default = None
    name = None  # TODO: add validation for uniqueness

    @classmethod
    def is_constant_attr(cls, name):
        if name in cls.__dict__.get('__const_attrs', {}):
            return True
        return False

    def __setattr__(self, name, value):
        if self.is_constant_attr(name):
            raise ConstantViolationException()
        super().__setattr__(name, value)

    def __getattribute__(self, name):
        if name == 'name':
            if not self.name:
                return type(self).__name__
            return self.name
        return super().__getattribute__(name)

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass
