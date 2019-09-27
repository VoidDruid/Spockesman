from typing import Callable, Any, Dict


def singleton(cls: type) -> Callable[..., Any]:
    """
    Singleton decorator for classes
    :param cls: any class
    :return: function, returning singleton instance of class or creating it if it does not exist yet
    """
    instances: Dict[type, Any] = {}

    def get_instance(*args: Any, **kwargs: Any) -> Any:
        """Returns single existing instance of the class."""
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance
