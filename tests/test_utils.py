from .util import BaseTestCase

from spockesman.util.string import upper_and_separate


class UtilsTestCase(BaseTestCase):
    def test_string_methods(self):
        first = upper_and_separate('TestString')
        self.assertEqual(first, 'TEST_STRING')
        second = upper_and_separate('Test')
        self.assertEqual(second, 'TEST')
