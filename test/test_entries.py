import re
import unittest

from sbmtools import ParameterFileEntry, convert_numericals, ParameterFileComment
from sbmtools.utils import parse_line


class MyTestCase(unittest.TestCase):
    def test_parameter_file_entry(self):
        initial_line = "1 2 3 this  is   a    test     "
        line = parse_line(initial_line)

        p = ParameterFileEntry(*[convert_numericals(x) for x in line])

        self.assertEqual(initial_line, p.write())

    def test_parameter_file_comment(self):
        initial_line = ";1 2 3 this  is   a    test     "
        line = parse_line(initial_line)

        p = ParameterFileComment(*[convert_numericals(x) for x in line])

        self.assertEqual(initial_line, p.write())


if __name__ == '__main__':
    unittest.main()
