from importlib import import_module

from ...util.singleton import singleton


class BackendNotLoaded(Exception):
    pass


@singleton
class Database:
    active = None

    def __getattr__(self, item):
        if item not in ('active', 'load_backend') and not self.activated:
            raise BackendNotLoaded
        else:
            return getattr(self, item)

    @property
    def activated(self):
        return bool(self.active)

    def load_backend(self, name, config):
        try:
            back = import_module('spockesman.context.backend.' + name)
        except ImportError:  # load plugged-in module
            back = import_module(name)  # TODO: support plugins in format spockesman.backend.*
        try:
            self.active = back.activate(config)
        except AttributeError:
            raise TypeError(f"Tried to load invalid backend module <{name}> - module has no <activate> attribute.\n"
                            f"Refer to spockesman.context.backend.redis for example of backend provider module.\n"
                            f"Imported module: {back}")

    def load(self, user_id):
        return self.active.load(user_id)

    def save(self, context):
        return self.active.save(context)

    def delete(self, *user_id):
        return self.active.delete(user_id)

    def delete_all(self):
        return self.active.delete_all()

    def __iter__(self):
        return iter(self.active)


database = Database()

