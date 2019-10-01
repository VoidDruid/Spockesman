from typing import Dict, Optional

from spockesman.states.base.metas.exceptions import ConstantViolationException
from spockesman.util.singleton import singleton

STATES: Dict[str, type] = {}
META_STATES: Dict[str, type] = {}


@singleton
class InitialStateHolder:
    __name = None
    __cls = None

    @property
    def name(self) -> Optional[str]:
        if self.__cls:
            return self.__cls.__name__
        return None

    @property
    def cls(self) -> Optional[type]:
        return self.__cls

    @cls.setter
    def cls(self, cls: type) -> None:
        if self.__cls:
            raise ConstantViolationException
        self.__cls = cls


INITIAL_STATE = InitialStateHolder()


def initial(cls: type) -> type:
    if INITIAL_STATE.cls:
        raise ValueError(
            f'Only one state can be initial!\n'
            f'Current initial state: {INITIAL_STATE.cls}, '
            f'you tried to set another initial state: {cls}'
        )
    INITIAL_STATE.cls = cls
    return cls
