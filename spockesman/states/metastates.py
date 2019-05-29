from .base import STATES


META_STATES = {}


def export(name):
    def decorator(cls):
        META_STATES[name] = cls
        return cls
    return decorator
