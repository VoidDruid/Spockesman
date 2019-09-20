from .util import reload, BaseTestCase


# NOTE: In this test case, we need local spockesman instances to test different backends
class BackendTest(BaseTestCase):
    user_id = '09876'

    @classmethod
    def setUpClass(cls):
        """We don't need class-wide M in this TestCase"""
        pass

    # TODO: create separate tests for different backends
    def test_backend_from_config(self):
        M = reload()
        M.setup('tests/config.yaml')
        context = M.Context(self.user_id)
        M.context.backend.database.save(context)
        loaded_context = M.context.backend.database.load(self.user_id)
        self.assertDictEqual(context.to_dict(), loaded_context.to_dict())
