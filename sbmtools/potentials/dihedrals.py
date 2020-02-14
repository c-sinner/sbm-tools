from sbmtools.potentials.base import AbstractPotential


class DihedralPotential(AbstractPotential):
    header = ';   ai     aj     ak     al ftype     phi0(deg)   Kd           mult'
    format = '{first_atom:6d} {second_atom:6d} {third_atom:6d} {fourth_atom:6d} {ftype:d} {angle:17.9E} {kd:17.9E} {multiplicity:d}'
    strength = 0.500000000E+00
    multiplicity = 3
    fields = [
        "first_atom",
        "second_atom",
        "third_atom",
        "fourth_atom",
        "ftype",
        "angle",
        "kd",
        "multiplicity",
    ]
    function_type = 1

    def __init__(self, pair=None):
        super(DihedralPotential, self).__init__(pair)

    def apply(self):
        return {
            "first_atom": self.pair.first_atom,
            "second_atom": self.pair.second_atom,
            "third_atom": self.pair.third_atom,
            "fourth_atom": self.pair.fourth_atom,
            "ftype": self.function_type,
            "angle": self.pair.angle,
            "kd": self.strength,
            "multiplicity": self.multiplicity
        }

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "<DihedralPotential strength: {0} multiplicity: {1}>".format(self.strength, self.multiplicity)


class ImproperDihedralPotential(DihedralPotential):
    strength = 0.100000000E+01
    multiplicity = 1

    def __repr__(self):
        return "<ImproperDihedralPotential strength: {0} multiplicity: {1}>".format(self.strength, self.multiplicity)


class AllAtomDihedralPotential(DihedralPotential):
    strength = 0.100000000E+01
    multiplicity = 2
    format = '{first_atom:6d} {second_atom:6d} {third_atom:6d} {fourth_atom:6d} {ftype:d} {angle:17.9E} {kd:17.9E}'

    def __repr__(self):
        return "<ImproperDihedralPotential strength: {0}>".format(self.strength, self.multiplicity)
