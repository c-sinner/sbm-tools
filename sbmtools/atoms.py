class AbstractAtom(object):
    def __init__(self, index=None, **kwargs):
        self.index = index
        self.kwargs = kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

    @staticmethod
    def get_kwargs_formatted(kwargs):
        return ' '.join(['{0}: {1}'.format(*kwarg) for kwarg in kwargs.items()])

    def __str__(self):
        return "{0} {1}".format(self.index, self.get_kwargs_formatted(self.kwargs))

    def __repr__(self):
        return "<AbstractAtom {0}>".format(self.__str__())

    def __eq__(self, other):
        return self.index == other.index and all(
            [getattr(self, parameter) == getattr(other, parameter) for parameter in
             set(list(self.kwargs.keys()) + list(other.kwargs.keys()))])


class Atom(AbstractAtom):
    def __init__(self, index):
        super(Atom, self).__init__(index)

    def __str__(self):
        return "{0}".format(self.index)


class AtomsList(list):
    object_class = AbstractAtom

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

    def __init__(self, atoms=None, **kwargs):
        super(AtomsList, self).__init__()

        if atoms:
            self._data = [self._convert_to_object_class(x) for x in atoms]
        else:
            self._data = list()

        for key, value in kwargs.items():
            setattr(self, key, value)

    def append(self, object):
        self._check_object_type(object, self.object_class)
        super(AtomsList, self).append(object)
        self._data.append(object)

    def insert(self, index, object):
        self._check_object_type(object, self.object_class)
        super(AtomsList, self).insert(index, object)
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
        return AtomsList([element for element in self._data if element in list(other)])

    def remove(self, other):
        return self - other

    def symmetric_difference(self, other):
        return (self - other) + (other - self)

    def __repr__(self):
        return "<{0} {1}>".format(self.__class__.__name__, self._data)

    def __add__(self, other):
        self._check_object_type(other, self.__class__)
        return AtomsList(self._data + list(other))

    def __sub__(self, other):
        self._check_object_type(other, self.__class__)
        return AtomsList([element for element in self._data if element not in list(other)])

    def __getitem__(self, item):
        return self._data[item]

    def __setitem__(self, index, item):
        self._check_object_type(item, self.object_class)
        self._data[index] = item

    def __len__(self):
        return len(self._data)

    def __iadd__(self, other):
        self._check_object_type(other, self.__class__)
        return AtomsList(self._data + list(other))

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