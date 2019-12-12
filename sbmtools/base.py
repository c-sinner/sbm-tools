import uuid
from datetime import date

class AbstractParameterFileParser(object):
    def __init__(self, data=None):
        self.data = data

    def parse(self):
        raise NotImplementedError


class AbstractParameterFile(object):
    parser = AbstractParameterFileParser

    def __init__(self, *args, **kwargs):
        super(AbstractParameterFile, self).__init__(*args, **kwargs)
        self.args = args
        self.kwargs = kwargs
        self.data = ''

    def __str__(self):
        super(AbstractParameterFile, self).__str__()

    @staticmethod
    def get_header():
        return '; Automated top file generated by sbmtools on the {0} with uuid {1}'.format(date.today().isoformat(),
                                                                                            uuid.uuid4().hex)

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

    def __init__(self, *args, **kwargs):
        super(AbstractParameterFileSection, self).__init__(*args, **kwargs)

    def __str__(self):
        super(AbstractParameterFileSection, self).__str__()

    @property
    def contents(self):
        raise NotImplementedError
