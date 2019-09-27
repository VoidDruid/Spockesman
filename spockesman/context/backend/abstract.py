from abc import ABCMeta, abstractmethod
from typing import Iterable, Iterator, Optional

from spockesman.context.context import Context


class AbstractBackend(metaclass=ABCMeta):
    """Class representing abstract backend for storing backends."""

    def deactivate(self) -> bool:
        return True

    @abstractmethod
    def load(self, user_id: str) -> Optional[Context]:
        pass

    @abstractmethod
    def save(self, context: Context) -> None:
        pass

    @abstractmethod
    def delete(self, *user_ids: Iterable[str]) -> None:  # TODO: return list of actually deleted ids
        pass

    @abstractmethod
    def delete_all(self) -> None:  # TODO: return list of deleted ids
        pass

    @abstractmethod
    def __iter__(self) -> Iterator[Context]:
        pass
