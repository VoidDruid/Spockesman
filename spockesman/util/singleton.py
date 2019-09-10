def singleton(klass):
    """
    Singleton decorator for classes
    :param klass: any class
    :return: function, returning singleton instance of class or creating it if it does not exist yet
    """
    instances = {}

    def get_instance(*args, **kwargs):
        """Returns single existing instance of the class."""
        if klass not in instances:
            instances[klass] = klass(*args, **kwargs)
        return instances[klass]
    return get_instance
