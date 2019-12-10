import uuid
from datetime import date

from sbmtools import PairsList, AbstractParameterFileParser
from sbmtools.potentials import LennardJonesPotential, AbstractPotential
from sbmtools.base import AbstractParameterFileSection, AbstractParameterFile
import re


class TopFileParser(AbstractParameterFileParser):
    sections_regex = r'\[[a-z\s]*\][a-zA-Z0-9\#\+\;\s\-\n\.\(\)]*\n'
    title_regex = r'\[\s*([a-zA-Z0-9]*)\s*\]'
    line_delimiter = '\n'

    def __init__(self, data):
        super().__init__(data)
        self.sections = []

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


class AbstractTopFileSection(AbstractParameterFileSection):
    title_format = ' [ {0} ]'
    header_format = ';'
    line_format = ''
    _title = ''
    fields = []
    _values = []
    attribute_delimiter = '\n'
    line_delimiter = '\n'

    @property
    def contents(self):
        return self.attribute_delimiter.join([
            self.title,
            self.header,
            self.values
        ])

    @property
    def title(self):
        return self.title_format.format(self._title)

    @property
    def unformatted_title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def header(self):
        return self.header_format.format(**dict(zip(self.fields, self.fields)))

    @property
    def values(self):
        if isinstance(self._values, str):
            return self._values
        else:
            return self.line_delimiter.join(
                [self.format_line(self.prepare_line(line)) for line in self.get_values()]
            )

    @values.setter
    def values(self, value):
        self._values = value

    def prepare_line(self, line):
        if isinstance(line, dict):
            return line
        else:
            try:
                return dict(zip(self.fields, line))
            except TypeError:
                print("Expected {0} to be a list of values".format(line))
                raise

    def format_line(self, line):
        return self.line_format.format(**line)

    def get_values(self):
        return self._values


class DefaultsSection(AbstractTopFileSection):
    def __init__(self):
        super().__init__()
        self.title = 'defaults'
        self.header_format = ';{nbfunc:>11s} {comb-rule:>12s} {gen-pairs}'
        self.line_format = '{nbfunc:12d} {comb-rule:12d} {gen-pairs}'
        self.fields = [
            'nbfunc',
            'comb-rule',
            'gen-pairs',
        ]
        self.values = [[1, 1, 'no']]


class AtomTypesSection(AbstractTopFileSection):
    def __init__(self):
        super().__init__()
        self.title = 'atomtypes'
        self.header_format = ';{name:5s} {mass:<7s} {charge:>5s} {ptype:5s} {c6:>4s} {c12:<12s}'
        self.line_format = ' {name:5s} {mass:<8.3f} {charge:<5.3f} {ptype:<4s} {c6:.3f} {c12:10E}'
        self.fields = [
            'name',
            'mass',
            'charge',
            'ptype',
            'c6',
            'c12',
        ]
        self.values = []


class MoleculeTypeSection(AbstractTopFileSection):
    def __init__(self):
        super().__init__()
        self.title = 'moleculetype'
        self.header_format = ';{name:22s} {nrexcl}'
        self.line_format = '{name:23s} {nrexcl}'
        self.fields = [
            'name',
            'nrexcl'
        ]
        self.values = [['Macromolecule', 3]]


class AtomsSection(AbstractTopFileSection):
    def __init__(self):
        super().__init__()
        self.title = 'atoms'
        self.header_format = ';{nr:>5s} {type} {resnr} {res:>4s} {atom:>5s} {cgnr} {charge} {mass}'
        self.line_format = '{nr:6d} {type:2s} {resnr:7d} {res:>4s} {atom:>3s} {cgnr:6d} {charge:>8.3f} {mass:>8.3f}'
        self.fields = [
            'nr',
            'type',
            'resnr',
            'res',
            'atom',
            'cgnr',
            'charge',
            'mass'
        ]


class PairsSection(AbstractTopFileSection):
    def __init__(self, pairs, potential):
        super().__init__()
        self.pairs = pairs
        self.potential = potential

        self.title = 'pairs'
        self.header_format = self.potential.header
        self.line_format = self.potential.format
        self.fields = self.potential.fields
        self.values = self.get_values()

    def get_values(self):
        values = super(PairsSection, self).get_values()  # don't forget to return values if they are set externally
        if values:
            return values
        return [getattr(potential, 'apply')() for potential in map(self.potential, self.pairs)]


class BondsSection(AbstractTopFileSection):
    def __init__(self):
        super().__init__()
        self.title = 'bonds'
        self.header_format = ';{index} {partner} {ftype}   {distance}   {kb}'
        self.line_format = '{index:6d} {partner:6d} {ftype:d}   {distance:.10E}   {kb:.10E}'
        self.fields = ['index', 'partner', 'ftype', 'distance', 'kb']


class ExclusionsSection(AbstractTopFileSection):
    def __init__(self):
        super().__init__()
        self.title = 'exclusions'
        self.header_format = ';{ai:>5s} {aj:>6s}'
        self.line_format = '{ai:6d} {aj:6d}'
        self.fields = [
            'ai',
            'aj'
        ]


class AnglesSection(AbstractTopFileSection):
    def __init__(self):
        super().__init__()
        self.title = 'angles'
        self.header_format = ';{ai:>5s} {aj:>6s} {ak:>6s} {ftype:5s} {th0dg:>10s} {ka:>15s}'
        self.line_format = '{ai:6d} {aj:6d} {ak:6d} {ftype:1d}   {th0dg:10E}    {ka:10E}'
        self.fields = [
            'ai',
            'aj',
            'ak',
            'ftype',
            'th0dg',
            'ka'
        ]


class DihedralsSection(AbstractTopFileSection):
    def __init__(self):
        super().__init__()
        self.title = 'dihedrals'
        self.header_format = ';{ai:>5s} {aj:>6s} {ak:>6s} {al:>6s} {ftype:5s} {phi0dg:>13s} {kd:>17s} {mult}'
        self.line_format = '{ai:6d} {aj:6d} {ak:6d} {al:6d} {ftype:1d} {phi0dg:17.9E} {kd:17.9E} {mult:1d}'
        self.fields = [
            'ai',
            'aj',
            'ak',
            'al',
            'ftype',
            'phi0dg',
            'kd',
            'mult'
        ]


class SystemSection(AbstractTopFileSection):
    def __init__(self):
        super().__init__()
        self.title = 'system'
        self.header_format = ';{name}'
        self.line_format = '{name}'
        self.fields = [
            'name',
        ]
        self.values = [['Macromolecule']]


class MoleculesSection(AbstractTopFileSection):
    def __init__(self):
        super().__init__()
        self.title = 'molecules'
        self.header_format = ';{name:15s} {#molec}'
        self.line_format = '{name:16s} {#molec}'
        self.fields = [
            'name',
            '#molec'
        ]
        self.values = [['Macromolecule', 1]]


class TopFile(AbstractParameterFile):
    pairs = PairsList()
    potential = LennardJonesPotential
    parser = TopFileParser

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

    default_kwargs = {
        "defaults_section": DefaultsSection(),
        "atom_types_section": AtomTypesSection(),
        "molecule_type_section": MoleculeTypeSection(),
        "atoms_section": AtomsSection(),
        "bonds_section": BondsSection(),
        "exclusions_section": ExclusionsSection(),
        "angles_section": AnglesSection(),
        "dihedrals_section": DihedralsSection(),
        "system_section": SystemSection(),
        "molecules_section": MoleculesSection()
    }

    def __init__(self, pairs=None, potential=LennardJonesPotential, **kwargs):
        super().__init__()
        if pairs is None:
            pairs = PairsList()
        kwargs = {**self.default_kwargs, **kwargs}

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
        if key == 'pairs':
            isinstance(value, PairsList)
            self.pairs_section = PairsSection(value, self.potential)
        if key == 'potential':
            isinstance(value(), AbstractPotential)
            self.pairs_section = PairsSection(self.pairs, value)
        super(TopFile, self).__setattr__(key, value)

    def get_header(self):
        return '; Automated top file generated by sbmtools on the {0} with uuid {1}'.format(date.today().isoformat(),
                                                                                            uuid.uuid4().hex)

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
            self.__getattribute__(key).values = self.data[self.__getattribute__(key).unformatted_title]
