import re

from sbmtools.potentials.dihedrals import AllAtomDihedralPotential
from sbmtools.utils import convert_numericals, parse_line
from sbmtools.potentials.pairs import GaussianPotential, CombinedGaussianPotential
from sbmtools.pairs import AtomPair, Angle, Dihedral, Atom, ExclusionsEntry, AtomType
from sbmtools.base import AbstractParameterFileParser, ParameterFileEntry, ParameterFileComment
from sbmtools.potentials.angles import AnglesPotential
from sbmtools.potentials.bonds import BondPotential
from sbmtools.potentials.dihedrals import ImproperDihedralPotential, DihedralPotential


class TopFileParser(AbstractParameterFileParser):
    title_regex = r'^\s*\[\s*([a-zA-Z0-9]*)\s*\]\s*$'

    def readline(self):
        attribute_name, line = super().readline()
        if self.contains_section_header(line):
            section_header = self.get_section_header(line)
            self.attribute_name = section_header
            return self.__next__()

        line = self.preprocess_line(line)
        if len(line) < 3:
            return self.__next__()
        elif len(line) == 3 and line[1] == ' ':
            return self.__next__()
        else:
            pass

        return self.attribute_name, self.process_entry(self.attribute_name, line)

    def get_section_header(self, line):
        m = re.match(self.title_regex, line)
        if m:
            return m.group(1)
        return None

    def contains_section_header(self, line):
        m = re.match(self.title_regex, line)
        if m:
            return True
        return False

    @staticmethod
    def preprocess_line(line):
        line = line.strip('\n')
        return line

    def process_entry(self, section_name, line):
        if re.match(r"^\s+;", line):
            entry = ParameterFileComment(*[convert_numericals(x) for x in parse_line(line)])
            return entry
        else:
            entry = ParameterFileEntry(*[convert_numericals(x) for x in parse_line(line)])

            if section_name == "atoms":
                return self.process_atoms_entry(entry)

            elif section_name == "atomtypes":
                return self.process_atomtypes_entry(entry)

            elif section_name == "pairs":
                return self.process_pairs_entry(entry)

            elif section_name == "bonds":
                return self.process_bonds_entry(entry)

            elif section_name == "exclusions":
                return self.process_exclusions_entry(entry)

            elif section_name == "angles":
                return self.process_angles_entry(entry)

            elif section_name == "dihedrals":
                return self.process_dihedrals_entry(entry)

            else:
                return entry

    @staticmethod
    def process_atoms_entry(entry):
        return Atom(entry[2], type=entry[4], resnr=entry[6], residue=entry[8], atom=entry[10], cgnr=entry[12],
                    charge=entry[14], mass=entry[16])

    @staticmethod
    def process_atomtypes_entry(entry):
        return AtomType(0, name=entry[2], mass=entry[4], charge=entry[6], ptype=entry[8], c10=entry[10], c12=entry[12])

    @staticmethod
    def process_pairs_entry(entry):
        if entry[6] == 5:
            return AtomPair(entry[2], entry[4], distance=entry[10], potential=GaussianPotential)
        if entry[6] == 6:
            return AtomPair(entry[2], entry[4], distance=entry[10], potential=CombinedGaussianPotential)
        return entry

    @staticmethod
    def process_bonds_entry(entry):
        if entry[6] == 1:
            return AtomPair(entry[2], entry[4], distance=entry[8], potential=BondPotential)
        return entry

    @staticmethod
    def process_exclusions_entry(entry):
        return ExclusionsEntry(entry[2], entry[4])

    @staticmethod
    def process_angles_entry(entry):
        if entry[8] == 1:
            return Angle(entry[2], entry[4], entry[6], angle=entry[10], potential=AnglesPotential)
        return entry

    @staticmethod
    def process_dihedrals_entry(entry):
        if entry[10] == 1:
            if entry[16] == 1:
                return Dihedral(entry[2], entry[4], entry[6], entry[8], angle=entry[12],
                                potential=ImproperDihedralPotential)
            if entry[16] == 3:
                return Dihedral(entry[2], entry[4], entry[6], entry[8], angle=entry[12],
                                potential=DihedralPotential)

        if entry[10] == 2:
            return Dihedral(entry[2], entry[4], entry[6], entry[8], angle=entry[12],
                            potential=AllAtomDihedralPotential)

        return entry
