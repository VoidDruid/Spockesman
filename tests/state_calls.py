import unittest
import importlib

M = importlib.reload(importlib.import_module('spockesman'))
STATES = M.states.base.STATES


class StateCallsTest(unittest.TestCase):
    user_id = '12345'
    context = M.Context(user_id)
    hello_ru = ('Привет!', None)
    hello_eng = ('Hello!', None)
    bye_ru = ('Пока!', None)
    pass_ru = ('Поехали', None)

    @classmethod
    def setUpClass(cls):
        M.load_config('tests/bot/config.yaml')

        @M.handler(M.Command.Start)
        def start(context, user_input):
            return cls.hello_ru

        @M.handler(M.Command.Echo)
        def echo(context, user_input):
            return user_input, None

        @M.handler(M.Command.End)
        def end(context, user_input):
            return cls.bye_ru

        @M.handler(M.Command.Passd)
        def passd(context, user_input):
            return cls.pass_ru

        @M.handler(M.Command.Hi)
        def hi_h(context, user_input):
            return cls.hello_eng

    def setUp(self):
        self.context = M.Context(self.user_id)

    def test_basic_state_f(self):
        self.assertEqual(STATES['Main'](self.context)('/start'), self.hello_ru)
        self.assertEqual(type(self.context.state).__name__, 'Repeat')

    def test_basic_state_s(self):
        self.assertEqual(STATES['Main'](self.context)('/hi'), self.hello_eng)
        self.assertEqual(type(self.context.state).__name__, 'Transient')

    def test_repeat_state(self):
        self.context.state = 'Repeat'
        self.assertEqual(self.context.state.cycle, M.Command.Echo)
        self.assertEqual(STATES['Repeat'](self.context)('lalala'), ('lalala', None))
        self.assertEqual(type(self.context.state).__name__, 'Repeat')

    def test_exit_repeat_state(self):
        self.context.state = 'Repeat'
        self.assertIn(M.Command.End, self.context.state.commands)
        self.assertEqual(STATES['Repeat'](self.context)('/end'), self.bye_ru)
        self.assertEqual(type(self.context.state).__name__, 'Main')

    def test_pass_state(self):
        self.context.state = 'Transient'
        self.assertTrue(hasattr(self.context.state, 'transition'))
        self.assertEqual(STATES['Transient'](self.context)('lala'), self.pass_ru)
        self.assertEqual(type(self.context.state).__name__, 'Repeat')
