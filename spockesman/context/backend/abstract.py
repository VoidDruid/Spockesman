from abc import ABCMeta, abstractmethod


class AbstractBackend(metaclass=ABCMeta):
    """Class representing abstract backend."""

    @abstractmethod
    def load(self, user_id):
        pass

    @abstractmethod
    def save(self, context):
        pass

    @abstractmethod
    def delete(self, *user_ids):
        pass

    @abstractmethod
    def delete_all(self):
        pass

    @abstractmethod
    def __iter__(self):
        pass
