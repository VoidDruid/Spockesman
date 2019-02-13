from .environment import STATES
from .exceptions import ConstantViolationException


# TODO: check if constant attrs exist
class StateMeta(type):

    def __setattr__(self, name, value):
        if name in self.__dict__.get('__const_attrs', {}):
            raise ConstantViolationException()
        super().__setattr__(name, value)

    def __new__(mcs, name, bases, dct):
        try:
            const = dct['const']
        except KeyError:
            const = tuple()
        if bases:
            last_const = bases[0].__dict__['__const_attrs']
        else:
            last_const = tuple()

        dct['__const_attrs'] = frozenset((*const, *last_const))

        cls = super().__new__(mcs, name, bases, dct)
        STATES[name] = cls
        return cls
