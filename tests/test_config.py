import importlib
import unittest

from .util import reload, BaseTestCase


class ConfigTest(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        cls.M = reload()
        cls.STATES = cls.M.states.base.STATES
        cls.M.setup('tests/config.yaml')

    def test_commands(self):
        self.assertIn('Start', self.M.Command)
        self.assertIn('End', self.M.Command)
        self.assertIn('Echo', self.M.Command)
        self.assertIn('Hi', self.M.Command)
        self.assertListEqual(self.M.Command.Start.triggers.all, ['/start'])
        self.assertEqual(self.M.Command.End.triggers.all, ['/end'])
        self.assertEqual(self.M.Command.Hi.triggers.all, ['/hi'])

    def test_backend(self):
        self.assertTrue(self.M.context.backend.database.activated)
        self.assertIsInstance(self.M.context.backend.database.active,
                              self.M.context.backend.sqlite_backend.SqliteBackend)

    def test_states(self):
        self.assertIn('Main', self.STATES)
        self.assertIn('Repeat', self.STATES)
        self.assertIn('Transient', self.STATES)

    def test_states_config(self):
        self.assertDictEqual(self.STATES['Main'].commands, {self.M.Command.Start: 'Repeat',
                                                            self.M.Command.Hi: 'Transient'})
        self.assertDictEqual(self.STATES['Repeat'].commands, {self.M.Command.End: 'Main'})
        self.assertEqual(self.STATES['Repeat'].cycle, self.M.Command.Echo)
        self.assertDictEqual(self.STATES['Transient'].commands, {})
        self.assertDictEqual(self.STATES['Transient'].transition,
                             {'Command': self.M.Command.Passd, 'State': 'Repeat'})
