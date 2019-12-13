from sbmtools import AtomPair, PairsList, AbstractParameterFileParser, AbstractAtomPair
from sbmtools.atoms import AtomsList, Atom
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


class TopFileSectionParser(object):
    title_regex = r'\[\s*([a-zA-Z0-9]*)\s*\]'
    line_delimiter = '\n'

    def __init__(self):
        self.title = ''
        self.values = []
        self.objects = []

    def export(self):
        return {'title': self.title, 'values': self.values, 'objects': self.objects}

    def parse(self, data):
        self.title = self.find_title(data)
        self.values = self.process_content(data)
        self.objects = self.process_values()
        return self.export()

    def find_title(self, data):
        m = re.match(self.title_regex, data)
        if m:
            return m.group(1)
        return ''

    def convert_numericals(self, items):
        result = []
        for item in items:
            try:
                result.append(int(item))
            except:
                try:
                    result.append(float(item))
                except:
                    result.append(item)
        return result

    def process_content(self, data):
        return [self.convert_numericals(line.split()) for line in data.split(self.line_delimiter)[1:] if line]

    def process_values(self):
        if self.title == 'pairs':
            return PairsList([AtomPair(value[0], value[1], 0.8) for value in self.values])
        elif isinstance(self.values[0][0], int) and isinstance(self.values[0][1], int):
            return PairsList([AbstractAtomPair(value[0], value[1]) for value in self.values])
        elif isinstance(self.values[0][0], int):
            return AtomsList([Atom(value[0]) for value in self.values])
        else:
            return []


class TopFileParser(TopFileBase, AbstractParameterFileParser):
    sections_regex = r'\[[a-z\s]*\][a-zA-Z0-9\#\+\;\s\-\n\.\(\)]*\n'
    title_regex = r'\[\s*([a-zA-Z0-9]*)\s*\]'
    line_delimiter = '\n'

    def __init__(self, data):
        super(TopFileParser, self).__init__(data)

    def parse(self):
        return self.postprocess_result(self.find_sections(self.preprocess_data(self.data)))

    # handle same titles
    def postprocess_result(self, sections_list):
        def flatten(list_of_lists):
            return [item for sublist in list_of_lists for item in sublist]
        #TODO: FIX THIS WITH REDUCE
        unique_keys = []
        [unique_keys.append(x['title']) for x in sections_list if x['title'] not in unique_keys]

        processed = {}
        for unique_key in unique_keys:
            processed[unique_key] = flatten(
                    [section['values'] for section in sections_list if section['title'] == unique_key])

        processed.update(self.export())

        return processed

    @staticmethod
    def preprocess_data(data):
        return re.sub(r';.*(\n|$)', '', data)

    @staticmethod
    def parse_section(section):
        section_parser = TopFileSectionParser()
        return section_parser.parse(section)

    def find_sections(self, data):
        return list(map(self.parse_section, re.findall(self.sections_regex, data, re.MULTILINE)))


class TopFile(TopFileBase, AbstractParameterFile):
    potential = LennardJonesPotential
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

    def __init__(self, pairs=None, potential=LennardJonesPotential, *args, **kwargs):
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
