from spockesman.logger import log
from spockesman.util.singleton import singleton

STATES = {}


@singleton
class InitialStateHolder:
    __name = None
    __cls = None

    @property
    def name(self):
        return self.__name

    @property
    def cls(self):
        return self.__cls


INITIAL_STATE = InitialStateHolder()


def initial(cls):
    INITIAL_STATE.__dict__['_InitialStateHolder__name'] = cls.__name__
    INITIAL_STATE.__dict__['_InitialStateHolder__cls'] = cls
    return cls
