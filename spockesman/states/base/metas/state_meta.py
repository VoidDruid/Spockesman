from .const import *
from .environment import STATES
from .exceptions import ConstantViolationException


# TODO: required attrs
# TODO: check if constant attrs exist
class StateMeta(type):

    def __setattr__(self, name, value):
        if name in self.__dict__.get(CONST_PRIVATE_NAME, {}):
            raise ConstantViolationException()
        super().__setattr__(name, value)

    def __new__(mcs, name, bases, dct):
        const = dct.get(CONST_PUBLIC_NAME)
        if not const:
            const = tuple()
        if bases:
            last_const = bases[0].__dict__[CONST_PRIVATE_NAME]
        else:
            last_const = tuple()
        dct[CONST_PRIVATE_NAME] = frozenset((*const, *last_const))
        cls = super().__new__(mcs, name, bases, dct)
        STATES[name] = cls
        return cls
