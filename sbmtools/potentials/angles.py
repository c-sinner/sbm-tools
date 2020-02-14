from sbmtools.potentials.base import AbstractPotential


class AnglesPotential(AbstractPotential):
    header = ';   ai     aj     ak func       th0(deg)                Ka'
    format = '{first_atom:6d} {second_atom:6d} {third_atom:6d} {ftype:d} {theta:17.9E} {ka:17.9E}'
    strength = 4.00000000E+01
    function_type = 1

    def __init__(self, pair=None):
        super(AnglesPotential, self).__init__(pair)

    def apply(self):
        return {
            "first_atom": self.pair.first_atom,
            "second_atom": self.pair.second_atom,
            "third_atom": self.pair.third_atom,
            "ftype": self.function_type,
            "theta": self.pair.angle,
            "ka": self.strength,
        }