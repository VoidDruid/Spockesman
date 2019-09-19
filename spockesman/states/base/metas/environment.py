from spockesman.states.base.metas.exceptions import ConstantViolationException
from spockesman.util.singleton import singleton

STATES = {}
META_STATES = {}


@singleton
class InitialStateHolder:
    __name = None
    __cls = None

    @property
    def name(self) -> str:
        if self.__cls:
            return self.__cls.__name__

    @property
    def cls(self) -> type:
        return self.__cls

    @cls.setter
    def cls(self, cls):
        if self.__cls:
            raise ConstantViolationException
        self.__cls = cls


INITIAL_STATE = InitialStateHolder()


def initial(cls) -> type:
    if INITIAL_STATE.cls:
        raise ValueError(f'Only one state can be initial!\n'
                         f'Current initial state: {INITIAL_STATE.cls}, you tried to set another initial state: {cls}')
    INITIAL_STATE.cls = cls
    return cls
