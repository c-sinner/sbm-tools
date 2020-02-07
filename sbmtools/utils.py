def convert_numericals(item):
    try:
        return int(item)
    except ValueError:
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
