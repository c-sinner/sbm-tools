

class AbstractPotential(object):
    def __init__(self, pair=None, **kwargs):
        self.format = ''
        self.header = ''
        self.pair = pair
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_values(self):
        raise NotImplementedError


class BondPotential(object):
    def __init__(self, pair=None):
        super(BondPotential, self).__init__(pair)
        self.header = ';ai     aj      func    r0(nm)  Kb'
        self.format = '{index:6d} {partner:6d} {ftype:d}  {dist:.8E} {kb:.8E}'
        self.strength = 0.200000000E+05
        self.function_type = 1

    def get_values(self):
        return {
            "index": self.pair.index,  #TODO: index might clash with builtins
            "partner": self.pair.partner,
            "ftype": self.function_type,
            "dist": self.pair.distance,
            "kb": self.strength,
        }


class LennardJonesPotential(AbstractPotential):
    header = ''
    format = ''

    def __init__(self, pair=None):
        super(LennardJonesPotential, self).__init__(pair)
        self.header = '; i j type and weight'
        self.format = '{index:6d} {partner:6d} {ftype:d}  {c6:.5E} {c12:.5E}'
        self.function_type = 1

    def get_values(self):
        return {
            "index": self.pair.index,  #TODO: index might clash with builtins
            "partner": self.pair.partner,
            "ftype": self.function_type,
            "c6": 2 * self.pair.distance**6,
            "c12": self.pair.distance**12,
        }


class C10Potential(AbstractPotential):
    def __init__(self, other=None):
        super(C10Potential, self).__init__()
        self.other = other
        self.header = '; i j type and weight'
        self.format = '{index:6d} {partner:6d} {ftype:d}  {c10:.5E} {c12:.5E}'
        self.function_type = 1

    def get_values(self):
        return {
            "index": self.pair.index,  #TODO: index might clash with builtins
            "partner": self.pair.partner,
            "function_type": self.function_type,
            "c10": 6 * self.pair.distance**10,
            "c12": 5 * self.pair.distance**12,
        }

