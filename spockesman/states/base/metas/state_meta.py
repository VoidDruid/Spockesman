from collections import Iterable

from spockesman.states.base.metas.const import *
from spockesman.states.base.metas.environment import STATES, META_STATES
from spockesman.states.base.metas.exceptions import ConstantViolationException


# TODO: required attrs
# TODO: implement check if constant attrs exist
class StateMeta(type):
    """Metaclass for all states, implements logic that joins them into state graph"""

    def __setattr__(self, name, value):
        if name in self.__dict__.get(CONST_PRIVATE_NAME, {}):
            raise ConstantViolationException()
        super().__setattr__(name, value)

    def __new__(mcs, name, bases, dct):
        const = dct.get(CONST_PUBLIC_NAME)
        is_meta = dct.get(IS_META_NAME, False)  # it will probably be useful later
        state_name = dct.get(NAME_FIELD_NAME, None)
        if state_name is None:
            state_name = name
            dct[NAME_FIELD_NAME] = name

        if not const:  # if const attr for class is empty, create empty tuple
            const = tuple()
        else:
            if isinstance(const, Iterable):
                if isinstance(const, str):
                    const = (const,)
            else:
                raise TypeError(
                    '<const> class attribute must be either an iterable of strings or a string'
                )
        if bases:  # get last parents const
            last_const = bases[0].__dict__[CONST_PRIVATE_NAME]
        else:
            last_const = tuple()
        dct[CONST_PRIVATE_NAME] = frozenset((*const, *last_const))  # join consts

        cls = super().__new__(mcs, name, bases, dct)  # create type
        if is_meta:  # save it
            META_STATES[state_name] = cls
        else:
            STATES[state_name] = cls
        return cls
