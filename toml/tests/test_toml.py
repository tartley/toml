import datetime
import unittest

from ..toml import loads


class LoadsTest(unittest.TestCase):

    def test_empty(self):
        self.assertEqual(loads(''), {})

    def test_comment(self):
        self.assertEqual(loads('# comment'), {})

    def test_assignment_integer(self):
        self.assertEqual(loads('abc=123'), {'abc': 123})

    # TODO integer should handle negatives

    def test_assignment_string(self):
        self.assertEqual(loads('abc = "def"'), {'abc': "def"})

    # TODO we don't handle escaped chars in a string

    def test_assignment_date(self):
        self.assertEqual(
            loads('dob = 1979-05-27T07:32:00Z'),
            {'dob': datetime.datetime(1979, 5, 27, 7, 32, 0)}
        )

    # TODO we don't handle timezones at all

    def test_assignment_array_empty(self):
        self.assertEqual(loads('abc=[]'), {'abc': []})
        self.assertEqual(loads('abc=[]'), {'abc': []})
        self.assertEqual(loads(' abc=[]'), {'abc': []})
        self.assertEqual(loads(' abc =[]'), {'abc': []})
        self.assertEqual(loads(' abc = []'), {'abc': []})
        self.assertEqual(loads(' abc = [ ]'), {'abc': []})
        self.assertEqual(loads(' abc = [ ] '), {'abc': []})

    def test_assignment_array_single_integer(self):
        self.assertEqual(loads('abc=[1]'), {'abc': [1]})

    def test_assignment_array(self):
        self.assertEqual(loads('abc=[1,2,3]'), {'abc': [1, 2, 3]})

    # TODO arrays of different types
    # TODO arrays of arrays
    # TODO heterogeneous arrays are not allowed
    # TODO array of (array of int) (array of str) is allowed

    def test_assignment_multiple(self):
        self.assertEqual(
            loads('abc = 123\ndef="hello"'),
            {'abc': 123, 'def': 'hello'}
        )

    def test_whitespace(self):
        self.assertEqual(loads('abc = 123'), {'abc': 123})

    def test_group(self):
        self.assertEqual(loads('[group]'), {'group': {}})

    def test_group_with_assignment(self):
        self.assertEqual(loads('[group]\nabc=123'), {'group': {'abc': 123}})

    def test_groups_and_assignments(self):
        self.assertEqual(loads('abc=123\n[group]\n'), {'group': {}, 'abc': 123})

