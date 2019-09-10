from collections import Iterable


def is_vector(obj):
    """
    Checks if object os a 'true iterable'
    :param obj: any object
    :return: true if object is iterable and not a string or a dict, else false
    """
    return isinstance(obj, Iterable) and not isinstance(obj, (str, dict))
