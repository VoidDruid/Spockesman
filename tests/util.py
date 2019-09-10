import sys
import importlib
import unittest

PACKAGE_NAME = 'spockesman'


def reload():
    to_pop = []
    for module_name, module in sys.modules.items():
        if module_name.startswith(PACKAGE_NAME):
            to_pop.append(module_name)
    for module_name in to_pop:
        sys.modules.pop(module_name)
    return importlib.reload(importlib.import_module(PACKAGE_NAME))


class BaseTestCase(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'M'):
            if cls.M.context.backend.database.active:
                cls.M.context.backend.database.delete_all()
