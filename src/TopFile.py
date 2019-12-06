from src.Potentials import LennardJonesPotential
from src.base import AbstractParameterFileSection, AbstractParameterFile


class AbstractTopFileSection(AbstractParameterFileSection):
    title = ''
    title_format = '[ {0} ]'
    header_format = ';'
    line_format = ''
    fields = []
    values = []

    # TODO write is not great as a name as the method it is not writing
    def write(self):
        return '\n'.join([
            self.write_title(),
            self.write_header(),
            self.write_values()
        ])

    def write_title(self):
        return self.title_format.format(self.title)

    def write_header(self):
        return self.header_format.format(**dict(zip(self.fields, self.fields)))

    def write_values(self):
        return self.line_format.format(**dict(zip(self.fields, self.values)))


class DefaultsSection(AbstractTopFileSection):
    def __init__(self):
        self.title = 'defaults'
        self.header_format = ';{nbfunc} {comb-rule} {gen-pairs}'
        self.line_format = '{nbfunc:05d} {comb-rule:5d} {gen-pairs:10s}'
        self.fields = [
            'nbfunc',
            'comb-rule',
            'gen-pairs',
        ]
        self.values = [1, 1, 'no']


class AtomTypesSection(AbstractTopFileSection):
    def __init__(self):
        self.title = 'atomtypes'
        self.header_format = ';{name}  {mass}     {charge}   {ptype} {c6}       {c12}'
        self.fields = [
            'name',
            'mass',
            'charge',
            'ptype',
            'c6',
            'c12',
        ]
        self.values = [

        ]


class MoleculeTypeSection(AbstractTopFileSection):
    def __init__(self):
        self.title = 'moleculetype'


class AtomsSection(AbstractTopFileSection):
    def __init__(self):
        self.title = 'atoms'


class PairsSection(AbstractTopFileSection):
    def __init__(self, pairs):
        self.title = 'pairs'
        self.header_format = LennardJonesPotential.header
        self.line_format = LennardJonesPotential.format
        self.values = self.get_values(pairs)

    def get_values(self, pairs):
        return map(LennardJonesPotential, pairs)


class BondsSection(AbstractTopFileSection):
    def __init__(self):
        self.title = 'bonds'


class ExclusionsSection(AbstractTopFileSection):
    def __init__(self):
        self.title = 'exclusions'


class AnglesSection(AbstractTopFileSection):
    def __init__(self):
        self.title = 'angles'


class DihedralsSection(AbstractTopFileSection):
    def __init__(self):
        self.title = 'dihedrals'


class SystemSection(AbstractTopFileSection):
    def __init__(self):
        self.title = 'system'
        self.header_format = '{name}'
        self.line_format = '{name}'
        self.fields = [
            'name',
        ]
        self.values = ['Macromolecule']


class MoleculesSection(AbstractTopFileSection):
    def __init__(self):
        self.title = 'molecules'
        self.header_format = '{name}'
        self.line_format = '{name}'
        self.fields = [
            'name',
            '#molec'
        ]
        self.values = ['Macromolecule', 1]


class TopFile(AbstractParameterFile):
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
        "pairs_section": PairsSection([]),
        "bonds_section": BondsSection(),
        "exclusions_section": ExclusionsSection(),
        "angles_section": AnglesSection(),
        "dihedrals_section": DihedralsSection(),
        "system_section": SystemSection(),
        "molecules_section": MoleculeTypeSection()
    }

    def __init__(self, *args, **kwargs):
        kwargs = {**self.default_kwargs, **kwargs}

        self.pairs = None
        self.potential = None

        for key, value in kwargs.items():
            setattr(self, key, value)

    def save(self):
        super(TopFile, self).save()

    def built(self):
        return "\n\n".join([self.__getattribute__(key).write() for key in self.default_sections])
