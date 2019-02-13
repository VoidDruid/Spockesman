from copy import deepcopy

from .environment import STATES
from .exceptions import ConstantViolationException


# TODO: check if constant attrs exist
class StateMeta(type):

    def __setattr__(self, name, value):
        if name in self.__dict__.get('__const_list', {}):
            raise ConstantViolationException()
        super().__setattr__(name, value)

    def __new__(mcs, name, bases, dct):
        try:
            const = dct['const']
        except KeyError:
            const = tuple()
        if bases:
            last_const = bases[0].const
        else:
            last_const = tuple()

        const = tuple({*const, *last_const})
        
        dct['const'] = const
        dct['__const_list'] = [*const]

        cls = super().__new__(mcs, name, bases, dct)
        STATES[name] = cls
        return cls
