class AbstractParameterFile(object):
    def __init__(self):
        pass

    def __str__(self):
        super(AbstractParameterFile, self).__str__()

    def setup(self, *args, **kwargs):
        """Initialize attributes shared by all view methods."""
        if hasattr(self, 'get') and not hasattr(self, 'head'):
            self.head = self.get
        self.args = args
        self.kwargs = kwargs

    def built(self):
        raise NotImplementedError

    def save(self):
        output = self.built()
        raise NotImplementedError


class AbstractParameterFileSection(object):
    title = ''

    def __str__(self):
        super(AbstractParameterFileSection, self).__str__()

    def write(self):
        raise NotImplementedError

