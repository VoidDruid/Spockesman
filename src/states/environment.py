STATES = {}
INITIAL_STATE = None


def state(cls):
    STATES[cls.__name__] = cls
    return cls


def initial(cls):
    global INITIAL_STATE
    STATES[cls.__name__] = cls
    INITIAL_STATE = cls.__name__
    return cls
