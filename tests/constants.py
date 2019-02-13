import unittest
import importlib

M = importlib.import_module('spockesman')


class ConstantsTest(unittest.TestCase):
    user_id = '12345'
    context = M.Context(user_id)

    def test_basic_constants(self):
        with self.assertRaises(M.states.ConstantViolationException):
            M.State.commands = []
        with self.assertRaises(M.states.ConstantViolationException):
            M.AwaitingState.commands = []
        with self.assertRaises(M.states.ConstantViolationException):
            M.AwaitingState.awaiting = 1

    def test_default_state_constants(self):
        state = M.State(self.context)
        with self.assertRaises(M.states.ConstantViolationException):
            state.commands = []

    def test_awaiting_state_constants(self):
        state = M.AwaitingState(self.context)
        with self.assertRaises(M.states.ConstantViolationException):
            state.commands = []
        with self.assertRaises(M.states.ConstantViolationException):
            state.awaiting = 1

    def test_custom_const(self):
        class NewState(M.State):
            test = "Test string"
            const = ('test',)
        with self.assertRaises(M.states.ConstantViolationException):
            NewState.test = "New string"
        with self.assertRaises(M.states.ConstantViolationException):
            NewState.commands = []

    def test_awaiting_custom_const(self):
        class NewState(M.AwaitingState):
            test = "Test string"
            const = ('test',)
        with self.assertRaises(M.states.ConstantViolationException):
            NewState.test = "New string"
        with self.assertRaises(M.states.ConstantViolationException):
            NewState.commands = []
        with self.assertRaises(M.states.ConstantViolationException):
            NewState.awaiting = 1

    def test_inherited_custom_const(self):
        class NewState(M.AwaitingState):
            test = "Test string"
            const = ('test',)

        class NewSecondState(NewState):
            const = ('another', )
        with self.assertRaises(M.states.ConstantViolationException):
            NewSecondState.test = "New string"
        with self.assertRaises(M.states.ConstantViolationException):
            NewSecondState.commands = []
        with self.assertRaises(M.states.ConstantViolationException):
            NewSecondState.awaiting = 1
        with self.assertRaises(M.states.ConstantViolationException):
            NewSecondState.another = 1
