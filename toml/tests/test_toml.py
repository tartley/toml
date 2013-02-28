import unittest

from ..toml import loads


class LoadsTest(unittest.TestCase):

    def test_empty(self):
        self.assertEqual(loads(''), {})

    def test_comment(self):
        self.assertEqual(loads('# comment'), {})

    def test_p_statement_assignment(self):
        self.assertEqual(loads('abc=123'), {'abc': 123})

