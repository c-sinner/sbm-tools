import unittest

from sbmtools import convert_numericals


class MyTestCase(unittest.TestCase):
    def test_convert_numericals(self):

        int_int = 5
        int_string = '5'

        self.assertEqual(5, convert_numericals(int_int))
        self.assertEqual(5, convert_numericals(int_string))

        float_float = 5.0
        float_string = '5.0'

        self.assertEqual(5.0, convert_numericals(float_float))
        self.assertEqual(5.0, convert_numericals(float_string))

        scientific_scientific = -5E+5
        scientific_string = '-5E+5'

        self.assertEqual(-5E+5, convert_numericals(scientific_scientific))
        self.assertEqual(-5E+5, convert_numericals(scientific_string))

        string_string = "test"
        self.assertEqual(string_string, convert_numericals(string_string))


if __name__ == '__main__':
    unittest.main()
