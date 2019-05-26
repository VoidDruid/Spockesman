import importlib
import unittest

M = importlib.reload(importlib.import_module('spockesman'))
STATES = M.states.base.STATES


class ConfigTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        M.load_config('tests/bot/config.yaml')

    def test_commands(self):
        self.assertIn('Start', M.Command)
        self.assertIn('End', M.Command)
        self.assertIn('Echo', M.Command)
        self.assertIn('Hi', M.Command)
        self.assertListEqual(M.Command.Start.triggers, ['/start'])
        self.assertEqual(M.Command.End.triggers, ['/end'])
        self.assertEqual(M.Command.Hi.triggers, ['/hi'])

    def test_backend(self):
        self.assertTrue(M.context.backend.database.activated)
        self.assertIsInstance(M.context.backend.database.active, M.context.backend.redis.RedisBackend)

    def test_states(self):
        self.assertIn('Main', STATES)
        self.assertIn('Repeat', STATES)
        self.assertIn('Transient', STATES)

    def test_states_config(self):
        self.assertDictEqual(STATES['Main'].commands, {M.Command.Start: 'Repeat', M.Command.Hi: 'Transient'})
        self.assertDictEqual(STATES['Repeat'].commands, {M.Command.End: 'Main'})
        self.assertEqual(STATES['Repeat'].cycle, M.Command.Echo)
        self.assertDictEqual(STATES['Transient'].commands, {})
        self.assertDictEqual(STATES['Transient'].transition, {'Command': M.Command.Passd, 'State': 'Repeat'})
