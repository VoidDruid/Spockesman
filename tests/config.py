import unittest
import importlib

M = importlib.import_module('spockesman')


class ConfigTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        M.load_config('tests/bot/config.yaml')

    def test_commands(self):
        self.assertIn('Start', M.Command)
        self.assertIn('End', M.Command)
        self.assertIn('Echo', M.Command)
        self.assertIn('Hi', M.Command)
        self.assertEqual(M.Command.Start.value, '/start')
        self.assertEqual(M.Command.End.value, '/end')
        self.assertEqual(M.Command.Hi.value, '/hi')

    def test_backend(self):
        self.assertTrue(M.context.backend.database.activated)
        self.assertTrue(isinstance(M.context.backend.database.active, M.context.backend.redis.RedisBackend))
