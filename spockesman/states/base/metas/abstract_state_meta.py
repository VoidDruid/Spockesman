from abc import ABCMeta

from spockesman.states.base.metas.state_meta import StateMeta


class AbstractStateMeta(StateMeta, ABCMeta):
    pass
