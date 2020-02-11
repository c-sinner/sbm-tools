import re


def convert_numericals(item):
    if str(item).replace('-', '').isdigit():
        return int(item)
    else:
        try:
            return float(item)
        except ValueError:
            return item


def safely(obj, accessors, default=""):
    accessor_list = accessors.split(".")
    try:
        return_value = obj
        for accessor in accessor_list:
            return_value = getattr(return_value, accessor)
        return return_value
    except AttributeError:
        return default


def parse_line(line, comment_character=";"):
    line = re.sub(r'^\s*' + re.escape(comment_character), '', line)
    return re.split(r'(\s+)', line)


def fortran_number_formatter(input_string):
    """
    The majority of GROMACS input files use Fortran number formatting in which the scientifically formatted
    numbers have a 0 as integer part and the value in the fractional part. -> 0.XXXXXXXXXE+EX

    This converter reformats scientific numbers in python by matching a group for the integer part, a group for
    the fractional part while dropping the last digit, a group for the sign of the exponent and finally the exponent
    that becomes incremented or decremented accordingly.
    """

    scientific_regexp = r"([1-9])\.([0-9]*)[0-9]E([+\-])([0-9]{2})"

    def converter(match):
        integer_part = match.group(1)
        fractional_part = match.group(2)
        exponent = int(match.group(4))
        sign = match.group(3)

        new_sign = match.group(3) if exponent > 1 else '+'
        new_exponent = exponent + 1 if sign == "+" else exponent - 1

        return '0.{}{}E{}{:02d}'.format(integer_part, fractional_part, new_sign, new_exponent)

    return re.sub(scientific_regexp, converter, input_string)
