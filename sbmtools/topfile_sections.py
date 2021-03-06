from sbmtools import AbstractParameterFileSection


class AbstractTopFileSection(AbstractParameterFileSection):
    title_format = ' [ {0} ]'
    header_format = ';'
    line_format = ''
    _title = ''
    fields = []
    attribute_delimiter = '\n'
    line_delimiter = '\n'

    def __init__(self, *args, **kwargs):
        super(AbstractTopFileSection, self).__init__(*args, **kwargs)
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def contents(self):
        return self.attribute_delimiter.join([
            self.title,
            self.header
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


class DefaultsSection(AbstractTopFileSection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        self.values = [[]]


class MoleculeTypeSection(AbstractTopFileSection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = 'moleculetype'
        self.header_format = ';{name:22s} {nrexcl}'
        self.line_format = '{name:23s} {nrexcl}'
        self.fields = [
            'name',
            'nrexcl'
        ]
        self.values = [['Macromolecule', 3]]


class AtomsSection(AbstractTopFileSection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
    def __init__(self, pairs, potential, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = 'bonds'
        self.header_format = ';{index} {partner} {ftype}   {distance}   {kb}'
        self.line_format = '{index:6d} {partner:6d} {ftype:d}   {distance:.10E}   {kb:.10E}'
        self.fields = ['index', 'partner', 'ftype', 'distance', 'kb']


class ExclusionsSection(AbstractTopFileSection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = 'exclusions'
        self.header_format = ';{ai:>5s} {aj:>6s}'
        self.line_format = '{ai:6d} {aj:6d}'
        self.fields = [
            'ai',
            'aj'
        ]


class AnglesSection(AbstractTopFileSection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = 'system'
        self.header_format = ';{name}'
        self.line_format = '{name}'
        self.fields = [
            'name',
        ]
        self.values = [['Macromolecule']]


class MoleculesSection(AbstractTopFileSection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = 'molecules'
        self.header_format = ';{name:15s} {#molec}'
        self.line_format = '{name:16s} {#molec}'
        self.fields = [
            'name',
            '#molec'
        ]
        self.values = [['Macromolecule', 1]]
