import unittest

from .util import reload, BaseTestCase


class BackendTest(BaseTestCase):
    user_id = '09876'

    # TODO: create separate tests for different backends
    # NOTE: we need local spockesman instance to test different backends
    def test_backend(self):
        local_M = reload()
        local_M.setup('tests/config.yaml')
        context = local_M.Context(self.user_id)
        local_M.context.backend.database.save(context)
        loaded_context = local_M.context.backend.database.load(self.user_id)
        self.assertDictEqual(context.to_dict(), loaded_context.to_dict())
