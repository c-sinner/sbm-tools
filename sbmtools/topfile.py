from sbmtools.pairs import PairsList
from sbmtools.topfile_base import TopFileBase
from sbmtools.base import AbstractParameterFile
from sbmtools.potentials.base import AbstractPotential
from sbmtools.topfile_parser import TopFileParser
from sbmtools.potentials.pairs import CombinedGaussianPotential


class TopFile(TopFileBase, AbstractParameterFile):
    potential = CombinedGaussianPotential
    parser = TopFileParser

    def __init__(self, path=None, pairs=None, potential=CombinedGaussianPotential, *args, **kwargs):
        super(TopFile, self).__init__(*args, **kwargs)

        self.init_pairs(pairs)
        self.init_potential(potential)

        for key, value in kwargs.items():
            setattr(self, key, value)

        if path:
            self.load(path)

    def init_pairs(self, pairs):
        if isinstance(pairs, PairsList):
            self.pairs = pairs
        elif pairs:
            raise TypeError(
                'Expected {0} to be an instance of type PairsList. Initiate a new PairsList object using PairsList()')
        else:
            pass

    def init_potential(self, potential):
        if isinstance(potential(), AbstractPotential):
            self.potential = potential
        elif potential:
            raise TypeError(
                'Expected {0} to inherit from AbstractPotential. \
                Initiate a new AbstractPotential object using AbstractPotential()')
        else:
            pass

    def save(self, path):
        super(TopFile, self).save(path)

    def write(self):
        output = "\n\n".join([self.header] + [self.__getattribute__(key).write() for key in self.default_sections])
        print(output)
