import unittest
import sys
sys.path.append('C:\\Users\\Jake\\Documents\\sbm-tools-master\\')
from sbmtools import TopFileParser



class TestTopFileParser(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestTopFileParser, self).__init__(*args, **kwargs)
        with open('C:\\Users\\Jake\\Documents\\sbm-tools-master\\test\\files\\external_top_file.top') as top_file:
            self.data = top_file.read()

    def setUp(self):
        self.parser = TopFileParser(self.data)

    def test_preprocess_data(self):
        test_string_with_line_comment = ';This is a comment\nThis is valid data\n~~~~This is valid data~~~~\n~~~~' + \
                                        ';This is a comment\n;This is a trailing comment'
        test_string_fixed = 'This is valid data\n~~~~This is valid data~~~~\n~~~~'

        self.assertEqual(self.parser.preprocess_data(test_string_with_line_comment), test_string_fixed)

    def test_sections_keys(self):
        sections = self.parser.parse_sections(self.data)
        section_keys = [section['title'] for section in sections]
        expected_section_keys = ['defaults',
                                 'atomtypes',
                                 'moleculetype',
                                 'atoms',
                                 'pairs',
                                 'pairs',  # pairs section is doubled for further test
                                 'bonds',
                                 'exclusions',
                                 'angles',
                                 'dihedrals',
                                 'system',
                                 'molecules']

        self.assertEqual(section_keys, expected_section_keys)

    def test_bonds_section_values(self):
        sections = self.parser.parse_sections(self.parser.preprocess_data(self.data))
        bonds_values = []
        for section in sections:
            if section['title'] == 'bonds':
                bonds_values += section['values']

        expected_bonds_values = [['1', '2', '1', '3.80269060E-01', '2.00000000E+04']]

        self.assertEqual(bonds_values, expected_bonds_values)

    def test_postprocess_results(self):
        sections_list = self.parser.parse_sections(self.parser.preprocess_data(self.data))
        sections = self.parser.postprocess_result(sections_list)

        expected_bonds_values = [[1, 2, 1, 0.38026906, 20000.0]]

        self.assertEqual(sections['bonds'], expected_bonds_values)

    def test_postprocess_results_repeated_section(self):
        """The idea is to combine these values in the order that they occur"""
        sections_list = self.parser.parse_sections(self.parser.preprocess_data(self.data))
        sections = self.parser.postprocess_result(sections_list)

        expected_pairs_values = [[2, 45, 1, 8.67324, 7.78048],
                                 [2, 2, 1, 8.67324, 7.78048]]

        self.assertEqual(sections['pairs'], expected_pairs_values)


if __name__ == '__main__':
    unittest.main()