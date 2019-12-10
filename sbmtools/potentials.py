class AbstractPotential(object):
    def __init__(self, pair=None, **kwargs):
        self.format = ''
        self.header = ''
        self.pair = pair
        for key, value in kwargs.items():
            setattr(self, key, value)

    def apply(self):
        raise NotImplementedError


class BondPotential(AbstractPotential):
    header = ';ai     aj      func    r0(nm)  Kb'
    format = '{index:6d} {partner:6d} {ftype:d}  {distance:.8E} {kb:.8E}'
    strength = 0.200000000E+05
    function_type = 1

    def __init__(self, pair=None):
        super(BondPotential, self).__init__(pair)

    def apply(self):
        return {
            "index": self.pair.index,
            "partner": self.pair.partner,
            "ftype": self.function_type,
            "distance": self.pair.distance,
            "kb": self.strength,
        }


class LennardJonesPotential(AbstractPotential):
    header = '; i j type and weight'
    format = '{index:6d} {partner:7d} {ftype:d}  {c6:.9E} {c12:.9E}'
    fields = [
        "index",
        "partner",
        "ftype",
        "c6",
        "c12",
    ]
    function_type = 1

    def __init__(self, pair=None):
        super(LennardJonesPotential, self).__init__(pair)

    def apply(self):
        return {
            "index": self.pair.index,
            "partner": self.pair.partner,
            "ftype": self.function_type,
            "c6": 2 * self.pair.distance ** 6,
            "c12": self.pair.distance ** 12,
        }


class C10Potential(AbstractPotential):
    header = '; i j type and weight'
    format = '{index:6d} {partner:6d} {ftype:d}  {c10:.5E} {c12:.5E}'
    function_type = 1

    def __init__(self, pair=None):
        super(C10Potential, self).__init__()
        self.pair = pair

    def apply(self):
        return {
            "index": self.pair.index,
            "partner": self.pair.partner,
            "function_type": self.function_type,
            "c10": 6 * self.pair.distance ** 10,
            "c12": 5 * self.pair.distance ** 12,
        }
