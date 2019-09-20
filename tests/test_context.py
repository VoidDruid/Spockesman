from .util import BaseTestCase


class ContextTest(BaseTestCase):
    user_id = '12345'

    @classmethod
    def setUpClass(cls):
        cls.setUpPackage(cls)
        cls.M.setup('tests/config.yaml')

    def test_context(self):
        context = self.M.Context(self.user_id)
        self.assertDictEqual({
            'state': None,
            'input': False,
            'command': None,
            'user_id': self.user_id,
            'data': {}
        }, context.to_dict())

    def test_raises_on_unregistered(self):
        class TestUnregisteredState:
            def __init__(self, context_):
                pass
        with self.assertRaises(TypeError):
            self.M.Context(self.user_id, TestUnregisteredState)

    def test_context_state(self):
        class TestState(self.M.State):
            def __init__(self, context_):
                pass
        context = self.M.Context(self.user_id, TestState)
        self.assertTrue(isinstance(context.state, TestState))
        self.assertDictEqual({
            'state': 'TestState',
            'input': False,
            'command': None,
            'user_id': self.user_id,
            'data': {}
        }, context.to_dict())

    def test_context_initial_state(self):
        @self.M.initial
        class TestInitialState(self.M.State):
            def __init__(self, context_):
                pass
        context = self.M.Context(self.user_id)
        self.assertTrue(isinstance(context.state, TestInitialState))
        self.assertDictEqual({
            'state': 'TestInitialState',
            'input': False,
            'command': None,
            'user_id': self.user_id,
            'data': {}
        }, context.to_dict())
