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

    def test_custom_transform(self):
        class NewState(M.State):
            test = "Test string"
            transform = ('test',)
        with self.assertRaises(M.states.ConstantViolationException):
            NewState.test = "New string"
        with self.assertRaises(M.states.ConstantViolationException):
            NewState.commands = []

    def test_awaiting_custom_transform(self):
        class NewState(M.AwaitingState):
            test = "Test string"
            transform = ('test',)
        with self.assertRaises(M.states.ConstantViolationException):
            NewState.test = "New string"
        with self.assertRaises(M.states.ConstantViolationException):
            NewState.commands = []
        with self.assertRaises(M.states.ConstantViolationException):
            NewState.awaiting = 1

    def test_inherited_custom_transform(self):
        class NewState(M.AwaitingState):
            test = "Test string"
            transform = ('test',)

        class NewSecondState(NewState):
            transform = ('another', )
        with self.assertRaises(M.states.ConstantViolationException):
            NewSecondState.test = "New string"
        with self.assertRaises(M.states.ConstantViolationException):
            NewSecondState.commands = []
        with self.assertRaises(M.states.ConstantViolationException):
            NewSecondState.awaiting = 1
        with self.assertRaises(M.states.ConstantViolationException):
            NewSecondState.another = 1
