import uuid
from datetime import date
from contextlib import ContextDecorator

from sbmtools.utils import convert_numericals


class WriteMixin(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self._data = [convert_numericals(arg) for arg in args]

    def __getitem__(self, item):
        return self._data[item]

    def __str__(self):
        return self.write()

    def write(self, write_header=False, header="", line_delimiter="\n", item_delimiter=" "):
        items = item_delimiter.join([str(item) for item in self._data])
        kwargs = item_delimiter.join([str(value) for value in self.kwargs.values()])

        output = items + item_delimiter + kwargs if kwargs else items

        if write_header:
            return header + line_delimiter + output
        else:
            return output


class ParameterFileEntry(WriteMixin, object):
    def __init__(self, *args, **kwargs):
        super(ParameterFileEntry, self).__init__(*args, **kwargs)

    def __repr__(self):
        return "<ParameterFileEntry {0} {1}>".format("  ".join([str(item) for item in self._data]),
                                                     " ".join(
                                                         ["{0}: {1}".format(*item) for item in self.kwargs.items()]))

    def write(self, write_header=False, header="", line_delimiter="\n", item_delimiter=" "):
        item_delimiter = ""
        return super(ParameterFileEntry, self).write(write_header, header, line_delimiter, item_delimiter)


class ParameterFileComment(ParameterFileEntry):
    def __init__(self, *args, **kwargs):
        super(ParameterFileComment, self).__init__(*args, **kwargs)

    def __repr__(self):
        return "<ParameterFileComment {0} {1}>".format("  ".join([str(item) for item in self._data]),
                                                       " ".join(
                                                           ["{0}: {1}".format(*item) for item in self.kwargs.items()]))

    def write(self, write_header=False, header="", line_delimiter="\n", item_delimiter=" ", comment_character=';'):
        item_delimiter = ""
        output = super(ParameterFileComment, self).write(False, item_delimiter=item_delimiter)
        return comment_character + output


class AbstractParameterFileParser(ContextDecorator):
    """
    Context manager and Iterator for opening a file and looping through the lines. The readline method can be overloaded
    to create more specific parsers.
    """

    def __init__(self, path=None, start=0):
        self.num = start
        self.attribute_name = "_data"
        self.path = path

    def __enter__(self):
        self.file_stream = open(self.path, 'r')
        return self

    def __exit__(self, *exc):
        self.file_stream.close()
        return False

    def __iter__(self):
        return self

    def __next__(self):
        self.num += 1
        return self.readline()

    def readline(self):
        value = self.file_stream.readline()
        if value:
            return self.attribute_name, value
        else:
            raise StopIteration


class AbstractParameterFile(object):
    parser = AbstractParameterFileParser

    def __init__(self, *args, **kwargs):
        super(AbstractParameterFile, self).__init__(*args, **kwargs)
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        super(AbstractParameterFile, self).__str__()

    @staticmethod
    def get_header():
        return '; Automated top file generated by sbmtools on the {0} with uuid {1}'.format(date.today().isoformat(),
                                                                                            uuid.uuid4().hex)

    def write(self):
        raise NotImplementedError

    def save(self, path):
        output = self.write()
        with open(path, 'w') as output_stream:
            output_stream.write(output)

    def load(self, path):
        with self.parser(path) as input_stream:
            for line in input_stream:
                self.process_line(*line)

    def process_line(self, attr, line):
        try:
            getattr(self, attr).append(line)
        except AttributeError:
            setattr(self, attr, line)
        except TypeError:
            # Check if we wanted to pass a comment. Comments can be discarded when an attribute list does not accept
            # them.
            if isinstance(line, ParameterFileComment):
                pass
            else:
                raise
