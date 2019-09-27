from importlib import import_module
from typing import Dict, Any, Optional, Iterable, Iterator

from spockesman.util.singleton import singleton
from spockesman.context.context import Context
from spockesman.context.backend.abstract import AbstractBackend


class BackendNotLoaded(Exception):
    pass


@singleton
class Database:
    """
    Singleton class, presenting interface for working with users' contexts
    """

    active: AbstractBackend = None  # type: ignore

    def __getattr__(self, item: str) -> Any:
        if item not in ('active', 'load_backend') and not self.activated:
            raise BackendNotLoaded
        return getattr(self, item)

    @property
    def activated(self) -> bool:
        return bool(self.active)

    def load_backend(self, name: str, config: Dict) -> None:
        try:
            back = import_module('spockesman.context.backend.' + name)
        except ImportError:  # load plugged-in module
            back = import_module(name)  # TODO: support plugins in format spockesman.backend.*
        try:
            self.active = back.activate(config)  # type: ignore
        except AttributeError:
            raise TypeError(
                f"Tried to load invalid backend module <{name}> "
                f"- module has no <activate> attribute.\n"
                f"Refer to spockesman.context.backend.redis "
                f"for example of backend provider module.\n"
                f"Imported module: {back}"
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
