from abc import ABCMeta


class ABCResult(metaclass=ABCMeta):
    """Abstract base class for results of transitions (functions bound to state graph's edges)"""
