"""Singleton implementation."""


def singleton(class_):
    """Singleton decorator for classes."""
    instances = {}

    def get_instance(*args, **kwargs):
        """Returns single existing instance of the class."""
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return get_instance
