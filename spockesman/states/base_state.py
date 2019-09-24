"""Abstract state, from which all others inherit."""

from abc import abstractmethod

from spockesman.states.base.metas import AbstractStateMeta, ConstantViolationException


class BaseState(metaclass=AbstractStateMeta):
    """
    Abstract class representing general user state.

    """

    # List of class attributes that should not be modified
    const = ('commands', 'is_meta', 'name', 'default')
    # Shows if class is a node in states graph or a 'template'.
    # Default is False (handled by metaclass)
    is_meta = True
    commands = {}  # dict of node's vertices
    default = None  # object that will be returned to processor if user got to this sate
    name = None  # state's name TODO: add validation for uniqueness

    @classmethod
    def is_constant_attr(cls, name) -> bool:
        # __const_attrs are added by metaclass, based on this class's 'const'
        # and 'const' of it's parents
        if name in cls.__dict__.get('__const_attrs', {}):
            return True
        return False

    def __setattr__(self, name, value):
        # prevents changing values of constant attributes
        if self.is_constant_attr(name):
            raise ConstantViolationException()
        super().__setattr__(name, value)

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass
