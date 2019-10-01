from importlib import import_module
from typing import Any, Dict, Iterable, Iterator, Optional

from spockesman.context.backend.abstract import AbstractBackend
from spockesman.context.context import Context
from spockesman.util.singleton import singleton


class BackendNotLoaded(Exception):
    pass


@singleton
class Database:
    """
    Singleton class, presenting interface for working with users' contexts
    """

    protected = ('deactivate_backend', 'load', 'save', '__iter__', 'delete', 'delete_all')
    active: AbstractBackend = None  # type: ignore

    def __getattribute__(self, item: str) -> Any:
        if item in super().__getattribute__('protected') and not super().__getattribute__(
            'activated'
        ):
            raise BackendNotLoaded
        return super().__getattribute__(item)

    @property
    def activated(self) -> bool:
        return bool(self.active)

    def load_backend(self, name: str, config: Dict) -> None:
        try:
            back = import_module('spockesman.context.backend.' + name)
        except ImportError:  # load plugin module
            back = import_module(name)  # TODO: support plugins in format spockesman.backend.*
        try:
            self.active = back.activate(config)  # type: ignore
        except AttributeError:
            raise TypeError(
                f'Tried to load invalid backend module <{name}> '
                f'- module has no <activate> attribute.\n'
                f'Refer to spockesman.context.backend.redis '
                f'for example of backend provider module.\n'
                f'Imported module: {back}'
            )

    def deactivate_backend(self) -> bool:
        if not self.active:
            return True
        return self.active.deactivate()

    def load(self, user_id: str) -> Optional[Context]:
        return self.active.load(user_id)

    def save(self, context: Context) -> None:
        return self.active.save(context)

    def delete(self, *user_ids: Iterable[str]) -> None:
        return self.active.delete(*user_ids)

    def delete_all(self) -> None:
        return self.active.delete_all()

    def __iter__(self) -> Iterator[Context]:
        return iter(self.active)


database = Database()
