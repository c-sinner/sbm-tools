import uuid
from datetime import date

from sbmtools import PairsList, AbstractParameterFileParser
from sbmtools.atoms import AtomsList
from sbmtools.potentials import LennardJonesPotential, AbstractPotential
from sbmtools.base import AbstractParameterFile
import re

from sbmtools.topfile_sections import MoleculesSection, SystemSection, AnglesSection, DihedralsSection, \
    ExclusionsSection, BondsSection, AtomsSection, MoleculeTypeSection, AtomTypesSection, DefaultsSection, PairsSection


class TopFileBase(object):
    def __init__(self, *args, **kwargs):
        super(TopFileBase, self).__init__(*args, **kwargs)
        self._atoms = AtomsList()
        self._pairs = PairsList()
        self._bonds = PairsList()
        self._exclusions = PairsList()
        self._angles = PairsList()
        self._dihedrals = PairsList()
        
    def display(self):
        return [
            self._atoms,
            self._pairs,
            self._bonds,
            self._exclusions,
            self._angles,
            self._dihedrals,
        ]

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


class TopFileParser(TopFileBase, AbstractParameterFileParser):
    sections_regex = r'\[[a-z\s]*\][a-zA-Z0-9\#\+\;\s\-\n\.\(\)]*\n'
    title_regex = r'\[\s*([a-zA-Z0-9]*)\s*\]'
    line_delimiter = '\n'

    def __init__(self, data):
        super(TopFileParser, self).__init__(data)

    def parse(self):
        return self.postprocess_result(self.parse_sections(self.preprocess_data(self.data)))

    # handle same titles
    @staticmethod
    def postprocess_result(sections_list):
        def flatten(list_of_lists):
            return [item for sublist in list_of_lists for item in sublist]

        def to_numeric(list_of_lists):
            result = []
            for item in list_of_lists:
                if isinstance(item, list):
                    result.append(to_numeric(item))
                else:
                    try:
                        result.append(int(item))
                    except:
                        try:
                            result.append(float(item))
                        except:
                            result.append(item)
            return result

        unique_keys = []
        [unique_keys.append(x['title']) for x in sections_list if x['title'] not in unique_keys]

        processed = {}
        for unique_key in unique_keys:
            processed[unique_key] = flatten(
                to_numeric(
                    [section['values'] for section in sections_list if section['title'] == unique_key]))

        return processed

    @staticmethod
    def preprocess_data(data):
        return re.sub(r';.*(\n|$)', '', data)

    def parse_sections(self, data):
        return list(map(self.parse_section, re.findall(self.sections_regex, data, re.MULTILINE)))

    def parse_section(self, section):
        m = re.match(self.title_regex, section)
        title = ''
        if m:
            title = m.group(1)

        values = [line.split() for line in section.split(self.line_delimiter)[1:] if line]
        return {"title": title, "values": values}


class TopFile(TopFileBase, AbstractParameterFile):
    potential = LennardJonesPotential
    parser = TopFileParser

    defaults_section = DefaultsSection(),
    atom_types_section = AtomTypesSection(),
    molecule_type_section = MoleculeTypeSection(),
    atoms_section = AtomsSection(),
    bonds_section = BondsSection(),
    exclusions_section = ExclusionsSection(),
    angles_section = AnglesSection(),
    dihedrals_section = DihedralsSection(),
    system_section = SystemSection(),
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

    def __init__(self, pairs=None, potential=LennardJonesPotential, **kwargs):
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

        self.atoms = AtomsList()
        self.bonds = PairsList()
        self.exclusions = PairsList()
        self.dihedrals = PairsList()

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __setattr__(self, key, value):
        if key == 'potential':
            isinstance(value(), AbstractPotential)
            self.pairs_section = PairsSection(self.pairs, value)
        super(TopFile, self).__setattr__(key, value)

    @staticmethod
    def get_header():
        return '; Automated top file generated by sbmtools on the {0} with uuid {1}'.format(date.today().isoformat(),
                                                                                            uuid.uuid4().hex)

    @TopFileBase.angles.setter
    def angles(self, value):
        super(TopFile, self).__setattr__('angles', value)  # This needs a parser first
        self.angles_section.values = value

    @TopFileBase.pairs.setter
    def pairs(self, value):
        isinstance(value, PairsList)
        super(TopFile, self).__setattr__('pairs', value)
        self.pairs_section = PairsSection(value, self.potential)

    def save(self, path):
        super(TopFile, self).save(path)

    def built(self):
        output = "\n\n".join(
            [self.get_header()] + [self.__getattribute__(key).contents for key in self.default_sections])
        for line in output.split('\n'):
            print(line)

    def load(self, path):
        super(TopFile, self).load(path)
        for key in self.default_sections:
            self.__getattribute__(key)[0].values = self.data[self.__getattribute__(key)[0].unformatted_title]
