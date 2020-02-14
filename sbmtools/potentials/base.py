

class AbstractPotential(object):
    def __init__(self, pair=None, **kwargs):
        self.format = ''
        self.header = ''
        self.pair = pair
        for key, value in kwargs.items():
            setattr(self, key, value)

    def apply(self):
        raise NotImplementedError
