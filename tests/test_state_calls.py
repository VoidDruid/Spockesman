import importlib
import unittest

from .util import reload, BaseTestCase


class StateCallsTest(BaseTestCase):
    user_id = '12345'

    hello_ru = ('Привет!', None)
    hello_eng = ('Hello!', None)
    bye_ru = ('Пока!', None)
    pass_ru = ('Поехали', None)

    @classmethod
    def setUpClass(cls):
        cls.M = reload()
        cls.STATES = cls.M.states.base.STATES
        cls.M.setup('tests/config.yaml')
        cls.context = cls.M.Context(cls.user_id)

        @cls.M.handler(cls.M.Command.Start)
        def start(context, user_input):
            return cls.hello_ru

        @cls.M.handler(cls.M.Command.Echo)
        def echo(context, user_input):
            return user_input, None

        @cls.M.handler(cls.M.Command.End)
        def end(context, user_input):
            return cls.bye_ru

        @cls.M.handler(cls.M.Command.Passd)
        def passd(context, user_input):
            return cls.pass_ru

        @cls.M.handler(cls.M.Command.Hi)
        def hi_h(context, user_input):
            return cls.hello_eng

    def setUp(self):
        self.context = self.M.Context(self.user_id)

    def test_basic_state_f(self):
        self.assertEqual(self.STATES['Main'](self.context)('/start', ()), self.hello_ru)
        self.assertEqual(type(self.context.state).__name__, 'Repeat')

    def test_basic_state_s(self):
        self.assertEqual(self.STATES['Main'](self.context)('/hi', ()), self.hello_eng)
        self.assertEqual(type(self.context.state).__name__, 'Transient')

    def test_repeat_state(self):
        self.context.state = 'Repeat'
        self.assertEqual(self.context.state.cycle, self.M.Command.Echo)
        self.assertEqual(self.STATES['Repeat'](self.context)('lalala', ()), ('lalala', None))
        self.assertEqual(type(self.context.state).__name__, 'Repeat')

    def test_exit_repeat_state(self):
        self.context.state = 'Repeat'
        self.assertIn(self.M.Command.End, self.context.state.commands)
        self.assertEqual(self.STATES['Repeat'](self.context)('/end', ()), self.bye_ru)
        self.assertEqual(type(self.context.state).__name__, 'Main')

    def test_pass_state(self):
        self.context.state = 'Transient'
        self.assertTrue(hasattr(self.context.state, 'transition'))
        self.assertEqual(self.STATES['Transient'](self.context)('lala', ()), self.pass_ru)
        self.assertEqual(type(self.context.state).__name__, 'Repeat')
