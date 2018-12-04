from ..logger import log
from ..util.singleton import singleton

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


def state(cls):
    log.debug(f'Registering state {cls.__name__}')
    STATES[cls.__name__] = cls
    return cls


def initial(cls):
    cls = state(cls)
    log.debug(f'Setting initial state: {cls.__name__}')
    INITIAL_STATE.__dict__['_InitialStateHolder__name'] = cls.__name__
    INITIAL_STATE.__dict__['_InitialStateHolder__cls'] = cls
    return cls
