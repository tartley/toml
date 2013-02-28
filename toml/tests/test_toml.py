import unittest

from ..toml import loads


class LoadsTest(unittest.TestCase):

    def test_empty(self):
        self.assertEqual(loads(''), {})

    def test_comment(self):
        self.assertEqual(loads('# comment'), {})

    def test_assignment_number(self):
        self.assertEqual(loads('abc=123'), {'abc': 123})

    def test_assignment_string(self):
        self.assertEqual(loads('abc = "def"'), {'abc': "def"})

    def test_assignment_multiple(self):
        self.assertEqual(
            loads('abc = 123\ndef="hello"'),
            {'abc': 123, 'def': 'hello'}
        )

    def test_whitespace(self):
        self.assertEqual(loads('abc = 123'), {'abc': 123})

