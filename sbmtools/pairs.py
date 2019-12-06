class AbstractAtomPair(object):
    def __init__(self, index=None, partner=None, **kwargs):
        self.index = index
        self.partner = partner
        self.kwargs = kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

    @staticmethod
    def get_kwargs_formatted(kwargs):
        return ' '.join(['{0}: {1}'.format(*kwarg) for kwarg in kwargs.items()])

    def __str__(self):
        return "{0} {1} {2}".format(self.index, self.partner, self.get_kwargs_formatted(self.kwargs))

    def __repr__(self):
        return "<AbstractAtomPair {0}>".format(self.__str__())

    def __eq__(self, other):
        return self.index == other.index and self.partner == other.partner and all(
            [getattr(self, parameter) == getattr(other, parameter) for parameter in
             set(list(self.kwargs.keys()) + list(other.kwargs.keys()))])


class AtomPair(AbstractAtomPair):
    def __init__(self, index, partner, distance):
        super(AtomPair, self).__init__(index, partner)
        self.distance = distance

    def __str__(self):
        return "{0} {1} - dist: {2}".format(self.index, self.partner, self.distance)


class PairsList(list):
    object_class = AbstractAtomPair

    @staticmethod
    def _check_object_type(object, target_type):
        if isinstance(object, target_type):
            pass
        else:
            raise TypeError(
                'expected {0} to be of type {1} but received type {2} instead.'.format(
                    object, target_type, type(object)))

    def _convert_to_object_class(self, object):
        if isinstance(object, self.object_class):
            return object
        try:
            return self.object_class(*object)
        except TypeError:
            print("Could not initialize instance of {0} with {1}. Expected a list or tuple of values.".format(
                self.object_class, object))

    def __init__(self, data=None, **kwargs):
        super(PairsList, self).__init__()

        if data:
            self._data = [self._convert_to_object_class(x) for x in data]
        else:
            self._data = list()

        for key, value in kwargs.items():
            setattr(self, key, value)

    def append(self, object):
        self._check_object_type(object, self.object_class)
        super(PairsList, self).append(object)
        self._data.append(object)

    def insert(self, index, object):
        self._check_object_type(object, self.object_class)
        super(PairsList, self).insert(index, object)
        self._data.insert(index, object)

    def extend(self, *args, **kwargs):
        raise AttributeError

    def sort(self, *args, **kwargs):
        raise AttributeError

    def add(self, other):
        return self + other

    def union(self, other):
        return self + (other - self)  # this is correct as commutativity is not given in our - implementation

    def intersection(self, other):
        return PairsList([element for element in self._data if element in list(other)])

    def difference(self, other):
        return self - other

    def symmetric_difference(self, other):
        return (self - other) + (other - self)

    def __repr__(self):
        return "<{0} {1}>".format(self.__class__.__name__, self._data)

    def __add__(self, other):
        self._check_object_type(other, self.__class__)
        return PairsList(self._data + list(other))

    def __sub__(self, other):
        self._check_object_type(other, self.__class__)
        return PairsList([element for element in self._data if element not in list(other)])

    def __getitem__(self, item):
        return self._data[item]

    def __setitem__(self, index, item):
        self._check_object_type(item, self.object_class)
        self._data[index] = item

    def __len__(self):
        return len(self._data)

    def __iadd__(self, other):
        self._check_object_type(other, self.__class__)
        return PairsList(self._data + list(other))

    def __imul__(self, *args, **kwargs):
        raise AttributeError

    def __iter__(self, *args, **kwargs):
        return iter(self._data)

    def __le__(self, *args, **kwargs):
        raise AttributeError

    def __lt__(self, *args, **kwargs):
        raise AttributeError

    def __mul__(self, *args, **kwargs):
        raise AttributeError

    def __eq__(self, other):
        return len(self) == len(other) and all([self[i] == other[i] for i in range(len(self))])

    def __ne__(self, *args, **kwargs):
        """ Return self!=value. """
        return NotImplemented

    def __rmul__(self, *args, **kwargs):
        raise AttributeError
