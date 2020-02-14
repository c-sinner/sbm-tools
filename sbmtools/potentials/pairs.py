import math

from sbmtools.potentials.base import AbstractPotential


class LennardJonesPotential(AbstractPotential):
    header = ';   ai     aj ftype             c6                c12'
    format = '{first_atom:6d} {second_atom:6d} {ftype:d} {c6:18.9E} {c12:18.9E}'
    fields = [
        "first_atom",
        "second_atom",
        "ftype",
        "c6",
        "c12",
    ]
    function_type = 1

    def __init__(self, pair=None):
        super(LennardJonesPotential, self).__init__(pair)

    def apply(self):
        return {
            "first_atom": self.pair.first_atom,
            "second_atom": self.pair.second_atom,
            "ftype": self.function_type,
            "c6": 2 * self.pair.distance ** 6,
            "c12": self.pair.distance ** 12,
        }


class C10Potential(AbstractPotential):
    header = '; i j type and weight'
    format = '{first_atom:6d} {second_atom:6d} {ftype:d}  {c10:.5E} {c12:.5E}'
    function_type = 1

    def __init__(self, pair=None):
        super(C10Potential, self).__init__()
        self.pair = pair

    def apply(self):
        return {
            "first_atom": self.pair.first_atom,
            "second_atom": self.pair.second_atom,
            "function_type": self.function_type,
            "c10": 6 * self.pair.distance ** 10,
            "c12": 5 * self.pair.distance ** 12,
        }


class GaussianPotential(AbstractPotential):
    header = ';   ai     aj ftype             Amplitude     mu    sigma'
    format = '{first_atom:6d} {second_atom:6d} {ftype:d} {amplitude:18.9E} {mu:18.9E} {sigma:18.9E}'
    fields = [
        "first_atom",
        "second_atom",
        "ftype",
        "amplitude",
        "mu",
        "sigma",
    ]
    function_type = 5
    strength = 1.0

    def __init__(self, pair=None):
        super(GaussianPotential, self).__init__(pair)

    def apply(self):
        return {
            "first_atom": self.pair.first_atom,
            "second_atom": self.pair.second_atom,
            "ftype": self.function_type,
            "amplitude": self.strength,
            "mu": self.pair.distance,
            "sigma": math.sqrt(self.pair.distance**2/(50*math.log(2, math.e)))
        }

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "<GaussianPotential str: {0}>".format(self.strength)


class CombinedGaussianPotential(AbstractPotential):
    header = ';   ai     aj ftype      Amplitude                 mu              sigma                  a'
    format = '{first_atom:6d} {second_atom:6d} {ftype:d} {amplitude:18.9E} {mu:18.9E} {sigma:18.9E} {a:18.9E}'
    fields = [
        "first_atom",
        "second_atom",
        "ftype",
        "amplitude",
        "mu",
        "sigma",
        "a",
    ]
    function_type = 6
    strength = 1.0

    def __init__(self, pair=None):
        super(CombinedGaussianPotential, self).__init__(pair)

    def apply(self):
        return {
            "first_atom": self.pair.first_atom,
            "second_atom": self.pair.second_atom,
            "ftype": self.function_type,
            "amplitude": self.strength,
            "mu": self.pair.distance,
            "sigma": math.sqrt(self.pair.distance**2/(50*math.log(2, math.e))),
            "a": 0.167772196E-04 #TODO: CHECK THIS VALUE
        }

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "<CombinedGaussianPotential str: {0}>".format(self.strength)
