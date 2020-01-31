import re

from sbmtools.base import AbstractParameterFile, AbstractParameterFileParser, ParameterFileEntry
from sbmtools.pairs import AtomPair, PairsList, AnglesList, DihedralsList, Angle, ExclusionsList, AbstractAtomGroup, \
    Dihedral, BondsList, AtomList, Atom
from sbmtools.potentials import AbstractPotential, AnglesPotential, BondPotential, ImproperDihedralPotential, \
    DihedralPotential
from sbmtools.potentials import LennardJonesPotential, GaussianPotential, CombinedGaussianPotential
from sbmtools.topfile_sections import MoleculesSection, SystemSection, AnglesSection, DihedralsSection, \
    ExclusionsSection, BondsSection, AtomsSection, MoleculeTypeSection, AtomTypesSection, DefaultsSection, PairsSection


class TopFileBase(object):
    def __init__(self, *args, **kwargs):
        super(TopFileBase, self).__init__(*args, **kwargs)
        self._atoms = AtomList()
        self._pairs = PairsList()
        self._bonds = BondsList()
        self._exclusions = ExclusionsList()
        self._angles = AnglesList()
        self._dihedrals = DihedralsList()

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


class TopFileParser(AbstractParameterFileParser):
    title_regex = r'^\s*\[\s*([a-zA-Z0-9]*)\s*\]\s*$'

    def readline(self):
        attribute_name, line = super().readline()
        if self.contains_section_header(line):
            section_header = self.get_section_header(line)
            self.attribute_name = section_header
            return self.__next__()

        line = self.preprocess_line(line)
        if not line:
            return self.__next__()

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
        line = re.sub(r';.*$', '', line)
        return line.strip(" ")

    def process_entry(self, section_name, line):
        line = line.split()

        if section_name == "atoms":
            return self.process_atoms_entry(line)

        if section_name == "pairs":
            return self.process_pairs_entry(line)

        if section_name == "bonds":
            return self.process_bonds_entry(line)

        elif section_name == "exclusions":
            return self.process_exclusions_entry(line)

        elif section_name == "angles":
            return self.process_angles_entry(line)

        elif section_name == "dihedrals":
            return self.process_dihedrals_entry(line)

        else:
            return line

    @staticmethod
    def process_atoms_entry(entry):
        return Atom(entry[0], type=entry[1], resnr=entry[2], residue=entry[3], atom=entry[4], cgnr=entry[5], charge=entry[6], mass=entry[7])

    @staticmethod
    def process_pairs_entry(entry):
        entry = ParameterFileEntry(*entry)
        if entry[2] == 5:
            return AtomPair(entry[0], entry[1], distance=entry[4], potential=GaussianPotential)
        if entry[2] == 6:
            return AtomPair(entry[0], entry[1], distance=entry[4], potential=CombinedGaussianPotential)
        return entry

    @staticmethod
    def process_bonds_entry(entry):
        entry = ParameterFileEntry(*entry)
        if entry[2] == 1:
            return AtomPair(entry[0], entry[1], distance=entry[3], potential=BondPotential)
        return entry

    @staticmethod
    def process_exclusions_entry(entry):
        return AbstractAtomGroup(*entry)

    @staticmethod
    def process_angles_entry(entry):
        entry = ParameterFileEntry(*entry)
        if entry[3] == 1:
            return Angle(entry[0], entry[1], entry[2], angle=entry[4], potential=AnglesPotential)
        return entry

    @staticmethod
    def process_dihedrals_entry(entry):
        entry = ParameterFileEntry(*entry)
        if entry[4] == 1:
            if entry[7] == 1:
                return Dihedral(entry[0], entry[1], entry[2], entry[3], angle=entry[5],
                                potential=ImproperDihedralPotential)
            if entry[7] == 3:
                return Dihedral(entry[0], entry[1], entry[2], entry[3], angle=entry[5],
                                potential=DihedralPotential)
        return entry


class TopFile(TopFileBase, AbstractParameterFile):
    potential = CombinedGaussianPotential
    parser = TopFileParser

    defaults_section = DefaultsSection()
    atom_types_section = AtomTypesSection()
    molecule_type_section = MoleculeTypeSection()
    atoms_section = AtomsSection()
    bonds_section = BondsSection()
    exclusions_section = ExclusionsSection()
    angles_section = AnglesSection()
    dihedrals_section = DihedralsSection()
    system_section = SystemSection()
    molecules_section = MoleculesSection()

    default_sections = [
        "defaults_section",
        "atom_types_section",
        "molecule_type_section",
        "atoms_section",
        "pairs_section",
        "bonds_section",
        "exclusions_section",
        "angles_section",
        "dihedrals_section",
        "system_section",
        "molecules_section",
    ]

    def __init__(self, path=None, pairs=None, potential=LennardJonesPotential, *args, **kwargs):
        super().__init__()

        if isinstance(pairs, PairsList):
            self.pairs = pairs
        elif pairs:
            raise TypeError(
                'Expected {0} to be an instance of type PairsList. Initiate a new PairsList object using PairsList()')
        else:
            pass

        if isinstance(potential(), AbstractPotential):
            self.potential = potential
        elif potential:
            raise TypeError(
                'Expected {0} to inherit from AbstractPotential. \
                Initiate a new AbstractPotential object using AbstractPotential()')
        else:
            pass

        self.pairs_section = PairsSection(self.pairs, self.potential)

        for key, value in kwargs.items():
            setattr(self, key, value)

        if path:
            self.load(path)

    def __setattr__(self, key, value):
        if key == 'potential':
            isinstance(value(), AbstractPotential)
            self.pairs_section = PairsSection(self.pairs, value)
        super(TopFile, self).__setattr__(key, value)

    @TopFileBase.atoms.setter
    def atoms(self, value):
        self._atoms = value
        self.atoms_section.values = value

    @TopFileBase.pairs.setter
    def pairs(self, value):
        self._pairs = value
        self.pairs_section = PairsSection(value, self.potential)

    @TopFileBase.bonds.setter
    def bonds(self, value):
        self._bonds = value
        self.bonds_section.values = value

    @TopFileBase.exclusions.setter
    def exclusions(self, value):
        self._exclusions = value
        self.exclusions_section.values = value

    @TopFileBase.angles.setter
    def angles(self, value):
        self._angles = value
        self.angles_section.values = value

    @TopFileBase.dihedrals.setter
    def dihedrals(self, value):
        self._dihedrals = value
        self.dihedrals_section.values = value

    def save(self, path):
        super(TopFile, self).save(path)

    def built(self):
        output = "\n\n".join(
            [self.get_header()] + [self.__getattribute__(key).contents for key in self.default_sections])
        for line in output.split('\n'):
            print(line)

    """
    def load(self, path):
        super(TopFile, self).load(path)
        self.atoms = self.data['atoms']
        self.pairs = self.data['pairs']
        self.bonds = self.data['bonds']
        self.exclusions = self.data['exclusions']
        self.angles = self.data['angles']
        self.dihedrals = self.data['dihedrals']

        self.defaults_section.values = self.data['defaults'],
        self.atom_types_section.values = self.data['atomtypes'],
        self.molecule_type_section.values = self.data['moleculetype'],
        self.system_section.values = self.data['system'],
        self.molecules_section.values = self.data['molecules']

        # for key in self.default_sections:
        #
        #    self.__getattribute__(key).values = self.data[self.__getattribute__(key).unformatted_title]
        #    #self.__getattribute__(key)[0].values = self.data[self.__getattribute__(key)[0].unformatted_title] 
    """
