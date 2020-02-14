from sbmtools.potentials import AbstractPotential


class BondPotential(AbstractPotential):
    header = ';   ai     aj func         r0(nm)                Kb'
    format = '{first_atom:6d} {second_atom:6d} {ftype:d}  {distance:16.9E} {kb:17.9E}'
    strength = 0.200000000E+05
    function_type = 1

    def __init__(self, pair=None):
        super(BondPotential, self).__init__(pair)

    def apply(self):
        return {
            "first_atom": self.pair.first_atom,
            "second_atom": self.pair.second_atom,
            "ftype": self.function_type,
            "distance": self.pair.distance,
            "kb": self.strength,
        }