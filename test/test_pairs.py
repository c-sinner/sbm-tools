import unittest
from sbmtools import AbstractPairsList, AbstractAtomGroup, Dihedral, AtomPair, Angle, DihedralPotential, BondPotential, \
    AnglesPotential


class TestPairs(unittest.TestCase):

    def test_init(self):
        # Initiate with a list of iterables.
        p1 = AbstractPairsList([[1, 2], [1, 3], [2, 3]])

        # Initiate with a list of AbstractAtomGroup objects.
        ap1 = AbstractAtomGroup(1, 2)
        ap2 = AbstractAtomGroup(1, 3)
        ap3 = AbstractAtomGroup(2, 3)

        p1 = AbstractPairsList([ap1, ap2, ap3])

    def test_add(self):
        ap1 = AbstractAtomGroup(1, 2)
        ap2 = AbstractAtomGroup(2, 2)
        ap3 = AbstractAtomGroup(3, 2)
        ap4 = AbstractAtomGroup(4, 2)
        ap5 = AbstractAtomGroup(5, 2)

        p1 = AbstractPairsList([ap1, ap2, ap3, ap4])
        p2 = AbstractPairsList([ap1, ap2, ap5])

        p3 = p1 + p2
        self.assertEqual(p3, AbstractPairsList([ap1, ap2, ap3, ap4, ap1, ap2, ap5]))

        p3 = p1.add(p2)
        self.assertEqual(p3, AbstractPairsList([ap1, ap2, ap3, ap4, ap1, ap2, ap5]))

    def test_remove(self):
        ap1 = AbstractAtomGroup(1, 2)
        ap2 = AbstractAtomGroup(2, 2)
        ap3 = AbstractAtomGroup(3, 2)
        ap4 = AbstractAtomGroup(4, 2)
        ap5 = AbstractAtomGroup(5, 2)

        p1 = AbstractPairsList([ap1, ap2, ap3, ap4])
        p2 = AbstractPairsList([ap1, ap2, ap5])

        p3 = p1 - p2
        self.assertEqual(p3, AbstractPairsList([ap3, ap4]))

        p3 = p1.remove(p2)
        self.assertEqual(p3, AbstractPairsList([ap3, ap4]))

    def test_union(self):
        ap1 = AbstractAtomGroup(1, 2)
        ap2 = AbstractAtomGroup(2, 2)
        ap3 = AbstractAtomGroup(3, 2)
        ap4 = AbstractAtomGroup(4, 2)
        ap5 = AbstractAtomGroup(5, 2)

        p1 = AbstractPairsList([ap1, ap2, ap3, ap4])
        p2 = AbstractPairsList([ap1, ap2, ap5])

        p3 = p1.union(p2)
        self.assertEqual(p3, AbstractPairsList([ap1, ap2, ap3, ap4, ap5]))

    def test_intersection(self):
        ap1 = AbstractAtomGroup(1, 2)
        ap2 = AbstractAtomGroup(2, 2)
        ap3 = AbstractAtomGroup(3, 2)
        ap4 = AbstractAtomGroup(4, 2)
        ap5 = AbstractAtomGroup(5, 2)

        p1 = AbstractPairsList([ap1, ap2, ap3, ap4])
        p2 = AbstractPairsList([ap1, ap2, ap5])

        p3 = p1.intersection(p2)
        self.assertEqual(p3, AbstractPairsList([ap1, ap2]))

    def test_symmetric_difference(self):
        ap1 = AbstractAtomGroup(1, 2)
        ap2 = AbstractAtomGroup(2, 2)
        ap3 = AbstractAtomGroup(3, 2)
        ap4 = AbstractAtomGroup(4, 2)
        ap5 = AbstractAtomGroup(5, 2)

        p1 = AbstractPairsList([ap1, ap2, ap3, ap4])
        p2 = AbstractPairsList([ap1, ap2, ap5])

        p3 = p1.symmetric_difference(p2)
        self.assertEqual(p3, AbstractPairsList([ap3, ap4, ap5]))


class TestBonds(unittest.TestCase):
    def test_bonds_equality(self):
        b1 = AtomPair(1, 2, distance=0.75)
        b2 = AtomPair(1, 2, distance=0.75)

        self.assertEqual(b1, b2)

        b3 = AtomPair(1, 2, 0.75, charge="+1.0")
        b4 = AtomPair(1, 2, distance=0.75, charge="+1.0")

        self.assertEqual(b3, b4)

    def test_bonds_write(self):
        b1 = AtomPair(1, 2, distance=0.75)
        self.assertEqual(b1.write(), "")

        b2 = AtomPair(1, 2, distance=0.75, potential=BondPotential)
        self.assertEqual(b2.write(), "     1      2 1  7.50000000E-01 2.00000000E+04")


class TestAngles(unittest.TestCase):
    def test_angles_equality(self):
        a1 = Angle(1, 2, 3, 0.75)
        a2 = Angle(1, 2, 3, angle=0.75)

        self.assertEqual(a1, a2)

    def test_angles_write(self):
        a1 = Angle(1, 2, 3, angle=0.75)
        self.assertEqual(a1.write(), "")

        a2 = Angle(1, 2, 3, angle=0.75, potential=AnglesPotential)
        self.assertEqual(a2.write(), "     1      2      3 1 7.50000000E-01 4.00000000E+01")


class TestDihedrals(unittest.TestCase):
    def test_dihedrals_equality(self):
        d1 = Dihedral(1, 2, 3, 4, 120)
        d2 = Dihedral(1, 2, 3, 4, 120)

        self.assertEqual(d1, d2)

        d1 = Dihedral(1, 2, 3, 4, 120, charge="+1.0")
        d2 = Dihedral(1, 2, 3, 4, 120, charge="+1.0")

        self.assertEqual(d1, d2)

    def test_dihedrals_write(self):
        d1 = Dihedral(1, 2, 3, 4, 120)
        self.assertEqual(d1.write(), "")

        d2 = Dihedral(1, 2, 3, 4, 120, potential=DihedralPotential)
        self.assertEqual(d2.write(), "     1      2      3      4 1 1.20000000E+02 5.00000000E-01 3")


if __name__ == '__main__':
    pairs_suite = unittest.TestLoader().loadTestsFromTestCase(TestPairs)
    dihedrals_suite = unittest.TestLoader().loadTestsFromTestCase(TestDihedrals)
    bonds_suite = unittest.TestLoader().loadTestsFromTestCase(TestBonds)
    angles_suite = unittest.TestLoader().loadTestsFromTestCase(TestAngles)

    all_tests = unittest.TestSuite([pairs_suite, dihedrals_suite, bonds_suite, angles_suite])
    unittest.TextTestRunner(verbosity=2).run(all_tests)
