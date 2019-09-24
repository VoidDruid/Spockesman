from uuid import uuid4

import spockesman

from .util import reload, BaseTestCase


class CustomContext(spockesman.Context):
    def __init__(self, *args, new_field=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.new_field = new_field


# NOTE: In this test case, we need local spockesman instances to test different backends
class BackendTest(BaseTestCase):
    @staticmethod
    def add_data(context):
        context.store('int', 1)
        context.store('bool', True)
        context.store('float', 3.3)
        context.store('str', 'string')
        context.store('list', ['string', 1, 3.3, True])
        context.store('dict', {'dict': True, '1': 3.3})

    def simple_context_check(self, M):
        user_id = uuid4().hex
        context = M.Context(user_id)
        self.add_data(context)
        M.context.backend.database.save(context)
        loaded_context = M.context.backend.database.load(user_id)
        self.assertDictEqual(context.to_dict(), loaded_context.to_dict())

    def test_backend_from_config(self):
        M = reload()
        M.setup('tests/config.yaml')
        self.simple_context_check(M)

    def test_sqlite_backend(self):
        M = reload()
        M.context.backend.database.load_backend('sqlite_backend', {'Name': 'test_db'})
        self.simple_context_check(M)

    def test_sqlite_backend_additional_fields(self):
        M = reload()
        M.context.backend.database.load_backend('sqlite_backend', {'Name': 'test_db'})
        user_id = uuid4().hex
        context = CustomContext(user_id, new_field='new_field_value')
        self.add_data(context)
        M.context.backend.database.save(context)
        loaded_context = M.context.backend.database.load(user_id)
        self.assertEqual(loaded_context.new_field, 'new_field_value')
        self.assertDictEqual(context.to_dict(), loaded_context.to_dict())
        self.assertEqual(type(loaded_context), CustomContext)

    # TODO: tests for redis backend
