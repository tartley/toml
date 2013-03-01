import datetime
import unittest

from ..toml import loads


# TODO integer should handle negatives
# TODO there may be no assignments in a group
# TODO we don't handle timezones at all


class LoadsTest(unittest.TestCase):

    def test_empty(self):
        self.assertEqual(loads(''), {})

    def test_comment(self):
        self.assertEqual(loads('# comment'), {})

    def test_assignment_number(self):
        self.assertEqual(loads('abc=123'), {'abc': 123})

    def test_assignment_string(self):
        self.assertEqual(loads('abc = "def"'), {'abc': "def"})

    def test_assignment_date(self):
        self.assertEqual(
            loads('dob = 1979-05-27T07:32:00Z'),
            {'dob': datetime.datetime(1979, 5, 27, 7, 32, 0)}
        )

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
        self.assertEqual(loads('abc=123\n[group]'), {'group': {}, 'abc': 123})

