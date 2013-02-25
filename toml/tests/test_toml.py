import unittest

from ..toml import loads


class LoadsTest(unittest.TestCase):

    def test_loads_empty_string(self):
        self.assertEqual(loads(''), None)

