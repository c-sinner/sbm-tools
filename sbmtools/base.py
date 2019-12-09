class AbstractParameterFileParser(object):
    def __init__(self, data=None):
        self.data = data

    def parse(self):
        raise NotImplementedError


class AbstractParameterFile(object):
    parser = AbstractParameterFileParser

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.data = ''

    def __str__(self):
        super(AbstractParameterFile, self).__str__()

    def built(self):
        raise NotImplementedError

    def save(self, path):
        output = self.built()
        output_stream = open(path, 'w')
        output_stream.write(output)
        output_stream.close()

    def load(self, path):
        with open(path, 'r') as input_stream:
            data = input_stream.read()
        self.data = self.parser(data).parse()


class AbstractParameterFileSection(object):

    def __str__(self):
        super(AbstractParameterFileSection, self).__str__()

    @property
    def contents(self):
        raise NotImplementedError
