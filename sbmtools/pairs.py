from sbmtools.potentials import GaussianPotential


class AbstractAtomGroup(object):
    def __init__(self, first_atom=None, second_atom=None, **kwargs):
        self.first_atom = first_atom
        self.second_atom = second_atom
        self.kwargs = kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

    @staticmethod
    def get_kwargs_formatted(kwargs):
        return ' '.join(['{0}: {1}'.format(*kwarg) for kwarg in kwargs.items()])

    def __str__(self):
        return "{0} {1} {2}".format(self.first_atom, self.second_atom, self.get_kwargs_formatted(self.kwargs))

    def __repr__(self):
        return "<AbstractAtomGroup {0}>".format(self.__str__())

    def __eq__(self, other):
        return self.first_atom == other.first_atom and self.second_atom == other.second_atom and all(
            [getattr(self, parameter) == getattr(other, parameter) for parameter in
             set(list(self.kwargs.keys()) + list(other.kwargs.keys()))])


class AtomPair(AbstractAtomGroup):
    def __init__(self, first_atom, second_atom, distance, potential, **kwargs):
        super(AtomPair, self).__init__(first_atom, second_atom, **kwargs)
        self.distance = distance
        self.potential = GaussianPotential

    def __str__(self):
        return "{0} {1} - dist: {2} - potential: {3}".format(self.first_atom, self.second_atom, self.distance,
                                                             self.potential)


class Angle(AbstractAtomGroup):
    def __init__(self, first_atom, second_atom, third_atom, phi, **kwargs):
        super(Angle, self).__init__(first_atom, second_atom, **kwargs)
        self.third_atom = third_atom
        self.phi = phi

    def __str__(self):
        return "{0} {1} {2} - phi: {3}".format(self.first_atom, self.second_atom, self.third_atom, self.phi)

    def __eq__(self, other):
        return super(Angle, self).__eq__(other) and self.third_atom == other.third_atom


class Dihedral(AbstractAtomGroup):
    def __init__(self, first_atom, second_atom, third_atom, fourth_atom, phi, psi, **kwargs):
        super(Dihedral, self).__init__(first_atom, second_atom, **kwargs)
        self.third_atom = third_atom
        self.fourth_atom = fourth_atom
        self.phi = phi
        self.psi = psi

    def __str__(self):
        return "{0} {1} {2} {3} - phi: {4} psi: {5}".format(
            self.first_atom, self.second_atom, self.third_atom, self.fourth_atom, self.phi, self.psi)

    def __eq__(self, other):
        return super(Dihedral, self).__eq__(other) and self.third_atom == other.third_atom and self.fourth_atom == other.fourth_atom and self.phi == other.phi and self.psi == other.psi


class AbstractPairsList(list):
    object_class = AbstractAtomGroup

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
        super(AbstractPairsList, self).__init__()

        if data:
            self._data = [self._convert_to_object_class(x) for x in data]
        else:
            self._data = list()

        for key, value in kwargs.items():
            setattr(self, key, value)

    def append(self, object):
        self._check_object_type(object, self.object_class)
        super(AbstractPairsList, self).append(object)
        self._data.append(object)

    def insert(self, index, object):
        self._check_object_type(object, self.object_class)
        super(AbstractPairsList, self).insert(index, object)
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
        return AbstractPairsList([element for element in self._data if element in list(other)])

    def remove(self, other):
        return self - other

    def symmetric_difference(self, other):
        return (self - other) + (other - self)

    def __repr__(self):
        return "<{0} {1}>".format(self.__class__.__name__, self._data)

    def __add__(self, other):
        self._check_object_type(other, self.__class__)
        return AbstractPairsList(self._data + list(other))

    def __sub__(self, other):
        self._check_object_type(other, self.__class__)
        return AbstractPairsList([element for element in self._data if element not in list(other)])

    def __getitem__(self, item):
        return self._data[item]

    def __setitem__(self, index, item):
        self._check_object_type(item, self.object_class)
        self._data[index] = item

    def __len__(self):
        return len(self._data)

    def __iadd__(self, other):
        self._check_object_type(other, self.__class__)
        return AbstractPairsList(self._data + list(other))

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


class PairsList(AbstractPairsList):
    object_class = AtomPair


class AnglesList(AbstractPairsList):
    object_class = Angle


class DihedralsList(AbstractPairsList):
    object_class = Dihedral
