import unittest
import importlib

M = importlib.import_module('spockesman')


class ConstantsTest(unittest.TestCase):
    user_id = '12345'
    context = M.Context(user_id)

    def test_default_state_constants(self):
        state = M.State(self.context)

        def test_commands_exception():
            state.commands = []
        self.assertRaises(M.states.ConstantViolationException, test_commands_exception)

    def test_awaiting_state_constants(self):
        state = M.AwaitingState(self.context)

        def test_commands_exception():
            state.commands = []

        def test_awaiting_exception():
            state.awaiting = 1
        self.assertRaises(M.states.ConstantViolationException, test_commands_exception)
        self.assertRaises(M.states.ConstantViolationException, test_awaiting_exception)

# TODO: tests for custom states
