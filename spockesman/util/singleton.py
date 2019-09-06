"""Singleton implementation."""


def singleton(klass):
    """Singleton decorator for classes."""
    instances = {}

    def get_instance(*args, **kwargs):
        """Returns single existing instance of the class."""
        if klass not in instances:
            instances[klass] = klass(*args, **kwargs)
        return instances[klass]
    return get_instance
