from sbmtools.pairs import PairsList, AnglesList, DihedralsList, ExclusionsList, \
    BondsList, AtomList, ParameterFileEntryList, AtomTypesList


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
        self._atomtypes = AtomTypesList()
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
            'defaults': self._defaults,
            'atomtypes': self._atomtypes,
            'moleculetype': self._moleculetype,
            'atoms': self._atoms,
            'pairs': self._pairs,
            'bonds': self._bonds,
            'exclusions': self._exclusions,
            'angles': self._angles,
            'dihedrals': self._dihedrals,
            'system': self._system,
            'molecules': self._molecules,
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
