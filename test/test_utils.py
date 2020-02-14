import unittest

from sbmtools.utils import convert_numericals, fortran_number_formatter


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

    def test_fortran_number_converter(self):
        single_number = '   2.000000000E+01'
        multiple_numbers = '   2.000000000E+01   3.000000000E+02'
        various_formats = '   2.000000000E+00   3.000000000E04    0.5454424245E+33'

        negative_exponent = '   2.000000000E-01'
        mixed_exponents = '   6.000000000E-07   8.000000000E+09'

        self.assertEqual('   0.200000000E+02', fortran_number_formatter(single_number))
        self.assertEqual('   0.200000000E+02   0.300000000E+03', fortran_number_formatter(multiple_numbers))
        self.assertEqual('   0.200000000E+01   3.000000000E04    0.5454424245E+33',
                         fortran_number_formatter(various_formats))

        self.assertEqual('   0.200000000E+00', fortran_number_formatter(negative_exponent))
        self.assertEqual('   0.600000000E-06   0.800000000E+10', fortran_number_formatter(mixed_exponents))


if __name__ == '__main__':
    unittest.main()
