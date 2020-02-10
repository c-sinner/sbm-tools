import re

from sbmtools import convert_numericals, ParameterFileComment
from sbmtools.base import AbstractParameterFile, AbstractParameterFileParser, ParameterFileEntry
from sbmtools.pairs import AtomPair, PairsList, AnglesList, DihedralsList, Angle, ExclusionsList, \
    Dihedral, BondsList, AtomList, Atom, ExclusionsEntry, ParameterFileEntryList
from sbmtools.potentials import AbstractPotential, AnglesPotential, BondPotential, ImproperDihedralPotential, \
    DihedralPotential
from sbmtools.potentials import GaussianPotential, CombinedGaussianPotential
from sbmtools.utils import parse_line


class TopFileBase(object):
    default_sections = [
        'defaults',
        'atomtypes',
        'moleculetype',

        'atoms',
        'pairs',
        'bonds',
        'exclusions',
        'angles',
        'dihedrals',

        'system',
        'molecules'
        ]

    def __init__(self, *args, **kwargs):
        super(TopFileBase, self).__init__(*args, **kwargs)
        self._defaults = ParameterFileEntryList(name='defaults')
        self._atomtypes = ParameterFileEntryList(name='atomtypes')
        self._moleculetype = ParameterFileEntryList(name='moleculetype')

        self._atoms = AtomList()
        self._pairs = PairsList()
        self._bonds = BondsList()
        self._exclusions = ExclusionsList()
        self._angles = AnglesList()
        self._dihedrals = DihedralsList()

        self._system = ParameterFileEntryList(name='system')
        self._molecules = ParameterFileEntryList(name='molecules')

    def export(self):
        return {
            'atoms': self._atoms,
            'pairs': self._pairs,
            'bonds': self._bonds,
            'exclusions': self._exclusions,
            'angles': self._angles,
            'dihedrals': self._dihedrals,
        }

    @property
    def atoms(self):
        return self._atoms

    @atoms.setter
    def atoms(self, value):
        self._atoms = value

    @property
    def pairs(self):
        return self._pairs

    @pairs.setter
    def pairs(self, value):
        self._pairs = value

    @property
    def bonds(self):
        return self._bonds

    @bonds.setter
    def bonds(self, value):
        self._bonds = value

    @property
    def exclusions(self):
        return self._exclusions

    @exclusions.setter
    def exclusions(self, value):
        self._exclusions = value

    @property
    def angles(self):
        return self._angles

    @angles.setter
    def angles(self, value):
        self._angles = value

    @property
    def dihedrals(self):
        return self._dihedrals

    @dihedrals.setter
    def dihedrals(self, value):
        self._dihedrals = value

    @property
    def defaults(self):
        return self._defaults

    @defaults.setter
    def defaults(self, value):
        self._defaults = value
        
    @property
    def atomtypes(self):
        return self._atomtypes

    @atomtypes.setter
    def atomtypes(self, value):
        self._atomtypes = value
        
    @property
    def moleculetype(self):
        return self._moleculetype

    @moleculetype.setter
    def moleculetype(self, value):
        self._moleculetype = value
        
    @property
    def system(self):
        return self._system

    @system.setter
    def system(self, value):
        self._system = value
        
    @property
    def molecules(self):
        return self._molecules

    @molecules.setter
    def molecules(self, value):
        self._molecules = value


class TopFileParser(AbstractParameterFileParser):
    title_regex = r'^\s*\[\s*([a-zA-Z0-9]*)\s*\]\s*$'

    def readline(self):
        attribute_name, line = super().readline()
        if self.contains_section_header(line):
            section_header = self.get_section_header(line)
            self.attribute_name = section_header
            return self.__next__()

        line = self.preprocess_line(line)
        if len(line) < 3:
            return self.__next__()
        elif len(line) == 3 and line[1] == ' ':
            return self.__next__()
        else:
            pass

        return self.attribute_name, self.process_entry(self.attribute_name, line)

    def get_section_header(self, line):
        m = re.match(self.title_regex, line)
        if m:
            return m.group(1)
        return None

    def contains_section_header(self, line):
        m = re.match(self.title_regex, line)
        if m:
            return True
        return False

    @staticmethod
    def preprocess_line(line):
        line = line.strip('\n')
        return line

    def process_entry(self, section_name, line):
        if re.match(r"^\s+;", line):
            entry = ParameterFileComment(*[convert_numericals(x) for x in parse_line(line)])
            return entry
        else:
            entry = ParameterFileEntry(*[convert_numericals(x) for x in parse_line(line)])

            if section_name == "atoms":
                return self.process_atoms_entry(entry)

            elif section_name == "pairs":
                return self.process_pairs_entry(entry)

            elif section_name == "bonds":
                return self.process_bonds_entry(entry)

            elif section_name == "exclusions":
                return self.process_exclusions_entry(entry)

            elif section_name == "angles":
                return self.process_angles_entry(entry)

            elif section_name == "dihedrals":
                return self.process_dihedrals_entry(entry)

            else:
                return entry

    @staticmethod
    def process_atoms_entry(entry):
        return Atom(entry[2], type=entry[4], resnr=entry[6], residue=entry[8], atom=entry[10], cgnr=entry[12], charge=entry[14], mass=entry[16])

    @staticmethod
    def process_pairs_entry(entry):
        if entry[6] == 5:
            return AtomPair(entry[2], entry[4], distance=entry[10], potential=GaussianPotential)
        if entry[6] == 6:
            return AtomPair(entry[2], entry[4], distance=entry[10], potential=CombinedGaussianPotential)
        return entry

    @staticmethod
    def process_bonds_entry(entry):
        if entry[6] == 1:
            return AtomPair(entry[2], entry[4], distance=entry[6], potential=BondPotential)
        return entry

    @staticmethod
    def process_exclusions_entry(entry):
        return ExclusionsEntry(entry[2], entry[4])

    @staticmethod
    def process_angles_entry(entry):
        if entry[8] == 1:
            return Angle(entry[2], entry[4], entry[6], angle=entry[10], potential=AnglesPotential)
        return entry

    @staticmethod
    def process_dihedrals_entry(entry):
        if entry[10] == 1:
            if entry[16] == 1:
                return Dihedral(entry[2], entry[4], entry[6], entry[8], angle=entry[12],
                                potential=ImproperDihedralPotential)
            if entry[16] == 3:
                return Dihedral(entry[2], entry[4], entry[6], entry[8], angle=entry[12],
                                potential=DihedralPotential)
        return entry


class TopFile(TopFileBase, AbstractParameterFile):
    potential = CombinedGaussianPotential
    parser = TopFileParser

    def __init__(self, path=None, pairs=None, potential=CombinedGaussianPotential, *args, **kwargs):
        super(TopFile, self).__init__(*args, **kwargs)

        self.init_pairs(pairs)
        self.init_potential(potential)

        for key, value in kwargs.items():
            setattr(self, key, value)

        if path:
            self.load(path)

    def init_pairs(self, pairs):
        if isinstance(pairs, PairsList):
            self.pairs = pairs
        elif pairs:
            raise TypeError(
                'Expected {0} to be an instance of type PairsList. Initiate a new PairsList object using PairsList()')
        else:
            pass

    def init_potential(self, potential):
        if isinstance(potential(), AbstractPotential):
            self.potential = potential
        elif potential:
            raise TypeError(
                'Expected {0} to inherit from AbstractPotential. \
                Initiate a new AbstractPotential object using AbstractPotential()')
        else:
            pass

    def save(self, path):
        super(TopFile, self).save(path)

    def write(self):
        output = "\n\n".join(
            [self.get_header()] + [self.__getattribute__(key).write() for key in self.default_sections])
        for line in output.split('\n'):
            print(line)
