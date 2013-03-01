import datetime
import textwrap
import unittest

import toml


class HappyDayTest(unittest.TestCase):

    def test_convert_example_test(self):

        example = textwrap.dedent('''\
            # This is a TOML document. Boom.

            title = "TOML Example"

            [owner]
            name = "Tom Preston-Werner"
            organization = "GitHub"
            bio = "GitHub Cofounder & CEO\\nLikes tater tots and beer."
            dob = 1979-05-27T07:32:00Z # First class dates? Why not?

            [database] # comment after a category
            server = "192.168.1.1" # comment after a key
            ports = [ 8001, 8001, 8002 ]
            connection_max = 5000
            enabled = true

            [servers]

                # You can indent as you please.
                [servers.alpha]
                ip = "10.0.0.1"
                dc = "eqdc10"

                # Tabs or spaces. TOML don't care.
            \t[servers.beta]
            \tip = "10.0.0.2"
            \tdc = "eqdc10"

            [clients]
            # Line breaks are OK when inside arrays
            data = [
                ["gamma", "delta"],
                [1, 2]
            ]
        ''')
        expected = dict(
            title = "TOML Example",
            owner = dict(
                name = "Tom Preston-Werner",
                organization = "GitHub",
                bio = "GitHub Cofounder & CEO\nLikes tater tots and beer.",
                dob = datetime.datetime(1979, 5, 27, 7, 32, 0)
            ),
            database = dict(
                server = "192.168.1.1",
                ports = [8001, 8001, 8002],
                connection_max = 5000,
                enabled = True,
            ),
            servers = dict(
                alpha = dict(ip = "10.0.0.1", dc = "eqdc10"),
                beta = dict(ip = "10.0.0.2", dc = "eqdc10")
            ),
            clients = dict(data = [["gamma", "delta"], [1, 2]]),
        )
        self.assertEqual(toml.loads(example), expected)

