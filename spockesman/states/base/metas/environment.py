from .exceptions import ConstantViolationException
from spockesman.logger import log
from spockesman.util.singleton import singleton

STATES = {}
META_STATES = {}

@singleton
class InitialStateHolder:
    __name = None
    __cls = None

    @property
    def name(self):
        if self.__cls:
            return self.__cls.__name__

    @property
    def cls(self):
        return self.__cls

    @cls.setter
    def cls(self, cls):
        if self.__cls:
            raise ConstantViolationException
        self.__cls = cls


INITIAL_STATE = InitialStateHolder()


def initial(cls):
    INITIAL_STATE.cls = cls
    return cls
