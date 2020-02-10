import unittest
import re

from sbmtools import ParameterFileEntry, convert_numericals


class MyTestCase(unittest.TestCase):
    def test_parameter_file_entry(self):
        initial_line = "1 2 3 this  is   a    test     "

        line = re.split(r'(\s+)', initial_line)
        line = [item for item in map(lambda x: re.sub(r'^\s{1,2}', '', x), line) if item]
        p = ParameterFileEntry(*[convert_numericals(x) for x in line])

        self.assertEqual(initial_line, p.write())


if __name__ == '__main__':
    unittest.main()
