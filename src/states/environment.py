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
    STATES[cls.__name__] = cls
    return cls


def initial(cls):
    cls = state(cls)
    INITIAL_STATE.__dict__['__name'] = cls.__name__
    INITIAL_STATE.__dict__['__cls'] = cls
    return cls
