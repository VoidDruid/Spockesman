from .base import STATES


META_STATES = {}


def ignore(cls):
    STATES.pop(cls.__name__, None)
    return cls


def export(name):
    def decorator(cls):
        META_STATES[name] = cls
        # TODO there should be a cleaner way to do it
        STATES.pop(cls.__name__, None)
        return cls
    return decorator
