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
        back = import_module('.'+name, package=__name__)
        self.active = back.activate(config)

    def load(self, user_id):
        return self.active.load(user_id)

    def save(self, user_id, context):
        return self.active.save(user_id, context)

    def delete(self, *user_id):
        return self.active.delete(user_id)

    def delete_all(self):
        return self.active.delete_all()

    def __iter__(self):
        return iter(self.active)


database = Database()


__all__ = ['database', 'BackendNotLoaded']
