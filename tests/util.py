import sys
import importlib
import unittest

PACKAGE_NAME = 'spockesman'


def reload():
    to_pop = []
    M = sys.modules.get(PACKAGE_NAME)
    if M:
        if M.context.backend.database.active:
            M.context.backend.database.deactivate_backend()
        for module_name, module in sys.modules.items():
            if module_name.startswith(PACKAGE_NAME):
                to_pop.append(module_name)
        for module_name in to_pop:
            sys.modules.pop(module_name)
    return importlib.reload(importlib.import_module(PACKAGE_NAME))


class BaseTestCase(unittest.TestCase):
    @staticmethod
    def setUpPackage(cls):
        cls.M = reload()

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'M') and cls.M.context.backend.database.active:
            cls.M.context.backend.database.delete_all()
