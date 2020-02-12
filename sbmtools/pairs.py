from sbmtools.potentials import AbstractPotential

from sbmtools import WriteMixin, ParameterFileEntry
from sbmtools.utils import safely, fortran_number_formatter


class AbstractAtom(WriteMixin, object):
    def __init__(self, first_atom=None, *args, **kwargs):
        super(AbstractAtom, self).__init__(*args, **kwargs)
        self.first_atom = first_atom

        for key, value in kwargs.items():
            setattr(self, key, value)

    @staticmethod
    def get_kwargs_formatted(kwargs):
        return ' '.join(['{0}: {1}'.format(*kwarg) for kwarg in kwargs.items()])

    def __str__(self):
        return "{0} {1} {2}".format(self.first_atom,
                                    " ".join([str(arg) for arg in self.args]),
                                    " ".join([str(value) for value in self.kwargs.values()]))  # TODO: Order of kwargs

    def __repr__(self):
        return "<AbstractAtom {0} {1}>".format(self.first_atom, self.get_kwargs_formatted(self.kwargs))

    def __eq__(self, other):
        return self.first_atom == other.first_atom and all(
            [getattr(self, parameter) == getattr(other, parameter) for parameter in
             set(list(self.kwargs.keys()) + list(other.kwargs.keys()))])

    def write(self, write_header=False, header="", line_delimiter="\n"):
        return header + line_delimiter + self.__str__() if write_header else self.__str__()


class Atom(AbstractAtom):
    def __str__(self):
        return "{first_atom:6d}{type:>4s}{resnr:8d}{residue:>5s}{atom:>5s}{cgnr:8d}{charge:8.3f}{mass:8.3f}".format(first_atom = self.first_atom, **self.kwargs)

    def __repr__(self):
        return "<Atom {0}>".format(self.__str__())


class AtomType(AbstractAtom):
    def __str__(self):
        return "{name:4s}{mass:>10.3f}{charge:10.3f} {ptype:<3s}{c10:7.3f}{c12:17.9E}".format(**self.kwargs)

    def __repr__(self):
        return "<AtomType {0}>".format(self.__str__())


class AbstractAtomGroup(AbstractAtom):
    def __init__(self, first_atom=None, second_atom=None, potential=None, *args, **kwargs):
        super(AbstractAtomGroup, self).__init__(first_atom, *args, **kwargs)
        self.second_atom = second_atom
        self.potential = potential  # TODO: This is not an instance, check this

    @property
    def is_bound(self):
        try:
            return isinstance(self.potential(), AbstractPotential)
        except TypeError:
            return False

    def __str__(self):
        if self.is_bound:
            return self.potential.format.format(**self.potential(self).apply())
        else:
            return ''

    def __repr__(self):
        return "<AbstractAtomGroup is_bound={0} {1} {2} {3}>".format(self.is_bound, self.first_atom, self.second_atom,
                                                                     self.get_kwargs_formatted(self.kwargs))

    def __eq__(self, other):
        return super(AbstractAtomGroup, self).__eq__(other) and self.second_atom == other.second_atom


class AtomPair(AbstractAtomGroup):
    def __init__(self, first_atom, second_atom, distance, **kwargs):
        super(AtomPair, self).__init__(first_atom, second_atom, **kwargs)
        self.distance = distance

    def __repr__(self):
        return "<Pair {0} {1} - dist: {2} - potential: {3}>".format(self.first_atom, self.second_atom, self.distance,
                                                                    self.potential)


class ExclusionsEntry(AbstractAtomGroup):
    def __init__(self, first_atom, second_atom, **kwargs):
        super(ExclusionsEntry, self).__init__(first_atom, second_atom, **kwargs)

    def __str__(self):
        return "{0:6d} {1:6d}".format(self.first_atom, self.second_atom)

    def __repr__(self):
        return "<Exclusion {0}>".format(self.__str__())


class Angle(AbstractAtomGroup):
    def __init__(self, first_atom, second_atom, third_atom, angle, **kwargs):
        super(Angle, self).__init__(first_atom, second_atom, **kwargs)
        self.third_atom = third_atom
        self.angle = angle

    def __repr__(self):
        return "<Angle {0} {1} {2} - theta: {3}>".format(self.first_atom, self.second_atom, self.third_atom, self.angle)

    def __eq__(self, other):
        return super(Angle, self).__eq__(other) and self.third_atom == other.third_atom and self.angle == other.angle


class Dihedral(AbstractAtomGroup):
    def __init__(self, first_atom, second_atom, third_atom, fourth_atom, angle, **kwargs):
        super(Dihedral, self).__init__(first_atom, second_atom, **kwargs)
        self.third_atom = third_atom
        self.fourth_atom = fourth_atom
        self.angle = angle

    def __repr__(self):
        return "<Dihedral {0} {1} {2} {3} - angle: {4} - potential: {5}>".format(
            self.first_atom, self.second_atom, self.third_atom, self.fourth_atom, self.angle, self.potential)

    def __eq__(self, other):
        return super(Dihedral, self).__eq__(other) and self.third_atom == other.third_atom and \
               self.fourth_atom == other.fourth_atom and self.angle == other.angle


class AbstractPairsList(WriteMixin, list):
    header = ""
    name = 'abstract pairs'
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
            raise TypeError("Could not initialize instance of {0} with {1}. Expected a list or tuple of values.".format(
                self.object_class, object))

    def __init__(self, data=None, *args, **kwargs):
        super(AbstractPairsList, self).__init__(*args, **kwargs)

        if data:
            self._data = [self._convert_to_object_class(x) for x in data]
        else:
            self._data = list()

        for key, value in kwargs.items():
            setattr(self, key, value)

    def write(self, write_header=False, header="", line_delimiter="\n"):
        header_delimiter = "\n"
        sorted_entries = self.sort_entries(self._data)
        write_header_list = [True] + [safely(x[0], 'potential.header') != safely(x[1], 'potential.header') for x in zip(sorted_entries, sorted_entries[1:])]
        entries = zip(sorted_entries, write_header_list)
        return ' [ {0} ]'.format(self.name) + header_delimiter + line_delimiter.join([fortran_number_formatter(x[0].write(x[1], safely(x[0], 'potential.header', self.header))) for x in entries])

    @staticmethod
    def sort_entries(data):
        return sorted(data, key=lambda x: (x.potential.header, x.first_atom, x.second_atom))

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
        return self.__class__(self._data + list(other))

    def __sub__(self, other):
        self._check_object_type(other, self.__class__)
        return self.__class__([element for element in self._data if element not in list(other)])

    def __getitem__(self, item):
        return self._data[item]

    def __setitem__(self, index, item):
        self._check_object_type(item, self.object_class)
        self._data[index] = item

    def __len__(self):
        return len(self._data)

    def __iadd__(self, other):
        self._check_object_type(other, self.__class__)
        return self.__class__(self._data + list(other))

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

    @property
    def length(self):
        return len(self._data)


class AbstractAtomList(AbstractPairsList):
    object_class = AbstractAtom

    @staticmethod
    def sort_entries(data):
        return sorted(data, key=lambda x: (x.potential.header, x.first_atom))


class ParameterFileEntryList(AbstractAtomList):
    name = 'generic block'
    object_class = ParameterFileEntry

    def __init__(self, data=None, name="", *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        self.name = name

    @staticmethod
    def sort_entries(data):
        return data


class AtomList(AbstractAtomList):
    header = ";   nr  type resnr  res   atom   cgnr  charge   mass"
    header_format = "{nr:6d} {type:>4s} {resnr:7d} {res:>4s} {atom:>3s} {cgnr:6d} {charge:>8.3f} {mass:>8.3f}"
    name = "atoms"
    object_class = Atom

    @staticmethod
    def sort_entries(data):
        return sorted(data, key=lambda x: x.first_atom)

    def write(self, write_header=False, header="", line_delimiter="\n"):
        header_delimiter = "\n"
        sorted_entries = self.sort_entries(self._data)
        write_header_list = [True] + [safely(x[0], 'potential.header') != safely(x[1], 'potential.header') for x in zip(sorted_entries, sorted_entries[1:])]
        entries = zip(sorted_entries, write_header_list)
        return ' [ {0} ]'.format(self.name) + header_delimiter + line_delimiter.join([x[0].write(x[1], self.header) for x in entries])


class AtomTypesList(AbstractAtomList):
    header = ";name  mass     charge   ptype c10       c12"
    header_format = "{name:4s}{mass:>10.3f}{charge:10.3f} {ptype:<3s}{c10:7.3f}{c12:17.9E}" #TODO: Why is this duplicted?
    name = "atomtypes"
    object_class = AtomType

    @staticmethod
    def sort_entries(data):
        return sorted(data, key=lambda x: x.name)


class PairsList(AbstractPairsList):
    name = "pairs"
    object_class = AtomPair


class BondsList(AbstractPairsList):
    name = "bonds"
    object_class = AtomPair


class ExclusionsList(AbstractPairsList):
    header = ";   ai     aj"
    name = "exclusions"
    object_class = ExclusionsEntry

    @staticmethod
    def sort_entries(data):
        return sorted(data, key=lambda x: (x.first_atom, x.second_atom))


class AnglesList(AbstractPairsList):
    name = "angles"
    object_class = Angle

    @staticmethod
    def sort_entries(data):
        return sorted(data, key=lambda x: (x.potential.header, x.first_atom, x.second_atom, x.third_atom))


class DihedralsList(AbstractPairsList):
    name = "dihedrals"
    object_class = Dihedral

    @staticmethod
    def sort_entries(data):
        return sorted(data,
                      key=lambda x: (x.potential.header, x.first_atom, x.second_atom, x.third_atom, x.fourth_atom))
