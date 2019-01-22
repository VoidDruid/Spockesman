from copy import deepcopy

from .environment import STATES
from .exceptions import ConstantViolationException

class StateMeta(type):

    def __setattr__(self, name, value):
        if name in self.__dict__.get('__const_list', {}):
            raise ConstantViolationException()
        super().__setattr__(name, value)

    def __new__(mcs, name, bases, dct):
        try:
            transform = dct['transform']
        except KeyError:
            transform = tuple()
        if bases:
            last_transform = bases[0].transform
        else:
            last_transform = tuple()

        transform = tuple({*transform, *last_transform})
        
        dct['transform'] = transform
        dct['__const_list'] = [*transform]

        cls = super().__new__(mcs, name, bases, dct)
        STATES[name] = cls
        return cls
