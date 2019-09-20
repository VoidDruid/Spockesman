from .util import BaseTestCase


class ConstantsTest(BaseTestCase):
    user_id = '12345'

    @classmethod
    def setUpClass(cls):
        cls.setUpPackage(cls)
        cls.context = cls.M.Context(cls.user_id)

    def test_basic_constants(self):
        with self.assertRaises(self.M.states.ConstantViolationException):
            self.M.State.commands = []
        with self.assertRaises(self.M.states.ConstantViolationException):
            self.M.CyclicState.commands = []
        with self.assertRaises(self.M.states.ConstantViolationException):
            self.M.CyclicState.cycle = 1

    def test_default_state_constants(self):
        state = self.M.State(self.context)
        with self.assertRaises(self.M.states.ConstantViolationException):
            state.commands = []

    def test_cyclic_state_constants(self):
        state = self.M.CyclicState(self.context)
        with self.assertRaises(self.M.states.ConstantViolationException):
            state.commands = []
        with self.assertRaises(self.M.states.ConstantViolationException):
            state.cycle = 1

    def test_custom_const(self):
        class NewState(self.M.State):
            test = "Test string"
            const = ('test',)
        with self.assertRaises(self.M.states.ConstantViolationException):
            NewState.test = "New string"
        with self.assertRaises(self.M.states.ConstantViolationException):
            NewState.commands = []

    def test_cyclic_custom_const(self):
        class NewState(self.M.CyclicState):
            test = "Test string"
            const = ('test',)
        with self.assertRaises(self.M.states.ConstantViolationException):
            NewState.test = "New string"
        with self.assertRaises(self.M.states.ConstantViolationException):
            NewState.commands = []
        with self.assertRaises(self.M.states.ConstantViolationException):
            NewState.cycle = 1

    def test_inherited_custom_const(self):
        class NewState(self.M.CyclicState):
            test = "Test string"
            const = ('test',)

        class NewSecondState(NewState):
            const = ('another', )
        with self.assertRaises(self.M.states.ConstantViolationException):
            NewSecondState.test = "New string"
        with self.assertRaises(self.M.states.ConstantViolationException):
            NewSecondState.commands = []
        with self.assertRaises(self.M.states.ConstantViolationException):
            NewSecondState.cycle = 1
        with self.assertRaises(self.M.states.ConstantViolationException):
            NewSecondState.another = 1
