import importlib
import unittest

M = importlib.reload(importlib.import_module('spockesman'))


class ContextTest(unittest.TestCase):
    user_id = '12345'

    @classmethod
    def setUpClass(cls):
        M.load_config('tests/bot/config.yaml')

    def test_context(self):
        context = M.Context(self.user_id)
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
        context = M.Context(self.user_id, TestUnregisteredState)
        with self.assertRaises(KeyError):
            state = context.state

    def test_context_state(self):
        class TestState(M.State):
            def __init__(self, context_):
                pass
        context = M.Context(self.user_id, TestState)
        self.assertTrue(isinstance(context.state, TestState))
        self.assertDictEqual({
            'state': 'TestState',
            'input': False,
            'command': None,
            'user_id': self.user_id,
            'data': {}
        }, context.to_dict())

    def test_context_initial_state(self):
        @M.initial
        class TestInitialState(M.State):
            def __init__(self, context_):
                pass
        context = M.Context(self.user_id)
        self.assertTrue(isinstance(context.state, TestInitialState))
        self.assertDictEqual({
            'state': 'TestInitialState',
            'input': False,
            'command': None,
            'user_id': self.user_id,
            'data': {}
        }, context.to_dict())
