import unittest
from sbmtools import PairsList, AbstractAtomGroup, Dihedral


class TestPairs(unittest.TestCase):

    def test_init(self):
        # Initiate with a list of iterables.
        p1 = PairsList([[1, 2], [1, 3], [2, 3]])

        # Initiate with a list of AbstractAtomGroup objects.
        ap1 = AbstractAtomGroup(1, 2)
        ap2 = AbstractAtomGroup(1, 3)
        ap3 = AbstractAtomGroup(2, 3)

        p1 = PairsList([ap1, ap2, ap3])

    def test_add(self):
        ap1 = AbstractAtomGroup(1, 2)
        ap2 = AbstractAtomGroup(2, 2)
        ap3 = AbstractAtomGroup(3, 2)
        ap4 = AbstractAtomGroup(4, 2)
        ap5 = AbstractAtomGroup(5, 2)

        p1 = PairsList([ap1, ap2, ap3, ap4])
        p2 = PairsList([ap1, ap2, ap5])

        p3 = p1 + p2
        self.assertEqual(p3, PairsList([ap1, ap2, ap3, ap4, ap1, ap2, ap5]))

        p3 = p1.add(p2)
        self.assertEqual(p3, PairsList([ap1, ap2, ap3, ap4, ap1, ap2, ap5]))

    def test_remove(self):
        ap1 = AbstractAtomGroup(1, 2)
        ap2 = AbstractAtomGroup(2, 2)
        ap3 = AbstractAtomGroup(3, 2)
        ap4 = AbstractAtomGroup(4, 2)
        ap5 = AbstractAtomGroup(5, 2)

        p1 = PairsList([ap1, ap2, ap3, ap4])
        p2 = PairsList([ap1, ap2, ap5])

        p3 = p1 - p2
        self.assertEqual(p3, PairsList([ap3, ap4]))

        p3 = p1.remove(p2)
        self.assertEqual(p3, PairsList([ap3, ap4]))

    def test_union(self):
        ap1 = AbstractAtomGroup(1, 2)
        ap2 = AbstractAtomGroup(2, 2)
        ap3 = AbstractAtomGroup(3, 2)
        ap4 = AbstractAtomGroup(4, 2)
        ap5 = AbstractAtomGroup(5, 2)

        p1 = PairsList([ap1, ap2, ap3, ap4])
        p2 = PairsList([ap1, ap2, ap5])

        p3 = p1.union(p2)
        self.assertEqual(p3, PairsList([ap1, ap2, ap3, ap4, ap5]))

    def test_intersection(self):
        ap1 = AbstractAtomGroup(1, 2)
        ap2 = AbstractAtomGroup(2, 2)
        ap3 = AbstractAtomGroup(3, 2)
        ap4 = AbstractAtomGroup(4, 2)
        ap5 = AbstractAtomGroup(5, 2)

        p1 = PairsList([ap1, ap2, ap3, ap4])
        p2 = PairsList([ap1, ap2, ap5])

        p3 = p1.intersection(p2)
        self.assertEqual(p3, PairsList([ap1, ap2]))

    def test_symmetric_difference(self):
        ap1 = AbstractAtomGroup(1, 2)
        ap2 = AbstractAtomGroup(2, 2)
        ap3 = AbstractAtomGroup(3, 2)
        ap4 = AbstractAtomGroup(4, 2)
        ap5 = AbstractAtomGroup(5, 2)

        p1 = PairsList([ap1, ap2, ap3, ap4])
        p2 = PairsList([ap1, ap2, ap5])

        p3 = p1.symmetric_difference(p2)
        self.assertEqual(p3, PairsList([ap3, ap4, ap5]))

    def test_dihedrals_equality(self):
        d1 = Dihedral(1, 2, 3, 4, 120)
        d2 = Dihedral(1, 2, 3, 4, 120)

        self.assertEqual(d1, d2)

        d1 = Dihedral(1, 2, 3, 4, 120, charge="+1.0")
        d2 = Dihedral(1, 2, 3, 4, 120, charge="+1.0")

        self.assertEqual(d1, d2)


if __name__ == '__main__':
    unittest.main()
