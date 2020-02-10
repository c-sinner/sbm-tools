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
